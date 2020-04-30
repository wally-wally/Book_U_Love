import re
import nltk
import json
from konlpy.tag import Okt
from nltk.corpus import stopwords
from pprint import pprint
from django.core.management.base import BaseCommand
from pathlib import Path
from backend import settings
from api import models

# 텍스트 전처리 과정을 거쳐서 단어의 개수 분포를 frontend 단에서 바로 사용할 수 있도록 list 형태로 출력
class Command(BaseCommand):

    def get_words(self, sentence):
        # 괄호, 따옴표, 반점, 온점, 물음표, 느낌표는 미리 제거하고 시작
        brace_set = ["(", ")", "[", "]", "{", "}", "“", "”", "‘", "’", "'", '"', ",", ".", ":"]
        for brace in brace_set:
            sentence = sentence.replace(brace, ' ')
        text = re.sub('<[^>]*>', '', sentence) # 텍스트 전처리를 하기 위해 html 태그 제거(DB에 저장된 description 내용은 변화 없음)

        # 텍스트 전처리하는데 필요한 정규표현식
        alpha = re.compile('[a-zA-Z]')
        no_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

        # 불용어(관사, 조사 등)
        stop_words = set(stopwords.words('english'))  # 영어 불용어
        with open('./korean_stop_words.json', encoding='UTF-8') as f:
            korean_stop_words = json.load(f) # 한글 불용어

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

        # (1) 단어 리스트들
        sorted_words = [] # 이 값을 frontend 단으로 전송
        for word_data in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True):
            sorted_words.append([word_data[0], word_data[1]])

        # (2) 가장 많이 쓰인 상위 2개 단어 => 핵심 키워드로 사용
        keywords = [sorted_words[0][0], sorted_words[1][0]]
        return sorted_words, keywords


    def _initialize(self):
        nltk.download('stopwords') # 본인 컴퓨터에 nltk 라이브러리의 stopwords(불용어) 데이터가 없는 경우 다운로드를 먼저 해야 함
        # [Test] pk가 1 ~ 10번 도서의 description을 가지고 단어의 개수 분포와 핵심 키워드 추출
        for i in range(1, 11):
            book_description = models.Book.objects.get(pk=i).description
            word_data = self.get_words(book_description)
            print(f'-------{i}번째 도서의 단어 개수 분포-------')
            pprint(word_data[0])
            print(f'{i}번째 도서의 핵심 키워드 : {word_data[1]}')
            print()


    def handle(self, *args, **kwargs):
        self._initialize()