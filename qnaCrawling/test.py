from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    url = urlopen(
        "https://mid.ebs.co.kr/teacher/middle/index?searchSiteCode=all&subjectCd=32000003&searchKeyword=&isSearch=Y")
    bsObject = bs(url, "html.parser")

    # a = bsObject.get("teacherid")
    # print(a)
    teacherIdLists = []
    teacherIds = bsObject.find_all("div", {"class": "teacher_box"})
    # teacherId = bsObject.find_all("div", {"class":"teacher_box"})
    for teacherId in teacherIds:
        teacherIdLists.append(teacherId["teacherid"])

    suburl = urlopen("https://mid.ebs.co.kr/teacher/view?teacherId=supernoil&subjectCd=32000003#qna/list/1/0/0/0")
    teacherQnAPage = bs(suburl, "html.parser")

    qnaTxt = teacherQnAPage.find_all("div", {"class":"innerTab"})
    qnaTxt = teacherQnAPage.find_all("table")

    print(qnaTxt)