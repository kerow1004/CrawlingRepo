from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

urllist ='http://www.yes24.com/Product/Goods/'
pageList = ['66023499']
# pageList = ['57704923','57704914','66792988', '66023499']
for i in pageList:

    isbn
    commodityName
    price1
    price2
    yesPoint
    reAuth
    pub
    sellNum.split(' ')[17]
    date


    html = urlopen(urllist + i)
    bsObject = BeautifulSoup(html, "html.parser")

    # print(bsObject.find_all("ul", {"class": "yesAlertLi"}))
    # auth = bsObject.find("span", {"class": "gd_auth"}).get_text()
    # yesPoint = bsObject.find("ul", {"class": "gd_infoLi"}).select('li')[0].text
    #
    # # print(auth.strip())
    # print(re.split(('\n|\r|원'), auth))
    # print(re.split(('\n|\r|원'), auth)[2].strip())
    # print(re.split(('\n|\r|원'), yesPoint)[1])

    if bsObject.find_all("td", {"class": "txt lastCol"})[
        2].text == '\r\n                            YES24 배송\r\n                        ':
        isbn = ''
    else:
        isbn = bsObject.find_all("td", {"class": "txt lastCol"})[2].text

    date = bsObject.find_all("td", {"class": "txt lastCol"})[0].text
    commodityName = bsObject.find("h2", {"class": "gd_name"}).text
    price1 = bsObject.find_all("em", {"class": "yes_m"})[0].text
    price1 = price1.split('원')[0]
    price2 = bsObject.find_all("em", {"class": "yes_m"})[1].text
    yesPoint = bsObject.find("ul", {"class": "gd_infoLi"}).select('li')[0].text
    yesPoint = yesPoint.split('원')[0].strip()
    auth = bsObject.find("span", {"class": "gd_auth"}).text
    if re.split(('\n|\r|원'), auth)[1] == '':
        reAuth = re.split(('\n|\r'), auth)[2].strip()
    else:
        reAuth = re.split(('\n|\r'), auth)[1].strip()
    pub = bsObject.find("span", {"class": "gd_pub"}).select('a')[0].text
    sellNum = bsObject.find("span", {"class": "gd_sellNum"}).text
    sellNum = sellNum.split(' ')[17]

    csvData = [ "'" + isbn,  commodityName, price1.split('원')[0], price2,
               yesPoint.split('원')[0].strip(), reAuth, pub, sellNum.split(' ')[17], date]

    categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[3].text
    # print('1====',categoryfull)
    categorys = categoryfull.split('\xa0')[-1:]
    # print('2====',categorys)
    category = categorys[0].split('\n')
    # print('3====',category)
    # print(category[1])

    if category[1] == '국내도서':

        for i in range(1, len(category), 2):
            print(category[i])

    elif category[1] == '중고샵':
        categorys = categoryfull.split('\xa0')[1]
        category = categorys.split('\n')
        print('========================')
        for i in range(1, len(category), 2):
            print(category[i])

    else:
        categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[2].text
        categorys = categoryfull.split('\xa0')[-1:]
        category = categorys[0].split('\n')
        for i in range(1, len(category), 2):
            print(category[i])

    categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})
    print(categoryfull)