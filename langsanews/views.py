from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import html5lib
import re
'''TempExec
import xlwt
from xlwt import Workbook
'''

#============================== langsakota.go.id ==============================# 
lgs_r = requests.get("https://www.langsakota.go.id/")
lgs_soup = BeautifulSoup(lgs_r.content, 'html5lib')

#make some list to save all langsa data
lgs_title = []
lgs_img = []
lgs_link = []
lgs_news = []
lgs_date = []

#make a loop from thr container to scrap the data
lgs = lgs_soup.find_all('div', {'class': 'news-inner-wrap-view news-clearfix'})
for n in lgs: 
    link1 = n.find('a').get('href')
    img1 = n.find('img').get('src')
    title1 = n.find('h3', {'class': 'news-title'}).text
    news1 = n.find('div', {'class': 'news-short-content'}).text.strip()
    temp_date = n.find('div', {'class': 'grid-date-post'}).text.strip()
    date1 = re.sub(r"\s*/\s*News Flash", "", temp_date) #dateregex
    lgs_link.append(link1)
    lgs_img.append(img1)
    lgs_title.append(title1)
    lgs_news.append(news1)
    lgs_date.append(date1)
    

'''#TEMPExec     
wb = Workbook()
sheet1 = wb.add_sheet('lgs_sheet')
sheet1.write(0, 0, 'Bulan')
sheet1.write(1, 0, 'jumlah')
wb.save('berita.xls')
'''


#endoflangsakota.go.id===========================================================

#============================== serambinews ==============================# 
srm_r = requests.get("https://aceh.tribunnews.com/nanggroe/langsa")
srm_soup = BeautifulSoup(srm_r.content, 'html5lib')

#make some list to save all serambi data
srm_title = []
srm_img = []
srm_link = []
srm_news = []
srm_date = []
#make a loop from thr container to scrap the data
srm = srm_soup.find_all('li', {'class': 'p1520 art-list pos_rel'})
for n in srm: 
    link1 = n.find('a').get('href')
    img1 = n.find('img').get('src')
    title1 = n.find('a').get('title')
    news1 = n.find('div', {'class': 'grey2 pt5 f13 ln18'}).text.strip()
    temp_date = n.find('time', {'class': 'foot timeago'}).get('title')
    date1 = re.sub(r"\s.*", "", temp_date).replace('-',' ') #dateregex    
    srm_link.append(link1)
    srm_img.append(img1)
    srm_title.append(title1)
    srm_news.append(news1)
    srm_date.append(date1)
#endofserambinews===============================================================

#============================== kompas.com ======================================# 
kmp_r = requests.get("https://www.kompas.com/tag/Langsa?sort=desc&page=1")
kmp_soup = BeautifulSoup(kmp_r.content, 'html5lib')

#make some list to save all kompas data
kmp_title = []
kmp_img = []
kmp_link = []
kmp_date = []

#make a loop from the container to scrap the data
div = ["col-bs9-6", "col-bs9-3", "article__list clearfix"]
for n in div:
    kmp = kmp_soup.find_all('div', {'class': n})
    for x in kmp:
        link1 = x.find('a').get('href')
        title1 = x.find('a', {'class': 'article__link'}).text
        img1 = x.find('img').get('src')
        temp_date = x.find('div', {'class': 'article__date'}).text
        date1 = re.sub(r",\s.*", "", temp_date).replace('/',' ')    #dateregex
        kmp_link.append(link1)
        kmp_img.append(img1)
        kmp_title.append(title1)
        kmp_date.append(date1)
#endofkompas.com===================================================================


#============================== antaranews.com ==============================# 
ant_r = requests.get("https://aceh.antaranews.com/daerah/kota-langsa")
ant_soup = BeautifulSoup(ant_r.content, 'html5lib')

#make some list to save all antara data
ant_title = []
ant_img = []
ant_link = []
ant_date = []


#make a loop from the container to scrap the data
article = ["news-block big-block", "simple-post simple-big clearfix"]
for n in article:
    ant = ant_soup.find_all('article', {'class': n})
    for x in ant:
        link1 = x.find('a').get('href')
        title1 = x.find('a').get('title')
        img1 = x.find('img').get('src')
        temp_date = x.find('p', {'class': 'simple-share'}).text
        date1temp = re.sub(r".*,\s", "", temp_date)
        date1 = re.sub(r"\s\d*:\d*", "", date1temp)
        ant_link.append(link1)
        ant_img.append(img1)
        ant_title.append(title1)
        ant_date.append(date1)
#endofantaranews.com===============================================================
















#send the variable from python code to index.html
def index(req):

    #zip the data from scrap result
    langsa = zip(lgs_link,lgs_title,lgs_img,lgs_news,lgs_date)    
    kompas = zip(kmp_link,kmp_title,kmp_img,kmp_date)
    antara = zip(ant_link,ant_title,ant_img,ant_date)
    serambi = zip(srm_link,srm_title,srm_img,srm_news,srm_date)    


    return render(req, 'index.html', 
    {'langsa':langsa, 'kompas':kompas, 'antara':antara, 'serambi':serambi})











