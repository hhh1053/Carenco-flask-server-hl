import json
import numpy as np
import cv2

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
    return splitted_data

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

  def generate_weight(self, preprocessed_data):
    weight_values = preprocessed_data[1154:1156]

    weight_list = []
    integer_value = 0
    for data_element in weight_values:
      value = int(data_element[0].upper(), 16) * 16 + int(data_element[1].upper(), 16)
      weight_list.append(value)
    integer_value = weight_list[0] / self.weight_coefficient
    # print(weight_values)
    return integer_value

  def generate_image(self, input_path, output_path):
    splitted_data = self.split_data(input_path)
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

    final_output_path = output_path + 'foot_image.jpg'
    # print('create : ', final_output_path)
    image_data = cv2.imwrite(final_output_path, dst)
    return dst, weight_values


if __name__ == '__main__':
    foot = Foot()
    test_data = foot.load_json('./sample_data.json')
    # print(test_data)
    foot.generate_image(test_data, './')