import os, pymongo, json, bcrypt
from flask import Flask, render_template, url_for, redirect, Response, request, jsonify
import config.setup as setup
import config.database as crud
from datetime import datetime
from pyfiglet import Figlet
from flask_cors import CORS, cross_origin
# import sqlite3 as sql
import mysql.connector
import threading
import openai
from bs4 import BeautifulSoup 
import urllib.parse
import requests 
import math, time
from flask import Flask, render_template,session,request,redirect,url_for,flash,send_from_directory,Response           
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor

import sys
import urllib.request
from urllib.error import HTTPError
from habanero import Crossref

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse,requests,time
import re

import undetected_chromedriver as uc 

class GetOpenAPI(threading.Thread):
        def __init__(self, id):
                self.id = id
                super(GetOpenAPI, self).__init__()
                self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'} 
                self.cr = Crossref()

        def doi_file(self, title):
                result = self.cr.works(query = title)
                doi = result['message']['items'][0]['DOI']
                year = result['message']['items'][0]['indexed']['date-time'].split("-")[0]
                BASE_URL = 'http://dx.doi.org/'
                url = BASE_URL + doi
                req = urllib.request.Request(url)
                req.add_header('Accept', 'application/x-bibtex')
                try:
                        with urllib.request.urlopen(req) as f:
                                bibtex = f.read().decode()
                        return doi, bibtex, year
                except HTTPError as e:
                        if e.code == 404:
                                return 'DOI not found.', 'file unavailable', 'unknown year' 
                        else:
                                return 'Service unavailable.', 'file unavailable', 'unknown year'

        def request_ai(self, question):
                openai.api_key = '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'
                response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=question,
                        temperature=0.9,
                        max_tokens=150,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        stop=[" Human:", " AI:"]
                )
                return response['choices'][0]['text'].replace("\n\n","") 
        def looking_scholar(self,input_keyword):
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                this_keyword = urllib.parse.quote(input_keyword).replace("%20", "+")
                url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+this_keyword+"+%28site%3Adl.acm.org+OR+site%3Aieeexplore.ieee.org+OR+site%3Asciencedirect.com+OR+site%3Alink.springer.com%29&hl=id&as_sdt=0%2C5&as_ylo=2018&as_yhi=2022"
                response=requests.get(url,headers=self.headers) 
                soup=BeautifulSoup(response.content,'lxml')
                if len(soup.select('[data-lid]')) == 0:
                        change_sentence = 'short this sentence "'+input_keyword+'"'
                        response_word = self.request_ai(change_sentence)
                        this_keyword = urllib.parse.quote(response_word).replace("%20", "+") 
                        url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+this_keyword+"+%28site%3Adl.acm.org+OR+site%3Aieeexplore.ieee.org+OR+site%3Asciencedirect.com+OR+site%3Alink.springer.com%29&hl=id&as_sdt=0%2C5&as_ylo=2018&as_yhi=2022"
                        response=requests.get(url,headers=self.headers) 
                        soup=BeautifulSoup(response.content,'lxml')

                for item in soup.select('[data-lid]'): 
                        try: 
                                data_reference = {}
                                research_id = self.id
                                data_reference['title'] = item.select('h3')[0].get_text()
                                data_reference['link'] = item.select('a')[0]['href']
                                data_reference['resume'] = item.select('.gs_rs')[0].get_text()
                                data_reference['keyword'] = input_keyword
                                cur.execute("INSERT INTO references_tb(research_id, title, link, resume, keyword) \
                                        VALUES(?,?,?,?,?)",[research_id,data_reference['title'],data_reference['link'],data_reference['resume'],data_reference['keyword']])
                                conn.commit()
                        except Exception as e: 
                                pass


        def get_references(self):
                real_question = []
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                research_id = self.id
                cur.execute("select paragraph_json from paragraph_tb where research_id="+research_id+" AND category='introduction'")
                data_introduction = cur.fetchone()
                data_introduction = json.loads(data_introduction[0])
                for key,value in data_introduction.items():
                        add_real_question = value.split(".")[0]
                        if(len(add_real_question.split(" ")) > 3):
                                real_question.append(add_real_question)
                
                cur.execute("select paragraph_json from paragraph_tb where research_id="+research_id+" AND category='literature'")
                data_literature = cur.fetchone()
                data_literature = json.loads(data_literature[0])
                for key,value in data_literature.items():
                        add_real_question = value.split(".")[0]
                        if(len(add_real_question.split(" ")) > 3):
                                real_question.append(add_real_question)
                
                cur.execute("select paragraph_json from paragraph_tb where research_id="+research_id+" AND category='methodology'")
                data_methodology = cur.fetchone()
                data_methodology = json.loads(data_methodology[0])
                for key,value in data_methodology.items():
                        add_real_question = value.split(".")[0]
                        if(len(add_real_question.split(" ")) > 3):
                                real_question.append(add_real_question)

                for _ in real_question:
                        self.looking_scholar(_)

        def get_ai(self):
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                cur.execute("select * from research_slr where id="+self.id)
                data = cur.fetchone()
                research_id = self.id
                research_introduction = data[3]
                research_literature = data[4]
                research_methodology = data[5]

                # # id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, category text, paragraph_json text, status text
                introduction_result = {}
                for _ in research_introduction.split("\n"):
                        introduction_result[_] = self.request_ai(_)
                introduction_result = json.dumps(introduction_result)
                # print(introduction_result)

                cur.execute("INSERT INTO paragraph_tb(research_id, category,paragraph_json,status) \
                    VALUES(?,?,?,?)",[research_id,"introduction",introduction_result,"finished"])
                conn.commit()

                literature_result = {}
                for _ in research_literature.split("\n"):
                        literature_result[_] = self.request_ai(_)
                literature_result = json.dumps(literature_result)
                # print(literature_result)
                
                cur.execute("INSERT INTO paragraph_tb(research_id, category,paragraph_json,status) \
                    VALUES(?,?,?,?)",[research_id,"literature",literature_result,"finished"])
                conn.commit()
                methodology_result = {}
                for _ in research_methodology.split("\n"):
                        methodology_result[_] = self.request_ai(_)
                methodology_result = json.dumps(methodology_result)
                # print(literature_result)
                
                cur.execute("INSERT INTO paragraph_tb(research_id, category,paragraph_json,status) \
                    VALUES(?,?,?,?)",[research_id,"methodology",methodology_result,"finished"])
                conn.commit()

        def get_bibtex(self):
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                cur.execute("select * from references_tb where research_id="+self.id)
                for _ in cur.fetchall():
                        id = _[0]
                        title = _[3] 
                        doi, bibtex, year = self.doi_file(title)
                        cur.execute('UPDATE references_tb SET doi=?, bibtex=?, year=?,  status=? WHERE id=?',[doi, bibtex, year, 'finished',id])
                        conn.commit()

        def run(self):
                self.get_ai()
                self.get_references()
                self.get_bibtex()

