import pymysql
class GetStatus():
    def __init__(self):
        pass
    def get_status(self):
        try:
            conn=pymysql.connect(host='192.168.7.31',
                                 user='ngoss_dim',
                                 password='ngoss_dim',
                                 database='label_support',
                                 charset='utf8')
            curson=conn.cursor()
            sql='select status from label_group_personas where status=4'
            curson.execute(sql)
            result=curson.fetchall()
            return result
        except Exception:
            print(Exception.args)
            return []