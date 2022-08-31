from requests import get
import numpy as np
import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import re



# Selenium class에서 성분 추출
def execute_element(selenium_class):
    global results
    for element in selenium_class:
        results = element.text
    return results
   
def movie_crawl(movie_name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #options.add_argument("headless")
    #options.add_argument('--start-fullscreen')
    options.add_argument('--kiosk')
    driver = webdriver.Chrome(options = options)
    #driver.set_window_size(1980, 1024)    
    # imdp 사이트에서 해당 영화 검색
    driver.get('https://www.imdb.com/search/')
    time.sleep(2)
        
    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="suggestion-search"]')
        search_box.send_keys(movie_name)
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a').click()
        time.sleep(2)
        title = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1'))
         # search_box.send_keys(Keys.RETURN)
         # 각 해당정보 추출
        rating = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]')) 
        genre1 = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/div[2]/a[1]/span'))
        genre2 = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/div[2]/a[2]/span'))
        story = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/span[3]'))
        year = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]/a'))
        movie_rate = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a'))
        director = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div/ul/li/a'))
        lead_actor = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li[1]'))
        sup_actor = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li[2]'))
        score = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[3]/a/span/span[1]/span'))
        vote = execute_element(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[3]'))
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div/div[1]/div/a/div').click()
        time.sleep(2)
        image = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/div[4]/img').get_attribute("src")
        # urllib.request.urlretrieve(image, "../image/str(movie_name)"+".jpg")
        image = image.replace("'",'')    
    except:
        driver.close()
        return None
    
    
    def convert_unit(value):
        unit = value[-1:] # 값의 맨마지막 값을 저장
        value = re.sub(r'[KM]', '',value) # K,M 이 있으면 제거
        if unit == 'K':                     # sales의 마지막 값에 K가 있으면 천을 곱하고 이외의 경우에는 100000 을 곱해준다
            value = float(value) * 1000
            return value
        elif unit =='M':
            value = float(value) * 100000
            return value
        else:
            return value

    vote = convert_unit(vote)
    info = [title, int(year), float(rating), float(score), vote , director, story, movie_rate, genre1, genre2, lead_actor, sup_actor, image]
    
    return info

