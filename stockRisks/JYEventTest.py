# coding:utf-8
# 传入securityCode、 factorType  返回计算结果
import pymssql
import cx_Oracle
import mysql.connector
#import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')

# 源数据库--SQL Server
connJY = pymssql.connect(host='10.31.90.170', user='jydev', password='jydev',
                         database='JYDB',
                         port='30012', charset='utf8')  # 连接信息
cursorJY = connJY.cursor()
#万得数据库---Oracle
 #db = cx_Oracle.connect(username/passwd@host:port/sevicename)
constring = "monitor/monitor_123@10.31.90.170:30011/WINDDB"

connWD = cx_Oracle.connect('monitor/monitor_123@10.31.90.170:30011/winddb')
connWD = cx_Oracle.connect(constring)
cursorWD = connWD.cursor()
#本地---mySql
#connJBT = mysql.connector.connect(host='10.31.90.118',user='root',password='!2D#34S3aA$', database='jsfund_sms_dev',port='3306',charset='utf8')
#cursorJBT = connJBT.cursor()

'''
print '20005 业绩预告股票在聚源、金贝塔数据库数据个数分别是：'+str(len(resultJY))+'、'+str(len(resultJBT))
lst=list(range(0,503))
for i in  lst:
    try:
        print resultJY[i],resultJBT[i]
    except:
        print 'sss'
for i in resultJY:
    print i        

'''

# 证券数目：应该是3529个证券--JY
sqlStr0 = 'select CompanyCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1 ORDER BY CompanyCode'
# sqlStr00='SELECT * FROM lc_relatedtrade where  CompanyCode = 91 and InfoPublDate>=\'2018-04-23 00:00:00\' order by InfoPublDate desc'
# 20001 总股本，应该是3529条数据，--JY
sqlStr01 = 'SELECT  CompanyCode,TotalShares FROM lc_newestsharestru  where CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1) ORDER BY CompanyCode '
# 20002 商誉--JY
sqlStr02 = 'select b.CompanyCode,b.GoodWill,b.InfoPublDate,b.EndDate,b.Mark from (SELECT max(id) id FROM lc_balancesheetnew where EndDate>\'2017-01-01 00:00:00\' and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode) t inner join lc_balancesheetnew b ON t.id=b.id  ORDER BY b.CompanyCode'
sqlStr021 = 'select count(*) from lc_balancesheetnew where InfoPublDate>\'2018-05-10 00:00:00\' and InfoPublDate<\'2018-08-07 00:00:00\''
# 20003 净资产  20009营业收入  20024 经营性现金流  20025 应收账款--JY
sqlStr03 = 'select CompanyCode,SEWithoutMI,OperatingReenue, NetOperateCashFlow, AccountReceivables,InfoPublDate,EndDate,InfoSource,Mark from (SELECT max(id) id FROM lc_maindatanew where EndDate>\'2018-01-01 00:00:00\' and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode) t inner join lc_maindatanew b ON t.id=b.id ORDER BY b.CompanyCode'
# 20004 违规行为--JY
sqlStr04 = 'SELECT CompanyCode,COUNT(ID) FROM lc_deregulation where AdminInst in(6,7,8)  and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)and InfoPublDate> \'2016-05-10 00:00:00\' and InfoPublDate<\'2018-09-08 00:00:00\' GROUP BY CompanyCode'


