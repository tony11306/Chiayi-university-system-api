from Interface.Service.ncyu_proxy_service import NCYUProxyServiceInterface
from flask_restful import Resource, reqparse
from flask import jsonify

class PersonalGradeHandler(Resource):

    def __init__(self, ncyu_proxy_service: NCYUProxyServiceInterface):
        self.ncyu_proxy_service = ncyu_proxy_service
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('webpid1', type=str, required=True, help='Webpid1 is required', location='json')
        super().__init__()
    
    def post(self):
        args = self.reqparse.parse_args()
        webpid1 = args['webpid1']

        return jsonify({
            'result': {
                '所有學期': self.ncyu_proxy_service.get_personal_courses(webpid1)
            }
        })