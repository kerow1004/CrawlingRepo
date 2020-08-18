from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv, datetime, shutil, os, boto3, re
from botocore.exceptions import ClientError
from openpyxl import Workbook

now = datetime.datetime.now()

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

    for page in range(1,2,1):
        url = urlopen(sUrl + str(page))
        # print(highSchoolUrl + str(page))
        bsObject = BeautifulSoup(url, "html.parser")


        for cover in bsObject.find_all("td", {"class":"goodsTxtInfo"}):

            bookurl = cover.select('a')[0].get('href')
            urllist.append(bookurl)

    for index, book_lank_url in enumerate(urllist):
        try:
            html = urlopen(yes24Url + book_lank_url)
            bsObject = BeautifulSoup(html, "html.parser")

            if bsObject.find_all("td", {"class":"txt lastCol"})[2].text == '\r\n                            YES24 배송\r\n                        ':
                isbn = ''
            else:
                isbn = bsObject.find_all("td", {"class":"txt lastCol"})[2].text

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
            # wf.writerow(csvData)
            categoryTuple = tuple(categoryList)
            print(categoryTuple)

            totalData = excelData + categoryTuple
            excelList.append(totalData)
            print(totalData)

        except:
            pass

    # f.close()
    sheet = book.active
    sheet.append(('크롤링일', '순위', 'ISBN', '상품번호', '상품명', '정가', '판매가', 'YES포인트', '저자', '출판사', '판매지수', '출간일', '분류'))
    print(excelList)
    for row in excelList:
        sheet.append(row)
        print(row)

    # book.save('/home/ec2-user/yes24crawling/data/'+school+'yes24crawling.xlsx')
    book.save('../data/'+school+'yes24crawling.xlsx')

def sendEmail():
    strDate = now.strftime('%Y년 %m월 %d일 ')   
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "yes24data@imath.tv"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "jinseong.kim@wonriedu.com", "kerow1004@gmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"

    # The subject line for the email.
    SUBJECT = strDate + "YES24 자료입니다."

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "YES24 자료"

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>""" + strDate + """YES24 자료입니다.</h1>
      <p>
        <a href='https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/highyes24crawling.csv'>https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/highyes24crawling.csv</a> 고등학교 자료입니다.</p>
        <a href='https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/middleyes24crawling.csv'>https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/middleyes24crawling.csv</a> 중학교 자료입니다.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                     'jinseong.kim@wonriedu.com',
                     'miae.kim@wonriedu.com',
                     'jinkyung.choi@wonriedu.com',
                     'jungwoo.nam@wonriedu.com',
                     'eunjeong.hwang@wonriedu.com',
                     'cheonho.choi@wonriedu.com',
                     'jisu.park@wonriedu.com',
                     'kicheol.kim@wonriedu.com',

                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def slackMessage(sUrl):
    url = urlopen(sUrl + '1')
    soupWeek = BeautifulSoup(url, "html.parser")
    bestYear = soupWeek.find("select", {"id": "bestyear"}).select('option[selected=""]')[0].text
    bestMonth = soupWeek.find("select", {"id": "bestmonth"}).select('option[selected=""]')[0].text
    bestWeek = soupWeek.find("select", {"id": "bestweek"}).select('option[selected=""]')[0].text

    now = datetime.datetime.now()
    strNow = now.strftime('%y%m%d')
    os.system(
        "curl -s -d 'payload={\"text\": \"YES24 " + bestYear + "년" + bestMonth + "월" + bestWeek + "주차 자료입니다.\"}' https://hooks.slack.com/services/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")
    os.system(
        "curl -s -d 'payload={\"text\": \"<https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/pastdata/" + strNow + "highyes24crawling.xlsx | 고등자료>, <https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/pastdata/" + strNow + "middleyes24crawling.xlsx | 중등자료>\"}' https://hooks.slack.com/services/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")



if __name__ == "__main__":
    urlList = ['http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013003&sumgb=08&PageNumber=', 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001001013002&sumgb=08&PageNumber=']
    schoolList = ['high', 'middle']
    strNow = now.strftime('%y%m%d')
    for i in range(1):
        yes24data(schoolList[i], urlList[i])

    # s3 = boto3.client('s3')
    #
    #
    # files = ['highyes24crawling.xlsx', 'middleyes24crawling.xlsx']
    #
    # bucket = 'yes24-crawling-csv'
    #
    #
    # for file in files:
    #     s3File = 'pastdata/'+ strNow +file
    #     s3.upload_file('/home/ec2-user/yes24crawling/data/' + file, bucket, file, ExtraArgs={'ACL':"public-read"})
    #     s3.upload_file('/home/ec2-user/yes24crawling/data/' + file, bucket, s3File, ExtraArgs={'ACL': "public-read"})
    #
    # # sendEmail()
    # slackMessage(urlList[0])