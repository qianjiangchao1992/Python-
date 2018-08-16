import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re

#获取第一页的内容
class ApplePPZhushou_Spyder():
    def __init__(self,url,savepath):
        self.url=url
        self.savepath=savepath
    @staticmethod
    def get_one_page(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        cookies = 'UM_distinctid=164acb194e75b7-0456ea908772d9-6114147a-100200-164acb194e8509; ctoken=k3gyKJ4teiIQ8JZHp1tUpp_web_ios; CNZZDATA1258416559=1817522181-1531903768-null%7C1531903768; Hm_lvt_80c7667d40c35eec40368ef5cd6547d4=1531905682; CNZZDATA1258416494=1148710464-1531904996-%7C1531904996; csrfToken=z6Xmtkn6l6ZykoM1K-Y65DsV; CNZZDATA1258416621=250215804-1531903572-https%253A%252F%252Fwww.25pp.com%252F%7C1531903572; Hm_lpvt_80c7667d40c35eec40368ef5cd6547d4=1531906623'
        cookies_dict = {}
        for cookie in cookies.split(';'):
            k, v = cookie.split('=', 1)
            cookies_dict[k.strip()] = v.strip()
        response = requests.get(url, headers=headers, cookies=cookies_dict)
        if response.status_code == 200:
            return response.text
        return None
#解析第一页内容，数据结构化
    def parse_one_page(self):
        html = self.get_one_page(self.url)
        soup = BeautifulSoup(html,'lxml')
        result=re.compile('cate_name=(.*?)\"\\s+data-stat-pos=\"cateList\"\\s+href=\"(.*?)\"')
        one_page=re.findall(result,str(soup))
        one_page_new={}
        for i in one_page:
            one_page_new[i[0]]=i[1]
        return one_page_new
#解析第二页内容，数据结构化
    def parse_two_page(self):
        urls=self.parse_one_page()
        for index in urls.keys():
            catname=index
            html=self.get_one_page(urls[index])
            soup=BeautifulSoup(html,'lxml')
            reI=re.compile('cate_name=(.*?)\"\\s+data-stat-pos=\"subCateList\"\\s+href=\"(.*?)\"')
            result=re.findall(reI,str(soup))
            result_new={}
            for i in result:
                result_new[i[0]]=i[1]
            for j in result_new.keys():
                html1=self.get_one_page(result_new[j])
                soup1=BeautifulSoup(html1,'lxml')
                re1=re.compile('class=\"page-num\".*?>(.*?)</a>')
                result1=re.findall(re1,str(soup1))
                if len(result1)==0:
                    k=2
                else:
                    k=int(result1[-1])+1
                for num in range(1,k):
                    p=(result_new[j]+'%s'+'/')%num
                    print(p)
                    try:
                        html_k=self.get_one_page(p)
                        soup_k=BeautifulSoup(html_k,'lxml')
                        re_ki=re.compile('app-info\".*?title=\".*?\">(.*?)</a>')
                        result_k=re.findall(re_ki,str(soup_k))
                        for appname in result_k:
                            yield {
                                'first_cate':catname,
                                'second_cate':j,
                                'APPNAME':appname
                            }
                    except:
                        return None
#对数据进行保存
	def write_txt(self):
        start_time=time.time()
        f=open(self.savepath,'w',encoding='utf-8')
        f.write('一级类目\t二级类目\tAPPname\n')
        for item in self.parse_two_page():
            f.write(item['first_cate']+'\t'+item['second_cate']+'\t'+item['APPNAME']+'\n')
        f.close()
        end_time=time.time()
        print('该程序运行时间为%s'%(end_time-start_time))
rt=ApplePPZhushou_Spyder('https://www.25pp.com/ios/game/',r'C:\Users\Administrator\Desktop\ApplePPZhushou_Spyder.txt')
rt.write_txt()