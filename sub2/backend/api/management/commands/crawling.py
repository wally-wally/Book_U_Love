import requests
from bs4 import BeautifulSoup

# res = requests.get('http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo=327309010')
res = requests.get('http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo=208040523')
# res = requests.get('http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo=292644896')

soup = BeautifulSoup(res.content, 'html.parser')

outer_blocks = soup.find_all('p')
# print(outer_blocks)

for i in range(len(outer_blocks)):
    # print(outer_blocks[i])
    if outer_blocks[i].get_text() == '책소개':
        disc = outer_blocks[i+1]
        # print(outer_blocks[i+1].get_text())
    elif outer_blocks[i].get_text() == '목차':
        contents = outer_blocks[i+1]

print('disc', disc)
print('contents', contents)
print(len('http://bimage.interpark.com/goods_image/0/5/2/3/'))
print('http://bimage.interpark.com/goods_image/7/2/7/3/307887273s.jpg'[48:57])
print('http://bimage.interpark.com/goods_image/0/5/8/4/240120584s.jpg'.index('s', 40))