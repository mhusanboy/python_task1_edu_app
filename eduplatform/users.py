from eduplatform.abstracts import AbstractRole
import datetime 
from eduplatform.enums import UserRole, AssignmentDifficulty
from eduplatform.entities import Assignment, Grade, Notification

class User(AbstractRole):
    def __init__(self, full_name, email, password, role):
        super().__init__(full_name, email, password)
        self.role = role
        self._notifications = []
        self.phone = None
        self.address = None

    def get_profile(self):
        return {
            "id": self._id,
            "full_name": self._full_name,
            "email": self._email,
            "role": self.role.value,
            "created_at": self._created_at,
            "phone": self.phone,
            "address": self.address
        }

    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif key == "full_name":
                self._full_name = value
            elif key == "email":
                self._email = value
            else:
                print(f"Warning: Cannot update unknown attribute '{key}' for user {self._full_name}.")
        print(f"Profile for {self._full_name} updated.")

    def add_notification(self, message, priority=0):
        new_notification = Notification(message, self._id, priority=priority)
        self._notifications.append(new_notification)
        print(f"Notification added for {self._full_name}: {message}")
        return new_notification

    def view_notifications(self, unread_only=False, important_only=False):
        filtered_notifications = []
        print(f"\nNotifications for {self._full_name}:")
        for notification in sorted(self._notifications, key=lambda n: n.priority, reverse=True):
            if unread_only and notification.is_read:
                continue
            if important_only and notification.priority < 1:
                continue
            filtered_notifications.append(notification.get_info())
            print(f"- [ID: {notification.id}] {'[READ]' if notification.is_read else '[UNREAD]'} [Priority: {notification.priority}] ({notification.created_at}): {notification.message}")
        return filtered_notifications

    def mark_notification_as_read(self, notification_id):
        for notification in self._notifications:
            if notification.id == notification_id:
                notification.mark_as_read()
                print(f"Notification {notification_id} marked as read for {self._full_name}.")
                return True
        print(f"Notification {notification_id} not found for {self._full_name}.")
        return False

    def delete_notification(self, notification_id):
        initial_count = len(self._notifications)
        self._notifications = [n for n in self._notifications if n.id != notification_id]
        if len(self._notifications) < initial_count:
            print(f"Notification {notification_id} deleted for {self._full_name}.")
            return True
        print(f"Notification {notification_id} not found for {self._full_name}.")
        return False

class Student(User):
    def __init__(self, full_name, email, password, grade):
        super().__init__(full_name, email, password, UserRole.STUDENT)
        self.grade = grade
        self.subjects = {}
        self.assignments = {}
        self.grades = {}

    def submit_assignment(self, assignment_obj, content, max_length=500):
        if len(content) > max_length:
            print(f"Error: Submission content exceeds maximum length of {max_length} characters.")
            return False

        if assignment_obj.deadline < datetime.datetime.now().isoformat():
            status = "Late Submitted"
            print(f"Warning: Assignment '{assignment_obj.title}' submitted late.")
        else:
            status = "Submitted"

        assignment_obj.add_submission(self._id, content)
        self.assignments[assignment_obj.id] = status
        print(f"Assignment '{assignment_obj.title}' submitted by {self._full_name}. Status: {status}")
        return True

    def view_grades(self, subject=None):
        print(f"\nGrades for {self._full_name} ({self.grade}):")
        if not self.grades:
            print("No grades recorded yet.")
            return {}

        filtered_grades = {}
        for s, grade_list in self.grades.items():
            if subject and s != subject:
                continue
            print(f"  Subject: {s}, Grades: {grade_list}")
            filtered_grades[s] = grade_list
        return filtered_grades

    def calculate_average_grade(self, subject=None):
        grades_to_average = []
        if subject:
            grades_to_average = self.grades.get(subject, [])
        else:
            for grade_list in self.grades.values():
                grades_to_average.extend(grade_list)

        if not grades_to_average:
            print(f"No grades to calculate average for {'subject ' + subject if subject else 'all subjects'}.")
            return 0.0
        avg = sum(grades_to_average) / len(grades_to_average)
        print(f"Average grade for {self._full_name} ({'subject ' + subject if subject else 'all subjects'}): {avg:.2f}")
        return avg

    def get_subject_stats(self, subject):
        grades = self.grades.get(subject, [])
        if not grades:
            return {"min": None, "max": None, "average": None}
        return {
            "min": min(grades),
            "max": max(grades),
            "average": sum(grades) / len(grades)
        }

