import requests
import time
from threading import Timer
from wxpy import *
bot=Bot()
def get_news():
    """获取金山词霸每日一句，英文和翻译"""
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content=r.json()['content']
    note=r.json()['note']
    return content,note
def send_news():
    try:
        contents=get_news()
    # 你朋友的微信名称，不是备注，也不是微信帐号。
        friends=['name1','name2','name3','name3']
        for name in friends:
            my_friend = bot.friends().search(u'%s'%(name))[0]
            my_friend.send(u"写个脚本试一试")
            my_friend.send(u"开始")
            my_friend.send(contents[1])
            your_name='yourname'
            my_friend.send(u"来自最爱你的朋友%s!"%(your_name))
            my_friend.send(u"结束")
            time.sleep(5)
    # 每86400秒（1天），发送1次
    except:
    # 你的微信名称，不是微信帐号。
        you_name="youname"
        my_friend = bot.friends().search('%s'%(you_name))[0]
        my_friend.send(u'今天消息发送失败!')
if __name__=="__main__":
    while True:
        send_news()
        time.sleep(86400)




