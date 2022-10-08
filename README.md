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

이슈 생성 후 이슈에 해당하는 브랜치 생성 -> 로컬에서 해당 브랜치로 작업 <br>
-> ```해당 브랜치 -> 메인 브랜치``` 로 pull request 를 날려 나머지 팀원이 변경 내용 확인 후 메인에 최종반영
  
<br>

### 커밋

- :sparkles: - 새로운 기능 개발
- :bug: - 버그 또는 오류 수정 
- :fire: - 코드 수정, 삭제
- :package: - 프로젝트 설정, 패키지 등 변경
- :heavy_plus_sign: - 기타

ex. :sparkles: 회원가입 기능 추가 <br>
ex. :bug: 로그인 실패 시 빈 페이지가 아닌 메인 페이지로 이동

&#43;

- 커밋 메세지는 한글로
- 커밋은 여러 번, 푸시는 한 번

<br>



