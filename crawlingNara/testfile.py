import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time, os
from openpyxl import Workbook

now = datetime.now()
todatdata = now.strftime('%y%m%d')

nsNoLists = ['835588', '835537']
totalLists = []

for nsNo in nsNoLists:
    book = Workbook()
    subPageSource = requests.get(
        'https://www.g2b.go.kr:8143/ep/preparation/prestd/preStdDtl.do?preStdRegNo=' + nsNo + '&referNo=&srchCl=&srchNo=&instCl=2&taskClCd=5&prodNm=%C0%FC%BD%C3&swbizTgYn=&instNm=&dminstCd=&fromRcptDt=2020%2F03%2F02&toRcptDt=2020%2F03%2F02&listPageCount=&orderbyItem=1&instSearchRange=&myProdSearchYn=&searchDetailPrdnmNo=&searchDetailPrdnm=&pubYn=Y&taskClCds=5&recordCountPerPage=10')
    bsObject = BeautifulSoup(subPageSource.text, 'html.parser')
    a = bsObject.find('div', {'class': 'section'}).find_all('tr')

    csvRows = []
    for row in a:
        for cell in row.findAll(['th', 'td']):
            csvRows.append(cell.get_text())
    titles = ['']
    values = [todatdata]
    if(len(totalLists) == 0):
        for n, csvRow in enumerate(csvRows):
            if (n % 2 != 1):
                titles.append(csvRow)

        for n, csvRow in enumerate(csvRows):
            if (n % 2 == 1):
                values.append(csvRow)
        titlesTuple = tuple(titles)
        totalLists.append(titlesTuple)
        valuesTuple = tuple(values)
        totalLists.append(valuesTuple)
    else:
        for n, csvRow in enumerate(csvRows):
            if (n % 2 == 1):
                values.append(csvRow)
        valuesTuple = tuple(values)
        totalLists.append(valuesTuple)
sheet = book.active
for totalList in totalLists:
    sheet.append(totalList)
book.save('./' + todatdata + 'naradata.xlsx')