class Teacher(User):
    def __init__(self, full_name, email, password):
        super().__init__(full_name, email, password, UserRole.TEACHER)
        self.subjects = []
        self.classes = []
        self.assignments_given = {}
        self.workload = 0

    def create_assignment(self, edu_platform, title, description, deadline, subject, class_id, difficulty=AssignmentDifficulty.MEDIUM):
        if subject not in self.subjects:
            print(f"Error: {self._full_name} does not teach {subject}.")
            return None
        if class_id not in self.classes:
            print(f"Error: {self._full_name} does not teach class {class_id}.")
            return None

        new_assignment = Assignment(
            title, description, deadline, subject, self._id, class_id, difficulty
        )
        edu_platform.add_assignment(new_assignment)
        self.assignments_given[new_assignment.id] = new_assignment
        print(f"Assignment '{title}' created by {self._full_name}.")

        for student_id in edu_platform.students_by_class.get(class_id, []):
            student = edu_platform.get_user_by_id(student_id)
            if student:
                student.add_notification(f"New assignment: '{title}' for {subject}. Deadline: {deadline}")
                for parent_id, parent in edu_platform.parents.items():
                    if student._id in parent.children:
                        parent.add_notification(f"Your child, {student._full_name}, has a new assignment: '{title}'.")
        return new_assignment

    def grade_assignment(self, edu_platform, assignment_id, student_id, grade_value, comment=""):
        assignment = self.assignments_given.get(assignment_id)
        if not assignment:
            print(f"Error: Assignment {assignment_id} not found or not created by {self._full_name}.")
            return False
        if student_id not in assignment.submissions:
            print(f"Error: Student {student_id} has not submitted assignment {assignment_id}.")
            return False
        if not (1 <= grade_value <= 5):
            print("Error: Grade value must be between 1 and 5.")
            return False

        assignment.set_grade(student_id, grade_value)
        
        student = edu_platform.get_user_by_id(student_id)
        if student and isinstance(student, Student):
            if assignment.subject not in student.grades:
                student.grades[assignment.subject] = []
            student.grades[assignment.subject].append(grade_value)
            print(f"Grade {grade_value} added for student {student._full_name} in subject {assignment.subject}.")

            new_grade = Grade(student_id, assignment.subject, grade_value, self._id, comment)
            edu_platform.add_grade(new_grade)

            student.add_notification(f"You received a grade of {grade_value} for '{assignment.title}' in {assignment.subject}.", priority=2)
            if grade_value < 3:
                for parent_id, parent in edu_platform.parents.items():
                    if student._id in parent.children:
                        parent.add_notification(f"Urgent: Your child, {student._full_name}, received a low grade ({grade_value}) for '{assignment.title}' in {assignment.subject}.", priority=3)
        return True

    def view_student_progress(self, edu_platform, student_id):
        student = edu_platform.get_user_by_id(student_id)
        if not student or not isinstance(student, Student):
            print(f"Error: Student with ID {student_id} not found.")
            return

        print(f"\nProgress for Student: {student._full_name} (ID: {student._id})")
        print(f"  Class: {student.grade}")
        print("  Subjects and Teachers:")
        for sub, tid in student.subjects.items():
            teacher = edu_platform.get_user_by_id(tid)
            print(f"    - {sub}: {teacher._full_name if teacher else 'N/A'}")

        print("  Assignments Submitted:")
        if not student.assignments:
            print("    No assignments submitted.")
        else:
            for assign_id, status in student.assignments.items():
                assignment = edu_platform.get_assignment_by_id(assign_id)
                print(f"    - {assignment.title if assignment else 'Unknown'}: {status}")

        student.view_grades()
        student.calculate_average_grade()

