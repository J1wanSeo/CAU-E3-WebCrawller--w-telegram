from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
import telegram
import requests
import os
import re
import psycopg2

today = datetime.datetime.today().strftime('%Y.%m.%d')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# python-telegram-bot 13.14 사용
apiToken = '#your_token'
chatID = '#your_api'
bot = telegram.Bot(token=apiToken)


def md2(stringex):
    str_md2 = stringex.replace('#','\#').replace('+','\+').replace('!','\!').replace('$','\$').replace("'","\'").replace('.','\.').replace(']','\]').replace('[','\[').replace('-','\-').replace('(','\(').replace(')','\)').replace('~','\~').replace('*','\*').replace('_','\_').replace('=','\=').replace('>','\>').replace('<','\<').replace('}','\}').replace('{','\{')
    return str_md2

final = ""
item = ""

try:
    # 분석하려는 주소
    url = "https://e3home.cau.ac.kr/em/em_1.php"
    res = requests.get(url)
    
    if res.status_code == 200:
        conn = psycopg2.connect(host="localhost", dbname="your_db", user="your_id", password="your_passwd", port="your_port")
        cur = conn.cursor()
        soup = BeautifulSoup(res.text, 'html.parser')
        article_lists = soup.select("tbody")
        sql_1 = "SELECT title FROM URL_ONE WHERE title = %s"
        for article_list in article_lists:
            detail = ""
            latest = article_list.select_one('td > div > a')
            date = article_list.select_one('td.td_datetime').get_text()
            cur.execute(sql_1, (latest.text,))
            result_1 = cur.fetchall()

            if len(result_1) == 0  and date == str(today):
                title = latest.text
                date = article_list.select_one('td.td_datetime').get_text()
                cur.execute("INSERT INTO URL_ONE (date,title) VALUES (%s, %s);", (date, title))
                conn.commit()
                num = re.sub(r'[^0-9]','', latest['href'])
                #javscript:view 내용 추출
                payload = {'p_idx': num, 'p_page': '1', 'code': 'b_1', 'p_mode': 'view', 'p_pgfile': '/em/em_1.php'}
                with requests.Session() as s:
                    req_1 = s.post('https://e3home.cau.ac.kr/em/em_1.php', data=payload)
                    soup_des = BeautifulSoup(req_1.text,"html.parser")
                    descriptions = soup_des.select('#em_w_con1')
                    for description in descriptions:
                        detail += description.get_text()
                item = md2(title) + "\n" + md2(detail) + "\n"

        if len(item) != 0:
            final += "*\[[e3](https://e3home.cau.ac.kr/em/em_1.php)\]*\n\n" +  item
    else:
        bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 E3Home 응답 안함**" + str(res.status_code) , parse_mode = 'MarkdownV2', disable_web_page_preview = True)

except Exception as e:
    bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 Error 발생** \n\n" + md2(str(e)), parse_mode = 'MarkdownV2', disable_web_page_preview = True)

