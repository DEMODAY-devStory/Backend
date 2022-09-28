# Backend of DevStory 

<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

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
