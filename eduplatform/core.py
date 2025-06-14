import datetime
from eduplatform.users import Admin, Teacher, Student, Parent, UserRole
from eduplatform.utils import export_to_xlsx, export_to_csv, export_to_sql
from pathlib import Path
import os

current_dir = Path(__file__).resolve().parent



class EduPlatform:
    def __init__(self):
        self.users = {}
        self.admins = {}
        self.teachers = {}
        self.students = {}
        self.parents = {}
        
        self.assignments = {}
        self.grades = {}
        self.schedules = {}
        self.notifications = {}
        
        self.users_by_email = {}
        self.students_by_class = {}

        self.export_log = []

        self._initialize_system_data()

    def _initialize_system_data(self):
        try:
            os.mkdir(current_dir/"eduplatform_dataset_files")
        except FileExistsError:
            pass
        except OSError as e:
            print(f"Error creating folder: {e}")
        try:
            os.mkdir(current_dir/"auto_exported_files")
        except FileExistsError:
            pass
        except OSError as e:
            print(f"Error creating folder: {e}")
        
        print("Initializing system with default data...")
        admin = Admin("Super Admin", "admin@edu.com", "adminpass")
        self.add_user(admin)

        teacher1 = Teacher("Husanboy Mansuraliyev", "mrhusanboy2006pm@gmail.com", "teachpass")
        teacher1.subjects = ["Math", "Informatics"]
        teacher1.classes = ["10-A", "11-B"]
        self.add_user(teacher1)

        student1 = Student("Mardon Hazratov", "mardonbekhazratov@gmail.com", "studentpass", "10-A")
        student1.subjects = {"Math": teacher1._id, "Informatics": teacher1._id}
        self.add_user(student1)

        student2 = Student("Shahriyor Yuldashev", "yuldshah@gmail.com", "studentpass", "10-A")
        student2.subjects = {"Math": teacher1._id}
        self.add_user(student2)
        
        parent1 = Parent("David Johnson", "david@edu.com", "parentpass")
        parent1.add_child(student1._id)
        self.add_user(parent1)
        
        print("System initialization complete.")

    def add_user(self, user_obj):
        if user_obj._email in self.users_by_email:
            return False
        
        self.users[user_obj._id] = user_obj
        self.users_by_email[user_obj._email] = user_obj

        if user_obj.role == UserRole.ADMIN:
            self.admins[user_obj._id] = user_obj
        elif user_obj.role == UserRole.TEACHER:
            self.teachers[user_obj._id] = user_obj
        elif user_obj.role == UserRole.STUDENT:
            self.students[user_obj._id] = user_obj
            if user_obj.grade not in self.students_by_class:
                self.students_by_class[user_obj.grade] = []
            self.students_by_class[user_obj.grade].append(user_obj._id)
        elif user_obj.role == UserRole.PARENT:
            self.parents[user_obj._id] = user_obj
        return True

    def remove_user(self, user_id):
        user = self.users.pop(user_id, None)
        if user:
            self.users_by_email.pop(user._email, None)
            if user.role == UserRole.ADMIN:
                self.admins.pop(user_id, None)
            elif user.role == UserRole.TEACHER:
                self.teachers.pop(user_id, None)
            elif user.role == UserRole.STUDENT:
                self.students.pop(user_id, None)
                if user.grade in self.students_by_class:
                    self.students_by_class[user.grade].remove(user_id)
            elif user.role == UserRole.PARENT:
                self.parents.pop(user_id, None)
            return True
        return False

    def get_user_by_id(self, user_id):
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        return self.users_by_email.get(email)

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            print(f"Authentication successful for {user._full_name} ({user.role.value}).")
            return user
        print("Authentication failed: Invalid email or password.")
        return None

    def add_assignment(self, assignment_obj):
        self.assignments[assignment_obj.id] = assignment_obj
        print(f"Assignment '{assignment_obj.title}' added to platform.")
        self._auto_export()

    def get_assignment_by_id(self, assignment_id):
        return self.assignments.get(assignment_id)

    def add_grade(self, grade_obj):
        self.grades[grade_obj.id] = grade_obj
        print(f"Grade {grade_obj.value} for student {grade_obj.student_id} added to platform.")
        self._auto_export()

    def add_schedule(self, schedule_obj):
        self.schedules[schedule_obj.id] = schedule_obj
        print(f"Schedule for class {schedule_obj.class_id} on {schedule_obj.day} added to platform.")

    def add_notification(self, notification_obj):
        self.notifications[notification_obj.id] = notification_obj

    def _auto_export(self):
        print("\nPerforming automatic data export...")
        self.export_to_xlsx(filename=current_dir/"auto_exported_files/auto_export.xlsx")
        self.export_to_csv(filename_prefix=current_dir/"auto_exported_files/auto_export_")
        self.export_to_sql(filename=current_dir/"auto_exported_files/auto_export.sql")
        self.export_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "action": "Auto Export",
            "formats": ["xlsx", "csv", "sql"]
        })
        print("Automatic export complete.")

    def validate_data_for_export(self):
        print("Validating data for export...")
        is_valid = True
        for user_id, user in self.users.items():
            if not user._full_name or not user._email:
                print(f"Validation Error: User {user_id} has empty full_name or email.")
                is_valid = False
        if is_valid:
            print("Data validation successful.")
        else:
            print("Data validation failed. Check for errors.")
        return is_valid

    def export_to_xlsx(self, filename=current_dir/"eduplatform_dataset_files/eduplatform_data.xlsx"):
        export_to_xlsx(self, filename)

    def export_to_csv(self, filename_prefix=current_dir/"eduplatform_dataset_files/edueduplatform_data_"):
        export_to_csv(self, filename_prefix)

    def export_to_sql(self, filename=current_dir/"eduplatform_dataset_files/eduplatform_data.sql"):
        export_to_sql(self, filename)

    def _scrape_data(self, url="https://www.olx.uz/"):pass



