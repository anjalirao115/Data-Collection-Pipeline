from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import uuid
import json
import urllib
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


'''This Scraper class extracts data from IMDB website and stores data in dictionaries. 
There are different methods defined for different tasks.'''

class Scraper:
    def __init__(self):
        print('This is a scraper class')

    
    def open_website(self, url):    
        """
        The method opens the url provided in Chrome and returns the driver, which can be used
        to as a variable to extract further information from the page.
        """
        s = Service('/home/anjali/work/aicore/data_collection_pipeline/test1/docker_prep/chromedriver')

        options = Options()
        options.add_argument("--headless") #headless mode removes GUI
        options.add_argument("--window-size=1920,1080") # Set windows fullsize so elements are in the correct location
        # user agent gets sent with the webrequest as a representation of your system, this makes the webserver think you're running it outside a docker container
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')
        # bypass some security features of chrome to allow it run inside a container
        options.add_argument('--no-sandbox')
        # Remove sharing memory between the system and the container, can cause issues
        options.add_argument("--disable-dev-shm-usage")
        # add the arguements to the chromedriver
        driver = webdriver.Chrome("/home/anjali/work/aicore/data_collection_pipeline/test1/docker_prep/chromedriver", options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().download_and_install(), options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        #chrome_options.add_argument('user-agent={0}'.format(user_agent))
        #driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        #driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options=chrome_options)
        #driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        #driver = webdriver.Chrome(options=chrome_options)

        #driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=webdriver.ChromeOptions() )

        #driver = webdriver.Chrome() 
        time.sleep(2)
        driver.get(url)
        return driver

    
    def accept_cookies(self):
        """
        The IMDB website has no cookies, still this part of the code is added here to remind that
        cookies are the first things to be handled after openiing a website.
        """
        try: 
            driver.switch_to.frame('gdpr-consent-notice') 
            accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except:
            pass

    
    def scroll_website(self, driver):    
        """
        The method slowly scolls the website from top to bottom in small steps.
        """
        for sections in np.linspace(0.1,0.94,30):
            driver.execute_script("window.scrollTo(0, "+str(sections)+"*document.body.scrollHeight);")
            time.sleep(1)

    def collect_links(self, driver):
        """
        The method collects links to all the products listed in the website and returns a list of links.
        """
        shows_container = driver.find_element(by=By.XPATH, value='//tbody[@class="lister-list"]')
        shows_list = shows_container.find_elements(by=By.XPATH, value='./tr')

        link_list = []
        uid_list = []

        for show in shows_list[0:4]:

            title = show.find_element(by=By.XPATH, value='./td[@class="titleColumn"]')

            a_tag = title.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)

            uid = link[69:105]
            uid_list.append(uid)
           
        print(f'Total number of shows are {len(link_list)}')

        return link_list

    def get_data_from_individual_page(self, driver):
        """
        The method collects data from an individual link passed to it opened in the driver. 
        """
        title = driver.find_element(by=By.XPATH, value='//h1[@data-testid="hero-title-block__title"]').text
        year = driver.find_element(by=By.XPATH, value='//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"]').text
        rating = driver.find_element(by=By.XPATH, value='//span[@class="sc-7ab21ed2-1 jGRxWM"]').text
        number_of_ratings = driver.find_element(by=By.XPATH, value='//div[@class="sc-7ab21ed2-3 dPVcnq"]').text
        return title, year, rating, number_of_ratings


    def get_image_url(self, driver):      
        """
        The method finds the url of image for an individual product-page and returns the url.
        """
        img_tag = driver.find_element(by=By.XPATH, value='//img[@class="ipc-image"]')
        img_url = img_tag.get_attribute('src')
        return img_url

    def create_folder(self, folder_name):
        """
        A method defined to create folder.
        """
        os.mkdir(folder_name)    
          

## Executing the code below to perform scrapping tasks.            
if __name__ == '__main__':
    imdb = Scraper() 

    ## Defining the url and opening it with driver
    url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
    driver = imdb.open_website(url)
    link_list = imdb.collect_links(driver)
    driver.close()
    print('All links are collected')

    ## Creating a raw_data folder to store data in to
    raw_data_folder = "/home/anjali/work/aicore/data_collection_pipeline/test1/raw_data"
    imdb.create_folder(raw_data_folder)
    print('Created raw_data folder \n')


    ## For loop to extract data from links
    for index, link in enumerate(link_list, start=1):

        print(f"Scraping data for show {index}")

        driver = imdb.open_website(link)
        title, year, rating, number_of_ratings = imdb.get_data_from_individual_page(driver)
        img_url = imdb.get_image_url(driver)

        friendly_id = link[29:36]
        uid = str(uuid.uuid4())

        dict = {'friendly_id':[], 'uid':[], 'title':[], 'year':[], 'rating':[], 'number_of_ratings':[], 'img_url':[]}
        
        dict['friendly_id'].append(friendly_id)
        dict['uid'].append(uid)
        dict['title'].append(title)
        dict['year'].append(year)
        dict['rating'].append(rating)
        dict['number_of_ratings'].append(number_of_ratings)
        dict['img_url'].append(img_url)
        print(f"Dictionary created for {title}")

        ## Creating folder recursively for individual product/link
        file_path = "/home/anjali/work/aicore/data_collection_pipeline/test1/raw_data/" + str(friendly_id)
        imdb.create_folder(file_path)

        ## Writing data in the files in the folders created above
        target_file = file_path+'/data.json'
        with open(target_file, 'w') as fp:
            json.dump(dict, fp, sort_keys=True, indent=4)

        print(f"Data saved for {title}")    

        ## Downloading image data
        image_path = file_path + '/images/'
        imdb.create_folder(image_path)
        image_name = image_path + str(friendly_id) + '.jpg'
        
        urllib.request.urlretrieve(img_url, image_name)

        print(f"Image saved for {title} \n") 

        time.sleep(2)
        driver.close()
        

