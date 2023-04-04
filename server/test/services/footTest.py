import json

import cv2
import os
import numpy as np

import server.services.foot as FootClass

# 테스트용 JSON 파일
current_directory = os.path.dirname(os.path.abspath(__file__))
sample_data = os.path.join(current_directory, '..', '..', 'resources', 'json', 'sample_data.json')


class TestFoot:

    def test_initialize_foot_instance(self):
        foot = FootClass.Foot()
        assert foot is not None

    def test_load_json(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        assert test_data is not None

    def test_split_data(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        splitted_data = foot.split_data(test_data)
        assert len(splitted_data) == 1180

    def test_data_preprocessing(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        splitted_data = foot.split_data(test_data)
        preprocessed_data = foot.data_preprocessing(splitted_data[20:])
        assert preprocessed_data.shape == (24, 48)

    def test_merged_data(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        splitted_data = foot.split_data(test_data)
        preprocessed_data = foot.data_preprocessing(splitted_data[20:])
        merged_data = foot.merged_data(preprocessed_data)
        assert merged_data.shape == (24, 24)

    def test_generate_weight(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        splitted_data = foot.split_data(test_data)
        weight_values = foot.generate_weight(splitted_data)
        assert isinstance(weight_values, float)

    def test_generate_image(self):
        foot = FootClass.Foot()
        test_data = foot.load_json(sample_data)
        dst, weight_values = foot.generate_image(test_data, './')
        assert dst.shape == (512, 512, 3)

        # Clean up the generated image
        os.remove('./foot_image.jpg')

    if __name__ == "__main__":
        test_initialize_foot_instance()
        test_load_json()
        test_split_data()
        test_data_preprocessing()
        test_merged_data()
        test_generate_weight()
        test_generate_image()
