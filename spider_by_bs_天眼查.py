#!/usr/bin/python
# -*- coding: UTF-8 -*-
#企业信息爬虫

from bs4 import BeautifulSoup
import pymysql
import threading
import config_parse
from Logger import Logger

logger = Logger(logname='log/log.txt', loglevel='INFO', logger="spider_by_bs.py").getlog()

global conn,cursor
conn = None
cursor = None

def init(cfg):
    try:
        global conn, cursor
        __host__ = cfg.get("host")
        __database__ = cfg.get("database")
        __user__ = cfg.get("user")
        __password__ = cfg.get("password")
        __port__ = cfg.get("port")
        __tablename__ = cfg.get("tablename")
        conn = pymysql.connect(host=__host__ ,user=__user__,passwd=__password__,db=__database__,port=int(__port__),charset='utf8')
        cursor = conn.cursor()
        logger.info('connect msyql database success !')
    except Exception,e:
        logger.error('connect msyql database fail ! : %s ',e)

def spider(html,cfg):
    #建立数据库连接
    init(cfg)
    try:
        #用Beautifulsoup lxml解释器进行解析
        soup = BeautifulSoup(html, "lxml")
        if not soup:
            logger.info('#### the website is empty ! ####')
            return

        #公司基本信息
        gsname = soup.find('h1',class_='name').get_text()
        if not gsname:
            logger.info('#### the company name info is not parsed ! ####')
            return
        gsinfo = soup.find(id="company_web_top").select_one('div[class="detail "]')
        qylxdh = gsinfo.select_one('> div:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(2)').get_text()
        email = gsinfo.select_one('> div:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(2)').get_text()
        website = gsinfo.select_one('> div:nth-of-type(2) > div:nth-of-type(1) ').get_text()
        summary = gsinfo.select_one('> div[class="summary"] > span:nth-of-type(2)').get_text()

        #工商信息
        gongshang = soup.find(id="_container_baseInfo").select('table > tbody')
        if not gongshang:
            logger.info('#### the company gongshang info is not parsed ! ####')
            return
        fddbr = gongshang[0].select_one('> tr:nth-of-type(1) > td:nth-of-type(1) div[class="name"] > a').get_text()
        zczb = gongshang[0].select_one('> tr:nth-of-type(1) td:nth-of-type(2) > div:nth-of-type(2)')['title']
        zctime = gongshang[0].select_one('> tr:nth-of-type(2) td:nth-of-type(1) > div:nth-of-type(2)').get_text()
        state = gongshang[0].select_one('> tr:nth-of-type(3) td:nth-of-type(1) > div:nth-of-type(2)').get_text()
        gszch = gongshang[1].select_one('> tr:nth-of-type(1) td:nth-of-type(2)').get_text()
        orgcode = gongshang[1].select_one('> tr:nth-of-type(1) td:nth-of-type(4)').get_text()
        xycode = gongshang[1].select_one('> tr:nth-of-type(2) td:nth-of-type(2)').get_text()
        gstype = gongshang[1].select_one('> tr:nth-of-type(2) td:nth-of-type(4)').get_text()
        nscode = gongshang[1].select_one('> tr:nth-of-type(3) td:nth-of-type(2)').get_text()
        hangye = gongshang[1].select_one('> tr:nth-of-type(3) td:nth-of-type(4)').get_text()
        yyqx = gongshang[1].select_one('> tr:nth-of-type(4) td:nth-of-type(2)').get_text()
        hzdate = gongshang[1].select_one('> tr:nth-of-type(4) td:nth-of-type(4)').get_text()
        nsrzz = gongshang[1].select_one('> tr:nth-of-type(5) td:nth-of-type(2)').get_text()
        nsrgm = gongshang[1].select_one('> tr:nth-of-type(5) td:nth-of-type(4)').get_text()
        sjmoney = gongshang[1].select_one('> tr:nth-of-type(6) td:nth-of-type(2)').get_text()
        djjg = gongshang[1].select_one('> tr:nth-of-type(6) td:nth-of-type(4)').get_text()
        cbrs = gongshang[1].select_one('> tr:nth-of-type(7) td:nth-of-type(2)').get_text()
        ywname = gongshang[1].select_one('> tr:nth-of-type(7) td:nth-of-type(4)').get_text()
        zcaddr = gongshang[1].select_one('> tr:nth-of-type(8) td:nth-of-type(2)').get_text()
        jyfw = gongshang[1].select_one('> tr:nth-of-type(9) td:nth-of-type(2) span[class="js-full-container hidden"]').get_text()

        #插入主表，返回qid
        cursor.execute('insert into tb_company_info(gsname,fddbr,zczb,zctime,state,gszch,orgcode,xycode,gstype,nscode,'
                       'hangye,yyqx,hzdate,nsrzz,nsrgm,sjmoney,djjg,cbrs,ywname,zcaddr,jyfw,qylxdh,email,website) '
                       'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (gsname,fddbr,zczb,zctime,state,gszch,orgcode,xycode,
                        gstype,nscode,hangye,yyqx,hzdate,nsrzz,nsrgm,sjmoney,djjg,cbrs,ywname,zcaddr,jyfw,qylxdh,email,website))
        # 返回的主键id
        qid = cursor.lastrowid
        #爬取其他信息插入从表
        threading.Thread(target=spider_zy, args=(soup,qid,cfg)).start()
        threading.Thread(target=spider_gd, args=(soup,qid, cfg)).start()
        threading.Thread(target=spider_tz, args=(soup,qid,cfg)).start()
        threading.Thread(target=spider_bg, args=(soup,qid, cfg)).start()
        threading.Thread(target=spider_kt, args=(soup,qid,cfg)).start()
        threading.Thread(target=spider_fygg, args=(soup,qid, cfg)).start()
        # threading.Thread(target=spider_sxr, args=(soup,qid, cfg)).start()
        threading.Thread(target=spider_zxr, args=(soup,qid, cfg)).start()
        #主表插入提交
        conn.commit()
        logger.info('parse website main info success !')
    except Exception,e:
        logger.error('parse  website main info fail : \n%s', e, exc_info=1)
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 释放数据库资源


