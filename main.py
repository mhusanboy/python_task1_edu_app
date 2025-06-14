import datetime
from eduplatform.core import EduPlatform
from eduplatform.users import Student, Teacher, Parent
from eduplatform.entities import Schedule
from eduplatform.enums import AssignmentDifficulty


def main():
    print("Starting EduPlatform Application Demo...\n")
    platform = EduPlatform()

    print("\n--- User Authentication ---")
    admin_user = platform.authenticate_user("admin@edu.com", "adminpass")
    teacher_user = platform.authenticate_user("mrhusanboy2006pm@gmail.com", "teachpass")
    student_user = platform.authenticate_user("mardonbekhazratov@gmail.com", "studentpass")
    parent_user = platform.authenticate_user("david@edu.com", "parentpass")

    platform.authenticate_user("fake@edu.com", "wrongpass")

    print("\n--- Admin Actions ---")
    if admin_user:
        new_student = Student("Cristiano Ronaldo", "CristianoRondaldo@gmail.com", "evepass", "9-B")
        admin_user.add_user(platform, new_student)
        
        teacher_user.update_profile(phone="998-94-123-45-67", address="123 Tashkent Rd")
        print(teacher_user.get_profile())

        admin_user.generate_report(platform)
        
    print("\n--- Teacher Actions ---")
    if teacher_user and isinstance(teacher_user, Teacher):
        deadline = (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        assignment1 = teacher_user.create_assignment(
            platform, "Algebra Homework 1", "Solve problems 1-5 from Chapter 3.",
            deadline, "Math", "10-A", AssignmentDifficulty.MEDIUM
        )

        deadline2 = (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat()
        assignment2 = teacher_user.create_assignment(
            platform, "Informatics Lab Report", "Write a report on the group python project.",
            deadline2, "Informatics", "11-B", AssignmentDifficulty.HARD
        )
        
        student3 = Student("Grace Lee", "grace@edu.com", "gracepass", "11-B")
        student3.subjects = {"Informatics": teacher_user._id}
        platform.add_user(student3)

    print("\n--- Student Actions ---")
    if student_user and isinstance(student_user, Student):
        if assignment1:
            student_user.submit_assignment(assignment1, "My detailed solutions for Algebra HW1.")
        
        student_user.view_grades()

    print("\n--- Teacher Grading ---")
    if teacher_user and isinstance(teacher_user, Teacher) and student_user:
        if assignment1:
            teacher_user.grade_assignment(platform, assignment1.id, student_user._id, 4, "Good effort, check problem 3.")

        teacher_user.view_student_progress(platform, student_user._id)

    if student_user and isinstance(student_user, Student):
        student_user.view_grades()
        student_user.calculate_average_grade()
        print(f"Student {student_user._full_name} Math Stats: {student_user.get_subject_stats('Math')}")

    print("\n--- Parent Actions ---")
    if parent_user and isinstance(parent_user, Parent) and student_user:
        parent_user.view_child_grades(platform, student_user._id)
        parent_user.view_child_assignments(platform, student_user._id)
        parent_user.receive_child_notification(platform, student_user._id)

    print("\n--- Notification Management ---")
    if student_user:
        student_user.add_notification("Don't forget your upcoming Informatics test!", priority=1)
        student_user.view_notifications()
        student_user.mark_notification_as_read(student_user._notifications[0].id)
        student_user.view_notifications(unread_only=True)
        student_user.view_notifications(important_only=True)
    
    print("\n--- Schedule Management ---")
    schedule10A_mon = Schedule("10-A", "Monday")
    platform.add_schedule(schedule10A_mon)
    
    schedule10A_mon.add_lesson("09:00", "Math", teacher_user._id, platform)
    schedule10A_mon.add_lesson("10:00", "Chemistry", teacher_user._id, platform)
    schedule10A_mon.add_lesson("11:00", "History", 999, platform)

    schedule11B_mon = Schedule("11-B", "Monday")
    platform.add_schedule(schedule11B_mon)
    schedule11B_mon.add_lesson("09:00", "Informatics", teacher_user._id, platform)

    schedule10A_mon.view_schedule()
    schedule11B_mon.view_schedule()

    print("\n--- Data Export ---")
    platform.export_to_xlsx()
    platform.export_to_csv()
    platform.export_to_sql()

    print("\nEduPlatform Application Demo Finished.")

if __name__ == "__main__":
    main()
