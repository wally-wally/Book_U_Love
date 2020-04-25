import re
import nltk
import json
import os
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from nltk.corpus import stopwords
from pprint import pprint
from api import models
from django.core.management.base import BaseCommand
from pathlib import Path
from backend import settings


# 텍스트 전처리하는데 필요한 정규표현식
alpha = re.compile('[a-zA-Z]')
no_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

# 불용어(관사, 조사 등)
stop_words = set(stopwords.words('english'))  # 영어 불용어
with open('./korean_stop_words.json', encoding='UTF-8') as f:
    korean_stop_words = json.load(f) # 한글 불용어

class Command(BaseCommand):
    def get_keyword_distribution(self, sentence):
        # 괄호, 따옴표, 반점, 온점, 물음표, 느낌표는 미리 제거하고 시작
        brace_set = ["(", ")", "[", "]", "{", "}", "“", "”", "‘", "’", "'", '"', ",", ".", ":", "?", "!"]
        for brace in brace_set:
            sentence = sentence.replace(brace, ' ')
        text = re.sub('<[^>]*>', '', sentence) # 텍스트 전처리를 하기 위해 html 태그 제거(DB에 저장된 description 내용은 변화 없음)


        # 딕셔너리에 해당 단어의 개수 기록
        def insert_dict(word):
            if word in words:
                word_count_dict[word] += 1
            else:
                word_count_dict[word] = 1

        okt = Okt()
        words = [] # 딕셔너리에 value를 결정할 때 사용됨
        word_count_dict = dict()
        for word in text.split():
            if alpha.match(word) == None: # 한글 단어인 경우
                extract_word = okt.pos(word, join=True) # 단어와 품사를 함께 표시 ex)'음식/Noun'
                for ext_word in extract_word:
                    w, posi = ext_word.split('/')[0], ext_word.split('/')[1]
                    try:
                        # 명사이면서 한글 불용어에 포함되지 않은 단어만 포함
                        if not w.isdecimal() and posi == 'Noun' and w not in korean_stop_words:
                            insert_dict(w)
                    except IndexError: # 에러 방지
                        pass
            else: # 영어가 혼합된 경우
                if no_hangul.match(word.lower()).group() not in stop_words:
                    insert_dict(no_hangul.match(word.lower()).group())
                    words.append(no_hangul.match(word.lower()).group())

        # 단어 개수 분포
        sorted_words = []
        for word_data in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True):
            sorted_words.append([word_data[0], word_data[1]])

        return sorted_words


    def get_more_info(self, bookID):
        res = requests.get(f'http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo={bookID}')
        soup = BeautifulSoup(res.content, 'html.parser')
        outer_blocks = soup.find_all('p')
        more_list = ['', '']
        for j in range(len(outer_blocks)):
            if outer_blocks[j].get_text() == '책소개':
                more_list[0] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
            elif outer_blocks[j].get_text() == '목차':
                more_list[1] = str(outer_blocks[j + 1]).replace('  ', '').replace('<p>', '').replace('</p>', '')
            if more_list[0] != '' and more_list[1] != '':
                break
        return more_list


    def get_book_data(self, bookID):
        params_data = {
            'key': 'D7E098C1C327E9ACFED718638C1BC436B925BDE77E7F6FF5CFE7ACD05D9B9511',
            'output': 'json',
            'query': bookID,
            'queryType': 'productNumber'
        }
        url = f'http://book.interpark.com/api/search.api?key={params_data["key"]}'
        response_data = requests.get(url, params = params_data).json()['item'][0]

        # 목차 정보, description 전체 내용 가져오기
        response_data["description"], response_data["contents"] = self.get_more_info(bookID)
        # return response_data
        
        # description에서 단어 개수 분포 추출
        if response_data["description"] == '': # description이 없는 경우 contents(목차) 정보로 단어 개수 분포 추출
            response_data["keywordDistribution"] = self.get_keyword_distribution(response_data["contents"])
        else: # description이 있는 경우
            response_data["keywordDistribution"] = self.get_keyword_distribution(response_data["description"])
        return response_data


    def _initialize(self):
        nltk.download('stopwords') # 텍스트 전처리를 위해 컴퓨터에 nltk 라이브러리의 stopwords(불용어) 데이터가 없는 경우 다운로드를 먼저 해야 함
        cat_nums = ['0101']
        for cat_num in cat_nums:
            html = requests.get(f'http://bookdb.co.kr/bdb/ElibMain.do?_method=initial&sc.catNo=0&sc.highCatNo={cat_num}&sc.page=1&sc.row=21&sc.sort=bestseller&sc.prdNo=&sc.query=&pageSn=1&pageSz=21').text
            soup = BeautifulSoup(html, 'html.parser')
            total_book_cnt = int(soup.select('#contWrap > div.contList > div.contSort > div.sorTxt > p > span:nth-of-type(2)')[0].text[:-1].replace(',', ''))
            print(f'{total_book_cnt}권 중 21권의 도서 데이터를 가져옵니다.')

            books_list = []
            for i in range(1, 21, 21):
                html = requests.get(f'http://bookdb.co.kr/bdb/ElibMain.do?_method=initial&sc.catNo=0&sc.highCatNo={cat_num}&sc.page=1&sc.row=21&sc.sort=bestseller&sc.prdNo=&sc.query=&pageSn={i}&pageSz=21').text
                soup = BeautifulSoup(html, 'html.parser')
                books = soup.select('#eLibTab_ly1 > ul > li')
                for book in books:
                    bookID = book.select('.pic > a')[0].get('href').split('(')[1].split(', ')[0]
                    books_list.append(self.get_book_data(bookID))
                    print('도서 한 권 정보 추출')
                print(f'-------{i}번 ~ {i + 20}번 도서 완료-------')

            with open (f'./book_list_{cat_num}.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(books_list, indent=2, ensure_ascii=False))
            
            print(f'*******{cat_num}번 카테고리 도서 정보 크롤링 완료*******')


    def handle(self, *args, **kwargs):
        self._initialize()