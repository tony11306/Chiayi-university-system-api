from firebase_admin import firestore
from cachetools import cached, TTLCache
from typing import Tuple, List, Dict, Any
import re

from Models.course import Course, CourseSchedule
from Models.semester import Semester

def _safe_int(value, default=0):
    """Safely converts a value to an integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def _dict_to_course(data: Dict[str, Any]) -> Course:
    """Maps a dictionary from Firestore to a Course object."""
    
    schedule_data = data.get('上課時間', [])
    schedule = [
        CourseSchedule(
            day_of_week=item.get('星期'),
            start_period=item.get('開始節次'),
            end_period=item.get('結束節次')
        ) for item in schedule_data
    ]

    return Course(
        course_category=data.get('選課類別', ''),
        course_subcategory=data.get('課程類別', ''),
        dept_code=data.get('開課系號', ''),
        course_serial_number=data.get('開課序號', ''),
        course_name=data.get('課程名稱', ''),
        syllabus_url=data.get('教學大綱', ''),
        permanent_course_id=data.get('永久課號', ''),
        offering_unit=data.get('開課單位', ''),
        academic_program=data.get('上課學制', ''),
        college=data.get('上課學院', ''),
        department=data.get('上課系所', ''),
        group=data.get('上課組別', ''),
        target_grade=data.get('適用年級'),
        class_section=data.get('上課班別', ''),
        requirement_type=data.get('課程修別', ''),
        credits=data.get('學分數'),
        hours=data.get('時數'),
        semesters=data.get('學期數'),
        instruction_mode=data.get('授課類別', ''),
        remarks=data.get('備註', ''),
        instructor=data.get('授課老師', ''),
        schedule=schedule,
        classroom=data.get('上課教室', ''),
        campus=data.get('校區', ''),
        capacity_limit=data.get('限修人數'),
        enrollment_restrictions=data.get('限選條件', '')
    )

class FirebaseProxy:
    def __init__(self, db: firestore.Client):
        self.db = db

    @cached(cache=TTLCache(maxsize=1, ttl=3600))
    def get_all_courses(self) -> Tuple[Semester, List[Course]]:
        """
        Fetches all courses from Firestore with a 1-hour cache.

        Returns:
            A tuple containing the Semester object and a list of Course objects.
        """
        print("Fetching course data from Firestore (not from cache)...")
        # 1. Get semester metadata
        metadata_ref = self.db.collection('metadata').document('current_semester')
        metadata_doc = metadata_ref.get()
        
        year, term = 0, 0
        if metadata_doc.exists:
            metadata_dict = metadata_doc.to_dict()
            year = _safe_int(metadata_dict.get('year'))
            term = _safe_int(metadata_dict.get('term'))
        semester = Semester(year=year, term=term)

        # 2. Get all courses
        courses_ref = self.db.collection('courses')
        docs = courses_ref.stream()
        courses = [_dict_to_course(doc.to_dict()) for doc in docs]

        return semester, courses