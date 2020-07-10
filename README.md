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

:round_pushpin: <b>Database</b> : `sqlite3` 

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

## :four: ERD Diagram

![Image Pasted at 2020-5-1 07-37](https://user-images.githubusercontent.com/52685250/80773944-6f7c6500-8b96-11ea-9deb-a76182b692fc.png)

<br>

## :five: Homepage Configuration

### (1) 메인 화면 & 리뷰 데이터 수집기

- 유저별 작성한 리뷰 데이터를 기반으로 도서를 추천받은 경우입니다.

![01](https://user-images.githubusercontent.com/52685250/81378207-dc1cd400-9141-11ea-8d69-dfe0a2379fa3.JPG)

- 도서 데이터 뿐만 아니라 도서 추천 관련 Youtube 영상들을 보실 수 있습니다.

![02](https://user-images.githubusercontent.com/52685250/81378209-dd4e0100-9141-11ea-9a1e-1c5e8018e32b.JPG)

- 작성된 도서 리뷰를 가지고 추천을 하기 때문에 처음 로그인하거나 작성한 리뷰 개수가 적은 유저의 경우 리뷰 데이터 수집을 위한 메인 페이지에서 리뷰 데이터 수집 페이지로 이동해서 리뷰를 작성할 수 있습니다.

![12](https://user-images.githubusercontent.com/52685250/81378498-5ea59380-9142-11ea-9128-bf2635e677b9.JPG)

<br>

### (2) 도서 상세 페이지

- 도서의 상세 정보와 해당 도서를 읽은 유저들의 리뷰를 볼 수 있습니다.
- 해당 도서에 관심이 있으면 `책 추가하기` 버튼을 눌러 내가 찜한 책 리스트에 추가할 수 있습니다.
- 리뷰 작성할 때 스포일러가 포함된 경우 `스포일러 있음`을 설정 후 저장하면 '스포일러가 있는 리뷰입니다' 텍스트로 대체되서 나오고 그럼에도 불구하고 보고 싶은 경우 `그래도 볼래요!` 버튼을 누르면 해당 리뷰가 보여지게 됩니다.

![14](https://user-images.githubusercontent.com/52685250/81379117-821d0e00-9143-11ea-8bc2-c875e4ea46fa.JPG)

- 또한 하단에는 해당 도서의 같은 카테고리에 있는 도서들 중 평점이 높거나 리뷰 개수가 많은 도서들을 추천해줍니다.

![15](https://user-images.githubusercontent.com/52685250/81379121-834e3b00-9143-11ea-8956-6a5008538781.JPG)

<br>

### (3) 작가 소개 페이지

- 각 도서의 작가 이름을 클릭하면 해당 작가의 상세 정보 페이지로 이동할 수 있습니다.
- 기본적인 생년월일, 출생지는 물론 작가의 출간도서 목록을 볼 수 있습니다.

![04](https://user-images.githubusercontent.com/52685250/80761001-bc4f4400-8b74-11ea-88bb-6dce4a531fdf.JPG)

<br>

### (4) 카테고리별 도서 리스트

- 데스크탑 화면에서 보는 경우 상단 메뉴에서 `ALL CATEGORY` 탭에서 카테고리를 선택하면 해당 카테고리의 도서들을 볼 수 있습니다.
- 우측 상단에서 평점 또는 리뷰 개수 순으로 정렬해서 볼 수도 있습니다.

![06](https://user-images.githubusercontent.com/52685250/81379461-1f784200-9144-11ea-8705-17c35e8768d9.JPG)

<br>

### (5) 검색 페이지

- 우측 상단의 검색창에 키워드를 검색하면 제목에 해당 키워드를 포함하는 도서 목록들을 볼 수 있습니다.

![07](https://user-images.githubusercontent.com/52685250/81378219-df17c480-9141-11ea-9930-0ff881cd3828.JPG)

<br>

### (6) TMI Center

- Book_U_Love에 저장된 도서 목록과 리뷰 데이터를 기반으로 다양한 정보를 볼 수 있는 TMI Center를 구성했습니다.

- 최근 1주일 간 상위 리뷰 데이터
  - 이번주 리뷰가 가장 많이 작성된 도서 목록 TOP 10을 볼 수 있습니다.

![16](https://user-images.githubusercontent.com/52685250/81379803-b7762b80-9144-11ea-95d4-3be257707d30.JPG)

- 동년배 책 분석
  - 같은 연령대와 성별을 가진 유저들이 작성된 리뷰가 많은 도서 목록을 리뷰 개수 순으로 볼 수 있습니다.

![17](https://user-images.githubusercontent.com/52685250/81379909-e7bdca00-9144-11ea-89cf-0e019669047f.JPG)

- 동년배 취향 분석
  - 같은 연령대와 성별을 가진 유저들이 작성한 리뷰 개수 순위를 도서 카테고리별로 정렬하여 차트로 볼 수 있게 구성했습니다.

![18](https://user-images.githubusercontent.com/52685250/81379902-e2f91600-9144-11ea-8092-2b3130b1c8d4.JPG)



- 카테고리별 전체 리뷰 분포
  - 대분류, 중분류, 소분류 카테고리 별로 작성된 도서 리뷰 개수 분포를 차트로 볼 수 있게 구성했습니다.

![19](https://user-images.githubusercontent.com/52685250/81379904-e391ac80-9144-11ea-97ff-6d751485ce49.JPG)

<br>

### (7) MY PAGE

- 유저의 선호 카테고리 분석 차트
  - 로그인한 유저의 작성된 리뷰 개수 분포를 카테고리별로 볼 수 있게 구성했습니다.

![20](https://user-images.githubusercontent.com/52685250/81379975-09b74c80-9145-11ea-9690-6c59b373ecb3.JPG)

- 회원님을 위한 맞춤 추천 도서 리스트
  - 도서 상세 페이지에서 `책 추가하기` 버튼을 클릭해서 저장한 찜한 도서 리스트를 볼 수 있습니다.

![21](https://user-images.githubusercontent.com/52685250/81379979-0a4fe300-9145-11ea-9dae-6874ea3ee1ec.JPG)

- 내가 작성한 리뷰 리스트
  - 내가 작성한 리뷰 평점, 내용을 볼 수 있습니다.

![22](https://user-images.githubusercontent.com/52685250/81379980-0ae87980-9145-11ea-953e-8412ee335176.JPG)

-  계정관리
   -  유저의 성별, 나이, 관심 카테고리를 설정할 수 있습니다.
   -  비밀번호 변경, 회월탈퇴 기능을 구현했습니다.

![23](https://user-images.githubusercontent.com/52685250/81379982-0ae87980-9145-11ea-9163-e38ad69d49f2.JPG)