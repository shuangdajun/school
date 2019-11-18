class StudentViewModel:
    def __init__(self,students):
        self.student_name=students.student_name
        self.student_sex=students.student_sex or ""
        self.student_age=students.student_age or ""
        self.student_phone=students.student_phone or ""
        self.student_landline=students.student_landline or ""

