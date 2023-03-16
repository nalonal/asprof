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
import requests, random

import undetected_chromedriver as uc 

from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

from collections import OrderedDict

import pandas as pd
import json
from pandas import json_normalize

def tor_requests(url):
        proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
        }
        headers = { 'User-Agent': UserAgent().random }
        with Controller.from_port(port = 9051) as c:
                c.authenticate(password='asprof')
                c.signal(Signal.NEWNYM)
                return requests.get(url, proxies=proxies, headers=headers)

def get_citatied(input_keyword):
        this_keyword = urllib.parse.quote(input_keyword).replace("%20", "+")
        url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+this_keyword
        th = 0
        while True:
                try:
                        response=tor_requests(url)
                        time.sleep(2)
                        soup=BeautifulSoup(response.content,'lxml')
                        soup = soup.select('[data-lid]')[0]
                        break
                except:
                        if(th > 5):
                                print("Scholar Network Error")
                                print(url)
                                return "Error"
                        else:
                                th = th+1
                                pass
        try:
                _ = soup.find_all("div", class_="gs_fl")[1]
        except:
                _ = soup.find_all("div", class_="gs_fl")[0]

        try:
                link = _.find_all("a")[2]
                final_link = link.text
                if final_link.find("Cited by") != -1:
                        final_link = final_link.replace("Cited by ","")
                else:
                        final_link = 0
                return final_link
        except:
                print("Scholar Crawling Element Error")
                return "Error"

class GetOpenAPI(threading.Thread):
        def __init__(self, id):
                self.id = id
                super(GetOpenAPI, self).__init__()
                self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'} 
                self.cr = Crossref()

        def doi_file(self, title):
                try:
                        result = self.cr.works(query = title)
                        doi = result['message']['items'][0]['DOI']
                        year = result['message']['items'][0]['indexed']['date-time'].split("-")[0]
                        BASE_URL = 'http://dx.doi.org/'
                        url = BASE_URL + doi
                        req = urllib.request.Request(url)
                        req.add_header('Accept', 'application/x-bibtex')
                        with urllib.request.urlopen(req) as f:
                                bibtex = f.read().decode()
                        return doi, bibtex, year
                except HTTPError as e:
                        if e.code == 404:
                                return 'DOI not found.', 'file unavailable', 'unknown year' 
                        else:
                                return 'Service unavailable.', 'file unavailable', 'unknown year'

        def request_ai(self, question):
                openai.api_key = ''
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
                # conn.row_factory = sql.Row
                this_keyword = urllib.parse.quote(input_keyword).replace("%20", "+")
                url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+this_keyword+"+%28site%3Adl.acm.org+OR+site%3Aieeexplore.ieee.org+OR+site%3Asciencedirect.com+OR+site%3Alink.springer.com%29&hl=id&as_sdt=0%2C5&as_ylo=2018&as_yhi=2022"
                # response=requests.get(url,headers=self.headers) 
                while True:
                        try:
                                response=tor_requests(url)
                                break
                        except:
                                pass
                time.sleep(1)
                soup=BeautifulSoup(response.content,'lxml')
                if len(soup.select('[data-lid]')) == 0:
                        change_sentence = 'short this sentence "'+input_keyword+'"'
                        response_word = self.request_ai(change_sentence)
                        this_keyword = urllib.parse.quote(response_word).replace("%20", "+") 
                        url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+this_keyword+"+%28site%3Adl.acm.org+OR+site%3Aieeexplore.ieee.org+OR+site%3Asciencedirect.com+OR+site%3Alink.springer.com%29&hl=id&as_sdt=0%2C5&as_ylo=2018&as_yhi=2022"
                        # response=requests.get(url,headers=self.headers)
                        while True:
                                try:
                                        response=tor_requests(url) 
                                        break
                                except:
                                        pass
                        time.sleep(1)
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
                                        VALUES(%s,%s,%s,%s,%s)",[research_id,data_reference['title'],data_reference['link'],data_reference['resume'],data_reference['keyword']])
                                conn.commit()
                        except Exception as e: 
                                pass


        def get_references(self):
                real_question = []
                conn = dbcon()
                cur = conn.cursor()
                # conn.row_factory = sql.Row
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
                # conn.row_factory = sql.Row
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
                    VALUES(%s,%s,%s,%s)",[research_id,"introduction",introduction_result,"finished"])
                conn.commit()

                literature_result = {}
                for _ in research_literature.split("\n"):
                        literature_result[_] = self.request_ai(_)
                literature_result = json.dumps(literature_result)
                # print(literature_result)
                
                cur.execute("INSERT INTO paragraph_tb(research_id, category,paragraph_json,status) \
                    VALUES(%s,%s,%s,%s)",[research_id,"literature",literature_result,"finished"])
                conn.commit()
                methodology_result = {}
                for _ in research_methodology.split("\n"):
                        methodology_result[_] = self.request_ai(_)
                methodology_result = json.dumps(methodology_result)
                # print(literature_result)
                
                cur.execute("INSERT INTO paragraph_tb(research_id, category,paragraph_json,status) \
                    VALUES(%s,%s,%s,%s)",[research_id,"methodology",methodology_result,"finished"])
                conn.commit()

        def get_bibtex(self):
                conn = dbcon()
                cur = conn.cursor()
                # conn.row_factory = sql.Row
                cur.execute("select * from references_tb where research_id="+self.id)
                for _ in cur.fetchall():
                        id = _[0]
                        title = _[3] 
                        doi, bibtex, year = self.doi_file(title)
                        cur.execute('UPDATE references_tb SET doi=%s, bibtex=%s, year=%s,  status=%s WHERE id=%s',[doi, bibtex, year, 'finished',id])
                        conn.commit()

        def run(self):
                self.get_ai()
                self.get_references()
                self.get_bibtex()