try:
    url_2 = 'https://www.disu.or.kr/community/notice'
    res_2 = requests.get(url_2)

    if res_2.status_code == 200:
        conn_2 = psycopg2.connect(host="localhost", dbname="your_db", user="your_id", password="your_passwd", port="your_port")
        cur_2 = conn_2.cursor()
        soup_2 = BeautifulSoup(res_2.text, 'html.parser')
        article_list_2 = soup_2.select("#zcmsprogram > div > table > tbody > tr")
        latest_2 = article_list_2[0].select_one('.title > a').text
        date_2 = str(article_list_2[0].select_one('td.text-center.hidden-xs-down.FS12').get_text().replace('-','.'))
        sql_2 = "SELECT title FROM URL_TWO WHERE title = %s"
        cur_2.execute(sql_2, (latest_2,))
        result_2 = cur_2.fetchall()
        if len(result_2) == 0 and date_2 == str(today) :
            title_2 = article_list_2[0].select_one('.title > a')
            title_2_text = title_2.get_text()
            
            # doc = {'date':date_2,'title':title_2_text}
            # db.url_2.insert_one(doc)
            cur_2.execute("INSERT INTO URL_TWO (date,title) VALUES (%s, %s);", (date_2, title_2_text))
            conn_2.commit()
            link_2 = 'https://www.disu.or.kr' + str(title_2['href'])
            description_2_soup = str(BeautifulSoup(req.urlopen(link_2), 'html.parser').select_one('#printbody > div > div.fixwidth.bbs_contents')).replace('<br/>','\n').replace('<strong>','').replace('</strong>','').replace('</div>','').replace('<div class="fixwidth bbs_contents">','')
            item_2 = '*\[POLARIS\]* \n\n*[' + md2(title_2_text)+ ']' + '(' + md2(link_2) + ')*\n' + md2(description_2_soup) + '\n'
            final += item_2
    else:
        bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 POLARIS 응답 안함**" + str(res_2.status_code) , parse_mode = 'MarkdownV2', disable_web_page_preview = True)
except Exception as e:
    bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 Error 발생** \n\n" + md2(str(e)), parse_mode = 'MarkdownV2', disable_web_page_preview = True)

try:
    url_3 = 'https://www.cau.ac.kr/cms/FR_PRO_CON/BoardRss.do?pageNo=1&pagePerCnt=15&MENU_ID=100&SITE_NO=2&BOARD_SEQ=4&S_CATE_SEQ=&BOARD_TYPE=C0301&BOARD_CATEGORY_NO=&P_TAB_NO=&TAB_NO=&P_CATE_SEQ=&CATE_SEQ=&SEARCH_FLD=SUBJECT&SEARCH='
    res_3 = requests.get(url_3)

    if res_3.status_code == 200:
        conn_3 = psycopg2.connect(host="localhost", dbname="your_db", user="your_id", password="your_passwd", port="your_port")
        cur_3 = conn_3.cursor()
        soup_3 = BeautifulSoup(res_3.text, 'lxml-xml')
        article_list_3 = soup_3.select("item")
        latest_3 = article_list_3[0].select_one('title').text 
        sql_3 = "SELECT title FROM URL_THREE WHERE title = %s"
        cur_3.execute(sql_3, (latest_3,))
        result_3 = cur_3.fetchall()
        if len(result_3) == 0:
            title_3 = article_list_3[0].select_one('title')
            title_3_text = title_3.get_text()
            author_3 = article_list_3[0].select('author')[0].get_text()
            date_3 = re.sub(r'[^0-9.]','', author_3)
            doc = {'date':date_3,'title':title_3_text}
            # db.url_3.insert_one(doc)
            cur_3.execute("INSERT INTO URL_THREE (date,title) VALUES (%s, %s);", (date_3, title_3_text))
            conn_3.commit()
            link_3 = str(title_3['href'])
            description_3 = article_list_3[0].select_one('description').get_text().replace('&nbsp;','')
            description_3_image = BeautifulSoup(req.urlopen(link_3), 'html.parser').select_one('div > dl > dd > p > p > img')
            if description_3_image == None:
                item_3 = '*\[CAU NOTICE\]* \n\n*[' + md2(title_3_text) + ']' + '(' + md2(link_3) + ')*\n' + "\n" + md2(description_3)
            else:
                des_3_img_src = str(description_3_image['src'])
                item_3 = '*\[CAU NOTICE\]* \n\n*[' + md2(title_3_text) + ']' + '(' + md2(link_3) + ')*\n' + "\n" + '[ ]('+ md2(des_3_img_src) + ')\n' + md2(description_3)
            
            final += item_3
    else:
        bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 CAU Notice 응답 안함**"+ str(res_3.status_code) , parse_mode = 'MarkdownV2', disable_web_page_preview = True)
