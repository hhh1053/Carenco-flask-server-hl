## Carenco-flask-server-hl API
### Foot Class Method 설명

**load_json(data)**<br>
- 입력: data (str) - 입력 데이터가 포함된 JSON 파일의 경로<br>
- 출력: self.data (json) - JSON 파일에서 읽은 입력 데이터가 포함된 json<br>
- 설명: JSON 파일에서 입력 데이터를 읽어들이고 클래스 인스턴스의 data 속성에 저장합니다.

**split_data(json_data)**<br>
- 입력: json_data (json) - 입력 데이터가 포함된 사전<br>
- 출력: splitted_data (list), id (문자열) - 데이터 요소의 목록과 입력 데이터의 ID<br>
- 설명: 입력 데이터를 개별 데이터 요소로 분할하고 일부 데이터 정리 및 서식 지정을 수행하여 데이터 요소의 목록과 입력 데이터의 ID를 반환합니다.

**data_preprocessing(data)**<br>
- 입력: data (list) - 데이터 요소의 목록<br>
- 출력: preprocessed (ndarray) - 처리된 입력 데이터의 NumPy 배열<br>
- 설명: 16진수 값을 10진수로 변환하고 데이터를 NumPy 배열로 변환하여 입력 데이터를 처리하고 결과 배열을 반환합니다.

**merged_data(data)**<br>
- 입력: data (ndarray) - 처리된 입력 데이터의 NumPy 배열<br>
- 출력: data_transformed (ndarray) - 변환된 입력 데이터의 NumPy 배열<br>
- 설명: 인접 열의 쌍 값들을 합산하여 입력 데이터를 변환하고 결과 배열을 반환합니다.

**remove_blank(data)**<br>
- 입력: data (ndarray) - 변환된 입력 데이터의 NumPy 배열<br>
- 출력: data (ndarray) - 공백 열이 제거된 변환된 입력 데이터의 NumPy 배열<br>
- 설명: 입력 데이터 배열에서 공백 열을 제거하고 결과 배열을 반환합니다.

**generate_weight(lst)**<br>
- 입력: lst (list) - 데이터 요소의 목록<br>
- 출력: weight (data) - 계산된 체중 값<br>
- 설명: 입력 데이터의 일부를 기반으로 체중 값을 계산하고 결과를 반환합니다.

**generate_image(input_path, output_path)**<br>
- 입력: input_path (str) - 입력 데이터 파일의 경로, output_path (문자열) - 출력 이미지 파일이 저장될 디렉토리의 경로<br>
- 출력: dst (ndarray), weight_values (실수) - 생성된 이미지의 NumPy 배열 및 체중 값<br>
- 설명: 입력 데이터를 기반으로 발 이미지를 생성하고 이미지를 저장합니다.

**generate_ocrdata_googleVision(image_path)**<br>
- 입력: image_path (str) - 입력 이미지 파일의 경로<br>
- 출력: output (json) - 체중, 근골격량 및 체지방량과 같은 추출된 숫자 값이 포함된 json<br>
- 설명: Google Vision API를 사용하여 이미지에서 숫자 값을 추출합니다.<br>

---
### Flask 서버 설명
- **Flask 서버**는 Foot 클래스, S3 클래스 및 Sql 클래스를 사용하여 작성되었습니다. API는 4 개의 엔드 포인트를 가지며 다음과 같습니다.

- "/image": 입력받은 이미지에 대해 Foot 클래스 generate_image()를 사용하여 발 이미지를 생성하고 S3 클래스를 사용하여 이미지를 S3 버킷에 업로드 한 다음 Sql 클래스를 사용하여 발 이미지 및 체중 값을 데이터베이스에 저장합니다. 이 API는 POST 방식으로 작동합니다.<br>

- "/health": 이 API는 건강 검사를 수행하도록 구성된 무응답 엔드 포인트입니다. GET 방식으로 작동합니다.<br>

- "/check": 이 API는 Flask 서버가 작동하는지 확인하기 위해 구성된 무응답 엔드 포인트입니다. GET 방식으로 작동합니다.<br>

- "/test": 입력받은 이미지에 대해 Foot 클래스 generate_ocrdata_googleVision()를 사용하여 Ocr을 통한 이미지에서 데이터를 파싱하여 데이터베이스에 정보를 저장하도록 구성된 테스트 API입니다. GET 방식으로 작동합니다.<br>
