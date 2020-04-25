import json
import os
import requests
from bs4 import BeautifulSoup

# 인터파크 도서 BOOK DB 전자도서관 홈페이지의 도서 리스트를 이용하여 도서 데이터를 크롤링하는 코드
# 활용 기술 : BeautifulSoup을 이용한 크롤링 + 인터파크 도서 API를 이용해 REST 통신으로 데이터 수집
# 최종적으로 동일선상의 디렉토리 레벨에 도서 데이터, 작가 데이터, 대분류 데이터, 중분류 데이터, 소분류 데이터를 담은 json 파일이 각각 생성

def get_author_data(authorID):
    # (1) 작가의 데이터를 담을 빈 딕셔너리 생성
    author_data = dict()
    author_html = requests.get(f'http://bookdb.co.kr/bdb/PersonDictionary.do?_method=writerDetail&prsnNo={authorID}').text
    author_soup = BeautifulSoup(author_html, 'html.parser')

    # (2) 작가 고유 ID
    author_data['author_id'] = authorID

    # (3) 작가 이름
    name = author_soup.select('.cateCenter > .writerInfo > .wName')[0].text.strip()
    author_data['name'] = name

    # (4) 작가 사진
    img_url = author_soup.select('.cateLeft > .writerPic > img')[0].get('src')
    author_data['img_url'] = img_url

    # (5) 작가 생년월일
    try: 
        bone_date = author_soup.select('.cateCenter > .writerInfo > .boneDate > span.date')[0].text.split(':')[1].strip()
    except IndexError:
        bone_date = '미등록'
    author_data['bone_date'] = bone_date

    # (6) 작가 출생지
    try:
        region = author_soup.select('.cateCenter > .writerInfo > .boneDate > span:nth-of-type(2)')[0].text.split(':')[1].strip()
    except IndexError:
        region = '미등록'
    author_data['region'] = region

    # (7) 작가 소개
    try:
        description = author_soup.select('.cateCenter > .writerInfo2 > p.content > span#txtWrapView1')[0].text.strip()
    except IndexError:
        description = author_soup.select('.cateCenter > .writerInfo2 > p.content > span#txtWrapView2')[0].text.strip()
    author_data['description'] = description.replace(u'\udb82', u'').replace(u'\udc54', u'').replace(u'\udc55', u'')

    author_list.append(author_data) # 최종 작가 데이터 형태


def get_more_info(bookID):
    global main_cat_id, sub_cat_id, detail_cat_id, main_cats_list, sub_cats_list, detail_cats_list
    res = requests.get(f'http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo={bookID}')
    soup = BeautifulSoup(res.content, 'html.parser')
    outer_blocks = soup.find_all('p')
    more_list = ['', '', ''] # 책소개(description)(index=0), 목차(contents)(index=1), 출판사 서평(publisher_review)(index=2)
    for j in range(len(outer_blocks)):
        if outer_blocks[j].get_text() == '책소개':
            more_list[0] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
        elif outer_blocks[j].get_text() == '목차':
            more_list[1] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
        elif outer_blocks[j].get_text() == '출판사 서평':
            more_list[2] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
        if more_list[0] != '' and more_list[1] != '' and more_list[2] != '':
            break

    # 대분류(index=0), 중분류(index=1), 소분류(index=2)
    category_set = []
    main_category = soup.select('p#locationMenu2')[0].text
    sub_category = soup.select('#locationMenu3')[0].text
    detail_category = soup.select('#locationMenu4')[0].text

    category_set.append(main_category)
    category_set.append(sub_category)
    category_set.append(detail_category)

    # 각 카테고리 명칭이 해당 모델에 없는 경우 데이터 추가
    if main_category not in main_cats: # 대분류
        main_cats.append(main_category)
        main_cat_dict = dict()
        main_cat_dict['id'] = main_cat_id
        main_cat_dict['name'] = main_category
        main_cats_list.append(main_cat_dict)
        main_cat_id += 1
    if sub_category not in sub_cats: # 중분류
        sub_cats.append(sub_category)
        sub_cat_dict = dict()
        sub_cat_dict['id'] = sub_cat_id
        sub_cat_dict['name'] = sub_category
        if main_category in main_cats:
            sub_cat_dict['parent'] = main_cats.index(main_category) + 1
        sub_cats_list.append(sub_cat_dict)
        sub_cat_id += 1
    if detail_category not in detail_cats: # 소분류
        detail_cats.append(detail_category)
        detail_cat_dict = dict()
        detail_cat_dict['id'] = detail_cat_id
        detail_cat_dict['name'] = detail_category
        if sub_category in sub_cats:
            detail_cat_dict['parent'] = sub_cats.index(sub_category) + 1
        detail_cats_list.append(detail_cat_dict)
        detail_cat_id += 1

    # 작가 고유 ID
    author_link = soup.select('div.writerInfo > div.infoTitle > a.bt_writerDB')[0].get('onclick')
    author_id = author_link.split('prsnNo=')[1].split('"')[0] # 책 상세 페이지에서 추출한 작가 고유 ID
    if author_id not in author_nums: # 처음으로 해당 작가를 가져오는 경우 작가 데이터 저장
        get_author_data(author_id)
        author_nums.append(author_id)

    return [more_list, category_set, author_id]


