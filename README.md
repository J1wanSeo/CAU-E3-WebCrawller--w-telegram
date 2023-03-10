# CAU E3 WebCrawller /w telegram

## Background
 - During School I usually miss the notice that could be helpful at my career. I thought that if there's robot that notice me when new articles come out. 
 - By these needs I made it by python(bs4) and telegram-bot-python.

## Ability
- It crawlles [e3home](https://e3home.cau.ac.kr/em/em_1.php) [Polaris CAU](https://www.disu.or.kr/community/notice?cidx=44) [CAU NOTICE](https://www.cau.ac.kr/cms/FR_PRO_CON/BoardRss.do?pageNo=1&pagePerCnt=15&MENU_ID=100&SITE_NO=2&BOARD_SEQ=4&S_CATE_SEQ=&BOARD_TYPE=C0301&BOARD_CATEGORY_NO=&P_TAB_NO=&TAB_NO=&P_CATE_SEQ=&CATE_SEQ=&SEARCH_FLD=SUBJECT&SEARCH=') every 1 mins by server.
- It checks with latest files
- latest.txt contains title of article which was latest during before run.

## ToDo
- [ ] add another website helpful to achieve higher career.
<<<<<<< HEAD
- [ ] link with MongoDB to substitue latest.txt files.
    - Code Structure:
        - Save date and title if new_title is not located in db
            - How? :  Save whole titles at standard time.
            - Managing Data : Delete it from DB after 2 days from article uploaded.
=======
- [ ] link with MongoDB to substitute latest.txt files.
>>>>>>> 5ec6b5ea88fa6fc4a5ab70f0c953a298346b0b3d
 
## edited 2023-03-08
- deleted parameter flag which delays code
- changed parse_format of telegram-bot to 'MarkdownV2'
- bot automatically gets articles body by entering article's address at POLARIS CAU Notice
- defined function name 'md2' that reconfigure texts in html to adjust it to 'Markdown Grammar'
