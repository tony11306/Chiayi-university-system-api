from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from course import CourseEndpoint
from login import LoginEndpoint
from grades import GradeEndpoint

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MINETYPE'] = 'application/json;charset=utf-8'
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


    api.add_resource(CourseEndpoint, '/course/<string:webpid1>')
    api.add_resource(LoginEndpoint, '/login/<string:account>/<string:password>')
    api.add_resource(GradeEndpoint, '/grade/<string:webpid1>')

    app.run(debug=False)


