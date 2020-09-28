import requests
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException
from bs4 import BeautifulSoup
from datetime import datetime
import time, os, re
from openpyxl import Workbook



a = "http://www.g2b.go.kr:8081/ep/preparation/prestd/preStdSrch.do?taskClCd=5"
b = "http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do?bidSearchType=1&taskClCds=5"
c = "http://www.g2b.go.kr:8101/ep/preparation/orderplan/orderplanPubList.do?taskClCd=5"

urlLists = [a]

now = datetime.now()
today = now.strftime('%Y/%m/%d')
todatdata = now.strftime('%y%m%d')

# driver = webdriver.PhantomJS('/Users/jinseongkim/phantomjs-2.1.1-macosx/bin/phantomjs')
searchLists = [""]
# searchLists = ["전시", "홍보", "기념", "체험", "과학", "생태", "생물", "교육", "안전", "테마", "상설", "박람", "기획", "유아", "어린이", "청소년", "역사", "문화", "실물모형", "에너지", "환경"]
totalLists = []
for searchList in searchLists:
    driver = webdriver.Chrome('/Users/jinseongkim/PycharmProjects/crawlingNara/chromedriver')
    driver.get("http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do?bidSearchType=1&taskClCds=5")
    print(searchList)
    search_box = driver.find_element_by_id('bidNm').send_keys(searchList)

    stDateBox = driver.find_element_by_css_selector('input[name="fromBidDt"]').clear()
    driver.find_element_by_css_selector('input[name="fromBidDt"]').send_keys(today)

    newlink = driver.find_element_by_css_selector('a[class="btn_mdl"]').click()

    pageSource = driver.page_source
    bs = BeautifulSoup(pageSource, 'html.parser')
    nsNoList = bs.find('tbody').select('a')
    print(nsNoList)

    nsNoLists = []
    for n, No in enumerate(nsNoList):
        if(n%2 != 1):
            nsNoLists.append(No.get('href'))
        # print(ds.text)
    print(nsNoLists)
    for nsNo in nsNoLists:
        book = Workbook()
        subPageSource = requests.get(nsNo)
        # subPageSource = requests.get('http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno=20200306870&bidseq=00&releaseYn=Y&taskClCd=5')
        bsObject = BeautifulSoup(subPageSource.text, 'html.parser')
        a = bsObject.find_all('div', {'class': 'section'})
        print(len(a))

        csvRows = []
        for aa in a:
            for row in aa.find_all('tr'):
                for cell in row.findAll(['th', 'td']):
                    csvRows.append(re.sub((r'\s+'), '', cell.get_text()))
        titles = ['검색']
        values = [searchList]
        if (len(totalLists) == 0):
            for n, csvRow in enumerate(csvRows):
                if (n % 2 != 1):
                    titles.append(csvRow)

            for n, csvRow in enumerate(csvRows):
                if (n % 2 == 1):
                    values.append(csvRow)
            titlesTuple = tuple(titles)
            print(titlesTuple)
            totalLists.append(titlesTuple)
            valuesTuple = tuple(values)
            print(valuesTuple)
            totalLists.append(valuesTuple)
        else:
            for n, csvRow in enumerate(csvRows):
                if (n % 2 == 1):
                    values.append(csvRow)
            valuesTuple = tuple(values)
            print(valuesTuple)
            totalLists.append(valuesTuple)
    # driver.quit()
# sheet = book.active
# for totalList in totalLists:
#     sheet.append(totalList)
# book.save('./' + todatdata + 'naradata.xlsx')




