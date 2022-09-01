from ast import Delete
from Model.course import Course
from Model.time import CourseTime
from typing import List
from Interface.Service.course_service import CourseServiceInterface
from flask_sqlalchemy import SQLAlchemy

class CourseService(CourseServiceInterface):
    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    @staticmethod
    def query_string_to_dict(query_string):
        MAPPING_TABLE = {
            '校區': 'campus',
            '上課系所': 'target_department_name',
            '適用年級': 'grade',
            '課程修別': 'course_type',
            '上課學院': 'college_name',
            '星期': 'day',
            '開始節次': 'start_time',
            '結束節次': 'end_time',
            '課程類別': 'course_category',
            '上課學制': 'education_level',
        }
        query_dict = {}
        for query in query_string.split('&'):
            if query == '':
                continue
            key, value = query.split('=')
            if key in MAPPING_TABLE and value != '':
                query_dict[MAPPING_TABLE[key]] = value

        return query_dict

    def get_courses(self, query_params) -> List[Course]:
        query_dict = self.query_string_to_dict(query_params)
        time_info = {}
        if 'day' in query_dict:
            time_info['day'] = query_dict['day']
            del query_dict['day']
        if 'start_time' in query_dict:
            time_info['start_time'] = query_dict['start_time']
            del query_dict['start_time']
        if 'end_time' in query_dict:
            time_info['end_time'] = query_dict['end_time']
            del query_dict['end_time']


        courses = self.db.session.query(Course).filter_by(
            **query_dict, 
        ).join(CourseTime).filter_by(
            **time_info
        ).all()

        return courses
    
    def get_course(self, query_params) -> Course:
        query_dict = self.query_string_to_dict(query_params)
        time_info = {}
        if 'day' in query_dict:
            time_info['day'] = query_dict['day']
            del query_dict['day']
        if 'start_time' in query_dict:
            time_info['start_time'] = query_dict['start_time']
            del query_dict['start_time']
        if 'end_time' in query_dict:
            time_info['end_time'] = query_dict['end_time']
            del query_dict['end_time']

        course = self.db.session.query(Course).filter_by(
            **query_dict, 
        ).join(CourseTime).filter_by(
            **time_info
        ).first()
        return course

    def add_course(self, course: Course):
        self.db.session.add(course)
        self.db.session.commit()
    
    def delete_course(self, course: Course):
        self.db.session.delete(course)
        self.db.session.commit()
    
    def update_course(self, course: Course):
        self.db.session.commit()
    
    

