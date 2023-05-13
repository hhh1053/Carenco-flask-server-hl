import io
import os
import json
import re
from typing import Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFont, ImageDraw, Image
# 구글 클라우드 패키지 설치( pip install google-cloud-vision(requirements.txt 에 추가예정) )
from google.cloud import vision

# 구글 api 사용을 위한 key
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =


class googleVision:

    def initialize_vision_client(self):
        return vision.ImageAnnotatorClient()

    def load_image(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        return cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_UNCHANGED)

    def preprocess_image(self, image):
        # Sharpen the image
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        img_sharpened = cv2.filter2D(image, -1, kernel)

        return img_sharpened

    def get_vision_response(self, client, image):
        height, width = image.shape
        print(f"가로(폭): {width} 픽셀")
        print(f"세로(높이): {height} 픽셀")
        vision_image = vision.Image(content=cv2.imencode('.jpg', image)[1].tobytes())
        return client.text_detection(image=vision_image)

    def draw_text_on_image(self, response, image):
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("AppleSDGothicNeoR.ttf", 15)

        for annotation in response.text_annotations:
            vertices = annotation.bounding_poly.vertices
            draw.rectangle([(vertices[0].x, vertices[0].y), (vertices[2].x, vertices[2].y)], outline=(255, 0, 0),
                           width=2)
            draw.text((vertices[0].x, vertices[0].y - 25), annotation.description, font=font, fill=(0, 0, 255))

        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def extract_text_from_response(self, response):
        text = ""
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            text += symbol.text
                        text += " "
                    text += "\n"
                text += "\n"
        return text

    def text_extraction(self, response, x1, y1, x2, y2):
        value_found = False
        for annotation in response.text_annotations:
            vertices = annotation.bounding_poly.vertices
            if vertices[0].x >= x1 and vertices[0].y >= y1 and \
                    vertices[2].x <= x2 and vertices[2].y <= y2:
                value = annotation.description.replace('\n', '')
                if not value_found:
                    if re.match(r'^\d*\.\d+$', value):
                        value_found = True
                        return value
                else:
                    if re.match(r'^\d*\.\d+$', value):
                        return value
        return 'Empty Value'

    def calculate_body_type(self, bmi: Optional[float], body_fat_percentage: Optional[float]) -> Optional[str]:
            def invalid_measurement() -> str:
                return "잘못된 값이 측정되었습니다."

            def not_measured() -> str:
                return "측정되지 않았습니다"

            try:
                bmi = float(bmi)
                body_fat_percentage = float(body_fat_percentage)
            except (TypeError, ValueError):
                return invalid_measurement()

            if not all([bmi, body_fat_percentage]):
                return not_measured()
            elif bmi <= 0 or body_fat_percentage <= 0:
                return invalid_measurement()

            body_type_conditions = [
                (bmi <= 18.5 and body_fat_percentage <= 18, "마름"),
                (bmi <= 18.5 and body_fat_percentage <= 28, "약간 마름"),
                (bmi <= 21.75 and body_fat_percentage > 28, "마른 비만"),
                (bmi <= 21.75 and body_fat_percentage <= 18, "근육형 날씬"),
                (bmi <= 21.75 and body_fat_percentage <= 23, "날씬"),
                (bmi <= 25 and body_fat_percentage <= 28, "적정"),
                (bmi <= 25 and body_fat_percentage <= 23, "근육형"),
                (bmi <= 25 and body_fat_percentage > 28, "통통"),
                (bmi > 25 and body_fat_percentage <= 23, "운동선수"),
                (bmi > 25 and body_fat_percentage <= 28, "통통"),
                (bmi > 25 and body_fat_percentage > 28, "비만"),
            ]

            for condition, body_type in body_type_conditions:
                if condition:
                    return body_type

            return invalid_measurement()

    def Inbody_Data_Extraction1(self, response):
        # 몸무게 데이터
        weight = self.text_extraction(response, 203, 533, 735, 570)
        # 근골격량 데이터
        skeletal_muscle_mass = self.text_extraction(response, 203, 570, 735, 615)
        # 체지방량 데이터
        body_fat_mass = self.text_extraction(response, 203, 623, 735, 660)

        return {
            "weight": weight,
            "skeletal_muscle_mass": skeletal_muscle_mass,
            "body_fat_mass": body_fat_mass
        }

    def Inbody_Data_Extraction2(self, response, img_width, img_height):
        # Body Composition Analysis
        body_water = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.17276350877192982,
                                     img_width * 0.25225897849462366, img_height * 0.20076726342710998)
        protein = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.20076726342710998,
                                  img_width * 0.25225897849462366, img_height * 0.22894736842105262)
        minerals = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.22894736842105262,
                                   img_width * 0.25225897849462366, img_height * 0.2556390977443609)
        body_fat = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.2556390977443609,
                                   img_width * 0.25225897849462366, img_height * 0.28382080200501254)

        # Skeletal Muscle and Fat Analysis
        weight = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.3453646616541353,
                                 img_width * 0.6121171826625387, img_height * 0.3725563909774436)
        skeletal_muscle_mass = self.text_extraction(response, img_width * 0.1627486437613011,
                                               img_height * 0.3725563909774436,
                                               img_width * 0.6121171826625387, img_height * 0.3997481203007519)
        body_fat_mass = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.3997481203007519,
                                        img_width * 0.6121171826625387, img_height * 0.42693984962406015)

        # Obesity Analysis
        BMI = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.4887218045112782,
                              img_width * 0.6121171826625387, img_height * 0.5159135338345865)
        body_fat_percentage = self.text_extraction(response, img_width * 0.1627486437613011, img_height * 0.5159135338345865,
                                              img_width * 0.6121171826625387, img_height * 0.5431052631578947)

        # Regional Muscle Analysis
        top_left = self.text_extraction(response, img_width * 0.04520936834634448, img_height * 0.5953953158260421,
                                   img_width * 0.04520936834634448, img_height * 0.6971871121019124)
        bottom_left = self.text_extraction(response, img_width * 0.16998191681735985, img_height * 0.6084367245657568,
                                      img_width * 0.16998191681735985, img_height * 0.7030732860520095)
        top_right = self.text_extraction(response, img_width * 0.1879766569075931, img_height * 0.5953953158260421,
                                    img_width * 0.18797665690759316, img_height * 0.6971871121019124)
        bottom_right = self.text_extraction(response, img_width * 0.22603504273504273, img_height * 0.7208646616541353,
                                       img_width * 0.29652406417112296, img_height * 0.762218045112782)
        center = self.text_extraction(response, img_width * 0.14484848484848484, img_height * 0.6597744360902256,
                                 img_width * 0.22603504273504273, img_height * 0.7092731829573935)

        # Regional Body Fat Analysis
        fat_top_left = self.text_extraction(response, img_width * 0.048824593128390596, img_height * 0.60843672456575689,
                                       img_width * 0.44300254452926207, img_height * 0.6597744360902256)
        fat_bottom_left = self.text_extraction(response, img_width * 0.3706981317215976, img_height * 0.7208646616541353,
                                          img_width * 0.44300254452926207, img_height * 0.762218045112782)
        fat_top_right = self.text_extraction(response, img_width * 0.5238726790450929, img_height * 0.618421052631579,
                                        img_width * 0.5961770918527577, img_height * 0.6597744360902256)
        fat_bottom_right = self.text_extraction(response, img_width * 0.5238726790450929, img_height * 0.7208646616541353,
                                           img_width * 0.5961770918527577, img_height * 0.762218045112782)
        fat_center = self.text_extraction(response, img_width * 0.443036754507628, img_height * 0.6603658536585366,
                                     img_width * 0.5246143205858428, img_height * 0.7089442896935933)

        return {
            "body_water": body_water,
            "protein": protein,
            "minerals": minerals,
            "body_fat": body_fat,
            "weight": weight,
            "skeletal_muscle_mass": skeletal_muscle_mass,
            "body_fat_mass": body_fat_mass,
            "BMI": BMI,
            "body_fat_percentage": body_fat_percentage,
            "top_left": top_left,
            "bottom_left": bottom_left,
            "top_right": top_right,
            "bottom_right": bottom_right,
            "center": center,
            "fat_top_left": fat_top_left,
            "fat_bottom_left": fat_bottom_left,
            "fat_top_right": fat_top_right,
            "fat_bottom_right": fat_bottom_right,
            "fat_center": fat_center
        }

    def google_ocr(self, image_path):
        client = self.initialize_vision_client()
        image = self.load_image(image_path)
        preprocessed_image = self.preprocess_image(image)
        img_width = image.shape[1]
        img_height = image.shape[0]
        response = self.get_vision_response(client, preprocessed_image)
        # print(response.text_annotations)
        response_text = self.extract_text_from_response(response)

        pattern_270 = re.compile(r'Inbody\s*270', re.IGNORECASE)
        pattern_370s = re.compile(r'Inbody\s*370s', re.IGNORECASE)

        # 인바디
        if pattern_270.search(response_text):
            output = self.Inbody_Data_Extraction1(response)
        elif pattern_370s.search(response_text):
            output = self.Inbody_Data_Extraction2(response, img_width, img_height)
        else:
            raise ValueError("응답 데이터에서 270s 또는 370s를 찾을 수 없습니다.")

        body_type = self.calculate_body_type(output['BMI'], output['body_fat_percentage'])
        output['body_type'] = body_type
        # # 이미지에 읽어들인 ocr읉 통해 읽어들인 데이터 입히는 함수
        # img_resized_with_text = draw_text_on_image(response, image)
        # # 어노테이션 이미지를 저장합니다.
        # cv2.imwrite('result.jpg', img_resized_with_text)

        # print('- Output -----------------')
        # print(json.dumps(output))

        return output


#  테스트용 코드
# def test():
#     ocr = googleVision()
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     image_path = os.path.join(current_directory, '..', 'resources', 'image', '8.png')
#
#     # image_path = 'resources/8.png'
#     output = ocr.google_ocr(image_path)
#     print("Results:")
#     print(json.dumps(output, ensure_ascii=False, indent=2))
#
#     # # Google Cloud Vision API를 사용해 얻은 텍스트 주석이 그려진 이미지를 불러옵니다.
#     # image_with_text = cv2.imread('result.jpg')
#     #
#     # # 이미지 출력합니다.
#     # cv2.imshow('Image with Text Annotations', image_with_text)
#     #
#     # # 키보드 입력을 대기합니다.
#     # cv2.waitKey(0)
#     #
#     # # 모든 OpenCV 창을 닫습니다.
#     # cv2.destroyAllWindows()
#
#
# test()