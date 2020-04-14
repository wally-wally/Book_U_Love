from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        # models.Book.objects.all().delete()
        books = dataframes["books"]
        print(models.Book.category)
        # for book in books.iterrows():
        #     print(book)

        books_bulk = [
            models.Book(
                isbn=book.isbn,
                title=book.title,
                description=book.description,
                priceStandard=book.priceStandard,
                coverSmallUrl=book.coverSmallUrl,
                coverLargeUrl=book.coverLargeUrl,
                category=models.Category.objects.filter(id=book.category),
                publisher=book.publisher,
                author=book.author,
                translator=book.translator,
                pubDate=book.pubDate,
            )
            for book in books.itertuples()
        ]
        print('iter')
        models.Book.objects.bulk_create(books_bulk)

        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()