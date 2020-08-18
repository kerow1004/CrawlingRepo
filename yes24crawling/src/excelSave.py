from openpyxl import Workbook
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

book = Workbook()


urllist = []
excelList = []

for page in range(1,2,1):
    url = urlopen('http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013003&sumgb=08&PageNumber=' + str(page))
    # print(highSchoolUrl + str(page))
    bsObject = BeautifulSoup(url, "html.parser")


    for cover in bsObject.find_all("td", {"class":"goodsTxtInfo"}):

        bookurl = cover.select('a')[0].get('href')
        urllist.append(bookurl)

for index, book_lank_url in enumerate(urllist):
    try:
        html = urlopen('http://www.yes24.com' + book_lank_url)
        bsObject = BeautifulSoup(html, "html.parser")

        if bsObject.find_all("td", {"class": "txt lastCol"})[
            2].text == '\r\n                            YES24 배송\r\n                        ':
            isbn = ''
        else:
            isbn = bsObject.find_all("td", {"class": "txt lastCol"})[2].text

        date = bsObject.find_all("td", {"class": "txt lastCol"})[0].text
        commodityNo = book_lank_url.split('/')[3]
        commodityName = bsObject.find("h2", {"class": "gd_name"}).text
        price1 = bsObject.find_all("em", {"class": "yes_m"})[0].text
        price2 = bsObject.find_all("em", {"class": "yes_m"})[1].text
        yesPoint = bsObject.find("ul", {"class": "gd_infoLi"}).select('li')[0].text
        auth = bsObject.find("span", {"class": "gd_auth"}).text
        if re.split(('\n|\r|원'), auth)[1] == '':
            reAuth = re.split(('\n|\r'), auth)[2].strip()
        else:
            reAuth = re.split(('\n|\r'), auth)[1].strip()
        pub = bsObject.find("span", {"class": "gd_pub"}).select('a')[0].text
        sellNum = bsObject.find("span", {"class": "gd_sellNum"}).text

        csvData = (index + 1, "'" + isbn, commodityNo, commodityName, price1.split('원')[0], price2,
                   yesPoint.split('원')[0].strip(), reAuth, pub, sellNum.split(' ')[17], date)
        excelList.append(csvData)
        # categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[3].text
        # categorys = categoryfull.split('\xa0')[-1:]
        # category = categorys[0].split('\n')

        # if category[1] == '국내도서':
        #
        #     for i in range(1, len(category), 2):
        #         csvData.append(category[i])
        #
        # elif category[1] == '중고샵':
        #     categorys = categoryfull.split('\xa0')[1]
        #     category = categorys.split('\n')
        #     for i in range(1, len(category), 2):
        #         csvData.append(category[i])
        #
        # else:
        #     categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[2].text
        #     categorys = categoryfull.split('\xa0')[-1:]
        #     category = categorys[0].split('\n')
        #     for i in range(1, len(category), 2):
        #         csvData.append(category[i])
        print(csvData)




        

    except:
        pass

sheet = book.active
sheet.append(('크롤링일','순위', 'ISBN', '상품번호', '상품명', '정가', '판매가', 'YES포인트', '저자', '출판사', '판매지수', '출간일', '분류'))
for row in excelList:
    sheet.append(row)
    print(row)


book.save('../exFile.xlsx')

