from api import models
from django.core.management.base import BaseCommand
from pathlib import Path
from backend import settings
import requests
import json
# import html.parser as htmlparser
import html
from bs4 import BeautifulSoup

url = 'http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo='
# parser = htmlparser.HTMLParser()
class Command(BaseCommand):
    def categorybestSeller(self,categoryId=101):
        params1 = {
            'key':'6DC249C8376B02DF365161A34E02EBC568955779AAE9AD461B4AE7AC609353EE',
            'output':'json',
            # 'sort' : 'customerRating',
            'categoryId': categoryId,
            # 'start': '2', 
            # 'queryType' : 'title'
        }
        response1 = requests.get('http://book.interpark.com/api/bestSeller.api',params=params1).json()
        n = 0
        for i in response1["item"]:
            prdNo = str(i['itemId'])
            res = requests.get(url+prdNo)
            soup = BeautifulSoup(res.content, 'html.parser')
            outer_blocks = soup.find_all('p')
            i['contents'] = ''
            for j in range(len(outer_blocks)):
                if outer_blocks[j].get_text() == '책소개':
                    disc = str(outer_blocks[j+1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
                    i['description'] = disc
                elif outer_blocks[j].get_text() == '목차':
                    contents = str(outer_blocks[j+1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
                    i['contents'] = contents
            main_c = soup.select('p#locationMenu2')   
            sub_c = soup.select('#locationMenu3')
            detail_c = soup.select('#locationMenu4')
            main, sub, detail = None, None, None
            if main_c:
                main = models.MainCategory.objects.filter(name=main_c[0].text)
                if not main:
                    main = models.MainCategory.objects.create(name=main_c[0].text)
                else:
                    main = main[0]
            if sub_c:
                sub = models.SubCategory.objects.filter(name=sub_c[0].text)
                if not sub:
                    sub = models.SubCategory.objects.create(name=sub_c[0].text,main=main)
                else:
                    sub = sub[0]
            if detail_c:
                detail = models.DetailCategory.objects.filter(name=detail_c[0].text)
                if not detail:
                    detail = models.DetailCategory.objects.create(name=detail_c[0].text,sub=sub)
                else:
                    detail = detail[0]
            try:
                book = models.Book.objects.create(
                    isbn=i['isbn'], title=i['title'], author=i['author'],
                    translator = i["translator"], description=html.unescape(i['description']),
                    priceStandard=i['priceStandard'], coverSmallUrl=i['coverSmallUrl'], 
                    coverLargeUrl=i['coverLargeUrl'], publisher=i['publisher'], pubDate=i['pubDate'],
                    mainCategory = main, subCategory= sub, detailCategory= detail,
                    contents=html.unescape(i['contents']),
                    # , customerReviewRank=i['customerReviewRank'], reviewCount=i['reviewCount']
                )
                n += 1
            except KeyError as k:
                i['isbn'] = ""
                book = models.Book.objects.create(
                    isbn=i['isbn'], title=i['title'], author=i['author'],
                    translator = i["translator"], description=html.unescape(i['description']),
                    priceStandard=i['priceStandard'], coverSmallUrl=i['coverSmallUrl'], 
                    coverLargeUrl=i['coverLargeUrl'], publisher=i['publisher'], pubDate=i['pubDate'],
                    contents=html.unescape(i['contents'])
                    # , customerReviewRank=i['customerReviewRank'], reviewCount=i['reviewCount']
                )
                n += 1
                # print(categoryId ,i['title'] ,k)
        return n
    
    def searchbestSeller(self):
        url = 'http://book.interpark.com/api/search.api'
        address = f'{url}?key=96F9DC97C95E0C958A266736010BD4356245A1D145542E687868193C06DD4290'
        # search = input()
        for j in range(1, 6):
            params2 = {
                        # 'query': search,
                        'query': '가',
                        # accuracy(기본값) : 정확도순, publishTime : 출간일, title : 제목, salesPoint : 판매량
                        # customerRating : 고객평점, reviewCount : 리뷰갯수, price : 가격오름순, priceDesc : 가격내림순
                        # 'sort': sort,
                        'start': j,
                        'output': 'json',
                        'maxResults': 100,
                    }
            response2 = requests.get(address,params=params2).json()
            n = 0
            for i in response2["item"]:
                S_Url = str(i['coverSmallUrl'])
                if S_Url.find('h'):
                    end = S_Url.index('h', 10)
                else:
                    end = 57
                prdNo = S_Url[48:end]
                res = requests.get(url+prdNo)
                soup = BeautifulSoup(res.content, 'html.parser')
                outer_blocks = soup.find_all('p')
                i['contents'] = ''
                for j in range(len(outer_blocks)):
                    if outer_blocks[j].get_text() == '책소개':
                        disc = str(outer_blocks[j+1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
                        i['description'] = disc
                    elif outer_blocks[j].get_text() == '목차':
                        contents = str(outer_blocks[j+1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
                        i['contents'] = contents
                try:
                    # print('try22')
                    # print(models.Book.columns)
                    book = models.Book.objects.create(
                        isbn=i['isbn'], title=i['title'], author=i['author'],
                        translator = i["translator"], description=html.unescape(i['description']),
                        priceStandard=i['priceStandard'], coverSmallUrl=i['coverSmallUrl'], 
                        coverLargeUrl=i['coverLargeUrl'], publisher=i['publisher'], pubDate=i['pubDate'],
                        category=models.Category.objects.get(id=i['categoryId']),
                        contents=html.unescape(i['contents'])
                        # customerReviewRank=i['customerReviewRank'], reviewCount=i['reviewCount']
                    )
                    n += 1
                except KeyError as k:
                    print('error22')
                    print(i)
                    print(i['title'] ,k)
            return n


    def _initialize(self):
        self.categorybestSeller(101)
        # for i in range(101,130):
        #     if i != 121:
        #         print('*---카테고리', i , '시작 ---*')
        #         print(self.categorybestSeller(i), '개 데이터')
        #         print('*---카테고리', i , '완료 ---*')

        # for i in range(201,218):
        #     print('*---카테고리', i , '시작 ---*')
        #     print(self.categorybestSeller(i), '개 데이터')
        #     print('*---카테고리', i , '완료 ---*')


        # # sort_by = ['accuracy', 'publishTime', 'title', 'salesPoint,', 
        # # 'customerRating', 'reviewCount', 'price', 'priceDesc']
        # # for sort in sort_by:
        # print('*---카테고리' , '시작 ---*')
        # print(self.searchbestSeller(), '개 데이터')
        # print('*---카테고리' , '완료 ---*')

            


    def handle(self, *args, **kwargs):
        self._initialize()