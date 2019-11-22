# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time


class NikeSeCreateAccountSpider(scrapy.Spider):
    name = 'nike_se_create_account'
    allowed_domains = ['nike.com']
    start_urls = ['http://nike.com/']

    def parse(self, response):
        # set driver and get start url
        driver = webdriver.Chrome('/home/zijie/alatest/myWork/nike_bot/chromedriver')
        driver.maximize_window()
        driver.get(self.start_urls[0])
        # click login button
        login_button = '//button[@data-type="click_navJoinLogin"]'
        WebDriverWait(driver, 100, 0.01).until(EC.element_to_be_clickable((By.XPATH, login_button)))
        driver.find_element_by_xpath(login_button).click()
        import pdb; pdb.set_trace()
        join_now = '//a[contains(@text(), "Join")]'
        # find input field
        login_email_input_field = '//input[@data-componentname="emailAddress"]'
        WebDriverWait(driver, 100, 0.01).until(EC.visibility_of_element_located((By.XPATH, login_email_input_field)))     
        driver.find_element_by_xpath(login_email_input_field).send_keys('liangzijie1437@gmail.com')

        pwd_input_field = '//input[@data-componentname="password"]'
        WebDriverWait(driver, 100, 0.01).until(EC.visibility_of_element_located((By.XPATH, pwd_input_field)))
        driver.find_element_by_xpath(pwd_input_field).send_keys('AAAdddjjj111')
        # login
        login_button = '//form[@id="nike-unite-loginForm"]//input[@value="LOG IN"]'
        driver.find_element_by_xpath(login_button).click()
        import pdb; pdb.set_trace()
