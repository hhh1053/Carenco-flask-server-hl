import random
from flask import Flask, request
from flask_restx import Api, Resource
from database.database import S3
from database.sql import Sql
from services.foot import Foot
import services.ocr as ocr

# Swagger(flask_restx) Configuration
app = Flask(__name__)
api = Api(app, version='1.0', title='Carenco Flask Server',
          description='Carenco Flask Server 입니다. 각 Api들을 테스트할 수 있습니다.')

class BaseService(Resource):
    def __init__(self):
        self.sql = Sql()
        self.foot = Foot()
        self.s3 = S3()

@api.route('/image')
class Image(BaseService):
    def put(self) -> str:
        ''' ID 값을 받아 사용자를 특정하고 이미지와 몸무게를 저장하는 Api '''
        params = request.get_json(force=True)
        if 'id' not in params:
            return {"error": "invalid request parameters: 'id' not found"}, 400

        id = params['id']
        _, weight_values = self.foot.generate_image(params, './')
        image_url = self.s3.ImageUploadToS3(id)
        self.sql.save(id, image_url, weight_values)
        return image_url


@api.route("/health")
class Health(Resource):
    def get(self):
        ''' Health Test Api '''
        return ""


@api.route("/check")
class Check(Resource):
    def get(self):
        ''' Check Test Api '''
        return "check"


@api.route('/ocr')
class Ocr(BaseService):
    def put(self) -> str:
        ''' 이미지 FILE을 받아 구글 Vision Api를 통해 OCR 진행하고 결과값을 받아 저장하는 Api '''
        if 'file' not in request.files:
            return {"error": "image file not found in request"}, 400

        file = request.files['file']
        data = ocr.googleVision.google_ocr(file)
        self.sql.create_health_info(data)
        return "test"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
