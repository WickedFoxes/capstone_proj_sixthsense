# capstone_proj_sixsense
자동화된 웹접근성 검사를 위한 웹서비스

## 프로그램 버전
- Java 23(https://www.oracle.com/kr/java/technologies/downloads/#java23)
- Gradle 8.10.1
- Python 3.12.7(https://www.python.org/downloads/release/python-3120/)
- node.js 22.12.0(https://nodejs.org/en/download/package-manager)
- mariadb 11.4(https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.4.4&os=windows&cpu=x86_64&pkg=msi&mirror=blendbyte)
- Chrome 131.0.6778.109

## 설치 및 실행
### backend 
1. capstone_proj_sixthsense/backend/sixthsense/src/main/resources/application.properties 설정
```
# 1. mariadb port, username, password 확인
spring.datasource.url=jdbc:mariadb://localhost:3306/sixthsense?useSSL=false
#spring.datasource.url=jdbc:mysql://localhost:3306/sixthsense?useSSL=false
spring.datasource.username=root
spring.datasource.password=root

# 2. backend 이미지 저장 경로 확인
image.save.path=c:\\Users\\user\\project\\capstone_proj_sixthsense\\backend\\sixthsense\\src\\main\\resources\\static\\img\\
engine.key=CAPSTONE_PROJECT_SIXSENSE_IMAGE_KEY

# 3. 크롬확장프로그램, frontend 도메인 주소 확인
chrome_ex_path=chrome-extension://*
frontend_domain_path=http://localhost:5175
```

2. backend build
```
cd capstone_proj_sixthsense\backend\sixthsens
gradlew build
```

3. backend 실행
```
cd capstone_proj_sixthsense\backend\sixthsens\build\libs
java -jar sixthsense-0.0.1-SNAPSHOT.jar
```

### frontend
1. capstone_proj_sixthsense/frontend/src/config.js 설정
```
# 1. backend 도메인 확인
const BASE_URL = "http://localhost:8080";
```

2. 라이브러리 설치
```
cd capstone_proj_sixthsense\frontend
npm install
```

3. frontend 실행
```
npm run dev
```

### engine
1. capstone_proj_sixthsense/engine/config.py 설정
```
#1. temp 파일 다운로드 경로
DOWNLOAD_TEMP_PATH = r"c:\\Users\\user\\project\\capstone_proj_sixthsense\\engine\\temp"

#2. 크롬 드라이버 경로
# 크롬 버전에 맞는 드라이버를 사용해야 한다.
# 크롬드라이버 설치 : https://developer.chrome.com/docs/chromedriver/downloads?hl=ko
CHROM_DRIVER_PATH = r"c:\\Users\\user\\project\\capstone_proj_sixthsense\\engine\\chromedriver\\chromedriver-win64\\chromedriver.exe"

#3. backend 도메인 경로
SERVER_NAME = r"http://localhost:8080"
SERVER_KEY="CAPSTONE_PROJECT_SIXSENSE_IMAGE_KEY"
```

2. 라이브러리 설치
```
cd capstone_proj_sixthsense/engine
(venv 또는 anaconda 실행)
pip install -r requirement.txt
```

3. engine 실행
```
python run.py
```


### chrome_extention
1. capstone_proj_sixthsense/chrome_extention/background.js 설정
```
# backend 도메인설정
let DOMAIN = "http://localhost:8080"
```

2. capstone_proj_sixthsense/chrome_extention/script.js 설정
```
# backend 도메인설정
let DOMAIN = "http://localhost:8080"
```

3. 크롬브라우저로 chrome://extensions/ 접속

4. '압축해제된 확장 프로그램을 로드합니다.' 클릭 후, capstone_proj_sixthsense/chrome_extention 불러오기기
![image](https://github.com/user-attachments/assets/fa8e0386-1586-4876-a56f-0259af6929e0)
