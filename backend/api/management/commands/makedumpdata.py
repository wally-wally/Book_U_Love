import html
import json
import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from api import models
from django.core.management.base import BaseCommand
from pathlib import Path
from backend import settings

# 인터파크 도서 BOOK DB 전자도서관 홈페이지의 도서 리스트를 이용하여 도서 데이터를 크롤링하는 코드
# 활용 기술 : BeautifulSoup을 이용한 크롤링 + 인터파크 도서 API를 이용해 REST 통신으로 데이터 수집
# 최종적으로 동일선상의 디렉토리 레벨에 도서 데이터, 작가 데이터, 대분류 데이터, 중분류 데이터, 소분류 데이터를 담은 json 파일이 각각 생성

# 승  '6DC249C8376B02DF365161A34E02EBC568955779AAE9AD461B4AE7AC609353EE',
# 병1 '96F9DC97C95E0C958A266736010BD4356245A1D145542E687868193C06DD4290',
# 병2 'A8D7B5A2D74E86AF74E30CBB266716E7259EDE23E41333E051C26F1F31F67310',
# 병3 '9CECAA2D79C3E3DB79FD0BFA254D16DC210F2D1EA1ECFBF5D3AFAB358FC164DA',
# 규  'D7E098C1C327E9ACFED718638C1BC436B925BDE77E7F6FF5CFE7ACD05D9B9511',

keys = [
    # '6DC249C8376B02DF365161A34E02EBC568955779AAE9AD461B4AE7AC609353EE',
    '96F9DC97C95E0C958A266736010BD4356245A1D145542E687868193C06DD4290',
    'A8D7B5A2D74E86AF74E30CBB266716E7259EDE23E41333E051C26F1F31F67310',
    '9CECAA2D79C3E3DB79FD0BFA254D16DC210F2D1EA1ECFBF5D3AFAB358FC164DA',
    'D7E098C1C327E9ACFED718638C1BC436B925BDE77E7F6FF5CFE7ACD05D9B9511'
]

# 작가 데이터 불러오기
with open('./api/fixtures/api/author.json', 'r', encoding='utf-8') as f:
    author_list = json.load(f)

author_nums = []
for author in author_list:
    author_nums.append(author.get('pk'))


# 메인카테고리 불러오기
with open('./api/fixtures/api/main_cats.json', 'r', encoding='utf-8') as f:
    main_cats_list = json.load(f)

main_cats = []
for main_cat in main_cats_list:
    main_cats.append(main_cat.get('fields').get('name'))

main_cat_id = len(main_cats) + 1


# sub 카테고리 불러오기
with open('./api/fixtures/api/sub_cats.json', 'r', encoding='utf-8') as f:
    sub_cats_list = json.load(f)

sub_cats = []
for main_cat in sub_cats_list:
    sub_cats.append(main_cat.get('fields').get('name'))

sub_cat_id = len(sub_cats) + 1


# detail 카테고리 불러오기
with open('./api/fixtures/api/detail_cats.json', 'r', encoding='utf-8') as f:
    detail_cats_list = json.load(f)

detail_cats = []
for sub_cat in detail_cats_list:
    detail_cats.append(sub_cat.get('fields').get('name'))

detail_cat_id = len(detail_cats) + 1


# author_nums, main_cats, sub_cats, detail_cats = [], [], [], [] # 새로 탐색된 항목을 구별하기 위한 리스트
# author_list, main_cats_list, sub_cats_list, detail_cats_list = [], [], [], [] # 실제로 json 파일로 만들 데이터
# main_cat_id, sub_cat_id, detail_cat_id = 1, 1, 1 # 대분류, 중분류, 소분류의 카테고리 ID를 부여하기 위한 변수

