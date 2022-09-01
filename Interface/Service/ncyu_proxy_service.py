class NCYUProxyServiceInterface:

    def login(self, account: str, password: str) -> str:
        raise NotImplementedError
    
    def get_student_grade(self, webpid1: str):
        raise NotImplementedError
    
    def get_personal_courses(self, webpid1: str):
        raise NotImplementedError