class GetLibrary(threading.Thread):
        def __init__(self, id):
                self.id = id
                super(GetLibrary, self).__init__() 

        def encode(self,string):
                this_string = string
                decode_string = ['+']
                encode_string = [' ']
                for e_string, d_string in zip(encode_string, decode_string):
                        this_string = this_string.replace(e_string, d_string)
                for e_string, d_string in zip(encode_string[::-1], decode_string[::-1]):
                        this_string = this_string.replace(e_string, d_string)

        def ieee(self,keyword_search,driver):
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                research_id = self.id

                temp_ieee_search = "("+keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')+")"
                ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
                ieee_search.replace(" ","%20")
                url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL"
                driver.get(url_conference) 

                th = 0
                while True:
                        try:
                                total = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]")))
                                break
                        except:
                                if(th > 3):
                                        break
                                else:
                                        pass
                try:
                        total_document = total.text.split("of ")[1].split(" ")[0].replace(",","")
                        total_page = math.ceil(int(total_document)/100)
                except:
                        total_document = 0
                        total_page = 0

                document_search = []
                no=1
                for per_page in range(total_page):
                        this_page = per_page+1
                        driver.get(url_conference+"&pageNumber="+str(this_page)) 
                        th = 0                        
                        while True:
                                try:
                                        this_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "List-results-items")))
                                        this_element = driver.find_elements(By.CLASS_NAME, "List-results-items")
                                        break
                                except:
                                        if(th > 3):
                                                break
                                        else:
                                                th = th+1
                                                pass
                                        
                        for per_this_element in this_element:
                                output_search = {}
                                try:
                                        title = per_this_element.find_elements(By.CLASS_NAME,"text-md-md-lh")[0].text
                                        link = per_this_element.find_elements(By.CLASS_NAME,"text-md-md-lh")[0].find_element(By.TAG_NAME,"a").get_attribute('href')
                                        try:
                                                author = per_this_element.find_element(By.CLASS_NAME,"author").text.replace("\n"," ")
                                        except:
                                                author = "None"     
                                        try:
                                                event = per_this_element.find_element(By.CLASS_NAME,"description").find_element(By.TAG_NAME,"a").text
                                        except:
                                                event = "None"
                                        try:
                                                description = per_this_element.find_element(By.CLASS_NAME,"publisher-info-container").text
                                                year = description.split(" | ")[0].replace("Year: ","")
                                                year = re.sub('[^0-9]','', year)
                                                publish_type = description.split(" | ")[1]
                                                publish_name = description.split(" | ")[2].replace("Publisher: ","")
                                        except:
                                                description = "None" 
                                                year = "None"
                                                publish_type = "None"
                                                publish_name = "None"
                                        output_search['title'] = title
                                        output_search['link'] = link
                                        output_search['author'] = author 
                                        output_search['event'] = event 
                                        output_search['year'] = year 
                                        output_search['publish_type'] = publish_type 
                                        output_search['publish_name'] = publish_name 
                                        output_search['source'] = "IEEE"
                                        # print(output_search) 
                                        cur.execute("INSERT INTO slr_tb(research_id, title,link,author,event, year, publish_type, publish_name, source) VALUES(?,?,?,?,?,?,?,?,?)",[research_id,title,link,author,event,year,publish_type, publish_name, "IEEE"])
                                        conn.commit()
                                except:
                                        pass
                                no=no+1

       
        def run(self):
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_experimental_option("detach", True)
                driver = webdriver.Chrome(options=chrome_options)
                conn = dbcon()
                cur = conn.cursor()
                conn.row_factory = sql.Row
                cur.execute("select * from research_slr where id="+self.id)
                data = cur.fetchone()
                research_id = self.id
                research_keyword = data[6]
                keyword_search = research_keyword
                self.ieee(keyword_search, driver)
                print("finished")
                # print(research_keyword)



