from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

ebsUrl = "https://mid.ebs.co.kr/teacher/middle/index?searchSiteCode=all&subjectCd=32000003&searchKeyword=&isSearch=Y"

qnaList = []

# Q&A페이지 이동
def pageMove(teacherNo):
    ff_driver = webdriver.Chrome('/Users/jinseongkim/chromedriver')
    ff_driver.implicitly_wait(3)
    ff_driver.get(ebsUrl)

    ff_driver.find_element_by_id("teacher_box_"+teacherNo).click()

    try:
        ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[1]/ul/li[3]/a""").click()
    except:
        pass

    # 총페이지 리스트에 담기
    # pages = ff_driver.find_element_by_class_name("page_wrap").text
    # pageList = []
    #
    # for page in pages:
    #     pageList.append(page)
    #
    # print(pageList)

    for page in range(1, 11):
        ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[""" + str(page) + """]""").click()
        ff_driver.implicitly_wait(3)

        # 각 페이지별 클로링
        for i in range(1, 21):
            try:
                qnaData = ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr["""+ str(i) +"""]/td/div[2]/div[1]/div""").text
                ff_driver.implicitly_wait(3)
                print(qnaData)
                qnaList.append(qnaData)
            except:
                pass



if __name__ == "__main__":
    bsObject = bs(urlopen(ebsUrl), "html.parser")
    teacherNos = bsObject.find_all("div", {"class": "teacher_box"})
    # 선생님페이지로 이동
    for teacherNo in range(len(teacherNos)):
        pageMove(str(teacherNo))
        # ff_driver.close()

    print(qnaList)


