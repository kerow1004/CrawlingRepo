from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv, datetime, time, re
from multiprocessing import Pool, Process
from openpyxl import Workbook


def yes24data(school, sUrl):
    book = Workbook()
    yes24Url = 'http://www.yes24.com'
    urllist = []
    excelList = []

    # if os.path.isfile('../data/'+school+'yes24crawling.csv') == True:
    #     shutil.move('../data/'+school+'yes24crawling.csv', '../data/pastdata/'+school+'/yes24crawling' + strNow + '.csv')

    # f = open('/home/ec2-user/yes24crawling/data/'+school+'yes24crawling.csv', 'w', encoding='cp949')
    # # f = open('../data/'+school+'yes24crawling.csv', 'w', encoding='utf-8')
    # wf = csv.writer(f)
    # wf.writerow(['크롤링일','순위', 'ISBN', '상품번호', '상품명', '정가', '판매가', 'YES포인트', '저자', '출판사', '판매지수', '출간일', '분류'])

    for page in range(1, 2, 1):
        url = urlopen(sUrl + str(page))
        # print(highSchoolUrl + str(page))
        bsObject = BeautifulSoup(url, "html.parser")

        for cover in bsObject.find_all("td", {"class": "goodsTxtInfo"}):
            bookurl = cover.select('a')[0].get('href')
            urllist.append(bookurl)

    for index, book_lank_url in enumerate(urllist):
        try:
            html = urlopen(yes24Url + book_lank_url)
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

            excelData = (strNow, index + 1, isbn, commodityNo, commodityName, price1.split('원')[0], price2,
                       yesPoint.split('원')[0].strip(), reAuth, pub, sellNum.split(' ')[17], date)

            categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[3].text
            categorys = categoryfull.split('\xa0')[-1:]
            category = categorys[0].split('\n')

            categoryList = []

            if category[1] == '국내도서':

                for i in range(1, len(category), 2):
                    categoryList.append(category[i])

            elif category[1] == '중고샵':
                categorys = categoryfull.split('\xa0')[1]
                category = categorys.split('\n')
                for i in range(1, len(category), 2):
                    categoryList.append(category[i])

            else:
                categoryfull = bsObject.find_all("ul", {"class": "yesAlertLi"})[2].text
                categorys = categoryfull.split('\xa0')[-1:]
                category = categorys[0].split('\n')
                for i in range(1, len(category), 2):
                    categoryList.append(category[i])

            categoryTuple = tuple(categoryList)
            print(categoryTuple)

            totalData = excelData + categoryTuple
            # wf.writerow(csvData)
            excelList.append(totalData)
            print(totalData)

        except:
            pass

    # f.close()
    sheet = book.active
    sheet.append(('크롤링일', '순위', 'ISBN', '상품번호', '상품명', '정가', '판매가', 'YES포인트', '저자', '출판사', '판매지수', '출간일', '분류'))
    for row in excelList:
        sheet.append(row)
        print(row)

    book.save('../data/' + school + 'yes24crawling.xlsx')


if __name__ == "__main__":
    now = datetime.datetime.now()
    strNow = now.strftime('%y%m%d')
    startTime = int(time.time())

    # urlList = 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013003&sumgb=08&PageNumber='
    urlList = ['http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013003&sumgb=08&PageNumber=', 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013002&sumgb=08&PageNumber=']
    # schoolList = ['high', 'middle']
    # pool = Pool(processes=12)
    procs = []

    for index, url in enumerate(urlList):
        proc = Process(target=yes24data, args=(index, url))
        procs.append(proc)

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()

    # s3 = boto3.client('s3')
    #
    # files = ['highyes24crawling.csv', 'middleyes24crawling.csv']
    #
    # bucket = 'yes24-crawling-csv'

    # for file in files:
    #     s3File = 'pastdata/'+ strNow +file
    #     s3.upload_file('../data/' + file, bucket, file, ExtraArgs={'ACL': "public-read"})
    #     s3.upload_file('../data/' + file, bucket, s3File, ExtraArgs={'ACL': "public-read"})
    endTime = int(time.time())
    print("총 작업 시간", (endTime - startTime))

