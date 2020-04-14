# 📔 [특화-Sub PJT Ⅰ] README

> ### 목표
>
> 데이터셋 분석 및 시각화

<br>

## :one: Tech Stack

- OS : `Windows 10`
- Language / Framework : `Python`(기본 과제 + 심화 과제), `Vue.js`(심화 과제)
- Main Library : `Pandas`, `Matplotlib`, `Chart.js` etc

- Used Editor : `Visual Studio Code`

<br>

## :two: Quick Start

:heavy_check_mark: <b>Requirement</b>

- `Python` : 3.6.8 or 3.7.x (<b><u>but, strongly recommend 3.6.8</u></b>)
- `Node.js` : 10.16.3 (심화 과제2를 로컬에서 구동할 경우 필요)
- `Vue CLI` : 4.2.3 (심화 과제2를 로컬에서 구동할 경우 필요)

:heavy_check_mark: <b>Installation - Sub 1 (기본 과제)</b>

```bash
cd sub1
pip install -r requirements.txt
python parse.py # req1-1
python analyze.py # req2-1 ~ req2-4
python visualize.py # req3-1 ~ req3-5
```

:heavy_check_mark: <b>Installation - Sub 1 (심화 과제1)</b>

```bash
cd sub1
cd advanced01
python parse.py
python analyze.py
python visualize.py # 심화 과제1
```

:heavy_check_mark: <b>Installation - Sub 1 (심화 과제2)</b>

```bash
cd sub1
cd advanced02
cd frontend
npm install
npm run serve # 심화 과제2
```

`심화 과제2`의 경우 로컬 서버 실행 후 터미널에서 `http://localhost:8080` 부분을 `Ctrl` + 마우스 왼쪽 클릭했을 때 아래와 같은 브라우저 화면이 열리면 성공

<img src="https://user-images.githubusercontent.com/52685250/77613239-89aa9e00-6f6d-11ea-9ded-fc72f1071bfc.JPG" width="900">

- 혹은 `심화 과제2`는 firebase로 배포된 홈페이지 주소로 접속해서도 볼 수 있다. <a href="https://ssafy-bigdata-pjt01.firebaseapp.com/" target="_blank">(바로 이동)</a>

<br>

## :three: Daily Essay

- 하루동안 진행했던 프로젝트 개발일지를 작성한 markdown 파일이다.

| <center>Date</center>        | <center>Go to Essay</center>                                 |
| ---------------------------- | ------------------------------------------------------------ |
| <center>03/23(Mon.)</center> | <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/daily_essay/0323.md" target="_blank">:page_facing_up: (Go)</a> |
| <center>03/24(Tue.)</center> | <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/daily_essay/0324.md" target="_blank">:page_facing_up: (Go)</a> |
| <center>03/25(Wed.)</center> | <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/daily_essay/0325.md" target="_blank">:page_facing_up: (Go)</a> |
| <center>03/26(Thu.)</center> | <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/daily_essay/0326.md" target="_blank">:page_facing_up: (Go)</a> |
| <center>03/27(Fri.)</center> | <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/daily_essay/0327.md" target="_blank">:page_facing_up: (Go)</a> |

<br>

## :four: Project Task Outputs(Screenshot)

---

:warning: <b>[참고!] 코드에 대한 자세한 설명을 확인하려면 :three: Daily Eassy를 참고!</b>

---

### :pushpin: 기본 과제

### 1. 데이터 전처리 <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/sub1/parse.py" target="_blank">(코드 보기)</a>

<img src="https://user-images.githubusercontent.com/52685250/77294740-1ebc5580-6d28-11ea-8228-fb72ddc46f12.JPG" width="1200">

<img src="https://user-images.githubusercontent.com/52685250/77294743-1fed8280-6d28-11ea-93aa-29f81884f64a.JPG" width="1200">

<br>

### 2. 데이터 분석 <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/sub1/analyze.py" target="_blank">(코드 보기)</a>

#### (1) 음식점 평점 순 출력 + (2) 최소 리뷰 개수 필터링

<img src="https://user-images.githubusercontent.com/52685250/77410313-0c145000-6dfe-11ea-8fae-376d6f407cbf.JPG" width="700">

<br>

#### (3) 리뷰 개수 기준 음식점 정렬

<img src="https://user-images.githubusercontent.com/52685250/77410628-8349e400-6dfe-11ea-897d-5c18354f1c5e.JPG" width="700">

<br>

#### (4) 리뷰 개수 기준 유저 정렬

<img src="https://user-images.githubusercontent.com/52685250/77411697-264f2d80-6e00-11ea-9510-cb5832312939.JPG" width="400">

<br>

### 3. 데이터 시각화 <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/sub1/visualize.py" target="_blank">(코드 보기)</a>

#### (1) 음식점 리뷰 수 분포 - `막대 그래프`

