from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import csv

ebsUrl = "https://mid.ebs.co.kr/teacher/middle/index?searchSiteCode=all&subjectCd=32000003&searchKeyword=&isSearch=Y"

qnaList = []

# Q&A페이지 이동
def pageCrawling(teacherNo):
    ff_driver = webdriver.Chrome('/Users/jinseongkim/chromedriver')
    ff_driver.implicitly_wait(3)
    ff_driver.get(ebsUrl)

    ff_driver.find_element_by_id("teacher_box_"+teacherNo).click()

    try:
        ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[1]/ul/li[3]/a""").click()
        returnUrl = ff_driver.current_url
    except:
        pass

    returnUrl = returnUrl.split("list")

    page = 1

    # with open('test.csv', 'w', encoding='utf-8', newline='') as writer_csv:
    #     writer = csv.writer(writer_csv, delimiter=',')

    while 1:
        url = returnUrl[0] + "list/" + str(page) + "/0/0/0"

        ff_driver.get(url)

        for i in range(1, 21, 2):

            qnaList = []
            try:
                ff_driver.implicitly_wait(3)
                qData = ff_driver.find_element_by_xpath(
                    """//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[""" + str(
                        i) + """]/td/div[2]/div[1]/div""").text
                qnaList.append(qData)
                aData = ff_driver.find_element_by_xpath(
                    """//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[""" + str(
                        i+1) + """]/td/div[2]/div[1]/div""").text
                qnaList.append(aData)
                print(qnaList)
            except:
                pass
            # writer.writerow(qnaList)
            # print(qnaList)

        if ff_driver.find_element_by_xpath(
                """//*[@id="container"]/div[4]/div/div/div[2]/div[5]""").text == "현재 등록된 게시물이 없습니다.":
            print("다음 선생님!!!" + ff_driver.find_element_by_xpath(
                """//*[@id="container"]/div[3]/div/div/div[1]/p/strong""").text)
            break
        page = page +1

    ff_driver.quit()

    # 총페이지 리스트에 담기


    # pages = ff_driver.find_element_by_class_name("page_wrap").text
    # pageList = []
    #
    # for page in pages:
    #     pageList.append(page)
    #
    # print(pageList)

    # for page in range(1, 11):
    #     ff_driver.implicitly_wait(3)
    #     ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[""" + str(page) + """]""").click()
    #
    #     # 각 페이지별 클로링
    #     for i in range(1, 21):
    #         try:
    #             ff_driver.implicitly_wait(3)
    #             qnaData = ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr["""+ str(i) +"""]/td/div[2]/div[1]/div""").text
    #             print(qnaData)
    #             qnaList.append(qnaData)
    #         except:
    #             pass



if __name__ == "__main__":
    bsObject = bs(urlopen(ebsUrl), "html.parser")
    teacherNos = bsObject.find_all("div", {"class": "teacher_box"})
    # 선생님페이지로 이동
    pageCrawling(str(9))

    print(qnaList)


