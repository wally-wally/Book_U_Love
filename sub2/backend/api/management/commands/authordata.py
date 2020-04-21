from api import models
from django.core.management.base import BaseCommand
from pathlib import Path
from backend import settings
import requests
import json
from bs4 import BeautifulSoup

class Command(BaseCommand):

    def authordata(self, file_id):
        with open(f'author_files/author_list{file_id}.json',encoding="utf-8") as f:
            authors = json.load(f)
        
        for author_data in authors:
            models.Author.objects.create(
                name = author_data["name"],
                imgUrl = author_data["img_url"],
                boneDate = '' if author_data["bone_date"] == '미등록' else author_data["bone_date"],
                region = '' if author_data["region"] == '미등록' else author_data["region"],
                description = author_data["description"]
            )
        

    def _initialize(self):
        for i in range(1, 9):
            print(f'---{i}번째 author 파일 DB 적재 시작---')
            self.authordata(i)
            print(f'---{i}번째 author 파일 DB 적재 종료---')


    def handle(self, *args, **kwargs):
        self._initialize()