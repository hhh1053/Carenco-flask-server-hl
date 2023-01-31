# -*- coding: utf-8 -*- 
import json
import cv2
import numpy as np
import uuid
import boto3
import pymysql
from flask import Flask, Response, request, send_file, jsonify, render_template
from requests_toolbelt import MultipartEncoder
import random

REGION='ap-northeast-2'
ACCESS_KEY_ID='AKIAQTAIP2INMKL7LST6'
ACCESS_SECRET_KEY='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'
BUCKET_NAME='carenco-image-server2'
LOCATION ='ap-northeast-2'


class Foot:
  def __init__(self):
    self.data = None
    self.image_data = None

  def load_json(self, data):
    with open(data) as f:
      json_data = json.load(f)
    self.data = json_data['data']
    return self.data

  def split_data(self, json_data):
    data = json_data['data']
    data = data.replace(u'\xa0', u'')
    split_data = [''.join(x) for x in zip(*[list(data[z::2]) for z in range(2)])]
    return split_data

  def data_preprocessing(self, data):
    preprocessed = []
    sub_data = []

    for data_element in data:
      value = int(data_element[0].upper(), 16) * 16 + int(data_element[1].upper(), 16)
      sub_data.append(value)
      if len(sub_data) == 48:
          preprocessed.append(sub_data)
          sub_data = []
    preprocessed = np.array(preprocessed[:1152])
    return preprocessed

  def remove_blank(self, data):
    data = np.array(data)
    data = np.delete(data, 0, 1)
    
    start_data_col = -1
    
    for col_idx in range(24):
      for row_idx in range(24):
        if data[row_idx][col_idx] > 0 and start_data_col == -1:
          start_data_col = col_idx
          break

    col_idx = start_data_col
    while col_idx < data.shape[1]:
      is_data = False
      for row_idx in range(24):
        if data[row_idx][col_idx] == 0:
          is_data = True

      if is_data:
          data = np.delete(data, col_idx, 1)
      col_idx += 1

    return data

  def generate_image(self, input_path, output_path):
    splitted_data = self.split_data(input_path)
    lst = (self.data_preprocessing(splitted_data))
    
    lst = self.remove_blank(lst)
    image_data = np.array(lst)
    sample = image_data.astype(np.uint8)
    
    resized_sample = cv2.resize(sample, (512, 512), interpolation=cv2.INTER_CUBIC)
    dst = cv2.applyColorMap(resized_sample, 16)

    final_output_path = output_path + 'foot_image.jpg'
    print('create : ', final_output_path)
    image_data = cv2.imwrite(final_output_path, dst)
    return dst


class S3:
  def ImageUploadToS3(self):
    s3_obj=self.s3_connection()

    new_name=str(uuid.uuid4())+'.jpg'
    print(new_name)

    self.s3_put_object(s3_obj,new_name)

    image_url=self.s3_get_image_url(new_name)
    return image_url

  def s3_connection(self):
      try:
          s3_obj = boto3.client(
              service_name='s3',
              region_name=REGION,
              aws_access_key_id=ACCESS_KEY_ID,
              aws_secret_access_key=ACCESS_SECRET_KEY
             
          )
      except Exception as e:
          print(e)
      else:
          print("s3 bucket connected!")
          return s3_obj
       
  def s3_put_object(self,s3_obj,new_name):
      s3_obj.upload_file('./foot_image.jpg',BUCKET_NAME,new_name,ExtraArgs={'ContentType':'image/jpg'})
      return True

  def s3_get_image_url(self,filename):
    image_url = f'https://{BUCKET_NAME}.s3.{LOCATION}.amazonaws.com/{filename}'
    return image_url

class Sql():

  def save(self,id,img_url,weight):
    conn = pymysql.connect(host='database-1.c5pmtrhecz2d.ap-northeast-1.rds.amazonaws.com', user='admin', db='carenco', password='zpdjdpszh', charset='utf8') 
    cursor = conn.cursor() 
    sql = "UPDATE carenco.foot_print SET image = %s,weight = %s WHERE id = %s" 
    cursor.execute(sql,(img_url,weight,id)) 
    conn.commit()

    # sql = "SELECT * FROM carenco.foot_print WHERE id=%s"
    # cursor.execute(sql,(id))
    # result=cursor.fetchall()
    # print(result)

    conn.close()  

  

app = Flask(__name__)

@app.route('/image', methods=['GET', 'POST'])
def classification():
  params = request.get_json(force=True)
  id = params['id']

  foot = Foot()
  foot.generate_image(params, './')

  s3 = S3()
  image_url=s3.ImageUploadToS3()

  sql = Sql()
  weight = random.randrange(40, 100)
  sql.save(id,image_url,weight)

 

  return image_url


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)