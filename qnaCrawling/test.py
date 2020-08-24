from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import csv


ebsUrl = "https://mid.ebs.co.kr/teacher/middle/index?searchSiteCode=all&subjectCd=32000003&searchKeyword=&isSearch=Y"

bsObject = bs(urlopen(ebsUrl), "html.parser")
teacherNos = bsObject.find_all("div", {"class": "teacher_box"})
# 선생님페이지로 이동
for teacherNo in range(1, 2):
    ff_driver = webdriver.Chrome('/Users/jinseongkim/chromedriver')
    ff_driver.implicitly_wait(3)
    ff_driver.get(ebsUrl)

    ff_driver.find_element_by_id("teacher_box_" + str(teacherNo)).click()

    try:
        ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[1]/ul/li[3]/a""").click()
        returnUrl = ff_driver.current_url
        # print(returnUrl)

        # returnUrl = returnUrl.split("list")
        # print(returnUrl)

        page = 1

        with open('./test.csv', 'w', encoding='utf-8', newline='') as writer_csv:
            writer = csv.writer(writer_csv, delimiter=',')
            writer.writerow(["teacher", "Question", "Answer"])

            while 1:
                url = returnUrl + "/" + str(page) + "/0/0/0"

                ff_driver.get(url)

                for i in range(1, 21, 2):

                    qnaList = []
                    try:
                        ff_driver.implicitly_wait(3)
                        tData = ff_driver.find_element_by_xpath(
                            """//*[@id="container"]/div[3]/div/div/div[1]/p/strong""").text
                        qnaList.append(tData)
                        qData = ff_driver.find_element_by_xpath(
                            """//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[""" + str(
                                i) + """]/td/div[2]/div[1]/div""").text
                        qnaList.append(qData)
                        aData = ff_driver.find_element_by_xpath(
                            """//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[""" + str(
                                i + 1) + """]/td/div[2]/div[1]/div""").text
                        qnaList.append(aData)
                        # print(qnaList)
                        writer.writerow(qnaList)
                    except:
                        pass

                print(url)
                if ff_driver.find_element_by_xpath(
                        """//*[@id="container"]/div[4]/div/div/div[2]/div[5]""").text == "현재 등록된 게시물이 없습니다.":
                    break

                    # 각 페이지별 클로링
                page = page + 1
    except:
        pass

    ff_driver.close()


