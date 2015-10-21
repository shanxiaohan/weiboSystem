# -*- coding: utf8 -*-
import MySQLdb 

conn=MySQLdb.connect(host='10.109.247.109',user='root',passwd='123456',db='weibotest1',charset='utf8')
cur=conn.cursor()  

#微博去重，将weibo表中新增的记录插入weibo_unique表中
def weiboUnique():
 
    sql1="select max(id) from `weibo_unique`"     #自增id
    res = cur.execute(sql1)
    max_previous = cur.fetchone()[0]            #注意是一个元组，fetchone()返回的是标识符1，需要取下标0得到数据
  
    sql2="insert into `weibo_unique` (select *,count(*) as `col` from `weibo` where `id`>%d group by `mid` having `col`>=1)" %max_previous
    cur.execute(sql2)
    conn.commit()
    
    
    
if __name__ == '__main__':
    
    weiboUnique()
    cur.close() 
    conn.close()
    print "关闭数据库连接~~"
    
    
    
    