from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

ebsUrl = "https://mid.ebs.co.kr/teacher/middle/index?searchSiteCode=all&subjectCd=32000003&searchKeyword=&isSearch=Y"

ff_driver = webdriver.Chrome('/Users/jinseongkim/chromedriver')
ff_driver.implicitly_wait(3)
ff_driver.get(ebsUrl)

qnaList = []

# Q&A페이지 이동
def pageMove(teacherNo):
    ff_driver.find_element_by_id("teacher_box_"+teacherNo).click()

    ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[1]/ul/li[3]/a""").click()

    # 총페이지 리스트에 담기
    pages = ff_driver.find_element_by_class_name("page_wrap").text
    pageList = []

    for page in pages:
        pageList.append(page)

    for page in pageList:
        ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[""" + page + """]""").click()


        # 각 페이지별 클로링
        for i in range(1, 21):
            try:
                ff_driver.implicitly_wait(3)
                qnaData = ff_driver.find_element_by_xpath("""//*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr["""+ str(i) +"""]/td/div[2]/div[1]/div""").text
                print(qnaData)
                qnaList.append(qnaData)
            except:
                pass





if __name__ == "__main__":
    bsObject = bs(urlopen(ebsUrl), "html.parser")
    teacherNos = bsObject.find_all("div", {"class": "teacher_box"})
    # 선생님페이지로 이동
    for teacherNo in range(len(teacherNos)):
        pageMove(teacherNo)
        ff_driver.close()





# print(pageList)


# print(ff_driver.current_url)
# ff_driver.find_element_by_name("btnK").click()

# WebDriverWait(ff_driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.r")))
#
# page_results = ff_driver.find_elements(By.CSS_SELECTOR, "h3.r")
#
# for item in page_results:
#     print(item.text)

#
# //*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[2]
# //*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[3]
# //*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[2]
# //*[@id="container"]/div[4]/div/div/div[2]/div[5]/span/a[1]
# //*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[1]/td/div[2]/div[1]/div
# //*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[2]/td/div[2]/div[1]/div
# //*[@id="container"]/div[4]/div/div/div[2]/form[2]/table/tbody/tr[3]/td/div[2]/div[1]/div