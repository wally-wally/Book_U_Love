# :books: Book_U_Love

<br>

<img src="https://user-images.githubusercontent.com/52685250/81321616-c79ef400-90cd-11ea-82f3-ef974586108e.png" width="550">

<br>

## :one: Overview

> <i>읽고는 싶지만 무엇을 읽어야 할 지 모르겠다면!</i>
>
> <i>"이제 저희가 추천해드릴게요."</i>
>
> <i>빅데이터로 추천받는 맞춤 도서로 코로나 피해 집콕하며 함께 교양 쌓아요</i>
>
> <i>도서 추천 서비스, <Book_U_Love> 개봉 박두!</i>

- BOOK_U_LOVE 서비스는 유저 데이터를 기반으로 하여 협업필터링(Collaborative Filtering)을 이용해 유저별 맞춤 도서를 추천해주는 서비스입니다.
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

- 우선 <a href="https://drive.google.com/open?id=1S_GsP1OsRENIWrGbzujkkJo1Ro0M4KzD" target="_blank">(여기)</a> 를 클릭해서 `dummy.json` 파일을 다운로드 받으신 후 `backend` > `api` > `fixtures` > `api` 위치에 저장해주세요.

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

### (1) 메인 화면 & 리뷰 데이터 수집기

- 유저별 작성한 리뷰 데이터를 기반으로 도서를 추천받은 경우입니다.

![01](https://user-images.githubusercontent.com/52685250/81378207-dc1cd400-9141-11ea-8d69-dfe0a2379fa3.JPG)

- 도서 데이터 뿐만 아니라 도서 추천 관련 Youtube 영상들을 보실 수 있습니다.

![02](https://user-images.githubusercontent.com/52685250/81378209-dd4e0100-9141-11ea-9a1e-1c5e8018e32b.JPG)

- 처음 로그인하거나 작성한 리뷰 개수가 적은 유저의 경우 메인 페이지에서 리뷰 데이터 수집 페이지로 이동할 수 있습니다.

![12](https://user-images.githubusercontent.com/52685250/81378498-5ea59380-9142-11ea-9128-bf2635e677b9.JPG)

<br>

### (2) 도서 상세 페이지

- 도서의 상세 정보와 해당 도서를 읽은 유저들의 리뷰를 볼 수 있습니다.
- 리뷰 작성할 때 스포일러가 포함된 경우 `스포일러 있음`을 설정 후 저장하면 다른 회원들이 

![14](https://user-images.githubusercontent.com/52685250/81379117-821d0e00-9143-11ea-8bc2-c875e4ea46fa.JPG)

- 또한 하단에는 해당 도서의 같은 카테고리에 있는 도서들 중 평점, 리뷰 개수 순으로 높은 도서들을 추천해줍니다.

![15](https://user-images.githubusercontent.com/52685250/81379121-834e3b00-9143-11ea-8956-6a5008538781.JPG)

<br>

### (3) 작가 소개 페이지

![04](https://user-images.githubusercontent.com/52685250/80761001-bc4f4400-8b74-11ea-88bb-6dce4a531fdf.JPG)

<br>

### (4) 카테고리별 도서 리스트

![06](https://user-images.githubusercontent.com/52685250/81379461-1f784200-9144-11ea-8705-17c35e8768d9.JPG)

<br>

### (5) 검색 페이지

![07](https://user-images.githubusercontent.com/52685250/81378219-df17c480-9141-11ea-9930-0ff881cd3828.JPG)

<br>

### (6) TMI Center

- 최근 1주일 간 상위 리뷰 데이터

![16](https://user-images.githubusercontent.com/52685250/81379803-b7762b80-9144-11ea-95d4-3be257707d30.JPG)

- 동년배 책 분석

![17](https://user-images.githubusercontent.com/52685250/81379909-e7bdca00-9144-11ea-89cf-0e019669047f.JPG)

- 동년배 취향 분석

![18](https://user-images.githubusercontent.com/52685250/81379902-e2f91600-9144-11ea-8092-2b3130b1c8d4.JPG)



- 카테고리별 전체 리뷰 분포

![19](https://user-images.githubusercontent.com/52685250/81379904-e391ac80-9144-11ea-97ff-6d751485ce49.JPG)

<br>

### (7) MY PAGE

- 유저의 선호 카테고리 분석 차트

![20](https://user-images.githubusercontent.com/52685250/81379975-09b74c80-9145-11ea-9690-6c59b373ecb3.JPG)

- 회원님을 위한 맞춤 추천 도서 리스트

![21](https://user-images.githubusercontent.com/52685250/81379979-0a4fe300-9145-11ea-9dae-6874ea3ee1ec.JPG)

- 내가 작성한 리뷰 리스트

![22](https://user-images.githubusercontent.com/52685250/81379980-0ae87980-9145-11ea-953e-8412ee335176.JPG)

-  계정관리

![23](https://user-images.githubusercontent.com/52685250/81379982-0ae87980-9145-11ea-9163-e38ad69d49f2.JPG)