# -*- coding: utf-8 -*-
import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import scrapy
import mysql.connector


class YaxinSpider(scrapy.Spider):
    name = 'yaxin'
    allowed_domains = ['yaxin.yunkushop.com/']
    start_urls = ['http://yaxin.yunkushop.com/']

    def parse(self, response):
        print(response.url)
        feature_links = response.xpath('//a[contains(@href, "feature")]/@href').extract()
        if not feature_links:
            print("website changed, please update code. ")
            self.send_email()
        for feature_link in feature_links:
            match = re.findall(r'feature\/[0-9]+', feature_link)
            if not match:
                continue
            url = match[0]
            siid = url.split('/')[1]
            if self.existed_in_db(siid):
                continue
            self.insert_link_to_db(url=url, siid=siid)
            break

    def existed_in_db(self, siid):
        select_query = """select souce_internal_id from test.yaxin where souce_internal_id = "{}"
        """
        conn = mysql.connector.connect(host="127.0.0.1", user="root", passwd="root", db="test")
        cur = conn.cursor()
        cur.execute(select_query.format(siid))
        result = cur.fetchall()
        if result:
            return True
        return False

    def insert_link_to_db(self, url, siid):
        conn = mysql.connector.connect(host="127.0.0.1", user="root", passwd="root", db="test")
        cur = conn.cursor()

        create_time = datetime.now()

        insert_query = """
                    INSERT INTO test.yaxin (souce_internal_id, url_string, create_time, update_time) 
                    VALUES ("{}", "{}", "{}", "{}")
                    """
        query_formated = insert_query.format(siid, url, create_time, create_time)
        cur.execute(query_formated)
        conn.commit()
        conn.close()

    def send_email(self):
        pass
        # sender = 'liangzijie1437@gmail.com'
        # receivers = ['563686452@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        #
        # # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        # message = MIMEText('有更新', 'plain', 'utf-8')
        # message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
        # message['To'] = Header("测试", 'utf-8')  # 接收者
        #
        # subject = '有更新'
        # message['Subject'] = Header(subject, 'utf-8')
        #
        # try:
        #     smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #     smtpObj.ehlo()
        #     smtpObj.login('liangzijie1437@gmail.com', 'gmliang1120')
        #     smtpObj.sendmail(sender, receivers, message.as_string())
        #     smtpObj.close()
        #     print('email sent !!')
        #
        # except smtplib.SMTPException:
        #     print("Error: 无法发送邮件")