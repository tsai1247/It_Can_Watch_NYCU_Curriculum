#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
import json

from typing import List, Tuple
import tkinter as tk

def endYear():
    time = datetime.now()
    return time.year - 1911 - 1 + (time.month+4) //6 //2

def getLoginInfomation():
    data = open('account', 'r', encoding='utf-8').readlines()
    try:
        acnt, passwd = data[0].strip(), data[1].strip()
    except:
        return None, None
        
    return acnt, passwd

def getCurriculum(messageLabel: tk.Label = None):
    def find_element(by: str = By.ID, value: Tuple[str, None] = None, timeout: float = 10) -> WebElement:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(by: str = By.ID, value: Tuple[str, None] = None, timeout: float = 10) -> List[WebElement]:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def log(text: str):
        if messageLabel is not None:
            messageLabel.config(text = messageLabel.cget('text') + text)
        else:
            print(text)

    account, password = getLoginInfomation()
    if account is None or password is None:
        log(f'學號或密碼填寫錯誤\n')
        open('account', 'w').write('')
        return False
        
    elif(not account.isdecimal()):
        log(f'學號 {account} 並非正確的陽明交通大學學號\n')
        open('account', 'w').write('')
        return False
    elif len(account) == 7:
        startyear = int(f'1{account[0:2]}')
    elif len(account) == 9:
        startyear = int(f'1{account[1:3]}')
    else:
        log(f'學號 {account} 並非正確的陽明交通大學學號\n')
        open('account', 'w').write('')
        return False

    log('安裝最新版的chrome driver... ')
    try:
        chromedriver_autoinstaller.install()
    except:
        log('網路錯誤，請檢查網路連線\n')
        return False

    log('完成\n')
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('log-level=2')

    log('建立selenium瀏覽器... ')
    driver = webdriver.Chrome(options=chrome_options)
    log('成功\n')
    driver.maximize_window()

    driver.get('https://portal.nycu.edu.tw/#/login?redirect=%2F')
    log('進入portal\n')
    sleep(0.2)
    log('登入中... ')
    find_element(By.ID, 'account').send_keys(account)
    find_element(By.ID, 'password').send_keys(password)
    find_element(By.CLASS_NAME, 'login').click()
    
    try:
        find_element(By.XPATH, '//a[text()="校園單一入口"]', 5)
    except TimeoutException:
        log('學號或密碼錯誤\n')
        open('account', 'w').write('')
        return False
    
    log('完成\n')
    sleep(0.2)

    log('進入學籍成績系統... \n')
    log('正在取得課程名稱...\n')
    driver.get(f'https://portal.nycu.edu.tw/#/schedule/index')
    

    curriculum_urls = [element.get_attribute('href') for element in find_elements(By.XPATH, '//div[@class="ceil-inner"]/a', timeout=5)]

    log(f'正在取得課程詳細資料... ')
    ret = []
    for url in curriculum_urls:
        driver.get(url)
        ret.append( {
            'url': url, 
            '課程名稱': find_element(By.NAME, 'cos_cname').text.split(' ')[1],
            '授課教師': find_element(By.NAME, 'tea_name').text,
            '開課單位': find_element(By.NAME, 'dep_name').text,
            '永久課號': find_element(By.NAME, 'cos_code').text,
            '學分數': find_element(By.NAME, 'cos_credit').text,
            '必/選修': find_element(By.NAME, 'sel_type').text,
            '上課時間/教室': find_element(By.NAME, 'cos_time').text,
            '課程概述與目標': find_element(By.NAME, 'col_outline').text,
            '學期作業、考試、評量': find_element(By.NAME, 'col_exam_score').text
        })
    
    log(f'完成\n')
    log(f'關閉連線，即將顯示課表...\n')
    driver.close()
    open('data.json', 'w', encoding='utf-8').write(json.dumps(ret))
    return True

# data = getCurriculum()