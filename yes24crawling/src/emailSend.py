import os, datetime
now = datetime.datetime.now()
strNow = now.strftime('%y%m%d')
os.system("curl -s -d 'payload={\"text\": \"YES24 "+ strNow +"일자 자료입니다.\"}' https://hooks.slack.com/services/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")
os.system("curl -s -d 'payload={\"text\": \"https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/pastdata/"+ strNow +"highyes24crawling.csv\"}' https://hooks.slack.com/services/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")
os.system("curl -s -d 'payload={\"text\": \"https://s3.ap-northeast-2.amazonaws.com/yes24-crawling-csv/pastdata/"+ strNow +"middleyes24crawling.csv\"}' https://hooks.slack.com/services/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")

datetime.datetime.isocalnoendar()