from typing import List

class CourseSchedule:
    def __init__(self, day_of_week: str, start_period: str, end_period: str):
        self.day_of_week = day_of_week
        self.start_period = start_period
        self.end_period = end_period

    def to_dict(self):
        return {
            "星期": self.day_of_week,
            "開始節次": self.start_period,
            "結束節次": self.end_period,
        }

class Course:
    def __init__(self, 
                 course_category: str,
                 course_subcategory: str,
                 dept_code: str,
                 course_serial_number: str,
                 course_name: str,
                 syllabus_url: str,
                 permanent_course_id: str,
                 offering_unit: str,
                 academic_program: str,
                 college: str,
                 department: str,
                 group: str,
                 target_grade: str,
                 class_section: str,
                 requirement_type: str,
                 credits: str,
                 hours: str,
                 semesters: str,
                 instruction_mode: str,
                 remarks: str,
                 instructor: str,
                 schedule: List['CourseSchedule'],
                 classroom: str,
                 campus: str,
                 capacity_limit: str,
                 enrollment_restrictions: str,
                 ):
        self.course_category = course_category
        self.course_subcategory = course_subcategory
        self.dept_code = dept_code
        self.course_serial_number = course_serial_number
        self.course_name = course_name
        self.syllabus_url = syllabus_url
        self.permanent_course_id = permanent_course_id
        self.offering_unit = offering_unit
        self.academic_program = academic_program
        self.college = college
        self.department = department
        self.group = group
        self.target_grade = target_grade
        self.class_section = class_section
        self.requirement_type = requirement_type
        self.credits = credits
        self.hours = hours
        self.semesters = semesters
        self.instruction_mode = instruction_mode
        self.remarks = remarks
        self.instructor = instructor
        self.schedule = schedule
        self.classroom = classroom
        self.campus = campus
        self.capacity_limit = capacity_limit
        self.enrollment_restrictions = enrollment_restrictions

    def to_dict(self):
        return {
            '選課類別': self.course_category,
            '課程類別': self.course_subcategory,
            '開課系號': self.dept_code,
            '開課序號': self.course_serial_number,
            '課程名稱': self.course_name,
            '教學大綱': self.syllabus_url,
            '永久課號': self.permanent_course_id,
            '開課單位': self.offering_unit,
            '上課學制': self.academic_program,
            '上課學院': self.college,
            '上課系所': self.department,
            '上課組別': self.group,
            '適用年級': self.target_grade,
            '上課班別': self.class_section,
            '課程修別': self.requirement_type,
            '學分數': self.credits,
            '時數': self.hours,
            '學期數': self.semesters,
            '授課類別': self.instruction_mode,
            '備註': self.remarks,
            '授課老師': self.instructor,
            '上課時間': [s.to_dict() for s in self.schedule],
            '上課教室': self.classroom,
            '校區': self.campus,
            '限修人數': self.capacity_limit,
            '限選條件': self.enrollment_restrictions,
        }