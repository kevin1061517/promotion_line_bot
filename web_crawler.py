from bs4 import BeautifulSoup as bf
import requests

def run():
    t = ''
    url = 'https://www.sportsnet.org.tw/schedule.php'
    rs = requests.session()
    res = rs.get(url)
    soup = bf(res.text, 'html.parser')
    for i in soup.select('.maincontent tr')[1:]:
        t+='{}  \n'.format(i.text.strip())
        if (i.select('td a')):
            t += '報名網址:{}\n'.format(i.select('td a')[0]['href'])
        t+='🏃🏃🏃🏃🏃\n'
    return t

def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = bf(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content
def yahoo_movie():
    url = 'https://movies.yahoo.com.tw/movie_thisweek.html?guccounter=1&guce_referrer=aHR0cHM6Ly9tb3ZpZXMueWFob28uY29tLnR3Lw&guce_referrer_sig=AQAAAIeddc72iLVwqIgS4Gb-SjqupoXFeFl-3ffJ90Y83F-fqYQiUCtA4lOFtWirZQqWexqJTDaRQMajC35ss4y3RG90c3C0vi-EtazGMtt0k3pO6wboGgESRnNu0pVU59bPlKIRRzUHsn4joqFtHDeLdIs8o1GyYluxgQ_bCkSMBrnv'
    rs = requests.session()
    res = rs.get(url)
    soup = bf(res.text, 'html.parser')
    title = [i.text.strip()[:10] for i in soup.select('.release_movie_name a')[::2]]
    rank =  [i.text.strip() for i in soup.select('dt .leveltext span')]
    time = [i.text.strip() for i in soup.select('.release_movie_time')]
    img = [i['src'] for i in soup.select('.gabtn img')[5::]]
    for i in range(10):
        title[i] += '\n{}\n期待度:{} '.format(time[i],rank[i])
    return title,img

#處理kkbox抓來的mp3網址
def process_mp3_url(url):
    res = requests.get(url).json()
    try:
        t = res['data'][0]['mp3_url']
        return t
    except:
        return '音樂版權未授權~'

