import requests
import os
import pandas as pd

DATA_DIR = "./"

DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

book_column = ('isbn','title','author','translator','description','priceStandard','coverSmallUrl',
                'coverLargeUrl', 'categoryId', 'publisher', 'pubDate')

def catogorybestSeller(categoryId=100):
    params = {
        'key':'6DC249C8376B02DF365161A34E02EBC568955779AAE9AD461B4AE7AC609353EE',
        'output':'json',
        # 'sort' : 'customerRating',
        'categoryId': categoryId,
        # 'start': '2', 
        # 'queryType' : 'title'

    }
    response = requests.get('http://book.interpark.com/api/bestSeller.api',params=params).json()
    bookdata= []
    for i in response["item"]:
        try:
            bookdata.append([i['isbn'], i['title'], i['author'], i["translator"],
                    i['description'], i['priceStandard'], i['coverSmallUrl'], 
                    i['coverLargeUrl'], i['categoryId'], i['publisher'], i['pubDate']
                ])
        except KeyError as k:
            print(categoryId ,i['title'] ,k)
            i['isbn'] = ""
            print('here')
            bookdata.append([i['isbn'], i['title'], i['author'], i["translator"],
                    i['description'], i['priceStandard'], i['coverSmallUrl'], 
                    i['coverLargeUrl'], i['categoryId'], i['publisher'], i['pubDate']])
            print(i)
            print('complete')
    print(response['searchCategoryName'],response['totalResults'])
    return bookdata




def BestSeller():
    bestseller = []
    for i in range(101,130):
        bestseller += catogorybestSeller(i)

    for i in range(201,218):
        bestseller += catogorybestSeller(i)

    print(len(bestseller))
    book_frame = pd.DataFrame(data=bestseller, columns=book_column)

    return {"books" : book_frame}

def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)

def load_dataframes():
    return pd.read_pickle(DUMP_FILE)

data = BestSeller()
dump_dataframes(data)

loaddata = load_dataframes()
print(data['books'].head())
