#!/usr/bin/python3
#-*- coding:utf-8 -*-
import os
from gotify import gotify
import json
import requests
import sys
# filename = 'akk'
import time

date = sys.argv[1]
# date = 'tmr'
sys_ts = time.time()
if date == 'today':
    timestr = time.strftime('%Y-%m-%d', time.localtime(sys_ts))
elif date == 'tmr':
    timestr = time.strftime('%Y-%m-%d', time.localtime(sys_ts+86400))
urlstr = [
    'https://ms.hljjkfp.com/yyglwebfb/webapi1.ashx?opt=gethosyy&cityid=2301',
    "https://ms.hljjkfp.com/yyglwebfb/webapi1.ashx?opt=gethosyy&cityid=2301&ymcs_id=02"
]

hos_ids = [
    '2301100101', 
    '2301100901',
    "2301100101",
    "2301100111",
    "2301100201",
    "2301100202",
    "2301100301",
    "2301100311",
    "2301100401",
    "2301100403",
    "23011004031",
    "23011004032",
    "2301100411",
    "2301100501",
    "2301100511",
    "2301100601",
    "2301100701",
    "2301100801",
    "2301100901",
    "2301100911",
    "2301100912",
    "2301100913",
    "2301101001",
    "2301101101",
    "2301101201",
    "2301101202",
    "2301101301",
    "2301101401",
    "2301101501",
    "2301101601",
    "2301101611",
    "2301101701",
    "2301101801",
    "2301101901",
    "2301102001",
    "2301102101",
    "2301102102",
    "2301102201",
    "2301102211",
    "2301102212",
    "2301102301",
    "2301102307",
    "2301102308",
    "2301102309",
    "2301102310",
    "2301102311",
    "2301102312"
]

# 市辖区	230101
# 道里区	230102
# 南岗区	230103
# 道外区	230104
# 平房区	230108
# 松北区	230109
# 香坊区	230110
# 呼兰区	230111
# 阿城区	230112
# 双城区	230113
# 依兰县	230123
# 方正县	230124
# 宾县	    230125
# 巴彦县	230126
# 木兰县	230127
# 通河县	230128
# 延寿县	230129
# 尚志市	230183
# 五常市	230184

data = {
    'hos_id':'',
    'yydate':timestr+' 00:00:00:000'
}

header = {
'Host': 'ms.hljjkfp.com',
'Content-Length': '54',
'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="90"',
'Sec-Ch-Ua-Mobile': '?0',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept': '*/*',
'Origin': 'https://ms.hljjkfp.com',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://ms.hljjkfp.com/ymyy/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}
gotify(title='疫苗预约运行开始',message=time.strftime('%H:%M:%S',time.localtime(sys_ts)),priority=3).send()
for i in range(60):
    sum_syhl = 0
    for i in hos_ids:
        title = '日期'+timestr+' 时间'+time.strftime('%H:%M:%S', time.localtime(sys_ts))
        data['hos_id'] = i
        response = requests.post(urlstr[1],data=data,headers = header)
        con=json.loads(response.text)
        result = ''
        count = 1
        if con['ret'] == '1':
            con['data'] = sorted(con['data'],key=lambda x:int(x['yysd']))
            for i in con['data']:
                if date == 'today':
                    time_stamp = time.mktime(time.strptime(timestr+i['yysd_name'][:5], '%Y-%m-%d%H:%M'))
                    if time_stamp < sys_ts:
                        continue
                sum_syhl += i['syhl']
                result += str(count) + '\n'
                #result += '预约地点：' + i['hos_name'] + '\n'
                result += '预约时间：' + i['yysd_name'] + '\n'
                result += '四项参数：' + 'sn:' + str(i['sn']) + ' 号量：' + str(i['hl']) + ' 剩余号量：' + str(i['syhl']) + ' 预约号量:' + str(i['yyhl']) + '\n'
                result += '余下参数：' + '可约第几针：' + i['yycs'] + ' flag:' + i['flag'] + '\n\n'
                count += 1
                if i['syhl'] != 0:
                    result = i['yysd_name']+'可预约！ 余量：'+str(i['syhl'])+'\n'+result
            if '可预约' not in result:
                result = '暂无可预约！\n' + result
                title = '暂无可预约！\n'+title+'\n'+con['data'][0]['hos_name']
    #            gotify(title=title, message=result, priority=3).send()
    #            gotify(title=title, message=result, priority=3, token='AOO4h_LgQJRmK4G').send()
            else:
                title = '可预约！\n'+title+'\n'+con['data'][0]['hos_name']
                gotify(title=title, message=result, priority=10).send()
                gotify(title=title, message=result, priority=10, token='AOO4h_LgQJRmK4G').send()
    if sum_syhl > 10:
        break
    time.sleep(10)
# result =str(strdict)
# print(result)
#else:
#    result = '当日未放号或未能成功查询，请手动检查'
#    gotify(title='疫苗预约定时查询'+timestr, message=result, priority=3).send()
