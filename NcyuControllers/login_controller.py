from flask import jsonify, abort
from flask_restful import Resource, reqparse
from Proxies.ncyu_proxy import NcyuAPIProxy
from .decorators import exception_decorator

class LoginEndpoint(Resource):
    def __init__(self, ncyu_api_proxy: NcyuAPIProxy) -> None:
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('account', type=str, required=True, help='account is required')
        self.reqparse_args.add_argument('password', type=str, required=True, help='password is required')
        self.ncyu_api_proxy = ncyu_api_proxy
        super().__init__()

    @exception_decorator
    def post(self):
        args = self.reqparse_args.parse_args()
        account = args['account']
        password = args['password']

        webpid1, error = self.ncyu_api_proxy.login(account, password)

        if error is not None:
            if error == "Login failed":
                abort(401, description=error)
            elif error == "Failed to solve captcha":
                abort(500, description=error)
            else:
                abort(417, description=error)
        
        return jsonify({'result': {'webpid1': webpid1}})
        