#爬虫主要人员内容
def spider_zy(soup,qid,cfg):
    try:
        # 主要成员
        zy_mode = soup.find(id='_container_staff')
        if zy_mode:
            zystaffs = zy_mode.select_one('table > tbody ').select('> tr')
            zy_list=[]
            for staff in zystaffs:
                ryname = staff.select_one('> td:nth-of-type(2) a').get_text()
                dqzw = staff.select_one('> td:nth-of-type(3)').get_text()
                zy_list.append((qid, ryname, dqzw))
            zy_sql = ('insert into tb_company_chief(qid,ryname,dqzw) values(%s,%s,%s)',zy_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(zy_sql,cfg)
        logger.info('parse website zhuyao info success !')
    except Exception,e:
        logger.error('parse  website zhuyao info  fail : \n%s', e,exc_info=1)

#爬虫股东信息内容
def spider_gd(soup,qid,cfg):
    try:
        # 股东信息
        gd_mode = soup.find(id="_container_holder")
        if gd_mode:
            gudongs = gd_mode.select_one('table > tbody ').select('> tr')
            gd_list=[]
            for holder in gudongs:
                gdname = holder.select_one('> td:nth-of-type(2) a').get_text()
                sjcz = holder.select_one('> td:nth-of-type(4)').get_text()
                czdate = holder.select_one('> td:nth-of-type(5)').get_text()
                gd_list.append((qid,gdname,sjcz,czdate))
            gd_sql = ('insert into tb_company_gd(qid,gdname,sjcz,czdate) values(%s,%s,%s,%s)', gd_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(gd_sql,cfg)
        logger.info('parse website gudong info success !')
    except Exception,e:
        logger.error('parse  website gudong info  fail : \n%s', e,exc_info=1)

#爬虫投资信息内容
def spider_tz(soup,qid,cfg):
    try:
        # 投资信息 ,防止有tr里面还有tbody，所以只取第一个table > tbody
        tz_mode = soup.find(id="_container_invest")
        if tz_mode:
            touzi = tz_mode.select_one('table > tbody ').select('> tr')
            tz_list=[]
            for invest in touzi:
                btzgsid = invest.select_one('> td:nth-of-type(2) a').get_text()
                cze = invest.select_one('> td:nth-of-type(4)').get_text()
                czdate1 = invest.select_one('> td:nth-of-type(6)').get_text()
                tz_list.append((qid,btzgsid,cze,czdate1))
            tz_sql = ('insert into tb_company_invest(qid,btzgsid,cze,czdate) values(%s,%s,%s,%s)',tz_list )
            # 从主表返回qid，再向从表多线程插入数据
            insert(tz_sql,cfg)
        logger.info('parse website touzi info success !')
    except Exception,e:
        logger.error('parse  website touzi info  fail : \n%s', e,exc_info=1)

#爬虫变更信息内容
def spider_bg(soup,qid,cfg):
    try:
        # 变更信息
        bg_mode = soup.find(id="_container_changeinfo")
        if bg_mode:
            biangeng = bg_mode.select_one('tbody').select('> tr')
            bg_list=[]
            for change in biangeng:
                bgkey = change.select_one('> td:nth-of-type(3)').get_text()
                bgValueBefore = change.select_one('> td:nth-of-type(4)').get_text()
                bgValue = change.select_one('> td:nth-of-type(5)').get_text()
                bgTime = change.select_one('> td:nth-of-type(2)').get_text()
                bg_list.append((qid,bgkey,bgValueBefore,bgValue,bgTime))
            bg_sql = ('insert into tb_company_change(qid,bgkey,bgValueBefore,bgValue,bgTime) values(%s,%s,%s,%s,%s)', bg_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(bg_sql,cfg)
        logger.info('parse website biangeng info success !')
    except Exception,e:
        logger.error('parse  website biangeng info  fail : \n%s', e,exc_info=1)

#爬虫开庭信息内容
def spider_kt(soup,qid,cfg):
    try:
        # 司法风险
        # 开庭公告
        kt_mode = soup.find(id="_container_announcementcourt")
        if kt_mode:
            kaiting = kt_mode.select_one('tbody').select('> tr')
            kt_list=[]
            for kt in kaiting:
                ktdate = kt.select_one('> td:nth-of-type(2)').get_text()
                reason = kt.select_one('> td:nth-of-type(3)').get_text()
                accuser = kt.select_one('> td:nth-of-type(4)').get_text()
                defendant = kt.select_one('> td:nth-of-type(5) ').get_text()
                # defendant = kt.select_one('> td:nth-of-type(6) span').get_text()  详情
                kt_list.append( (qid,ktdate,reason,accuser,defendant))
            kt_sql = ('insert into tb_company_kaiting(qid,ktdate,reason,accuser,defendant) values(%s,%s,%s,%s,%s)',kt_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(kt_sql,cfg)
        logger.info('parse website kaiting info success !')
    except Exception,e:
        logger.error('parse  website kaiting info  fail : \n%s', e,exc_info=1)

#爬虫法院公告信息内容
def spider_fygg(soup,qid,cfg):
    try:
        # 法院公告
        fygg_mode = soup.find(id="_container_court")
        if fygg_mode:
            fayuangg = fygg_mode.select_one('tbody').select('> tr')
            fy_list = []
            for fygg in fayuangg:
                kddate = fygg.select_one('> td:nth-of-type(2)').get_text()
                appellate = fygg.select_one('> td:nth-of-type(3)').get_text()
                defendant1 = fygg.select_one('> td:nth-of-type(4)').get_text()
                ggtype = fygg.select_one('> td:nth-of-type(5)').get_text()
                fayuan = fygg.select_one('> td:nth-of-type(6)').get_text()
                fy_list.append((qid,kddate,appellate,defendant1,ggtype,fayuan))
                # defendant = kt.select_one('> td:nth-of-type(7) span').get_text()   详情
            fygg_sql = ('insert into tb_company_fygg(qid,kddate,appellate,defendant,ggtype,fayuan) values(%s,%s,%s,%s,%s,%s)', fy_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(fygg_sql,cfg)
        logger.info('parse website fayuangonggao info success !')
    except Exception,e:
        logger.error('parse  website fayuangonggao info  fail : \n%s', e,exc_info=1)

#爬虫失信人信息内容
def spider_sxr(soup,qid,cfg):
    try:
        # 失信人
        logger.info('parse website shixinren info success !')
    except Exception,e:
        logger.error('parse  website shixinren info  fail : \n%s', e,exc_info=1)

#爬虫被执行人信息内容
def spider_zxr(soup,qid,cfg):
    try:
        # 被执行人
        zx_mode = soup.find(id="_container_zhixing")
        if zx_mode:
            zhixing = zx_mode.select_one('tbody').select('> tr')
            zx_list = []
            for bzxr in zhixing:
                liandate = bzxr.select_one('> td:nth-of-type(2)').get_text()
                zxbd = bzxr.select_one('> td:nth-of-type(3)').get_text()
                casecode = bzxr.select_one('> td:nth-of-type(4)').get_text()
                fayuan1 = bzxr.select_one('> td:nth-of-type(5)').get_text()
                zx_list.append((qid,liandate,zxbd,casecode,fayuan1))
            zx_sql = ('insert into tb_company_bzxr(qid,liandate,zxbd,casecode,fayuan) values(%s,%s,%s,%s,%s)', zx_list)
            # 从主表返回qid，再向从表多线程插入数据
            insert(zx_sql,cfg)
        logger.info('parse website zhixingren info success !')
    except Exception,e:
        logger.error('parse  website zhixingren info  fail : \n%s', e,exc_info=1)


#多线程插入
def insert(sql,cfg):
    try:
        __host__ = cfg.get("host")
        __database__ = cfg.get("database")
        __user__ = cfg.get("user")
        __password__ = cfg.get("password")
        __port__ = cfg.get("port")
        __tablename__ = cfg.get("tablename")
        conn = pymysql.connect(host=__host__ ,user=__user__,passwd=__password__,db=__database__,port=int(__port__),charset='utf8')
        cur = conn.cursor()
        cur.executemany(sql[0],sql[1])
        conn.commit()
        logger.debug('insert into database success ! \nSQL : %s %s ',sql[0],sql[1])
    except Exception,e:
        logger.error('insert into database fail ! : \nSQL : %s %s  \n%s',sql[0],sql[1], e, exc_info=1)
    finally:
        cur.close()
        conn.close()

#
if __name__=='__main__':
    cfg = config_parse.ConfigUtils('E://zhc.txt')
    # url=''
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}  # 设置头文件信息
    # response = requests.get('C:/Users/Administrator/Desktop/zhc.html', headers=headers).content    # 提交requests get 请求
    response = open('C:/Users/Administrator/Desktop/baidu.html','r')
    spider(response,cfg)
