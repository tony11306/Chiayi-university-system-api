from flask import jsonify
from flask_restful import Resource, reqparse
from .decorators import exception_decorator
from Proxies.ncyu_proxy import NcyuAPIProxy

class GradeController(Resource):
    def __init__(self, ncyu_api_proxy: NcyuAPIProxy) -> None:
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('webpid1', type=str, required=True, help='webpid1 is required')
        self.ncyu_api_proxy = ncyu_api_proxy
        super().__init__()

    @exception_decorator
    def post(self):
        args = self.reqparse_args.parse_args()
        webpid1 = args['webpid1']
        
        grades = self.ncyu_api_proxy.get_grades(webpid1)
        
        return jsonify({'result': {'所有學期': grades}})