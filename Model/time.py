from ..app import db
from sqlalchemy import Column, Integer, String, ForeignKey

class CourseTime(db.Model):
    __tablename__ = 'Time'
    id = Column(Integer, primary_key=True)
    day = Column(String(10))
    start_time = Column(String(10))
    end_time = Column(String(10))
    course_id = Column(Integer, ForeignKey('Course.id'))