# :books: Book_U_Love

<br>

<img src="https://user-images.githubusercontent.com/52685250/80765397-e5c09d80-8b7d-11ea-8193-7b61baa0345e.png" width="400">

<br>

## :one: Overview

> <i>읽고는 싶지만 무엇을 읽어야 할 지 모르겠다면!</i>
>
> <i>"이제 저희가 추천해드릴게요."</i>
>
> <i>빅데이터로 추천받는 맞춤 도서로 코로나 피해 집콕하며 함께 교양 쌓아요</i>
>
> <i>도서 추천 서비스, <Book_U_Love> 개봉 박두!</i>

- BOOK_U_LOVE는(은) 유저 데이터를 기반으로 하여 협업필터링(Collaborative Filtering)을 이용해 유저별 맞춤 도서를 추천해주는 서비스입니다.
- 선호 성향이 비슷한 사용자들을 같은 그룹화, 동일 그룹 선호 상품 추천하는 방식입니다.
- 프로젝트 기간 : 20.03.23 ~ 20.05.01

<br>

## :two: Tech Stack

:round_pushpin: <b>Frontend</b> : `Vue.js`

:round_pushpin: <b>Backend</b> : `Django`

:round_pushpin: <b>Database</b> : `MySQL` 

:round_pushpin: <b>Development Enviornment</b> : Python 3.7.4,  Django 2.2.7, Node.js higher than 10.16x, Vue CLI higher than 4.2.x

:round_pushpin: <b>Using Editor</b> : Visual Studio Code

<br>

## :three: Quick Start

### :pushpin: Local에서 실행

:heavy_check_mark: <b>Backend Installation & Run</b>

```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata api/dummy.json
python manage.py runserver
```

:heavy_check_mark: <b>Frontend Installation & Run</b>

```
cd frontend
npm instlal
npm run serve
```

<br>

### :pushpin: 배포 환경에서 실행

- http://i02b205.p.ssafy.io/ 주소를 접속해서 볼 수 있습니다.

<br>

## :four: ERD Diagram

![Image Pasted at 2020-5-1 07-37](https://user-images.githubusercontent.com/52685250/80773944-6f7c6500-8b96-11ea-9deb-a76182b692fc.png)

<br>

## :five: Homepage Configuration

### (1) 메인 화면

- 비로그인 상태

![01](https://user-images.githubusercontent.com/52685250/80760993-ba858080-8b74-11ea-87bc-60480082eeb5.JPG)

- 로그인 상태
  - 관심 카테고리를 설정하고 작성한 리뷰 데이터를 기반으로 도서를 추천받은 경우입니다.

![02](https://user-images.githubusercontent.com/52685250/80760997-bbb6ad80-8b74-11ea-8e61-22cda658ee31.JPG)

<br>

### (2) 도서 상세 페이지

![03](https://user-images.githubusercontent.com/52685250/80760999-bbb6ad80-8b74-11ea-87ab-89db2fc2c890.JPG)

<br>

### (3) 작가 소개 페이지

![04](https://user-images.githubusercontent.com/52685250/80761001-bc4f4400-8b74-11ea-88bb-6dce4a531fdf.JPG)

<br>

### (4) MY PAGE > 계정관리

![05](https://user-images.githubusercontent.com/52685250/80761003-bce7da80-8b74-11ea-823d-c0492f9095b9.JPG)

<br>

### (5) MY PAGE > MY BOOKS

- 도서 상세 페이지에서 읽고 싶은 책에 `찜하기` 버튼을 클릭해서 `내가 읽고 싶은 책` 리스트를 볼 수 있습니다.
- 그리고 각 도서에 리뷰를 작성하면 리뷰를 작성한 도서들을 볼 수 있습니다.

### ![06](https://user-images.githubusercontent.com/52685250/80761004-bce7da80-8b74-11ea-93ff-bef29ff9524f.JPG)