class Command(BaseCommand):
    def make_dumpdata(self):
        def get_author_data(authorID):
            print('get_author_data')
            # (1) 작가의 데이터를 담을 빈 딕셔너리 생성
            author_data = dict()
            author_html = requests.get(f'http://bookdb.co.kr/bdb/PersonDictionary.do?_method=writerDetail&prsnNo={authorID}').text
            author_soup = BeautifulSoup(author_html, 'html.parser')

            # (2) 작가 고유 ID(authorID => pk로 저장)

            # (3) 작가 이름
            name = author_soup.select('.cateCenter > .writerInfo > .wName')[0].text.strip()
            author_data['name'] = name

            # (4) 작가 사진
            img_url = author_soup.select('.cateLeft > .writerPic > img')[0].get('src')
            author_data['imgUrl'] = img_url

            # (5) 작가 생년월일
            try: 
                bone_date = author_soup.select('.cateCenter > .writerInfo > .boneDate > span.date')[0].text.split(':')[1].strip()
            except IndexError:
                bone_date = '미등록'
            author_data['boneDate'] = bone_date

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


            print('authorID', authorID)
            try:
                add_author = models.Author.objects.create(
                    pk=int(authorID),
                    name=author_data["name"],
                    imgUrl=author_data["imgUrl"],
                    boneDate=author_data["boneDate"] if author_data["boneDate"] != '미등록' else None,
                    region=author_data["region"] if author_data["region"] != '미등록' else None,
                    description=author_data["description"]
                )
            except:
                print('IntegrityError!!!')
                return


            # author_list.append(author_dumpdata) # 최종 작가 데이터 형태


        def get_more_info(bookID):
            global main_cats_list, sub_cats_list, detail_cats_list, main_cats
            res = requests.get(f'http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo={bookID}').text
            soup = BeautifulSoup(res, 'html.parser')
            outer_blocks = soup.find_all('p')
            more_list = ['', '', ''] # 책소개(description)(index=0), 목차(contents)(index=1), 출판사 서평(publisherReview)(index=2)
            for j in range(len(outer_blocks)):
                if outer_blocks[j].get_text() == '책소개':
                    more_list[0] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '').replace(u'\udb82', u'').replace(u'\udc54', u'').replace(u'\udc55', u'').replace(u'\udbc0', u'').replace(u'\udc00', u'').replace(u'\udc53', u'').replace(u'\udb80', u'').replace(u'\udeb1', u'').replace(u'\udeb2', u'').replace(u'\udeb3', u'').replace(u'\udeb4', u'').replace(u'\udeb5', u'').replace(u'\udd24', u'')
                elif outer_blocks[j].get_text() == '목차':
                    more_list[1] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '').replace(u'\udb82', u'').replace(u'\udc54', u'').replace(u'\udc55', u'').replace(u'\udbc0', u'').replace(u'\udc00', u'').replace(u'\udc53', u'').replace(u'\udb80', u'').replace(u'\udeb1', u'').replace(u'\udeb2', u'').replace(u'\udeb3', u'').replace(u'\udeb4', u'').replace(u'\udeb5', u'').replace(u'\udd24', u'')
                elif outer_blocks[j].get_text() == '출판사 서평':
                    more_list[2] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '').replace(u'\udb82', u'').replace(u'\udc54', u'').replace(u'\udc55', u'').replace(u'\udbc0', u'').replace(u'\udc00', u'').replace(u'\udc53', u'').replace(u'\udb80', u'').replace(u'\udeb1', u'').replace(u'\udeb2', u'').replace(u'\udeb3', u'').replace(u'\udeb4', u'').replace(u'\udeb5', u'').replace(u'\udd24', u'')
                if more_list[0] != '' and more_list[1] != '' and more_list[2] != '':
                    break

            # 대분류(index=0), 중분류(index=1), 소분류(index=2)
            category_set = []
            print('분류 전')
            try:
                main_category = soup.select('#locationMenu2')[0].text
            except IndexError:
                main_category = ''
            main = models.MainCategory.objects.filter(name=main_category)[0].id if models.MainCategory.objects.filter(name=main_category) else None
            category_set.append(main)
            try:
                sub_category = soup.select('#locationMenu3')[0].text
            except IndexError:
                sub_category = ''
            sub = models.SubCategory.objects.filter(name=sub_category)[0].id if models.SubCategory.objects.filter(name=sub_category) else None
            category_set.append(sub)

            try:
                detail_category = soup.select('#locationMenu4')[0].text
            except IndexError:
                detail_category = ''
            detail = models.DetailCategory.objects.filter(name=detail_category)[0].id if models.DetailCategory.objects.filter(name=detail_category) else None
            category_set.append(detail)

            print(category_set)

            # 작가 고유 ID
            author_ids = []
            try:
                author_links = soup.select('div.writerInfo > div.infoTitle > a.bt_writerDB')
                for i in range(len(author_links)):
                    if '[역]' not in soup.select('div.writerInfo > div.infoTitle > span')[i].text:
                        print(author_links[i].get('onclick').split('prsnNo=')[1].split('"')[0])
                        author_ids.append(int(author_links[i].get('onclick').split('prsnNo=')[1].split('"')[0])) # 책 상세 페이지에서 추출한 작가 고유 ID
            except IndexError:
                author_ids = []
            
            print('if len')
            if len(author_ids):
                print('if len 통과')
                for author_id in author_ids:
                    # print(author_id, author_nums)
                    if author_id not in author_nums: # 처음으로 해당 작가를 가져오는 경우 작가 데이터 저장
                        print('작가 리스트에 없음')
                        # 작가정보 author_list에 추가하는 함수
                        get_author_data(str(author_id))

                        # print('authort_nums 위', author_nums)
                        author_nums.append(author_id)
                        # print('authort_nums 아래', author_nums)
                    print('있음')

            return [more_list, category_set, author_ids]


        def get_book_data(bookID):
            # KEY = keys[(pk-1)//5000]
            params_data = {
                'key': keys[(book_pk-1)//7000], # 인터파크 도서 API KEY 입력
                'output': 'json',
                'query': bookID,
                'queryType': 'productNumber'
            }
            url = f'http://book.interpark.com/api/search.api?key={params_data["key"]}'
            response_data = requests.get(url, params = params_data).json()['item'][0]
        
            # 다수의 작가인 경우도 있기 때문에 리스트 형태로 저장
            authors = response_data['author'].split(',')
            response_data['author'] = authors
            
            # 목차 정보, description의 전체 내용과 카테고리, 작가 ID 가져오기
            more_Info = get_more_info(bookID)
            # print('more_Info', more_Info)
            response_data["description"], response_data["contents"], response_data["publisherReview"] = more_Info[0]
            response_data["mainCategory"] = more_Info[1][0]
            response_data["subCategory"] = more_Info[1][1]
            response_data["detailCategory"] = more_Info[1][2]
            response_data["authorID"] = more_Info[2]

            dumpdata_fields = dict()
            dumpdata_fields["isbn"] = response_data["isbn"] if 'isbn' in response_data else None
            dumpdata_fields["title"] = response_data["title"]
            dumpdata_fields["description"] = response_data["description"]
            dumpdata_fields["priceStandard"] = response_data["priceStandard"]
            dumpdata_fields["coverSmallUrl"] = response_data["coverSmallUrl"]
            dumpdata_fields["coverLargeUrl"] = response_data["coverLargeUrl"]
            dumpdata_fields["mainCategory"] = response_data["mainCategory"]
            dumpdata_fields["subCategory"] = response_data["subCategory"] if response_data["subCategory"] != None else None
            dumpdata_fields["detailCategory"] = response_data["detailCategory"] if response_data["detailCategory"] != None else None
            dumpdata_fields["publisher"] = response_data["publisher"]
            dumpdata_fields["translator"] = response_data["translator"]
            dumpdata_fields["pubDate"] = response_data["pubDate"]
            dumpdata_fields["contents"] = response_data["contents"]
            dumpdata_fields["publisherReview"] = response_data["publisherReview"]
            dumpdata_fields["author"] = response_data["authorID"]
            dumpdata_fields["like_user"] = []
            
            print('dump pass')
            # book_dumpdata = dict()
            # book_dumpdata["model"] = "api.book"
            # book_dumpdata["pk"] = pk
            add_book = models.Book.objects.create(
                isbn=dumpdata_fields["isbn"],
                title=dumpdata_fields["title"],
                description=dumpdata_fields["description"],
                priceStandard=dumpdata_fields["priceStandard"],
                coverSmallUrl=dumpdata_fields["coverSmallUrl"],
                coverLargeUrl=dumpdata_fields["coverLargeUrl"],
                mainCategory=models.MainCategory.objects.get(pk=dumpdata_fields["mainCategory"]) if dumpdata_fields["mainCategory"] != None else None,
                subCategory=models.SubCategory.objects.get(pk=dumpdata_fields["subCategory"]) if dumpdata_fields["subCategory"] != None else None,
                detailCategory=models.DetailCategory.objects.get(pk=dumpdata_fields["detailCategory"]) if dumpdata_fields["detailCategory"] != None else None,
                publisher=dumpdata_fields["publisher"],
                translator=dumpdata_fields["translator"],
                pubDate=dumpdata_fields["pubDate"],
                contents=dumpdata_fields["contents"],
                publisherReview=dumpdata_fields["publisherReview"],
            )
            for p in dumpdata_fields["author"]:
                print(p)
                add_book.author.add(*models.Author.objects.filter(pk=p))

            print('add_book pass')

            # return dumpdata_fields


        cat_nums = ['0101']

        # pk = 1
        book_pk = 11722
        for cat_num in cat_nums:
            crawling_book_count = {
                '0101': 3360, '0102': 840,
                '0201': 840, '0203': 840, '0202': 840, '0204': 840,
                '0301': 420, '0304': 420, '0305': 420, '0307': 420, '0302': 420,
                '0405': 210, '0401': 210, '0402': 210,
                '0505': 420, '0501': 420, '0504': 420, '0509': 420, '0503': 420
            }
            book_cnt = crawling_book_count[cat_num]
            for i in range(2311, book_cnt, 21): # 두 번째 인자가 각 카테고리별로 가져오는 책 권수인데 가져오고 싶은 책 권수의 숫자를 입력하되 반드시 21의 배수로 입력할 것!!
                html = requests.get(f'http://bookdb.co.kr/bdb/ElibMain.do?_method=initial&sc.catNo=0&sc.highCatNo={cat_num}&sc.page=1&sc.row=21&sc.sort=bestseller&sc.prdNo=&sc.query=&pageSn={i}&pageSz=21').text
                soup = BeautifulSoup(html, 'html.parser')
                books = soup.select('#eLibTab_ly1 > ul > li')
                for book in books:
                    bookID = book.select('.pic > a')[0].get('href').split('(')[1].split(', ')[0]
                    if cat_num == '0101' and bookID == '254987909': continue
                    if cat_num == '0101' and bookID == '210905960': continue
                    if cat_num == '0101' and bookID == '210905970': continue
                    if cat_num == '0307' and bookID == '298788430': continue
                    if cat_num == '0503' and bookID == '283580020': continue
                    if cat_num == '0503' and bookID == '212522331': continue
                    if cat_num == '0503' and bookID == '241623009': continue
                    if cat_num == '0503' and bookID == '295663957': continue
                    if cat_num == '0503' and bookID == '219528540': continue
                    if cat_num == '0503' and bookID == '219528486': continue
                    if cat_num == '0503' and bookID == '219528592': continue
                    if cat_num == '0503' and bookID == '219528622': continue
                    if cat_num == '0503' and bookID == '219528652': continue
                    if cat_num == '0502' and bookID == '274357955': continue
                    # book_dumpdata = dict()
                    # book_dumpdata["model"] = "api.book"
                    # book_dumpdata["pk"] = pk
                    # book_dumpdata["fields"] = get_book_data(bookID)
                    get_book_data(bookID)
                    # books_list.append(book_dumpdata)

                    print('도서 한 권 정보 추출')
                    # pk += 1
                    book_pk += 1
                print(f'-------{i}번 ~ {i + 20}번 도서 완료-------')

            print(f'*******{cat_num}번 카테고리 도서 정보 크롤링 완료*******')

            
    def _initialize(self):
        self.make_dumpdata()


    def handle(self, *args, **kwargs):
        self._initialize()