class GetLibraryTest(threading.Thread):
        def __init__(self, input_keyword):
                self.input_keyword = input_keyword
                super(GetLibraryTest, self).__init__() 
       
        def run(self):
                options = uc.ChromeOptions() 
                options.headless = True 
                # driver = uc.Chrome(service=Service(ChromeDriverManager().install()), use_subprocess=True, options=options)
                driver = uc.Chrome(use_subprocess=True, options=options) 
                keyword_search = self.input_keyword

                #ieee
                temp_ieee_search = "("+keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')+")"
                ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
                ieee_search = ieee_search.replace(' ','%20')
                url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL"
                # driver.get(url_conference)
                
                # total = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]")))
                # total_document = total.text.split("of ")[1].split(" ")[0].replace(",","")

                # print(url_conference)
                # print(driver.page_source)
                # th = 0 
                # while True:
                #         try: 
                #                 driver.get(url_conference)
                #                 time.sleep(20)
                #                 total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
                #                 print(total_ieee)
                #                 break
                #         except:
                #                 if(th < 3):
                #                         th=th+1
                #                         pass
                #                 else:
                #                         total_ieee = False
                #                         break

                # if(total_ieee != False):
                #         print(total_ieee)
                # else:
                #         print("Load Page Error")
                        
                driver.get(url_conference)
                # time.sleep(20)
                total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
                print(total_ieee)

                # time.sleep(10)
                # total = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')))
                # total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')

                # print(total.text)
                # with open('text2.html', 'w') as f:
                #         f.write(url_conference)

                # ### cloudfare bypass ####
                # print("reset driver")
                # handle = driver.current_window_handle
                # driver.service.stop()
                # time.sleep(6)
                # # driver = uc.Chrome(options=options) 
                # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                # driver.switch_to.window(handle)
                # print(driver.page_source)



                # driver.maximize_window()  
                # time.sleep(10)
                # print(driver.page_source)
                # driver.save_screenshot("ieee2.png") 
                # th = 0
                # while True:
                #         try:
                #                 total = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]")))
                #                 break
                #         except:
                #                 if(th > 3):
                #                         break
                #                 else:
                #                         print("error 2")
                #                         th = th+1
                #                         pass
                # try:
                #         total_document = total.text.split("of ")[1].split(" ")[0].replace(",","")
                #         # total_page = math.ceil(int(total_document)/100)
                # except:
                #         total_document = 0
                #         # total_page = 0

                # print(total_document)

                # conn = dbcon()
                # cur = conn.cursor()
                # conn.row_factory = sql.Row
                # cur.execute("select * from research_slr where id="+self.id)
                # data = cur.fetchone()
                # research_id = self.id
                # research_keyword = data[6]
                # keyword_search = research_keyword
                # self.ieee(keyword_search, driver)
                # print("finished")
                # print(research_keyword)


