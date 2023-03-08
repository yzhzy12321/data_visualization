import wordcloud  
import pandas as pd  
import numpy as np  
from PIL import Image  
data = pd.read_excel('music_message.xlsx',names=['url', 'title', 'play', 'user'])  
#根据播放量排序，只取前五十个  
data = data.sort_values('play',ascending=False).head(50)  
  
#font_path指明用什么样的字体风格，这里用的是电脑上都有的微软雅黑  
w1 = wordcloud.WordCloud(width=1000,height=700,  
                         background_color='black',  
                         font_path='msyh.ttc')  
print(data['title'])
words=[i for i in data['title'].to_dict().keys()]
print(words)
txt=''
for i in words:
    for j in range(2):
        txt+=i[j]
    txt+='\n'

# txt = "\n".join(i for i in words)
print(txt)
w1.generate(txt)  
w1.to_file('.\词云.png')  