class GetLibrary(threading.Thread):
        def __init__(self, id):
                self.id = id
                self.conn = dbcon()
                self.cur = self.conn.cursor()
                self.cr = Crossref()
                
                self.options = uc.ChromeOptions() 
                self.options.add_argument('--headless')
                self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), use_subprocess=True, options=self.options) 
                super(GetLibrary, self).__init__() 

        def doi_file(self, title):
                result = self.cr.works(query = title)
                # result = self.cr.works(query = title)
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

        def get_bibtex(self):
                research_id = self.id
                self.cur.execute("select * from slr_tb where research_id="+research_id)
                for _ in self.cur.fetchall():
                        id = _[0]
                        title = _[3] 
                        doi, bibtex, year = self.doi_file(title)
                        self.cur.execute('UPDATE slr_tb SET bibtex=%s WHERE id=%s',[bibtex,id])
                        self.conn.commit()

        def run(self):
                self.cur.execute("select * from research_slr where id="+self.id)
                data = self.cur.fetchone()
                research_id = self.id
                research_keyword = data[6]
                keyword_search = research_keyword
                self.ieee(keyword_search)
                self.sciencedirect(keyword_search)
                self.acm(keyword_search)
                self.ieee_crawling()
                self.sciencedirect_crawling()
                self.acm_crawling()
                self.get_bibtex()

        def ieee_crawling(self):
                research_id = self.id
                self.cur.execute("select * from slr_tb where research_id="+research_id+" AND source='ieee' AND status IS NULL")
                data_total_process_references = self.cur.fetchall()
                for _ in data_total_process_references:
                        this_id = _[0]
                        self.driver.get(_[3]) 
                        time.sleep(10)
                        try:
                                abstract = self.driver.find_element(By.CLASS_NAME,"abstract-text").text.replace("Abstract:\n","")
                                doi = self.driver.find_element(By.CLASS_NAME,"stats-document-abstract-doi").text.replace("DOI: ","")
                        except:
                                abstract = ""
                                doi = ""
                        strencode = abstract.encode("ascii", "ignore")
                        abstract = strencode.decode()
                        self.cur.execute('UPDATE slr_tb SET abstract=%s, doi=%s, status=%s WHERE id=%s',[abstract, doi, "finished", this_id])
                        self.conn.commit()

        def sciencedirect_crawling(self):
                research_id = self.id
                self.cur.execute("select * from slr_tb where research_id="+research_id+" AND source='Sciencedirect' AND status IS NULL")
                data_total_process_references = self.cur.fetchall()
                for _ in data_total_process_references:
                        this_id = _[0]
                        self.driver.get(_[3])
                        time.sleep(10)
                        try:
                                abstract = self.driver.find_element(By.CLASS_NAME,"abstract").text.replace("Abstract\n","")
                                doi = self.driver.find_element(By.CLASS_NAME,"doi").text.replace("https://doi.org/","")
                        except:
                                abstract = ""
                                doi = ""
                        strencode = abstract.encode("ascii", "ignore")
                        abstract = strencode.decode()
                        self.cur.execute('UPDATE slr_tb SET abstract=%s, doi=%s, status=%s WHERE id=%s',[abstract, doi, "finished", this_id])
                        self.conn.commit()
        
        def acm_crawling(self):
                research_id = self.id
                self.cur.execute("select * from slr_tb where research_id="+research_id+" AND source='ACM Digital Library' AND status IS NULL")
                data_total_process_references = self.cur.fetchall()
                for _ in data_total_process_references:
                        this_id = _[0]
                        self.driver.get(_[3])
                        time.sleep(10)
                        try:
                                abstract = self.driver.find_element(By.CLASS_NAME,"abstractInFull").text
                                authors = self.driver.find_elements(By.CLASS_NAME,"loa__author-name")
                                this_author = [per_authors.text for per_authors in authors]
                                author = "; ".join(this_author)
                        except:
                                abstract = ""
                                author = ""
                        strencode = abstract.encode("ascii", "ignore")
                        abstract = strencode.decode()
                        self.cur.execute('UPDATE slr_tb SET abstract=%s, author=%s, status=%s WHERE id=%s',[abstract, author, "finished", this_id])
                        self.conn.commit()
                
                
        def acm(self, keyword_search):
                research_id = self.id
                temp_acm_search = "(Title:("+keyword_search+"))"
                temp_acm_search = temp_acm_search+" OR "+temp_acm_search.replace("Title","Abstract")+" OR "+temp_acm_search.replace("Title","Keyword")
                acm_search = temp_acm_search.replace('(','%28').replace(":","%3A").replace('"',"%22").replace(" ","+").replace(')','%29')
                url_acm = "https://dl.acm.org/action/doSearch?AllField="+acm_search+"&pageSize=100"
                self.driver.get(url_acm) 
                time.sleep(10)
                try:
                        total_document = self.driver.find_element(By.CLASS_NAME,"hitsLength").text.replace(",","")
                        total_page = math.ceil(int(total_document)/100)
                except:
                        total_document = 0
                        total_page = 0

                for per_page in range(total_page):
                        self.driver.get(url_acm+"&startPage="+str(per_page)) 
                        time.sleep(10)
                        this_element =self.driver.find_elements(By.CLASS_NAME, "search__item")
                        for per_this_element in this_element:
                                output_search = {}
                                title = per_this_element.find_element(By.CLASS_NAME,"issue-item__title").text
                                link = per_this_element.find_element(By.CLASS_NAME,"issue-item__title").find_element(By.TAG_NAME,"a").get_attribute('href')
                                try:
                                        author = per_this_element.find_element(By.CLASS_NAME,"truncate-list").text.replace(",",";")
                                except:
                                        author = "None"
                                try:
                                        event = per_this_element.find_element(By.CLASS_NAME,"issue-item__detail").find_elements(By.TAG_NAME,"span")[0].text
                                except:
                                        event = "None"
                                try:
                                        year = per_this_element.find_element(By.CLASS_NAME,"issue-item__detail").find_elements(By.TAG_NAME,"span")[1].text.split(",")[0].split(" ")[-1]
                                        year = re.sub('[^0-9]','', year)
                                except:
                                        year = "None" 
                                try:
                                        publish_type = per_this_element.find_element(By.CLASS_NAME,"issue-heading").text
                                except:
                                        publish_type = "None"
                                try:
                                        doi = per_this_element.find_element(By.CLASS_NAME,"issue-item__detail").find_elements(By.TAG_NAME,"span")[-1].text.replace("https://doi.org/","")
                                except:
                                        doi = "None"

                                publish_name = event
                                citation = get_citatied(title)
                                self.cur.execute("INSERT INTO slr_tb(research_id, title,link,author,event, year, publish_type, publish_name, source, citation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[research_id,title,link,author,event,year,publish_type, publish_name, "ACM Digital Library",citation])
                                self.conn.commit()


        def sciencedirect(self, keyword_search):
                research_id = self.id
                #sd
                sciencedirect_search = keyword_search.replace("(","%28").replace(" ","%20").replace(")","%29")
                url_sciencedirect = 'https://www.sciencedirect.com/search?tak='+sciencedirect_search+'&show=100&articleTypes=REV%2CFLA&lastSelectedFacet=articleTypes'
                self.driver.get(url_sciencedirect)
                time.sleep(10)
        
                try:
                        total_document = self.driver.find_element(By.CLASS_NAME,"ResultsFound").text.split(" ")[0].replace(",","")
                        total_page = math.ceil(int(total_document)/100)

                except:
                        total_document = 0
                        total_page = 0
  
                for per_page in range(total_page):
                        self.driver.get(url_sciencedirect+"&offset="+str(per_page)) 
                        time.sleep(3)
                        this_element = self.driver.find_elements(By.CLASS_NAME, "ResultItem")
                        for per_this_element in this_element:
                                output_search = {}
                                title = per_this_element.find_element(By.CLASS_NAME,"result-list-title-link").text
                                link = per_this_element.find_element(By.TAG_NAME,"a").get_attribute('href')
                                try:
                                        author = [name_author.text for name_author in per_this_element.find_elements(By.CLASS_NAME,"author")]
                                        author = "; ".join(author)
                                except:
                                        author = "None"
                                try:
                                        event = per_this_element.find_elements(By.CLASS_NAME,"anchor-text")[1].text
                                except:
                                        event = "None"
                                try:
                                        year = per_this_element.find_element(By.CLASS_NAME,"srctitle-date-fields").text.split(" ")[-1]
                                        year = re.sub('[^0-9]','', year)
                                except:
                                        year = "None"
                                try:    
                                        publish_type = per_this_element.find_element(By.CLASS_NAME,"article-type").text
                                except:
                                        publish_type = "None"
                                
                                publish_name = event
                                citation = get_citatied(title)
                                self.cur.execute("INSERT INTO slr_tb(research_id, title,link,author,event, year, publish_type, publish_name, source, citation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[research_id,title,link,author,event,year,publish_type, publish_name, "Sciencedirect", citation])
                                self.conn.commit()



        def ieee(self, keyword_search):
                research_id = self.id
                ieee_keyword_search = "("+keyword_search+")"
                temp_ieee_search = ieee_keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')
                # temp_ieee_search = "("+keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')+")"
                ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
                ieee_search = ieee_search.replace(' ','%20')
                url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL"
                self.driver.get(url_conference)
                time.sleep(10)
                try:
                        total_ieee = self.driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
                        total_document = total_ieee.text.split("of ")[1].split(" ")[0].replace(",","")
                        total_page = math.ceil(int(total_document)/100)
                except:
                        total_document = 0
                        total_page = 0
                document_search = []
                no=1
                for per_page in range(total_page):
                        this_page = per_page+1
                        self.driver.get(url_conference+"&pageNumber="+str(this_page)) 
                        time.sleep(10)
                        this_element =self.driver.find_elements(By.CLASS_NAME, "List-results-items")
                        for per_this_element in this_element:
                                output_search = {}
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
                                citation = get_citatied(title)
                                self.cur.execute("INSERT INTO slr_tb(research_id, title,link,author,event, year, publish_type, publish_name, source, citation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[research_id,title,link,author,event,year,publish_type, publish_name, "IEEE", citation])
                                self.conn.commit()


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
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_title text, research_author text, research_introduction text, research_literature text, research_methodology text, research_keyword text, created_date text, output text, status char(20), research_map text, summary text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS config\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, title text, category text, value text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS paragraph_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, category text, paragraph_json text, status text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS references_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, paragraph_id text, title text, link text, resume text, keyword text, doi text, bibtex text, year text, status text, relevant text);''')

        curr.execute('''CREATE TABLE IF NOT EXISTS slr_tb\
                (id INTEGER PRIMARY KEY AUTO_INCREMENT, research_id text, title text, link text, author text, event text, year text, publish_type text, publish_name text, doi text, abstract text, source text, status text, relevant text, bibtex text, resume text, keyword text, citation text);''')

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


# cors = CORS(app, resources={r"/*": {"origins": "*"}})
#https://pypi.org/project/bcrypt/ -> bcrypt documentation
