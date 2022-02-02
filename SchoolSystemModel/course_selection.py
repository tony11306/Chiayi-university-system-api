from flask import jsonify, abort
from flask_restful import Resource, reqparse
import requests
import json
from bs4 import BeautifulSoup
from SchoolSystemModel.decorators import exception_decorator

with open('./SchoolSystemModel/current_semester_course_datas/current_semester_course_datas.json', 'r', encoding='utf-8') as f:
    _datas = json.load(f)
    _data = _datas['所有課程']
    _semester = _datas['選課學年']

_CLASS_MAP = {'1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    'F': 5,
    '5': 6,
    '6': 7,
    '7': 8,
    '8': 9,
    '9': 10,
    'A': 11,
    'B': 12,
    'C': 13,
    'D': 14
}

class CourseSelectionEndpoint(Resource):

    def __init__(self) -> None:
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

        for course in _data:
            if campus is not None and course['校區'] != campus:
                continue
            if department is not None and course['上課系所'] != department:
                continue
            if grade is not None and course['適用年級'] != grade:
                continue
            if course_type is not None and course['課程修別'] != course_type:
                continue
            if academy is not None and course['上課學院'] != academy:
                continue
            if course_classification is not None and course['課程類別'] != course_classification:
                continue
            if education_level is not None and course['上課學制'] != education_level:
                continue
            if day is not None or start_class is not None or end_class is not None:
                flag = False
                for course_time in course['上課時間']:
                    isMatch = True
                    if day is not None and course_time['星期'] != day:
                        isMatch = False
                    if start_class is not None and end_class is not None:
                        if _CLASS_MAP[start_class] > _CLASS_MAP[course_time['開始節次']] or _CLASS_MAP[end_class] < _CLASS_MAP[course_time['結束節次']]:
                            isMatch = False
                    elif start_class is not None and course_time['開始節次'] != start_class:
                        isMatch = False
                    elif end_class is not None and course_time['結束節次'] != end_class:
                        isMatch = False
                    flag = flag or isMatch
                if not flag:
                    continue

            result.append(course)

        return jsonify({'result': result, 'semester': _semester})