### Carenco-flask-server-hl API
- "/image": "PUT" 메소드 사용, 사용자 ID를 입력받아 이미지를 가공하여 DB에 저장하는 Api입니다.

- "/health": "GET" 메소드 사용, 리턴값이 없는 Api 입니다. 

- "/check": "GET" 메소드 사용, 리턴값은 "Check"를 가진 Api 입니다.

- "/test": "PUT" 메소드 사용, 리턴값은 현재 "Test" 를 가지고 있으며 request 받은 Inbody이미지를 OCR하여 인바디내용을 데이터 파싱하여 DB에 저장하는 Api입니다.
