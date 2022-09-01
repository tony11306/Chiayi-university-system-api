from Interface.Service.course_service import CourseServiceInterface
from flask_restful import Resource, reqparse
from flask import jsonify, request
import urllib.parse

class CourseSelectionHandler(Resource):
    
    def __init__(self, course_service: CourseServiceInterface):
        self.course_service = course_service
        super().__init__()

    def get(self):
        query_string = urllib.parse.unquote(request.query_string)
        return jsonify({
            'result': list(map(lambda course: course.to_json(), self.course_service.get_courses(query_string)))
        })