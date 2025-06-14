import enum

class UserRole(enum.Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

class AssignmentDifficulty(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"