from bs4 import BeautifulSoup
import urllib.request as req
from dateutil.parser import parse
import telegram
import requests
import os
from pymongo import MongoClient
import pymongo
import re

today = datetime.datetime.today().strftime('%Y.%m.%d')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# python-telegram-bot==13.14
apiToken = '#your_token'
chatID = '#your_api'
bot = telegram.Bot(token=apiToken)
client = MongoClient('localhost', 27017)
db = client.cau

def md2(stringex):
    str_md2 = stringex.replace('+','\+').replace('!','\!').replace('$','\$').replace("'","\'").replace('.','\.').replace(']','\]').replace('[','\[').replace('-','\-').replace('(','\(').replace(')','\)').replace('~','\~').replace('*','\*').replace('_','\_').replace('=','\=').replace('>','\>').replace('<','\<').replace('}','\}').replace('{','\{')
    return str_md2

final = ""

# url
url = "https://e3home.cau.ac.kr/em/em_1.php"
res = req.urlopen(url)
url_2 = 'https://www.disu.or.kr/community/notice?cidx=44'
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
date = article_list[0].select_one('td.td_datetime').get_text()
latest_2 = article_list_2[0].select_one('.title > a').text 
latest_3 = article_list_3[0].select_one('title').text 



# article_list 

if len(list(db.url_1.find({'title':latest},{'_id':False}))) == 0 and date == str(today):
    title = latest
    doc = {'date':date,'title':title}
    db.url_1.insert_one(doc)
    item = "*\[[e3](https://e3home.cau.ac.kr/em/em_1.php)\]*\n\n" +  md2(title) + "\n\n"
    final += item

# with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
#     before = f_read.readline()
#     if before != latest:
#         title = article_list[0].select_one('td > div > a').get_text()
#         #date = article_list[0].select_one('td.td_datetime').get_text()
#         item = "*\[[e3](https://e3home.cau.ac.kr/em/em_1.php)\]*\n\n" +  md2(title) + "\n\n"
#         final += item
#     f_read.close()

# with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
#     f_write.write(latest)
#     f_write.close()


        
# article_list_2 
if len(list(db.url_2.find({'title':latest_2},{'_id':False}))) == 0:
    title_2 = article_list_2[0].select_one('.title > a')
    title_2_text = title_2.get_text()
    date_2 = str(article_list_2[0].select_one('td.text-center.hidden-xs-down.FS12').get_text().replace('-','.'))
    doc = {'date':date_2,'title':title_2_text}
    db.url_2.insert_one(doc)
    link_2 = 'https://www.disu.or.kr' + str(title_2['href'])
    description_2_soup = str(BeautifulSoup(req.urlopen(link_2), 'html.parser').select_one('#printbody > div > div.fixwidth.bbs_contents')).replace('<br/>','\n').replace('<strong>','').replace('</strong>','').replace('</div>','').replace('<div class="fixwidth bbs_contents">','')
    item_2 = '*\[POLARIS\]* \n\n*[' + md2(title_2_text)+ ']' + '(' + md2(link_2) + ')*\n' + md2(description_2_soup) + '\n'
    final += item_2

# with open(os.path.join(BASE_DIR, 'latest_2.txt'), 'r+') as f_read:
#     before = f_read.readline()
#     if before != latest_2:
#         title_2 = article_list_2[0].select_one('.title > a')
#         title_2_text = title_2.get_text()
#         link_2 = 'https://www.disu.or.kr' + str(title_2['href'])
#         description_2_soup = str(BeautifulSoup(req.urlopen(link_2), 'html.parser').select_one('#printbody > div > div.fixwidth.bbs_contents')).replace('<br/>','\n').replace('<strong>','').replace('</strong>','').replace('</div>','').replace('<div class="fixwidth bbs_contents">','')
#         #date_2 = article_list_2[0].select_one('td.text-center.hidden-xs-down.FS12').get_text().replace('-','.')
#         item_2 = '*\[POLARIS\]* \n\n*[' + md2(title_2_text)+ ']' + '(' + md2(link_2) + ')*\n' + md2(description_2_soup) + '\n'
#         final += item_2
#     f_read.close()

# with open(os.path.join(BASE_DIR, 'latest_2.txt'), 'w+') as f_write:
#     f_write.write(latest_2)
#     f_write.close()



    

# article_list_3    
if len(list(db.url_3.find({'title':latest_3},{'_id':False}))) == 0:
    title_3 = article_list_3[0].select_one('title')
    title_3_text = title_3.get_text()
    author_3 = article_list_3[0].select('author')[0].get_text()
    date_3 = re.sub(r'[^0-9.]','', author_3)
    doc = {'date':date_3,'title':title_3_text}
    db.url_3.insert_one(doc)
    link_3 = str(title_3['href'].replace('=','\=').replace('-','\-'))
    description_3 = article_list_3[0].select_one('description').get_text().replace('&nbsp;','')
    item_3 = '*\[CAU NOTICE\]* \n\n*[' + md2(title_3_text) + ']' + '(' + link_3 + ')*\n' + "\n" + md2(description_3)
    final += item_3

# with open(os.path.join(BASE_DIR, 'latest_3.txt'), 'r+') as f_read:
#     before = f_read.readline()
#     if before != latest_3:
#         title_3 = article_list_3[0].select_one('title')
#         title_3_text = title_3.get_text()
#         link_3 = str(title_3['href'].replace('=','\=').replace('-','\-'))
#         description_3 = article_list_3[0].select_one('description').get_text().replace('&nbsp;','')
#         item_3 = '*\[CAU NOTICE\]* \n\n*[' + md2(title_3_text) + ']' + '(' + link_3 + ')*\n' + "\n" + md2(description_3)
#         final += item_3
#     f_read.close()

# with open(os.path.join(BASE_DIR, 'latest_3.txt'), 'w+') as f_write:
#     f_write.write(latest_3)
#     f_write.close()
        
 
if len(final) != 0:
    bot.sendMessage(chat_id = chatID, text= "\n" + final + "\n", parse_mode = 'MarkdownV2', disable_web_page_preview = True)

exit()