<img src="https://user-images.githubusercontent.com/52685250/77611164-f327ae00-6f67-11ea-8426-a691481fd5c9.png" width="1100">

<br>

#### (2) 평균 평점 분포 - `파이 차트`

<img src="https://user-images.githubusercontent.com/52685250/77416370-1e46bc00-6e07-11ea-838a-6de64180fea2.JPG" width="800">

<br>

#### (3) 유저 리뷰 수 분포 - `히스토그램`

<img src="https://user-images.githubusercontent.com/52685250/77418240-f73db980-6e09-11ea-988a-fe30afc6e281.JPG" width="1100">

<br>

#### (4) 유저 나이대, 성별 분포 - `이중 막대 그래프`

- 1년 단위로 끊어서 데이터 분석 후 그래프로 표현

  <img src="https://user-images.githubusercontent.com/52685250/77419764-48e74380-6e0c-11ea-9aa5-94c7af3638a8.JPG" width="1100">

- 10년 단위로 끊어서 데이터 분석 후 그래프로 표현

  <img src="https://user-images.githubusercontent.com/52685250/77606089-f451de80-6f59-11ea-9557-7b5a36fb7c89.png" width="1100">

<br>

#### (5) 음식점 위치 분포 - `지도`

:heavy_check_mark: <b>repository를 clone 받은 후 `sub1` 폴더 > `project_outpus` 폴더 로 이동 후 `req3-5.html` 파일을 실행하면 볼 수 있습니다.</b>

- 선정 주제 : <b><u>리뷰 개수가 5개 이상 등록된 대전광역시의 음식점</u></b>

- 선정 이유 : 지도에 표현하는 것을 실습하기 위해 간단하게 리뷰 개수를 가지고 필터링했고 SSAFY 대전캠퍼스에서 공부하고 있기 때문에 하루 일과를 마친 후 맛집 탐방을 하는데 도움이 되고자 이 주제를 선정했다.

- 처음 열었을 때 화면

  <img src="https://user-images.githubusercontent.com/52685250/77530639-05a4d780-6ed5-11ea-9d62-018217a6f637.JPG" width="1100">

- 9개의 마커가 모인 클러스터를 클릭했을 때 지도 화면

  <img src="https://user-images.githubusercontent.com/52685250/77530643-063d6e00-6ed5-11ea-840a-902934cbd169.JPG" width="1100">

- 원하는 음식점 마커를 클릭했을 때 나오는 상세정보

  <img src="https://user-images.githubusercontent.com/52685250/77530646-063d6e00-6ed5-11ea-9752-6d8e97e4bacb.JPG" width="320">

- `네이버 검색 결과로 바로 이동`을 클릭했을 때 새 탭으로 나오는 화면

  <img src="https://user-images.githubusercontent.com/52685250/77530647-06d60480-6ed5-11ea-824d-b07e15b057d4.JPG" width="1100">

<br>

### :pushpin: 심화 과제

### 1. 데이터 분석 심화 <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/sub1/advanced01/visualize.py" target="_blank">(코드 보기)</a>

:heavy_check_mark: <b>repository를 clone 받은 후 `sub1` 폴더 > `project_outpus` 폴더 로 이동 후 `adv1.html` 파일을 실행하면 볼 수 있습니다.</b>

- 선정 주제 : <b><u>서울 초밥 음식점들 중 리뷰가 3.5점 이상인 음식점들의 위치를 지도에 표시하기</u></b>(단, 리뷰는 5개 이상 작성되는 음식점들만 해당)

- 선정 이유 : 최근 코로나 사태로 자유롭게 돌아다니지 못하고 있는데 코로나 사태가 진정되고 서울로 놀러갈 수 있는 날이 오면 서울 초밥 맛집을 꼭 가고야 말겠다는 다짐으로 이러한 주제를 선정했다.

- 처음 열었을 때 초기화면

  <img src="https://user-images.githubusercontent.com/52685250/77532460-3f2b1200-6ed8-11ea-9fb8-aa4060c0f195.JPG" width="1100">

- 7로 표시된 클러스터 부분을 클릭했을 때 화면

  <img src="https://user-images.githubusercontent.com/52685250/77532462-3fc3a880-6ed8-11ea-9ed1-99a9145b0863.JPG" width="1100">

- 각 마커를 클릭했을 때 나오는 음식점의 상세정보

  <img src="https://user-images.githubusercontent.com/52685250/77532465-3fc3a880-6ed8-11ea-8541-9947a5fd10c1.JPG" width="350">

<br>

### 2. 데이터 시각화 심화 <a href="https://lab.ssafy.com/s02-bigdata-sub1/s02p21b222/blob/master/sub1/advanced02/" target="_blank">(코드 보기)</a>

