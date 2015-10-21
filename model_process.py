# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
#上面三行解决读入的ASCII字符不能转化成Unicode编码，因为读入文件的字符流默认为ASCII编码，编码转换会出问题，这样就预先设定了为utf8
import os
import MySQLdb
"""
训练模型的输入输出数据处理，将weibo_unique表和结果表的增量作为model的输入文本，模型analyse_result
analyse_result表比weibo_unique多两个字段score和dist
readIn():从weibo_unique表中读数据，写入/home/shanxiaohan/tmsvm/memememememememememe/mysqldata/data文件，注意编码问题
writeOut():从/home/shanxiaohan/tmsvm/memememememememememe/data.result读入文件，写入analyse_result表
"""

conn=MySQLdb.connect(host='10.109.247.109',user='root',passwd='123456',db='weibotest1',charset='utf8')
cur=conn.cursor() 

def readIn():
    sql1="select max(id) from `analyse_result`"
    res1 = cur.execute(sql1)
    max_result = cur.fetchone()[0] 
     
    inputFile=open('/home/shanxiaohan/tmsvm/memememememememememe/mysqldata/data','w')
    
    #取weibo_unique和analyse_result自增id的差值
    sql2="select * from weibo_unique where id>%d" %max_result
    res2=cur.execute(sql2)
    weibos=cur.fetchmany(res2)
    weibos=list(weibos)
    
    #weibo_unique表中字段：mid || uid || content || likeNum || forwardNum || commentNum || time
    #source || topic || id ||col (id和col是后加的字段)
    for item in range(len(weibos)):
        weibo=weibos[item]
        for i in weibo:
            i=unicode(i)+u'\t'
            inputFile.write(i.encode('utf-8','ignore'))

        inputFile.write('\n')
      #print '\t'.join(weibo).encode('utf-8')        
      
    inputFile.close()


def writeOut():
    #将结果文件导出到数据库的analyse_result表
    outFile = open('/home/shanxiaohan/tmsvm/memememememememememe/data.result','r')

    sql1="insert into `analyse_result` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for each_line in outFile:

        if each_line!='\n':
            #将字符串each_line.strip('')删除首位的空格（默认），再根据Tab分隔（str分隔成list）
            each_line1=each_line.strip('').split('\t')    
            del each_line1[-1]                             #删除末尾的换行符(\n)，注意下标为-1代表最后一个
            for item in each_line1:
                item=item.replace('^','||')

            row=[]
            for i in each_line1:
                row.append(i)
            #执行插入语句的参数列表为元组
            cur.execute(sql1,tuple(row))
    
    #注意将所有cur.execute()执行完再conn.commit()
    conn.commit()

    """
        如果不加开头的三句话，默认从文件读入的为ASCII字符流，要先decode再encode，但超过128的不能解码
        #print  item.decode("ascii").encode("utf-8")
        #each_line="".join(each_line)

    """

if __name__=="__main__":
    
    readIn()
    writeOut()
    cur.close() 
    conn.close()
