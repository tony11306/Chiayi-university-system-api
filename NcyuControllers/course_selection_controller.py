from flask import jsonify
from flask_restful import Resource, reqparse
from .decorators import exception_decorator
from Proxies.firebase_proxy import FirebaseProxy

_CLASS_MAP = {'1': 1, '2': 2, '3': 3, '4': 4, 'F': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, 'A': 11, 'B': 12, 'C': 13, 'D': 14}

class CourseSelectionController(Resource):
    def __init__(self, firebase_proxy: FirebaseProxy) -> None:
        self.firebase_proxy = firebase_proxy
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('校區', type=str, required=False)
        self.reqparse_args.add_argument('上課系所', type=str, required=False)
        self.reqparse_args.add_argument('適用年級', type=str, required=False)
        self.reqparse_args.add_argument('課程修別', type=str, required=False)
        self.reqparse_args.add_argument('上課學院', type=str, required=False)
        self.reqparse_args.add_argument('星期', type=str, required=False)
        self.reqparse_args.add_argument('開始節次', type=str, required=False)
        self.reqparse_args.add_argument('結束節次', type=str, required=False)
        self.reqparse_args.add_argument('課程類別', type=str, required=False)
        self.reqparse_args.add_argument('上課學制', type=str, required=False)
        super().__init__()

    @exception_decorator
    def get(self):
        args = self.reqparse_args.parse_args()
        
        # Fetch data from FirebaseProxy
        semester_obj, courses_list = self.firebase_proxy.get_all_courses()

        # Filter logic
        campus = args['校區']
        department = args['上課系所']
        grade = args['適用年級']
        course_type = args['課程修別']
        academy = args['上課學院']
        day = args['星期']
        start_class = args['開始節次']
        end_class = args['結束節次']
        course_classification = args['課程類別']
        education_level = args['上課學制']

        result = []

        for course in courses_list:
            if campus is not None and course.campus != campus:
                continue
            if department is not None and course.department != department:
                continue
            if grade is not None and str(course.target_grade) != grade:
                continue
            if course_type is not None and course.requirement_type != course_type:
                continue
            if academy is not None and course.college != academy:
                continue
            if course_classification is not None and course.course_subcategory != course_classification:
                continue
            if education_level is not None and course.academic_program != education_level:
                continue
            
            # Time filtering
            if day is not None or start_class is not None or end_class is not None:
                flag = False
                for course_time in course.schedule:
                    isMatch = True
                    if day is not None and course_time.day_of_week != day:
                        isMatch = False
                    
                    # Safely get mapped values, default to a high number if not found
                    req_start_mapped = _CLASS_MAP.get(start_class, 99)
                    req_end_mapped = _CLASS_MAP.get(end_class, 0)
                    course_start_mapped = _CLASS_MAP.get(str(course_time.start_period), 99)
                    course_end_mapped = _CLASS_MAP.get(str(course_time.end_period), 0)

                    if start_class is not None and end_class is not None:
                        if req_start_mapped > course_start_mapped or req_end_mapped < course_end_mapped:
                            isMatch = False
                    elif start_class is not None and course_time.start_period != int(start_class):
                        isMatch = False
                    elif end_class is not None and course_time.end_period != int(end_class):
                        isMatch = False
                    
                    if isMatch:
                        flag = True
                        break # Found a matching time slot
                
                if not flag:
                    continue

            result.append(course)

        # Serialize result back to dicts for JSON response
        result_dicts = [c.to_dict() for c in result]

        return jsonify({'result': result_dicts, 'semester': str(semester_obj)})