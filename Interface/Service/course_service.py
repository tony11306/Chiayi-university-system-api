from typing import List
from Model.course import Course

class CourseServiceInterface:

    def get_courses(self, query_params) -> List[Course]:
        raise NotImplementedError
    
    def get_course(self, query_params) -> Course:
        raise NotImplementedError

    def add_course(self, course: Course):
        raise NotImplementedError
    
    def delete_course(self, course: Course):
        raise NotImplementedError
    
    def update_course(self, course: Course):
        raise NotImplementedError
    
