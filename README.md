# SSAFY Bigdata project

## :information_source: Project Info

* 프로젝트 명 : Book_U_Love

* 팀 명 : 다뭉비싸(다섯명이 뭉쳐야 비로소 싸피!)

* 프로젝트 개요 

  > 읽고는 싶지만 무엇을 읽어야 할 지 모르겠다면!
  >   "이제 저희가 추천해드릴게요."
  >   빅데이터로 추천받는 맞춤 도서로
  >   코로나 피해 집콕하며 함께 교양 쌓아요 
  >   도서 추천 서비스, <Book_U_Love> 개봉 박두!

* 팀원 역할

  * 이승열
    * Merge

  * 심규현
    * Frontend 한땀한땀 장인
  * 박태수
    * Backend 정보수집가
  * 이병주
    * Backend 분석가
  * 김아현
    * Frontend 디자이너

* 기술 스택

  * BackEnd
    * Django
  * FrontEnd
    * Vue

## :gear: How to Run

**Backend**

(지금은 아직 유저 정보는 없고 책 데이터만 있는 상태 / 추후 유저 관련 dummp data 추가 예정)

```sh
cd sub2/backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py makedumpdata
python manage.py loaddata api/dummy.json
python manage.py runserver
```

**Frontend**

```sh
cd sub2/frontend
npm install
npm run serve
```
