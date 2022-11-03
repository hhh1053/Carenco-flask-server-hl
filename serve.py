# -*- coding: utf-8 -*- 
import json
import cv2
import numpy as np
from flask import Flask, Response, request, send_file, jsonify, render_template

from requests_toolbelt import MultipartEncoder

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

# Initialize the flask application
app = Flask(__name__)

@app.route('/image', methods=['GET', 'POST'])
def classification():
  params = request.get_json(force=True)
  foot = Foot()
  foot.generate_image(params, './')

  m = MultipartEncoder(fields={'files' : ('./foot_image.jpg', open('./foot_image.jpg', 'rb'),
                              'image.jpg')})
  
  return Response(m.to_string(), mimetype=m.content_type)
if __name__ == "__main__":
  app.run(host='localhost', port=5000)