def copyright():
	print(Figlet(font='slant').renderText(setup.TEXT_WELCOME))

client = pymongo.MongoClient(setup.PATH_MONGODB)
db= client[setup.DB_NAME]

app = Flask(__name__, template_folder='web', static_folder='web')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 600
# app.config['CKEDITOR_EXTRA_PLUGINS'] = ['youtube']

ckeditor = CKEditor(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

def dbcon():
        # conn = sql.connect("database/asprof.db")
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="2wsx@WSX1qazZAQ!",
                port=13306
        )
        curr = conn.cursor()
        curr.execute("CREATE DATABASE IF NOT EXISTS asprof_db")
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="2wsx@WSX1qazZAQ!",
                port=13306,
                database = "asprof_db"
        )
        curr = conn.cursor()
        curr.execute('''CREATE TABLE IF NOT EXISTS research_slr\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_title text, research_author text, research_introduction text, research_literature text, research_methodology text, research_keyword text, created_date text, output text, status char(20), research_map text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS config\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, title text, category text, value text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS paragraph_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, category text, paragraph_json text, status text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS references_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, paragraph_id text, title text, link text, resume text, keyword text, doi text, bibtex text, year text, status text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS slr_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, title text, link text, author text, event text, year text, publish_type text, publish_name text, doi text, abstract text, source text, status text);''')

        config_data = [
                ('FACEBOOK_SESSION', 'facebook','','FACEBOOK_SESSION', 'facebook'),
                ('OPENGPT_SESSION_1', 'openai','','OPENGPT_SESSION_1', 'openai'),
                ('OPENGPT_SESSION_2', 'openai','','OPENGPT_SESSION_2', 'openai'),
                ('OPENGPT_SESSION_3', 'openai','','OPENGPT_SESSION_3', 'openai'),
                ('OPENGPT_SESSION_4', 'openai','','OPENGPT_SESSION_4', 'openai'),
                ]
        curr.executemany("INSERT INTO config(title,category,value) \
                    SELECT %s,%s,%s WHERE NOT EXISTS(SELECT 1 FROM config WHERE title = %s AND category = %s)",config_data)
	
        conn.commit()
        return conn



#Create table research_slr_


# cors = CORS(app, resources={r"/*": {"origins": "*"}})
#https://pypi.org/project/bcrypt/ -> bcrypt documentation
