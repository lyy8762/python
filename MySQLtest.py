# coding:utf-8
# 演示mysql的连接、操作

import mysql.connector

conn = mysql.connector.connect(host='10.31.90.118',user='root',password='!2D#34S3aA$',database='jsfund_sms_dev',port='3306',charset='utf8')  #连接信息

cursor=conn.cursor()  #创建游标

#查询操作
sqlString='select mobile,create_time,sms_text from system_msg_sms_main where mobile=15000000001 ORDER BY create_time DESC LIMIT 1'
cursor.execute(sqlString)
values=cursor.fetchall()
print values

cursor.close()          #关闭游标
conn.close()            #关闭数据库的连接