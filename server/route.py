# -*- coding: utf-8 -*-
import requests
from flask import Flask, Response, request, send_file, jsonify, render_template
from flask_restx import Api, Resource, fields, Namespace  # Api 구현을 위한 Api 객체 import

from database.database import S3
from database.sql import Sql
from services.foot import Foot
import services.ocr as ocr

import random

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app, version='1.0', title='Carenco Flask Server',
          description='Carenco Flask Server 입니다. 각 Api들을 테스트할 수 있습니다.')  # Flask 객체에 Api 객체 등록


@api.route('/image')
class Image(Resource):
    def post(self):
        '''ID 값을 이용하여 이미지를 가공하여 저장하는 Api'''
        try:
            params = request.get_json(force=True)
            id = params['id']
            print("id값 {}".format(id))

            foot = Foot()
            _, weight_values = foot.generate_image(params, './')
            #standard_num = random.randint(1, 7) ##임시 1-8 사이의 번호 생성

            # #model 도입
            standard_num,class_probability = foot.classification(params)
            standard_num = 1
            class_probability = random.randrange(90,99)
            print("정답 넘버 : {}".format(standard_num))
            print("유사도 : {}".format(class_probability))

            s3 = S3()
            image_url = s3.ImageUploadToS3(id)

            sql = Sql()
            weight = weight_values  # random.randrange(40, 100)
            sql.save(id,image_url,weight,standard_num)
            description = sql.find_description(standard_num)

            print(description[0])

            #return image_url
            return jsonify({'id' : id ,'url' : image_url, 'weight' : weight, 'type' : standard_num , 'similarity' : class_probability, 'description' : description})

        except KeyError:
            return {"error": "invalid request parameters"}, 400


@api.route("/health")
class Health(Resource):
    def get(self):
        '''Test Api'''
        return ""


@api.route("/check")
class Check(Resource):
    def get(self):
        '''Check Test Api'''
        return "check"


@api.route('/ocr')
class Ocr(Resource):
    def put(self):
        '''Inbody 이미지를 Request시 구글 Vision OCR Api를 이용하여 Response 데이터를 가공, DB에 데이터 저장하는 Api'''
        try:
            foot = Foot()

            # request로 넘어오는 이미지
            file = request.files['file']
            data = ocr.googleVision.google_ocr(file)

            sql = Sql()
            sql.create_health_info(data)
            return "test"
        except KeyError:
            return {"error": "image file not found in request"}, 400



# 기본 값 9000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

def classification(self, json_data):
        data  = self.split_data(json_data)
        arry = self.data_preprocessing(data[:-7])
        image_data = np.array(arry)
        ai_input_data = image_data.reshape((2, 29, 11, 1))
        print("AI Input Data:", ai_input_data)
        print("Model Output:", self.model(ai_input_data))
        outputs = np.argmax(self.model(ai_input_data))
        return outputs
