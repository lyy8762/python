# coding:utf-8
# 传入securityCode、 factorType  返回计算结果
import mysql.connector
from decimal import Decimal


class calcFactor():
    def __init__(self):
        self.connJY = mysql.connector.connect(host='10.31.90.109', user='root', password='Jsisc@2015++',
                                         database='event-data-jy',
                                         port='3306', charset='utf8')  # 连接信息
        self.cursorJY = self.connJY.cursor()
        self.connWD = mysql.connector.connect(host='10.31.90.109', user='root', password='Jsisc@2015++',
                                         database='event-data-wd',
                                         port='3306', charset='utf8')  # 连接信息
        self.cursorWD = self.connWD.cursor()


    def calcFactor(self,secuCode,factorType):


        #查询companyCode
        self.cursorJY.execute('SELECT companyCode,chinameabbr FROM secumain_stock WHERE secucode =' + secuCode)
        result = self.cursorJY.fetchall()
        companyCode=result[0][0]
        companyName=result[0][1]

        #查询基本数据 ：取净资产、,营业收入,经营性现金流,应收账款
        sqlStr = 'SELECT SEWithoutMI, OperatingReenue, NetOperateCashFlow, AccountReceivables,InfoPublDate,EndDate,InfoSource,Mark FROM lc_maindatanew where CompanyCode = %s and EndDate>\'2017-01-01 00:00:00\' order by EndDate desc,Mark' % str(companyCode)
        self.cursorJY.execute(sqlStr)
        resultAll = self.cursorJY.fetchall()
        SEWithoutMI = resultAll[0][0]   #最新净资产
        OperatingReenue=resultAll[0][1]  #营业收入
        NetOperateCashFlow=resultAll[0][2]  #经营性现金流
        AccountReceivables=resultAll[0][3]  #应收账款



        if factorType=='50001':
            sqlStr1='SELECT * FROM lc_relatedtrade where TradeType in (9,10,11) and InfoPublDate>= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 3 YEAR) and CompanyCode ='+str(companyCode[0][0])
            self.cursorJY.execute(sqlStr1)
            self.cursorJY.fetchall()
            print(secuCode+' 证券的【50001】关联资产注入（剥离）----[3年内并购+资产剥离中关联交易的次数] 是：  '+str(self.cursorJY.rowcount))

        if factorType=='50002':
            sqlStr2= 'SELECT * FROM lc_relatedtrade where InfoPublDate>= DATE_ADD(\'2018-07-23 00:00:00\',INTERVAL - 3 MONTH) and CompanyCode = ' +str(companyCode[0][0])
            self.cursorJY.execute(sqlStr2)
            self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50002】关联交易----[3个月内公司关联交易记录次数] 是：  ' + str(self.cursorJY.rowcount))

        if factorType=='50003':
            sqlStr31= 'SELECT GoodWill,InfoPublDate,EndDate,Mark FROM lc_balancesheetnew where CompanyCode = %s and mark = 1  and EndDate>\'2017-01-01 00:00:00\' order by EndDate desc'%str(companyCode[0][0])
            self.cursorJY.execute(sqlStr31)
            result31=self.cursorJY.fetchall()
            goodWill=result31[0][0]

            print (secuCode + ' 证券的【50003】商誉----[商誉/净资产*100%] 是：  ' + str(format(Decimal(goodWill*100/SEWithoutMI), '.5f')))

        if factorType=='50004':
            sqlStr= 'SELECT * FROM lc_merger where CompanyCode = %s and Initialinfopubldate >= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 3 YEAR)'%str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50004】并购----[3年内并购次数] 是：  ' + str(self.cursorJY.rowcount))

        if factorType == '50005':
            sqlStr1 = 'select S_PLEDGE_RATIO,S_ENDDATE from asharepledgeproportion where S_INFO_WINDCODE =%s order by S_ENDDATE desc;'%secuCode
            self.cursorWD.execute(sqlStr1)
            result=self.cursorWD.fetchall()
            print (secuCode + ' 证券的【50005】质押----[质押比例值] 是：  ' + str(result[0][0]))

        if factorType=='50007':
            sqlStr= 'SELECT * FROM lc_deregulation where AdminInst in(6,7,8) and CompanyCode = %s and InfoPublDate>= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 1 MONTH) order by InfoPublDate desc;'%str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50007】违规----[近1个月以来出现的违规次数] 是：  ' + str(self.cursorJY.rowcount))

        if factorType == '50008':
            sqlStr = 'SELECT LatestSuitSum FROM `event-data-jy`.lc_suitarbitration where CompanyCode =%s  and InfoPublDate>= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 1 MONTH) order by InfoPublDate desc' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result=self.cursorJY.fetchall()
            s=0
            v = [x[0] for x in result]   #第一列的值
            for i in v:
                if float(i)>float(SEWithoutMI)*0.05:
                    s=s+1
            print (secuCode + ' 证券的【50008】诉讼仲裁----[近1个月仲裁涉案数涉及金额超过净资产5% 的次数] 是：  ' + str(s))

        if factorType == '50009':
            sqlStr = 'SELECT SEWithoutMI FROM lc_maindatanew where CompanyCode = %s and EndDate=\'2017-12-31 00:00:00\' order by EndDate desc,Mark' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            SEWithoutMIbefore = result[0][0]  # 上一年净资产
            print (secuCode + ' 证券的【50009】净资产锐减----[净资产/上年末净资产*100%] 是：  ' + str(SEWithoutMI/SEWithoutMIbefore))

        if factorType == '50010':
            sqlStr = 'SELECT OpinionType FROM lc_auditopinion where InfoSource = \'年度报告\' and CompanyCode = %s ORDER BY EndDate DESC;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            if result[0][0]==1:
                print (secuCode + ' 证券的【50010】审计意见----[是否无保留意见0或1] 是：无保留意见, 0')
            else:
                print (secuCode + ' 证券的【50010】审计意见----[是否无保留意见0或1] 是：有保留意见, 1')

        if factorType == '50011':
            sqlStr = 'SELECT SpecialTradeType FROM lc_specialtrade where InnerCode = %s order by InfoPublDate desc;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            print (result[0][0])
            if result[0][0] in(1,5,7,8,9,10):
                print (secuCode + ' 证券的【50011】退市风险----[存0或1，添加st或取消st] 是：有退市风险，存1')
            else:
                print (secuCode + ' 证券的【50011】审计意见----[是否无保留意见0或1] 是：无退市风险， 存0')

        if factorType == '50012':
            sqlStr = 'SELECT DebtAssetsRatio,EndDate FROM lc_mainindexnew where CompanyCode = %s and EndDate>\'2017-01-01 00:00:00\' order by EndDate desc;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50012】资产负债率----[存资产负债率值] 是：   ' + str(result[0][0]))
        if factorType == '50013':
            print (secuCode + ' 证券的【50013】经营性现金流----[经营活动产生的现金流量净额/营业收入*100%] 是：  '  +str(format(Decimal(NetOperateCashFlow*100/OperatingReenue), '.5f')))
        if factorType == '50014':
            print (secuCode + ' 证券的【50014】应收账款----[应收账款/营业收入*100%] 是：  ' +str(format(Decimal(AccountReceivables*100/OperatingReenue), '.5f')))
        if factorType == '50015':
            sqlStr = 'select NetProfit,InfoSource,EndDate,Mark from LC_QIncomeStatementNew where CompanyCode = %s and InfoPublDate >\'2017-01-01 00:00:00\' GROUP BY EndDate,NetProfit order by EndDate desc,Mark;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50015】业绩实亏----[当前时间前4个季度的净利润相加] 是：   ' + str(result[0][0]+result[1][0]+result[2][0]+result[3][0]))

        if factorType == '50016':
            sqlStr = 'SELECT InteBearDebtToTotalCapital,EndDate FROM lc_mainindexnew where CompanyCode = %s and EndDate>\'2017-01-01 00:00:00\' order by EndDate desc;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50016】带息债务/全部投入资本----[存带息债务/全部投入资本的值] 是：   ' + str(result[0][0]))

        if factorType == '50017':
            #去掉了重复的记录的情况
            sqlStr = 'SELECT * FROM lc_performanceforecast where Forcasttype in(1,7,8,18)  and CompanyCode = %s and InfoPublDate>= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 3 MONTH) GROUP BY InfoPublDate,EndDate;' % str(companyCode[0][0])
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50017】业绩预亏----[近三个月出现业绩出现业绩预亏次数] 是：   ' + str(self.cursorJY.rowcount))

        if factorType == '50018':
            # 查询解禁股本、总股本
            sqlStr = 'SELECT NewMarketableAShares,TotalAShares FROM lc_sharesfloatingschedule where CompanyCode = %s and StartDateForFloating <= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL + 1 MONTH) and StartDateForFloating >= \'2018-07-26 00:00:00\' order by InfoPublDate desc;' % str( \
                companyCode)
            self.cursorJY.execute(sqlStr)
            result = self.cursorJY.fetchall()
            sum=0
            v = [x[0] for x in result]
            for i in v:
                sum=sum+i
            print (secuCode + ' 证券的【50018】限售股解禁----[未来一个月解禁股票数/总股本*100%] 是：   ' + str(format(Decimal(sum*100/result[0][1]), '.5f')))

        if factorType == '50019':
            #查询大股东、高管减持数量
            print (companyName)
            sqlStr = 'select F5_1842 from TB_OBJECT_1842  where F2_1842 like \'%TCL%\' and RP_GEN_DATETIME >= DATE_ADD(\'2018-07-25 00:00:00\',INTERVAL - 3 MONTH);'
            self.cursorWD.execute(sqlStr)
            result = self.cursorWD.fetchall()
            sum=0
            v = [x[0] for x in result]
            for i in v:
                sum=sum+i

            # 查询总股本
            sqlStr = 'SELECT TotalShares,XGRQ,EndDate,InfoPublDate FROM lc_newestsharestru where CompanyCode =%s order by EndDate desc;'% str(companyCode)
            self.cursorJY.execute(sqlStr)
            TotalShares = self.cursorJY.fetchall()

            print (secuCode + ' 证券的【50019】大股东及高管减持----[过去三个月减持数/总股本*100%（要算复权） 是：   ' + str(format(Decimal(sum*100/TotalShares[0][0]), '.7f')))

        if factorType == '50020':
            sqlStr = 'SELECT COUNT(CompanyCode) FROM lc_greatevents where InfoSource like \'%平仓%\' and InfoSource not like \'%消除%\' and InfoSource not like \'%解除%\' and  InfoSource not like \'%交易平仓%\' and CompanyCode = %s and InfoPublDate>= DATE_ADD(\'2018-07-26 00:00:00\',INTERVAL - 1 YEAR) order by InfoPublDate desc;'% str(companyCode).decode('utf8')
            self.cursorJY.execute(sqlStr)
            self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50020】平仓风险----[1年内平仓风险] 是：   ' + str(self.cursorJY.rowcount))

        if factorType == '50021':
            # 查询总股本
            sqlStr = 'select * from  stocknegativenews where WINDCODES like \'%s%\' and MKTSENTIMENTS LIKE \'%负面%\' and OPDATE >=DATE_ADD(\'2018-07-25 00:00:00\',INTERVAL - 1 MONTH);'% str(companyCode)
            self.cursorJY.execute(sqlStr)
            self.cursorJY.fetchall()
            print (secuCode + ' 证券的【50021】舆论警讯----[每日前21个交易日的负面新闻个数/上市公司总市值] 是：   ' +str(self.cursorJY.rowcount))

        self.cursorJY.close()
        self.connJY.close()
        self.cursorWD.close()
        self.connWD.close()

if __name__ == '__main__':
    cal = calcFactor()
    '''
    cal.calcFactor('600382','50001')
    cal.calcFactor('000100','50002')
    cal.calcFactor('000100', '50003')
    cal.calcFactor('600236', '50004')
    #cal.calcFactor('000507', '50005')   #WDDB
    
    cal.calcFactor('000507', '50007')
    cal.calcFactor('601558', '50008')
    cal.calcFactor('601558', '50009')
    cal.calcFactor('000100', '50010')
    cal.calcFactor('000100', '50011')
    cal.calcFactor('000100', '50012')
    cal.calcFactor('000100', '50013')
    cal.calcFactor('000100', '50014')
    cal.calcFactor('000100', '50015')
    cal.calcFactor('000100', '50016')
    cal.calcFactor('002592', '50017')   # 要验证有两条数据的情况 companyCode=150858
    cal.calcFactor('603880', '50018')   # 要验证有两条数据的情况 companyCode=175296
    cal.calcFactor('603880', '50019')
    cal.calcFactor('300216', '50020')
    cal.calcFactor('000100', '50021')    
'''

    cal.calcFactor('300216', '50021')




