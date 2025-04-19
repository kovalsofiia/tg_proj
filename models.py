class BaseUserData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.full_name = None
        self.phone_number = None
        self.role = None

class StudentData(BaseUserData):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.faculty = None
        self.education_degree = None
        self.specialty = None
        self.course = None

class EmployeeData(BaseUserData):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.faculty = None
        self.department = None
        self.position = None
