import itchat
import numpy as np
import pandas as pd
from collections import defaultdict
import re
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
NickName = friends[0]['NickName']
os.mkdir(NickName)
file = '\%s' %NickName
cp = os.getcwd() #��ǰ·��
path = os.path.join(cp+file) #�ոմ������Ǹ��ļ��еľ���·��
os.chdir(path) #�л�·��
number_of_friends = len(friends)
df_friends = pd.DataFrame(friends)
print(number_of_friends)
print(df_friends)
df_friends.to_excel(r'C:\Users\Administrator\Desktop\weixinhaoyou_zz.xls')

