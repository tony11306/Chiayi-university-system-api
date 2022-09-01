from Interface.Service.ncyu_proxy_service import NCYUProxyServiceInterface
from flask_restful import Resource, reqparse
from flask import abort, jsonify

class LoginHandler(Resource):

    def __init__(self, ncyu_proxy_service: NCYUProxyServiceInterface):
        self.ncyu_proxy_service = ncyu_proxy_service
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account', type=str, required=True, help='Account is required', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='Password is required', location='json')
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        account = args['account']
        password = args['password']

        return jsonify({
            'result': {
                'webpid1': self.ncyu_proxy_service.login(account, password)
            }
        })