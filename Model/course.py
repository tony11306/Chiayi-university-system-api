from Model.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, CHAR
from sqlalchemy.orm import relationship

class Course(db.Model):
    __tablename__ = 'Course'
    id = Column(Integer, primary_key=True)
    selection_category = Column(String(255), nullable=False)
    course_category = Column(String(255), nullable=False)
    department_code = Column(String(64), nullable=False)
    course_number = Column(String(64), nullable=False)
    name = Column(String(255), nullable=False)
    outline_url = Column(String(255), nullable=False)
    permanent_course_number = Column(String(64), nullable=False)
    department_name = Column(String(64), nullable=False)
    education_level = Column(String(64), nullable=False)
    college_name = Column(String(64), nullable=False)
    target_department_name = Column(String(64), nullable=False)
    group_type = Column(String(64), nullable=False)
    grade = Column(Integer, nullable=False)
    class_ = Column(String(64), nullable=False)
    course_type = Column(String(64), nullable=False)
    credit = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    semester_count = Column(Integer, nullable=False)
    teaching_type = Column(String(64), nullable=False)
    remark = Column(String(255), nullable=False)
    teacher_name = Column(String(255), nullable=False)
    course_time = relationship('CourseTime', backref='Course')
    classroom = Column(String(255), nullable=False)
    campus = Column(String(255), nullable=False)
    sutdent_limit = Column(Integer, nullable=False)
    limit_condition = Column(String(255), nullable=False)

    def to_json(self):	
        return {	
            '選課類別': self.selection_category,	
            '課程類別': self.course_category,	
            '開課系號': self.department_code,	
            '開課序號': self.course_number,	
            '課程名稱': self.name,	
            '教學大綱': self.outline_url,	
            '永久課號': self.permanent_course_number,	
            '開課單位': self.department_name,	
            '上課學制': self.education_level,	
            '上課學院': self.college_name,	
            '上課系所': self.target_department_name,	
            '上課組別': self.group_type,	
            '適用年級': self.grade,	
            '上課班別': self.class_,	
            '課程修別': self.course_type,	
            '學分數': self.credit,	
            '時數': self.hour,	
            '學期數': self.semester_count,	
            '授課類別': self.teaching_type,	
            '備註': self.remark,	
            '授課老師': self.teacher_name,	
            '上課時間': list(map(lambda time: time.to_json(), self.course_time)),	
            '上課教室': self.classroom,	
            '校區': self.campus,	
            '限修人數': self.sutdent_limit,	
            '限選條件': self.limit_condition	
        }