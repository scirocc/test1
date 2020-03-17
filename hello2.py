import sys,datetime,time
# sys.path.append('D:/Tinysoft/Analyse.NET')
sys.path.append('D:/Program Files/Tinysoft/Analyse.NET')

import TSLPy3 as ts
import cx_Oracle as cx

def transit(time_of_tianruan_style):
    beginT = datetime.datetime.strptime('18991230000000', '%Y%m%d%H%M%S')
    beginT+=datetime.timedelta(time_of_tianruan_style)
    beginT=datetime.datetime.strftime(beginT,"%Y%m%d%H%M%S")
    return(beginT)

def get_sCode_sDate(sDate):
    while True:
        ts.ConnectServer('211.100.23.205', 443)
        # ts.LoginServer('chancehunt', 'chnchnt')
        ts.LoginServer('fuchunguang', 'Fcg=888888')
        if ts.Logined() == True:
            print('已登录')
            # sql = 'stocks:=GetBk(\'上证A股;深证A股;创业板;中小企业板\');return stocks;'
            # result = (ts.RemoteExecute(sql, {}))[1]
            sCode = []
            # for data in result:
            #     sCode.append(data.decode('utf8'))
            # sCode.append('IF01')
            sCode.append('IC00')
            # sCode.append('IH01')
            # sCode.append('SH000016')
            sCode.append('SH000905')
            ts.Disconnect()
            break
    return(sCode)


def getData(sCode,sDate):
    while True:
        ts.ConnectServer('211.100.23.205', 443)
        ts.LoginServer('fuchunguang', 'Fcg=888888')
        if ts.Logined() == True:
            print('已登录')
            daycount = 0
            for code in sCode:
                #########deal min1
                hCodeInfo1min={}
                with open('./{}_5s.csv'.format(code),'w')as f:
                    f.write('code,mtime,open,high,low,close,vol,amount\n')
                    for date in sDate:
                        daycount += 1
                        # sql = 'setsysparam(pn_stock(),\'{}\');' \
                        #       'setsysparam(PN_Cycle(), cy_1m());setsysparam(pn_date(),inttodate({}));' \
                        #       'return nday({},"mdate",datetimetostr(sp_time()),"open",Open(),"high",High(),"low",Low(),"close",Close(),"vol",Vol(),"amount",Amount());' \
                        #     .format(code, date, 240)  # 240个正好是一天
                        sql = 'setsysparam(pn_stock(),\'{}\');' \
                              'setsysparam(PN_Cycle(), cy_5s());setsysparam(pn_date(),inttodate({}));' \
                              'return nday({},"mdate",datetimetostr(sp_time()),"open",Open(),"high",High(),"low",Low(),"close",Close(),"vol",Vol(),"amount",Amount());' \
                            .format(code, date, 2880)  # 240个正好是一天
                        result = (ts.RemoteExecute(sql, {}))[1]
                        if result:
                            for data in result:
                                temp = data[b'mdate'].decode('gbk').replace(':', '').replace('-', '').replace(' ', '')
                                if temp[:4]=='2019' or temp[:4]=='2020':
                                    print(data[b'vol'])
                                    f.write('{},{},{},{},{},{},{},{}\n'.format(code,
                                                                       temp,
                                                                       data[b'open'],
                                                                       data[b'high'],
                                                                       data[b'low'],
                                                                        data[b'close'],
                                                                        data[b'vol'],
                                                                        data[b'amount']))
                                    print('{},{},{},{},{},{},{},{}\n'.format(code,
                                                                       temp,
                                                                       data[b'open'],
                                                                       data[b'high'],
                                                                       data[b'low'],
                                                                        data[b'close'],
                                                                        data[b'vol'],
                                                                        data[b'amount']))
            ts.Disconnect()
            break
        else:
            print('天软未登录')
    return 0

def get_sDate():
    x=20190101
    sDate=[20190101]
    beginT=datetime.datetime.strptime('20190101',"%Y%m%d")
    while True:
        beginT+=datetime.timedelta(days=1)
        if beginT>datetime.datetime.strptime('20200311',"%Y%m%d"):
            break
        else:
            sDate.append(int(datetime.datetime.strftime(beginT,"%Y%m%d")))
    print(sDate)
    return(sDate)

def main(day):
    sDate=get_sDate()
    sCode = get_sCode_sDate(sDate)
    getData(sCode, sDate)

main(1)