from bs4 import BeautifulSoup
import urllib.request as req
from dateutil.parser import parse
import telegram
import requests
import datetime
import os
# from pymongo import MongoClient
# import pymongo
import re
import psycopg2

today = datetime.datetime.today().strftime('%Y.%m.%d')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# python-telegram-bot==13.14
apiToken = '#your_token'
chatID = '#your_api'
bot = telegram.Bot(token=apiToken)
# client = MongoClient('localhost', 27017)
# db = client.cau
conn = psycopg2.connect(host="localhost", dbname="cau-e3", user="cau-python", password="cau-python", port="5433")
cur = conn.cursor()

def md2(stringex):
    str_md2 = stringex.replace('#','\#').replace('+','\+').replace('!','\!').replace('$','\$').replace("'","\'").replace('.','\.').replace(']','\]').replace('[','\[').replace('-','\-').replace('(','\(').replace(')','\)').replace('~','\~').replace('*','\*').replace('_','\_').replace('=','\=').replace('>','\>').replace('<','\<').replace('}','\}').replace('{','\{')
    return str_md2

final = ""

try:
    # url
    url = "https://e3home.cau.ac.kr/em/em_1.php"
    res = req.urlopen(url)
    url_2 = 'https://www.disu.or.kr/community/notice'
    res_2 = req.urlopen(url_2)
    url_3 = 'https://www.cau.ac.kr/cms/FR_PRO_CON/BoardRss.do?pageNo=1&pagePerCnt=15&MENU_ID=100&SITE_NO=2&BOARD_SEQ=4&S_CATE_SEQ=&BOARD_TYPE=C0301&BOARD_CATEGORY_NO=&P_TAB_NO=&TAB_NO=&P_CATE_SEQ=&CATE_SEQ=&SEARCH_FLD=SUBJECT&SEARCH='
    res_3 = requests.get(url_3)

    # html deparsing
    soup = BeautifulSoup(res, 'html.parser')
    soup_2 = BeautifulSoup(res_2, 'html.parser')
    soup_3 = BeautifulSoup(res_3.text, 'lxml-xml')


    # extraction
    article_list = soup.select("tbody > tr")
    article_list_2 = soup_2.select("#zcmsprogram > div > table > tbody > tr")
    article_list_3 = soup_3.select("item")


    latest = article_list[0].select_one('td > div > a').text
    latest_2 = article_list_2[0].select_one('.title > a').text 
    latest_3 = article_list_3[0].select_one('title').text 


    date = article_list[0].select_one('td.td_datetime').get_text()
    date_2 = str(article_list_2[0].select_one('td.text-center.hidden-xs-down.FS12').get_text().replace('-','.'))
    

    sql_1 = "SELECT title FROM URL_ONE WHERE title = %s"
    sql_2 = "SELECT title FROM URL_TWO WHERE title = %s"
    sql_3 = "SELECT title FROM URL_THREE WHERE title = %s"

    cur.execute(sql_1, (latest,))
    result = cur.fetchall()

    if len(result) == 0 and date == str(today):
        title = latest
        # doc = {'date':date,'title':title}
        # db.url_1.insert_one(doc)

        cur.execute("INSERT INTO URL_ONE (date,title) VALUES (%s, %s);", (date, title))
        conn.commit()
        item = "*\[[e3](https://e3home.cau.ac.kr/em/em_1.php)\]*\n\n" +  md2(title) + "\n\n"
        final += item

    cur.execute(sql_2, (latest_2,))
    result = cur.fetchall()

    if len(result) == 0 and date_2 == str(today) :
        title_2 = article_list_2[0].select_one('.title > a')
        title_2_text = title_2.get_text()
        
        # doc = {'date':date_2,'title':title_2_text}
        # db.url_2.insert_one(doc)
        cur.execute("INSERT INTO URL_TWO (date,title) VALUES (%s, %s);", (date_2, title_2_text))
        conn.commit()
        link_2 = 'https://www.disu.or.kr' + str(title_2['href'])
        description_2_soup = str(BeautifulSoup(req.urlopen(link_2), 'html.parser').select_one('#printbody > div > div.fixwidth.bbs_contents')).replace('<br/>','\n').replace('<strong>','').replace('</strong>','').replace('</div>','').replace('<div class="fixwidth bbs_contents">','')
        item_2 = '*\[POLARIS\]* \n\n*[' + md2(title_2_text)+ ']' + '(' + md2(link_2) + ')*\n' + md2(description_2_soup) + '\n'
        final += item_2

    cur.execute(sql_3, (latest_3,))
    result = cur.fetchall()

    if len(result) == 0:
        title_3 = article_list_3[0].select_one('title')
        title_3_text = title_3.get_text()
        author_3 = article_list_3[0].select('author')[0].get_text()
        date_3 = re.sub(r'[^0-9.]','', author_3)
        doc = {'date':date_3,'title':title_3_text}
        # db.url_3.insert_one(doc)
        cur.execute("INSERT INTO URL_THREE (date,title) VALUES (%s, %s);", (date_3, title_3_text))
        conn.commit()
        link_3 = str(title_3['href'].replace('=','\=').replace('-','\-'))
        description_3 = article_list_3[0].select_one('description').get_text().replace('&nbsp;','')
        item_3 = '*\[CAU NOTICE\]* \n\n*[' + md2(title_3_text) + ']' + '(' + link_3 + ')*\n' + "\n" + md2(description_3)
        final += item_3

   
    
    if len(final) != 0:
        bot.sendMessage(chat_id = chatID, text= "\n" + final + "\n", parse_mode = 'MarkdownV2', disable_web_page_preview = True)

    exit()
except Exception as e:
    bot.sendMessage(chat_id = yourPrivateID, text= "**Script 실행 중 Error 발생** \n", parse_mode = 'MarkdownV2', disable_web_page_preview = True)
    exit()