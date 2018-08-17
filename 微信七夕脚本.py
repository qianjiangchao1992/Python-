# 第一步：爬取情话大全网站，把情话内容按格式存储在本地文件
# 第二步：爬贴吧我爱你相关图片存储
# 第三步：利用itchat自动连接微信
# 第四步：设置要发送的信息格式
# 第五步：运行main函数
from selenium import webdriver
import requests
import datetime
import itchat
import os
from lxml import etree
import re
import time
import random
def crawl_love_words():
    print("正在抓取情话。。。。")
    browser=webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    url='http://www.binzz.com/yulu2/3588.html'
    browser.get(url)
    html=browser.page_source
    Selector=etree.HTML(html)
    love_words_xpath='//div[@id="content"]/p/text()'
    love_words=Selector.xpath(love_words_xpath)
    love_word_path=r'D:\path7xi\lovewords.txt'
    for i in love_words:
        word=i.strip('\n\t\u3000\u3000').strip()
        with open(love_word_path,'a+') as f:
            f.write(word+'\n')
    print("抓取情话完成！")
    return love_word_path
def crawl_love_images():
    print('正在抓取我爱你图片')
    pic_path=r'D:\path7xi_img'
    for i in range(1,22):
        url='http://tieba.baidu.com/p/3108805355?pn={}'.format(i)
        response=requests.get(url)
        html=response.text
        pattle=re.compile(r'<div.*?class="d_post_content j_d_post_content.*?">.*?<img class="BDE_Image"\s+src="(.*?)".*?>.*?</div>',re.S)
        image_url=re.findall(pattle,html)
        for j,data in enumerate(image_url):
            pics=requests.get(data)
            #os.mkdir(pic_path)
            fq=open(pic_path+'\\'+str(i)+'_'+str(j)+'.jpg','wb')
            fq.write(pics.content)
            fq.close()
        return pic_path
        print("图片抓取完成")
def send_news(names):
    # 计算认识时间
    inLovedate=datetime.datetime(2018,8,16)
    todayDate=datetime.datetime.today()
    inLovedays=(todayDate-inLovedate).days

    #file_path=crawl_love_words()
    pages=random.randint(1,120)
    with open(r'D:\path7xi\lovewords.txt','r') as file:
        #print(inLovedays)
        #print(file.readlines())
        love_word=file.readlines()[pages].split('：')[1]
    itchat.auto_login(hotReload=True)
    my_friends=itchat.search_friends(name=names)
    goodfriend=my_friends[0]['UserName']
   # print(goodfriend)
    message="""
    亲爱的{}:
    下午好，今天是我们认识的第{}天~
    今天想对你说的话是：
    {}
    最后也是最重要的!
    """.format(names,str(inLovedays),love_word)
    itchat.send(message,toUserName=goodfriend)
    files=os.listdir(r'D:\path7xi_img')
    nums=len(files)
    pages_img=random.randint(1,nums)
    file=files[pages_img]
    love_image_file='D:\\path7xi_img\\'+file
    try:
        itchat.send_image(love_image_file,toUserName=goodfriend)
    except Exception as e:
        print(e)
def main():
    names=input('请输入好友名称:')
    crawl_love_words()
    crawl_love_images()
    send_news(names)
if __name__=='__main__':
        curr_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        love_time=curr_time.split(" ")[1]
        main()
        print('每天如此美好，现在时间:'+love_time)


