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
    self.weight_coefficient = 3.7

  def load_json(self, data):
    with open(data, 'r') as j:
      json_data = json.loads(j.read())
    self.data = json_data # json_data['data']
    return self.data

  def split_data(self, json_data):
    data = json_data['data']
    data = data.upper()
    data = data.replace(u'\xa0', u'')
    splitted_data = [''.join(x) for x in zip(*[list(data[z::2]) for z in range(2)])]
    return splitted_data, json_data['id']

  def data_preprocessing(self, data):
    preprocessed = []
    sub_data = []
    for data_element in data:
        value = int(data_element[0].upper(), 16) * 16 + int(data_element[1].upper(), 16)
        sub_data.append(value)
        if len(sub_data) == 48:
            preprocessed.append(sub_data)
            sub_data = []
    return np.array(preprocessed)
  
  def merged_data(self, data):
    data_transformed = np.zeros((24, 24))
    for row_idx in range(24):
      for col_idx in range(0, 48, 2):
        data_transformed[row_idx][col_idx//2] = data[row_idx][col_idx] + data[row_idx][col_idx+1]

    return data_transformed

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
        if sum(data[:, col_idx]) < 105: 
            is_data = True
      if is_data:
          data = np.delete(data, col_idx, 1)
      col_idx += 1
    return data

  def generate_weight(self, lst):
    weight_values = lst[-6:-4]

    weight_list = []
    weight = -1
    for data_element in weight_values:
      value = int(data_element[0].upper(), 16) * 16 + int(data_element[1].upper(), 16)
      weight_list.append(value)
    weight = (weight_list[0] + weight_list[1]) / 7.2
    return weight

  def generate_image(self, input_path, output_path):
    splitted_data, id = self.split_data(input_path)
    weight_values =  self.generate_weight(splitted_data)
    lst = (self.data_preprocessing(splitted_data[20:]))
    # lst = self.remove_blank(lst)
    lst = self.merged_data(lst)
    image_data = np.array(lst)
    sample = image_data.astype(np.uint8)
    
    # sample = np.interp(sample, (sample.min(), sample.max()), (0, 255))

    # Normalize matrix values between 0 and 255
    heatmap = cv2.normalize(sample, None, 0, 256, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # heatmap = cv2.GaussianBlur(heatmap, (15, 15), 0)
    heatmap = cv2.resize(heatmap, (512, 512))
    
    # Apply a colormap to the normalized matrix
    dst = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    heatmap = cv2.GaussianBlur(heatmap, (21, 21), 0)
    # resized_sample = cv2.resize(sample, (512, 512), interpolation=cv2.INTER_CUBIC)
    # dst = cv2.applyColorMap(resized_sample, 16)

    final_output_path = output_path + 'foot_image_{}.jpg'.format(str(id))
    # print('create : ', final_output_path)
    image_data = cv2.imwrite(final_output_path, dst)
    return dst, weight_values

class S3:
  def ImageUploadToS3(self, id):
    s3_obj=self.s3_connection()

    new_name=str(uuid.uuid4())+'.jpg'
    print(new_name)

    self.s3_put_object(s3_obj,new_name, id)

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
       
  def s3_put_object(self,s3_obj,new_name, id):
      s3_obj.upload_file('./foot_image_{}.jpg'.format(id),BUCKET_NAME,new_name,ExtraArgs={'ContentType':'image/jpg'})
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
  _, weight_values = foot.generate_image(params, './')

  s3 = S3()
  image_url=s3.ImageUploadToS3(id)

  sql = Sql()
  weight = weight_values # random.randrange(40, 100)
  sql.save(id,image_url,weight)

 

  return image_url

@app.route("/health",methods=['GET'])
def health():
  return ""

@app.route("/check",methods=['GET'])
def check():
  return "check"
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