class Parent(User):
    def __init__(self, full_name, email, password):
        super().__init__(full_name, email, password, UserRole.PARENT)
        self.children = []
        self.notification_preferences = {"low_grade_alert": True, "new_assignment_alert": True}

    def add_child(self, student_id):
        if student_id not in self.children:
            self.children.append(student_id)
            print(f"Child (ID: {student_id}) added for {self._full_name}.")
            return True
        print(f"Child (ID: {student_id}) already linked to {self._full_name}.")
        return False

    def view_child_grades(self, edu_platform, child_id):
        if child_id not in self.children:
            print(f"Error: Child with ID {child_id} is not linked to {self._full_name}.")
            return
        child = edu_platform.get_user_by_id(child_id)
        if child and isinstance(child, Student):
            child.view_grades()
            child.calculate_average_grade()
        else:
            print(f"Error: Child with ID {child_id} not found or is not a student.")

    def view_child_assignments(self, edu_platform, child_id):
        if child_id not in self.children:
            print(f"Error: Child with ID {child_id} is not linked to {self._full_name}.")
            return
        child = edu_platform.get_user_by_id(child_id)
        if child and isinstance(child, Student):
            print(f"\nAssignments for {child._full_name}:")
            if not child.assignments:
                print("  No assignments recorded.")
            else:
                for assign_id, status in child.assignments.items():
                    assignment = edu_platform.get_assignment_by_id(assign_id)
                    print(f"  - {assignment.title if assignment else 'Unknown'}: {status}")
        else:
            print(f"Error: Child with ID {child_id} not found or is not a student.")

    def receive_child_notification(self, edu_platform, child_id):
        if child_id not in self.children:
            print(f"Error: Child with ID {child_id} is not linked to {self._full_name}.")
            return
        child_user = edu_platform.get_user_by_id(child_id)
        if child_user:
            print(f"\nNotifications for {self._full_name} regarding {child_user._full_name}:")
            self.view_notifications()
        else:
            print(f"Child with ID {child_id} not found.")

class Admin(User):
    def __init__(self, full_name, email, password):
        super().__init__(full_name, email, password, UserRole.ADMIN)
        self.permissions = ["manage_users", "generate_reports", "manage_system_settings"]

    def add_user(self, edu_platform, user_obj):
        if edu_platform.get_user_by_email(user_obj._email):
            print(f"Error: User with email {user_obj._email} already exists.")
            return False
        edu_platform.add_user(user_obj)
        print(f"User '{user_obj._full_name}' ({user_obj.role.value}) added by Admin {self._full_name}.")
        return True

    def remove_user(self, edu_platform, user_id):
        if self._id == user_id:
            print("Error: Admin cannot remove themselves.")
            return False
        if edu_platform.remove_user(user_id):
            print(f"User with ID {user_id} removed by Admin {self._full_name}.")
            return True
        print(f"Error: User with ID {user_id} not found to remove.")
        return False

    def generate_report(self, edu_platform):
        print(f"\n--- System Report generated by Admin {self._full_name} ({datetime.datetime.now().isoformat()}) ---")
        print(f"Total Users: {len(edu_platform.users)}")
        print(f"  Admins: {sum(1 for u in edu_platform.users.values() if u.role == UserRole.ADMIN)}")
        print(f"  Teachers: {sum(1 for u in edu_platform.users.values() if u.role == UserRole.TEACHER)}")
        print(f"  Students: {sum(1 for u in edu_platform.users.values() if u.role == UserRole.STUDENT)}")
        print(f"  Parents: {sum(1 for u in edu_platform.users.values() if u.role == UserRole.PARENT)}")

        print(f"\nTotal Assignments: {len(edu_platform.assignments)}")
        print(f"Total Grades: {len(edu_platform.grades)}")
        print(f"Total Schedules: {len(edu_platform.schedules)}")
        print(f"Total Notifications: {sum(len(u._notifications) for u in edu_platform.users.values())}")

        print("\nStudent Performance Overview:")
        for student in edu_platform.students.values():
            print(f"  - {student._full_name} (ID: {student._id}, Class: {student.grade})")
            student.calculate_average_grade()
        print("--- End of Report ---")
        return {
            "total_users": len(edu_platform.users),
            "total_assignments": len(edu_platform.assignments),
            "total_grades": len(edu_platform.grades)
        }
