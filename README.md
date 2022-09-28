# Backend of DevStory 

<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

- [초기 셋팅](#초기-셋팅) <br>
- [실행](#실행) <br>
- [개발 규칙](#개발-규칙)

## 초기 셋팅

### 1. 로컬 레포지토리 생성
```
git clone https://github.com/DEMODAY-devStory/backend.git
```

### 2. 가상 환경 생성 및 실행
- Windows
```
cd backend
python -m venv myvenv
source myvenv/Script/activate
pip install django
pip install -r requirements.txt
```

- Mac
```
cd backend
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install django
pip3 install -r requirements.txt
```

<br>

## 실행

### 1. 가상 환경 실행
위 초기 셋팅에서 진행했을 경우 넘어간다
- Windows
```
cd backend
source myvenv/Script/activate
```

- Mac
```
cd backend
source myvenv/bin/activate
```

### 2. 데이터베이스 업데이트
Mac은 ```python``` -> ```python3``` 로 실행

```
python manage.py makemigrations
python manage.py migrate
```

### 3. 서버 실행
```
python manage.py runserver
```

<br>

## 개발 규칙

### 브랜치

- ```main``` - 프론트와 소통하는 최종 코드로, 백엔드 내 테스트를 통과한 코드
- ```develop``` - 백엔드 내부에서 공유하는 코드로, 로컬 테스트를 통과한 코드

*정리*

로컬 환경에서 개발 및 테스트 후 ```develop``` 으로 push <br>

이후 해당 기능이 완성되었다 싶으면 ```main``` 으로 merge <br>

만약, ```main``` 에서 프론트와 연동 후 오류 발생시 로컬에서 수정 후 바로 ```main``` 에 push <br>
  -> 이후 ```main``` -> ```develop``` 으로 브랜치 업데이트
  
<br>

### 커밋

- :sparkles: - 새로운 기능 개발
- :bug: - 버그 또는 오류 수정 
- :fire: - 코드 수정, 삭제
- :package: - 프로젝트 설정, 패키지 등 변경
- :heavy_plus_sign: - 기타

ex. :sparkles: 회원가입 기능 추가 <br>
ex. :bug: 로그인 실패 시 빈 페이지가 아닌 메인 페이지로 이동

<br>