- Vue.js를 이용해 Chart.js 라이브러리를 사용해보는 실습과정을 진행했다.
- 앞의 과정과 동일하게 데이터 전처리, 분석 과정을 거친 후 <b>원하는 데이터를 선별하여 json 파일로 만든 후(`backend` 폴더)</b> <b>Vue.js 에서 새로 가공한 json 파일을 읽어 그래프의 데이터로 활용했다.(`frontend` 폴더)</b>

#### (1) 리뷰 개수가 20개 이상 작성된 음식점 중 BEST6 - `막대 그래프`

<img src="https://user-images.githubusercontent.com/52685250/77713913-12cbde80-701b-11ea-8b0a-e8238d6298d8.JPG" width="1100">

- `전체 데이터 보기`를 선택하는 경우 리뷰 개수가 20개 이상 작성된 음식점 중 평균 평점이 3.5점 이상인 음식점들의 데이터가 보임
- 4.5점 이상은 빨간색, 4.0점 이상 4.5점 미만은 초록색, 4.0점 미만은 파란색으로 평점에 색깔 구분

<img src="https://user-images.githubusercontent.com/52685250/77713916-13fd0b80-701b-11ea-96f7-939bd62df040.JPG" width="1100">

<br>

#### (2) SSAFY 캠퍼스가 있는 지역(서울, 대전, 광주, 구미)별 평균 평점 3.5점 이상인 음식점 비율 분포 - `도넛 차트`

- 백분율 수치가 높을수록 그 도시에 맛집이 많다는 의미를 내포하고 있다.

<img src="https://user-images.githubusercontent.com/52685250/77605564-9cff3e80-6f58-11ea-933a-d47606e79999.JPG" width="1100">

<br>

#### (3) 전체 음식점의 평균 평점 분포 - `파이 차트`

- req.3-2 에서 matplotlib 라이브러리를 통해 구현한 내용은 chart.js를 이용해서 구현했다.

<img src="https://user-images.githubusercontent.com/52685250/77709512-a77c0f80-700e-11ea-9df7-fd570cb8f353.JPG" width="1000">

<br>

## :five: Review

- 이번 빅데이터 프로젝트를 하면서 데이터를 전처리, 분석하고 시각화하는 과정을 진행했다.
  - 예전에 Numpy 라이브러리는 사용해본 경험이 있는데 Pandas 라이브러리는 이번에 처음 사용해보았다. 그래서 중간중간에 사용법을 잘 몰라서 모듈 사용법 등을 찾는데 시간이 많이 걸렸다.
  - 하지만 이번 프로젝트를 진행하면서 Pandas가 Numpy에 비해 데이터들을 내가 원하는대로 더 쉽고 유동적으로 가공할 수 있고 분석할 수 있어서 결과적으로는 더 좋았던 것 같다.
  - 처음에는 Pandas 사용법을 잘 몰라서 하드코딩 레벨로 코드를 구성했는데 과제를 하면 할수록 Pandas에서 제공하는 모듈들의 사용법을 더 익히니까 코드의 길이도 간결해지고 Pandas 답게 코드를 작성할 수 있었다.
  - 추후 팀 프로젝트를 진행하면서 데이터 분석을 할 일이 생긴다면 Sub_PJT - 1에서 익혔던 내용들을 바탕으로 잘 구현할 수 있을 것 같다.
- 또한 빅데이터 첫 번째 Sub Project를 진행하면서 평소에 관심이 있던 차트 라이브러리를 활용해서 그래프 그리는 과제를 할 수 있어서 좋았다.
  - 예전에 간단한 토이 프로젝트로 분석한 데이터를 vue-echarts 라이브러리로 구현한 적이 있었는데 이 라이브러리를 이용해서 구현한 사람들도 많이 없고 공식 문서에 나와 있는 내용도 충분하지 않아서 구현하는데 많이 어려웠다.
  - 또한 원하는대로 사이즈 조정도 잘 되지 않아서 다른 차트 라이브러리로 바꿔야 겠다고 생각하고 못 바꾸고 있었는데 이번 프로젝트를 통해서 다양한 라이브러리를 사용할 수 있었다.
  - 하지만 이번에 대중적으로 유명한 Chart.js 라이브러리를 활용해서 구현하니까 사용한 사람들도 많아서 나와 비슷한 고민을 가진 사람들의 해결 방법을 찾으면서 쉽게 해결할 수 있었다.
  - 뿐만 아니라 Python의 matplotlib 라이브러리도 함께 사용해보았는데 둘 다 좋은 차트 라이브러리이지만 Chart.js가 matplotlib에 비해 유동적으로 원하는 형태로 표현할 수 있고 반응형 웹에서도 올바르게 작동할 수 있어서 장점이 더 많은 것 같다.
  - 추후 팀 프로젝트를 진행하면서 더 좋은 차트 라이브러리가 있다면 그 라이브러리도 사용해보고 사용자가 보기에 좋은 인사이트를 얻을 수 있는 차트를 만들어봐야겠다.