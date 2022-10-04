from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome() 
url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

time.sleep(2)

driver.get(url)

shows_container = driver.find_element(by=By.XPATH, value='//tbody[@class="lister-list"]')
shows_list = shows_container.find_elements(by=By.XPATH, value='./tr')

for shows in shows_list:

    title = shows.find_element(by=By.XPATH, value='//td[@class="titleColumn"]')
    print(title.text)

