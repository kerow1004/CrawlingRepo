import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ff_driver = webdriver.Chrome('/Users/jinseongkim/chromedriver')
ff_driver.get("http://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=/pt/menu/frameTgong.do?url=http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do")

query = ff_driver.find_element_by_name("prodNm").send_keys("범죄")
ff_driver.find_element_by_name("btnK").click()

# WebDriverWait(ff_driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.r")))
#
# page_results = ff_driver.find_elements(By.CSS_SELECTOR, "h3.r")
#
# for item in page_results:
#     print(item.text)