except Exception as e:
    bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 Error 발생** \n\n" + md2(str(e)), parse_mode = 'MarkdownV2', disable_web_page_preview = True)

try:
    url_4 = 'https://www.idec.or.kr/edu/apply/list/?&category=&type=list'
    res_4 = requests.get(url_4)
    if res_4.status_code == 200:
        conn_4 = psycopg2.connect(host="localhost", dbname="your_db", user="your_id", password="your_passwd", port="your_port")
        cur_4 = conn_4.cursor()
        item_4 = ""
        sql_4 = "SELECT title FROM URL_4 WHERE title = %s"
        soup_4 = BeautifulSoup(res_4.text, 'html.parser')
        article_list_4 = soup_4.select(".hand")
        latest_4 = article_list_4[0].select_one(".left > b").text
        cur_4.execute(sql_4, (latest_4,))
        result_4 = cur_4.fetchall()
        if len(result_4) == 0:
            article_4 = article_list_4[0]
            if article_4.select_one(".left > b") is not None:
                title_4 = article_4.select_one(".left > b").get_text().strip()
                where_4 = article_4.select_one(".bold").get_text().strip()
                when_4 = article_4.select(".bold")[2].get_text().strip()
                link_4 = article_4['onclick'].replace("location.href='",'https://www.idec.or.kr').replace("';",'')
                description_4 = '교육장소: ' + where_4 + '\n' + '신청기간: ' + when_4 + "\n" 
                cur_4.execute("INSERT INTO URL_4 (date,title) VALUES (%s, %s);", (today, latest_4))
                conn_4.commit()
                item_4 = '*\[반도체설계교육센터\]* \n\n*[' + md2(title_4) + ']' + '(' + md2(str(link_4)) + ')*\n' + "\n" + md2(description_4)
                final += item_4

except Exception as e:
    bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 Error 발생** \n\n" + md2(str(e)), parse_mode = 'MarkdownV2', disable_web_page_preview = True)
    
try:
    url_5 = 'https://abeek.cau.ac.kr/notice/list.jsp'
    res_5 = requests.get(url_5)
    if res_5.status_code == 200:
        conn_5 = psycopg2.connect(host="localhost", dbname="your_db", user="your_id", password="your_passwd", port="your_port")
        cur_5 = conn_5.cursor()
        item_5 = ""
        sql_5 = "SELECT title FROM URL_5 WHERE title = %s"
        soup_5 = BeautifulSoup(res_5.text, 'html.parser')
        article_list_5 = soup_5.select("tbody > tr > td.left > a")
        latest_5 = article_list_5[0].text
        cur_5.execute(sql_5, (latest_5,))
        result_5 = cur_5.fetchall()
        if len(result_5) == 0:
            article_5 = article_list_5[0]
            if article_5 is not None:
                title_5 = article_5.get_text().strip()
                seq_5 = article_list_5[0]['seq']
                link_5 = 'https://abeek.cau.ac.kr/notice/view.jsp?sc_board_seq=1&pk_seq=' + seq_5
                description_5 = BeautifulSoup(req.urlopen(link_5), 'html.parser').select_one('#bulletinContentLayer').get_text().replace('&nbsp',' ')
                cur_5.execute("INSERT INTO URL_5 (date,title) VALUES (%s, %s);", (today, latest_5))
                conn_5.commit()
                item_5 = '*\[공학교육혁신센터\]* \n\n*[' + md2(title_5) + ']' + '(' + md2(str(link_5)) + ')*\n' + "\n" + md2(description_5)
                final += item_5

except Exception as e:
    bot.sendMessage(chat_id = chatID, text= "**Script 실행 중 Error 발생** \n\n" + md2(str(e)), parse_mode = 'MarkdownV2', disable_web_page_preview = True)
    
if len(final) != 0:
    bot.sendMessage(chat_id = chatID, text= "\n" + final + "\n", parse_mode = 'MarkdownV2')

exit()
