import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import xlwt
import time
import re
#获取第一页的内容
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    cookies = '__jdu=1423189521; shshshfpa=686010d8-f280-9e28-d524-0b53ddcd3e8c-1526292388; shshshfpb=11e5abc3839ce413daac211b35ed39650c88311fdaa4c66d05af95fae6; PCSYCityID=1607; ipLoc-djd=1-72-2799-0; user-key=1d27b185-974b-438b-ae21-121af6dcd2dd; cn=0; unick=%E7%88%B1%E5%AD%A6%E4%B9%A0%E7%88%B1%E5%B7%A5%E4%BD%9C%E7%9A%84%E4%BA%BA; pinId=FeoPVeHM2gdP3bRbPrgbr7V9-x-f3wj7; pin=327143273-253734; _tp=6qt6OUxYB4AWLUsPn4mwVvZgi7u1Nf%2Bv0tcz387vamo%3D; _pst=327143273-253734; unpl=V2_ZzNtbRIFQEFzCUYBLBlcVWIDFw5LBRQdJl9BUSkcVAdvUUZcclRCFXwUR11nGVsUZwIZX0pcRhxFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4aXgVuCxZeQmdzEkU4dl14H1wFZzMTbUNnAUEpCEdQchxaSGcGEV9CXksRdgh2VUsa; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ac2e701df11a414b8cf9bf64c4939ce0|1534387188841; 3AB9D23F7A4B3C9B=MQBL365TXV4KTOZFPZEMXELCHS7H6DRLYDWYLOPXQPJKBZ2KOMXHSTRIODSYO55L5D3ALSATELTG7GE5T6ZSM6FRZ4; __jdc=122270672; mt_xid=V2_52007VwMXUV9YW1IbShlsUjMLRwFVXQZGShxNXBliC0cBQQtTUk9VTlkMN1YbW11dUg4eeRpdBW4fE1tBWFVLH04SXAZsARNiX2hSahdIGlsDbwIaWlVeV1MYTRlbDWQzElRZXA%3D%3D; shshshfp=cfce054275aa3b9e2ce179de7eb94ec1; __jda=122270672.1423189521.1495784280.1534410944.1534415546.67; wlfstk_smdl=9s2nbzd1b34vtgqk7dqszj65npzcakzk; TrackID=1EpvoF5Z65BCuzhL20q3CDwMLRigKdiGqiD0b9GhmvaFr15MVxyjCfh6uZ8rOk7ZnXXNMcillSjCfco3ZnX-n9XIYrM5wGbHNrs390HaWVSw; thor=631C5C479B980AAC15625CA83FEAACE30F4362BF363F21E465C1F4542946AD4CFD430BD0253E8A0F62498F6EFC395EAD1265423CE3EF6E116EF9DA2566DDCD151A666080A492FF86060F6353EAD14931F1C3A707BDF89418C9974AE069E5FCC279A7A5C66D21A1C0CB657506D0969AA7C433722BA5A92C8E236DD73849FA25647B498F3E65055EB0E73A271AC8073400A8DB5C22F1BF2C9C24CFC78A651FD8FE; ceshi3.com=201; shshshsID=71c76aac3031d43d67b8ad39bb765bcc_2_1534415558723; __jdb=122270672.4.1423189521|67.1534415546'
    cookies_dict = {}
    for cookie in cookies.split(';'):
        k, v = cookie.split('=', 1)
        cookies_dict[k.strip()] = v.strip()
    response = requests.get(url, headers=headers, cookies=cookies_dict)
    #print(response.status_code)
    if response.status_code == 200:
        return response.text
    else:
        return None
def get_first():
    pattle = re.compile(r'href="(.*?)"')
    result=[]
    for i in range(1,159):
        url = 'https://list.jd.com/list.html?cat=9987,653,655&page=%d&sort=sort_rank_asc&trans=1&JL=6_0_0' % (i)
        html = get_one_page(url)
        time.sleep(1)
        soup = BeautifulSoup(html,'lxml')
        #print(soup)
        urls = soup.select('li.gl-item div div.p-img a')
        for href in urls:
            href_result=re.findall(pattle, str(href))
            yield href_result
        if i%15==0:
            time.sleep(30)
        else:
            pass


def get_two():
    htmls=get_first()
    count=0
    pattle=re.compile(r'<dd>(.*?)</dd>')
    #print(htmls)
    for html1 in htmls:
        html=get_one_page('http:'+html1[0])
        with open(r'C:\Users\Administrator\Desktop\JD—urls.txt','a+') as f1:
            f1.write('http:'+html1[0]+'\n')
        #print(html)
        soup=BeautifulSoup(html,'lxml')
        info=soup.select('.Ptable .Ptable-item')
        for infos in info:
            #print(infos.find('h3').get_text())
            if (infos.find('h3').get_text())=='主体':
                infos1=re.findall(pattle,str(infos))
            else:
                pass
        #print(infos)
        #time.sleep(100)
        try:
            brand=infos1[0]
        except:
            brand='null'
        try:
            model=infos1[1]
        except:
            model='null'
        try:
            net_model=infos1[2]
        except:
            net_model='null'
        try:
            product_year=infos1[3]
        except:
            product_year='null'
        try:
            product_month=infos1[4]
        except:
            product_month='null'
        count+=1
        print('完成第%d次写入'%(count))
        yield((brand,model,net_model,product_year,product_month))
def get_data():
    f=open(r'C:\Users\Administrator\Desktop\JD_56_106.txt','w+')
    item = get_two()
    f.write('品牌\t型号\t入网型号\t上市年份\t上市月份\n')
    #print(item)
    for items in item:
        #print(type(items1))
        #for items in items1:
        #print(items[0])
        f.write(items[0]+'\t'+items[1]+'\t'+items[2]+'\t'+items[3]+'\t'+items[4]+'\n')
    #print('完成写入')
    f.close()
get_data()

