# 20005业绩预告--JY
sqlStr05 = ' SELECT CompanyCode,COUNT(*) FROM  lc_performanceforecast where Forcasttype in(1,7,8,18) and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  and InfoPublDate>\'2016-05-10 00:00:00\' and InfoPublDate<\'2018-08-07 00:00:00\' GROUP BY CompanyCode'
# 20006 财务审计意见--JY
sqlStr06 = '  SELECT companycode,COUNT(ID) FROM lc_auditopinion where  EndDate>\'2016-12-01 00:00:00\' and InfoSource = \'年度报告\' and CompanyCode  in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)    GROUP BY CompanyCode order by CompanyCode '
#20007 退市风险状态--JY
sqlStr07='select InnerCode,InfoPublDate,SecurityAbbr,SpecialTradeType from (SELECT max(id) id FROM lc_specialtrade where InnerCode in(select innercode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY InnerCode) t inner join lc_specialtrade b ON t.id=b.id ORDER BY b.InnerCode'
# 20008 资产负债率、 20011 带息债务/全部投入资本--JY
sqlStr08 = ' select CompanyCode,DebtAssetsRatio,InteBearDebtToTotalCapital,EndDate from (SELECT max(id) id FROM lc_mainindexnew where EndDate>\'2016-01-01 00:00:00\' and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode) t inner join lc_mainindexnew b ON t.id=b.id ORDER BY b.CompanyCode'
# 20010 资产负债率--JY
sqlStr10 = 'select CompanyCode,InfoPublDate,InfoSource,EndDate,Mark,NetProfit from (SELECT max(id) id FROM LC_QIncomeStatementNew where EndDate>\'2016-01-01 00:00:00\' and CompanyCode in(select CompanyCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode) t inner join LC_QIncomeStatementNew b ON t.id=b.id ORDER BY b.CompanyCode '
# 20013 股权解禁数量--JY
sqlStr13='SELECT CompanyCode ,NewMarketableAShares,TotalAShares ,AccuMarketableAShares ,NonMarketableAShares  FROM lc_sharesfloatingschedule where StartDateForFloating <= \'2018-10-26 00:00:00\'   and StartDateForFloating >= \'2018-09-26 00:00:00\' and CompanyCode  in(select CompanyCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)   order by CompanyCode'
# 20015 平仓风险--JY
sqlStr31 = 'SELECT * FROM lc_greatevents where InfoSource like \'%平仓%\' and InfoSource not like \'%消除%\' and InfoSource not like \'%解除%\' and  InfoSource not like \'%交易平仓%\' and    InfoPublDate> \'2018-07-06 00:00:00\'   ORDER BY InfoPublDate DESC  '
sqlStr15 = '  SELECT COUNT(*)  FROM lc_relatedtrade where TradeType in (9,10,11) and InfoPublDate>= \'2016-01-01 00:00:00\' and InfoPublDate<= \'2018-10-07 00:00:00\'  '
# 20016 关联资产注入（剥离）行为--JY
sqlStr16 = 'SELECT CompanyCode,COUNT(ID)  FROM lc_relatedtrade where InfoPublDate>\'2016-05-10 00:00:00\' and TradeType in (9,10,11) and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode ORDER BY CompanyCode'
# 20017 关联交易次数--JY
sqlStr171 = 'SELECT * FROM  lc_relatedtrade where  CompanyCode = 75 and InfoPublDate>\'2018-05-10 00:00:00\' '
sqlStr17 = 'select CompanyCode,COUNT(ID) from lc_relatedtrade where InfoPublDate>\'2018-05-10 00:00:00\' and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode ORDER BY CompanyCode'
# 20018 并购次数--JY
sqlStr18 = ' SELECT CompanyCode,COUNT(ID)  FROM lc_merger where Initialinfopubldate >\'2018-08-10 00:00:00\' and CompanyCode in(select companycode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY CompanyCode ORDER BY CompanyCode'
#20021 20022 冻结解冻股数--JY
sqlStr21='SELECT CompanyCode,count(*) FROM lc_sharefp where TypeSelect = 2 and CompanyCode in(select CompanyCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)   GROUP BY CompanyCode order by CompanyCode'
#20023 诉讼仲裁金额--JY
sqlStr23='SELECT CompanyCode,count(*) FROM lc_suitarbitration where InfoPublDate>  \'2018-07-14 00:00:00\' and CompanyCode in(select CompanyCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1) GROUP BY CompanyCode order by CompanyCode'

sqlStr231='SELECT CompanyCode,count(*) FROM lc_suitarbitration where InfoPublDate>  \'2016-07-14 00:00:00\' and CompanyCode in(264) GROUP BY CompanyCode'

#20026 股本复权系数--JY
sqlStr26='SELECT InnerCode,count(*) FROM  LC_Dividend where InnerCode in(select InnerCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  and (Bonusshareratio is not null or Tranaddshareraio is not null) GROUP BY InnerCode order by InnerCode'
sqlStr261=' select count(*) from (SELECT max(id) id FROM LC_Dividend where InnerCode in(select InnerCode from secumain where secucategory=1 and secumarket in(83,90) and listedstate=1)  GROUP BY InnerCode) t inner join LC_Dividend b ON t.id=b.id'

#20030 质押比例--WD
sqlStr30 ='select S_INFO_WINDCODE,COUNT(*) from WIND.asharepledgeproportion   GROUP BY S_INFO_WINDCODE order by S_INFO_WINDCODE'
#20014 董监高+大股东减持数量   --多了数据
sqlStr14="select F2_1842,COUNT(*) t from  WIND.TB_OBJECT_1842  where RP_GEN_DATETIME >=to_date('2018-07-26 00:00:00' , 'yyyy-mm-dd hh24:mi:ss')  GROUP BY F2_1842 ORDER BY t"
sqlStr141="select * from  WIND.TB_OBJECT_1842  where RP_GEN_DATETIME >= '2018-05-15 00:00:00'  AND F2_1842='亚泰集团'"
#20027 负面新闻--WD
sqlStr27="select COUNT(*)  from WIND.stocknegativenews where PUBLISHDATE>=to_date('2018-08-16','yyyy-mm-dd') and  WINDCODES like '%002680%'"
#20028 总市值--WD
sqlStr28="select * from WIND.TB_OBJECT_5004 where F16_1090 = '000100'"
#sqlStr28="select * from WIND.TB_OBJECT_5004 where F2_5004=20180816"

sqlStr99="select COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_cols where table_name= \"stocknegativenews\""
sql111='SELECT * FROM lc_sharesfloatingschedule where JSID = 590569630835'

#cursorJY.execute(sqlStr23)
#result = cursorJY.fetchall()

cursorWD.execute(sqlStr27)
result = cursorWD.fetchall()

print(len(result))
# 打印所有记录
for i in result:
    print (i)
    #print i[0].decode('gbk') +', ' +str(i[1])  #对20014 有不识别的编码输出时


cursorJY.close()
connJY.close()

#cursorWD.close()
#connWD.close()