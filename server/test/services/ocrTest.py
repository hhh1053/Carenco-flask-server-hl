import os
import pytest
import server.services.ocr as ocr

# 테스트용 이미지
current_directory = os.path.dirname(os.path.abspath(__file__))
test_image_path = os.path.join(current_directory, '..', '..', 'resources', 'image', '8.png')

class TestOcr:

    def test_initialize_vision_client(self):
        gv = ocr.googleVision()
        client = gv.initialize_vision_client()
        assert client is not None

    def test_load_image(self):
        gv = ocr.googleVision()
        image = gv.load_image(test_image_path)
        assert image is not None

    def test_preprocess_image(self):
        gv = ocr.googleVision()
        image = gv.load_image(test_image_path)
        preprocessed_image = gv.preprocess_image(image)
        assert preprocessed_image is not None

    def test_get_vision_response(self):
        gv = ocr.googleVision()
        client = gv.initialize_vision_client()
        image = gv.load_image(test_image_path)
        preprocessed_image = gv.preprocess_image(image)
        response = gv.get_vision_response(client, preprocessed_image)
        assert response is not None

    def test_extract_text_from_response(self):
        gv = ocr.googleVision()
        client = gv.initialize_vision_client()
        image = gv.load_image(test_image_path)
        preprocessed_image = gv.preprocess_image(image)
        response = gv.get_vision_response(client, preprocessed_image)
        text = gv.extract_text_from_response(response)
        assert text is not None

    def test_calculate_body_type(self):
        gv = ocr.googleVision()
        body_type = gv.calculate_body_type(24, 37.3)
        assert body_type == "통통"

    def test_Inbody_Data_Extraction1(self):
        gv = ocr.googleVision()
        client = gv.initialize_vision_client()
        image = gv.load_image(test_image_path)
        preprocessed_image = gv.preprocess_image(image)
        response = gv.get_vision_response(client, preprocessed_image)
        output = gv.Inbody_Data_Extraction1(response)
        assert output is not None

    def test_Inbody_Data_Extraction2(self):
        gv = ocr.googleVision()
        client = gv.initialize_vision_client()
        image = gv.load_image(test_image_path)
        preprocessed_image = gv.preprocess_image(image)
        response = gv.get_vision_response(client, preprocessed_image)
        img_width = image.shape[1]
        img_height = image.shape[0]
        output = gv.Inbody_Data_Extraction2(response, img_width, img_height)
        assert output is not None

    def test_google_ocr(self):
        gv = ocr.googleVision()
        output = gv.google_ocr(test_image_path)
        assert output is not None
