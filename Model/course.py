from ..app import db
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