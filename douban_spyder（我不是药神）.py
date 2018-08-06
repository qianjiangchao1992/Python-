from bs4 import BeautifulSoup
import requests
import re
import time
def parse_url(urls):
    url=urls
    cookies='bid=SvROcxpZ-Ls; ll="118282"; __yadk_uid=VG0INWPWOgurwRL7xoCkWzMdDGg7iSPU; _vwo_uuid_v2=DA57B34CB5333F8F7EF29ABE635E9FBCE|71a1547ae6c685d496e7647c1a2a3dda; gr_user_id=1724e62d-11e7-49e0-9722-c1a4f4508f64; viewed="1231271_6523762_10590856"; ps=y; douban-fav-remind=1; __utma=30149280.1850926694.1496198705.1533178064.1533533865.23; __utmc=30149280; __utmz=30149280.1533533865.23.19.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1850926694.1496198705; _gid=GA1.2.99185222.1533533871; dbcl2="172926397:XHLff0K99UM"; ck=Q5TK; push_noty_num=0; push_doumail_num=0; __utmv=30149280.17292; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1533533881%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1595439815.1529890553.1530239770.1533533881.8; __utmb=223695111.0.10.1533533881; __utmc=223695111; __utmz=223695111.1533533881.8.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.13.10.1533533865; _pk_id.100001.4cf6=c2e52b724e20f6d2.1529890553.8.1533534631.1530239828.'
    cookies_dict={}
    for cookie in cookies.split(';'):
        k,v=cookie.split('=',1)
        cookies_dict[k.strip()]=v.strip()
    #print (cookies_dict)
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    response=requests.get(url,headers=header,cookies=cookies_dict)
    soup = BeautifulSoup(response.text,'lxml')
    namecitycomment=[]
    for text in soup.select('td[valign="top"]')[:]:
        tx = str(text.text).split('\n')
        while '' in tx:
            tx.remove('')
        data = []
        for i in tx:
            data.append(i.strip())
        if len(data)!=0:
            namecitycomment.append(data)
        else:
            pass
    #print(namecitycomment)
    pattle=re.compile(r'<span class="allstar(.*?)" title="(.*?)"></span>')
    souptx=re.findall(pattle,str(soup))
    #print(souptx)
    allinfo=[]
    for k1,v1 in zip(namecitycomment,souptx):
        yield {
            'name':k1[0],
            'city':k1[1],
            'date':k1[2],
            '评分':int(v1[0])/10,
            '推荐力度':v1[1],
            '评论内容':k1[-1]
        }
def main():
    start_time=time.time()
    f = open(r'C:\Users\Administrator\Desktop\douban_wobushiyaoshen.txt', 'w', encoding='utf-8')
    f.write('name\tcity\tdate\t评分\t推荐力度\t评论内容\n')
    for i in range(25):
        d=20*i
        url='https://movie.douban.com/subject/26752088/collections?start='+str(d)
        for item in parse_url(url):
            f.write(item['name']+'\t'+item['city']+'\t'+item['date']+'\t'+str(item['评分'])+'\t'+item['推荐力度']+'\t'+item['评论内容']+'\n')
        time.sleep(5)
        print(url)
    f.close()
    end_time=time.time()
    print('程序运行时间为%.4f'%(end_time-start_time))
main()




