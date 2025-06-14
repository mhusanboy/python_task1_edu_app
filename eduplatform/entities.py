import datetime 
from eduplatform.enums import AssignmentDifficulty

class Assignment:
    _next_id = 1

    def __init__(self, title, description, deadline, subject, teacher_id, class_id, difficulty=AssignmentDifficulty.MEDIUM):
        self.id = Assignment._next_id
        Assignment._next_id += 1
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty
        self.submissions = {}
        self.grades = {}

    def add_submission(self, student_id, content):
        self.submissions[student_id] = content
        print(f"Submission for assignment '{self.title}' added by student {student_id}.")

    def set_grade(self, student_id, grade_value):
        self.grades[student_id] = grade_value
        print(f"Grade {grade_value} set for student {student_id} on assignment '{self.title}'.")

    def get_status(self, student_id=None):
        if student_id:
            if student_id in self.grades:
                return f"Graded: {self.grades[student_id]}"
            elif student_id in self.submissions:
                return "Submitted (Not Graded)"
            else:
                return "Not Submitted"
        
        now = datetime.datetime.now().isoformat()
        if now > self.deadline:
            return "Closed (Past Deadline)"
        return "Open"

class Grade:
    _next_id = 1

    def __init__(self, student_id, subject, value, teacher_id, comment=""):
        self.id = Grade._next_id
        Grade._next_id += 1
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = datetime.datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.comment = comment

    def update_grade(self, new_value, new_comment=""):
        if not (1 <= new_value <= 5):
            print("Error: Grade value must be between 1 and 5.")
            return False
        self.value = new_value
        self.comment = new_comment
        self.date = datetime.datetime.now().isoformat()
        print(f"Grade {self.id} updated to {self.value}.")
        return True

    def get_grade_info(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }

class Schedule:
    _next_id = 1

    def __init__(self, class_id, day):
        self.id = Schedule._next_id
        Schedule._next_id += 1
        self.class_id = class_id
        self.day = day
        self.lessons = {}

    def add_lesson(self, time, subject, teacher_id, edu_platform):
        if time in self.lessons:
            print(f"Error: A lesson already exists at {time} for class {self.class_id} on {self.day}.")
            return False

        for sch_id, schedule in edu_platform.schedules.items():
            if schedule.day == self.day and time in schedule.lessons:
                existing_lesson = schedule.lessons[time]
                if existing_lesson.get("teacher_id") == teacher_id:
                    print(f"Error: Teacher {teacher_id} is already scheduled to teach {existing_lesson['subject']} in class {schedule.class_id} at {time} on {self.day}.")
                    return False

        self.lessons[time] = {"subject": subject, "teacher_id": teacher_id}
        print(f"Lesson '{subject}' added for class {self.class_id} at {time} on {self.day}.")
        return True

    def view_schedule(self):
        print(f"\nSchedule for Class {self.class_id} on {self.day}:")
        if not self.lessons:
            print("  No lessons scheduled.")
            return {}
        
        sorted_lessons = sorted(self.lessons.items())
        for time, details in sorted_lessons:
            print(f"  - {time}: Subject: {details['subject']}, Teacher ID: {details['teacher_id']}")
        return self.lessons

    def remove_lesson(self, time):
        if time in self.lessons:
            del self.lessons[time]
            print(f"Lesson at {time} removed from schedule for class {self.class_id} on {self.day}.")
            return True
        print(f"Error: No lesson found at {time} for class {self.class_id} on {self.day}.")
        return False


class Notification:
    _next_id = 1

    def __init__(self, message, recipient_id, created_at=None, is_read=False, priority=0):
        self.id = Notification._next_id
        Notification._next_id += 1
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
        self.is_read = is_read
        self.priority = priority

    def send(self):
        print(f"Notification {self.id} (for {self.recipient_id}) is ready to be sent.")

    def mark_as_read(self):
        self.is_read = True

    def get_info(self):
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "is_read": self.is_read,
            "priority": self.priority
        }