def get_book_data(bookID):
    params_data = {
        'key': '', # 인터파크 도서 API KEY 입력
        'output': 'json',
        'query': bookID,
        'queryType': 'productNumber'
    }
    url = f'http://book.interpark.com/api/search.api?key={params_data["key"]}'
    response_data = requests.get(url, params = params_data).json()['item'][0]

    # 목차 정보, description의 전체 내용과 카테고리, 작가 ID 가져오기
    more_Info = get_more_info(bookID)
    response_data["description"], response_data["contents"], response_data["publisher_review"] = more_Info[0]
    response_data["category_set"] = more_Info[1]
    response_data["author_id"] = more_Info[2]

    return response_data


author_nums, main_cats, sub_cats, detail_cats = [], [], [], [] # 새로 탐색된 항목을 구별하기 위한 리스트
author_list, main_cats_list, sub_cats_list, detail_cats_list = [], [], [], [] # 실제로 json 파일로 만들 데이터
main_cat_id, sub_cat_id, detail_cat_id = 1, 1, 1 # 대분류, 중분류, 소분류의 카테고리 ID를 부여하기 위한 변수

# cat_nums은 추후 아래 리스트로 교체
# cat_nums = ['0101', '0102', '0103', '0201', '0202', '0203', '0204', '0301', '0302', '0303', '0304', '0305', '0306', '0307', '0401', '0402', '0403', '0404', '0405', '0501', '0502', '0503', '0504', '0505', '0506', '0507', '0508', '0509']
# 또는 cat_nums에 숫자를 임의로 지정하여(ex. ['0101', '0102']) 각 카테고리별로 가져오는 책 권수를 다르게 할 수도 있음
cat_nums = ['0101']
for cat_num in cat_nums:
    books_list = []
    for i in range(1, 120, 21): # 120 부분이 각 카테고리별로 가져오는 책 권수인데 가져오고 싶은 책 권수의 숫자를 입력하되 반드시 21의 배수로 입력할 것!!
        html = requests.get(f'http://bookdb.co.kr/bdb/ElibMain.do?_method=initial&sc.catNo=0&sc.highCatNo={cat_num}&sc.page=1&sc.row=21&sc.sort=bestseller&sc.prdNo=&sc.query=&pageSn={i}&pageSz=21').text
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.select('#eLibTab_ly1 > ul > li')
        for book in books:
            bookID = book.select('.pic > a')[0].get('href').split('(')[1].split(', ')[0]
            books_list.append(get_book_data(bookID))
            print('도서 한 권 정보 추출')
        print(f'-------{i}번 ~ {i + 20}번 도서 완료-------')

    with open (f'./book_data_sample.json', 'w', encoding='UTF-8') as f: # 책 데이터
        f.write(json.dumps(books_list, indent=2, ensure_ascii=False))

    with open (f'./author_data_sample.json', 'w', encoding='UTF-8') as f: # 작가 데이터
        f.write(json.dumps(author_list, indent=2, ensure_ascii=False))

    with open (f'./main_cats_data_sample.json', 'w', encoding='UTF-8') as f: # 대분류 카테고리 데이터
        f.write(json.dumps(main_cats_list, indent=2, ensure_ascii=False))

    with open (f'./sub_cats_data_sample.json', 'w', encoding='UTF-8') as f: # 중분류 카테고리 데이터
        f.write(json.dumps(sub_cats_list, indent=2, ensure_ascii=False))

    with open (f'./detail_cats_data_sample.json', 'w', encoding='UTF-8') as f: #소분류 카테고리 데이터
        f.write(json.dumps(detail_cats_list, indent=2, ensure_ascii=False))
    
    print(f'*******{cat_num}번 카테고리 도서 정보 크롤링 완료*******')