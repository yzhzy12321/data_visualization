from bs4 import BeautifulSoup  
import requests  
import time  
  
headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
}  
  
for i in range(0, 1330, 35):  
    print(i)  
    time.sleep(2)  
    url = 'https://music.163.com/discover/playlist/?cat=华语&order=hot&limit=35&offset=' + str(i)#修改这里即可  
    response = requests.get(url=url, headers=headers)  
    html = response.text  
    soup = BeautifulSoup(html, 'html.parser')  
    # 获取包含歌单详情页网址的标签  
    ids = soup.select('.dec a')  
    # 获取包含歌单索引页信息的标签  
    lis = soup.select('#m-pl-container li')  
    print(len(lis))  
    for j in range(len(lis)):  
        # 获取歌单详情页地址  
        url = ids[j]['href']  
        # 获取歌单标题  
        title = ids[j]['title']  
        # 获取歌单播放量  
        play = lis[j].select('.nb')[0].get_text()  
        # 获取歌单贡献者名字  
        user = lis[j].select('p')[1].select('a')[0].get_text()  
        # 输出歌单索引页信息  
        print(url, title, play, user)  
        # 将信息写入CSV文件中  
        with open('playlist.csv', 'a+', encoding='utf-8-sig') as f:  
            f.write(url + ',' + title + ',' + play + ',' + user + '\n')  
  
from bs4 import BeautifulSoup  
import pandas as pd  
import requests  
import time  
  
df = pd.read_csv('playlist.csv', header=None, error_bad_lines=False, names=['url', 'title', 'play', 'user'])  
  
headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
}  
  
for i in df['url']:  
    time.sleep(2)  
    url = 'https://music.163.com' + i  
    response = requests.get(url=url, headers=headers)  
    html = response.text  
    soup = BeautifulSoup(html, 'html.parser')  
    # 获取歌单标题  
    title = soup.select('h2')[0].get_text().replace(',', '，')  
    # 获取标签  
    tags = []  
    tags_message = soup.select('.u-tag i')  
    for p in tags_message:  
        tags.append(p.get_text())  
    # 对标签进行格式化  
    if len(tags) > 1:  
        tag = '-'.join(tags)  
    else:  
        tag = tags[0]  
    # 获取歌单介绍  
    if soup.select('#album-desc-more'):  
        text = soup.select('#album-desc-more')[0].get_text().replace('\n', '').replace(',', '，')  
    else:  
        text = '无'  
    # 获取歌单收藏量  
    collection = soup.select('#content-operation i')[1].get_text().replace('(', '').replace(')', '')  
    # 歌单播放量  
    play = soup.select('.s-fc6')[0].get_text()  
    # 歌单内歌曲数  
    songs = soup.select('#playlist-track-count')[0].get_text()  
    # 歌单评论数  
    comments = soup.select('#cnt_comment_count')[0].get_text()  
    # 输出歌单详情页信息  
    print(title, tag, text, collection, play, songs, comments)  
    # 将详情页信息写入CSV文件中  
    with open('music_message.csv', 'a+', encoding='utf-8') as f:  
        # f.write(title + '/' + tag + '/' + text + '/' + collection + '/' + play + '/' + songs + '/' + comments + '\n')  
        f.write(title + ',' + tag + ',' + text + ',' + collection + ',' + play + ',' + songs + ',' + comments + '\n')  