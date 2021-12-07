# -*- coding: utf-8 -*- 

from urllib.request import Request, urlopen 
from urllib.parse import urlencode, quote_plus
import pandas as pd
from pandas.io.json import json_normalize
import json
def mydata(n,y):
    page = n
    year = y
    url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
    service_key='LKjo8XF5txX8H22lwnkS8JvF9z2QjkZSYwqkTDBUHJIFyS4inE6miPybyMUmQtYHWINNMGlVxIkDFDyUjbvpXw=='
    queryParams = '?' + urlencode({quote_plus('ServiceKey') : service_key,
                                   quote_plus('pageNo') : page,
                                   quote_plus('numOfRows') : 500,
                                   quote_plus('dataType') : 'JSON', 
                                   quote_plus('dataCd') : 'ASOS', 
                                   quote_plus('dateCd') : 'HR',
                                   quote_plus('startDt') : str(year)+'0101',
                                   quote_plus('startHh') : '01', 
                                   quote_plus('endDt') : str(year+1)+'0101', 
                                   quote_plus('endHh') : '01', 
                                   quote_plus('stnIds') : '108' })
    response = urlopen(url + queryParams) 
    json_api = response.read().decode("utf-8")
    json_file = json.loads(json_api)
    df=pd.json_normalize(json_file['response']['body']['items']['item'])
    rows = json_file['response']['body']['numOfRows']
    total = json_file['response']['body']['totalCount']
    if page*rows<total:
        return pd.concat([df,mydata(page+1,year)])
    else:
        return df

data1 = mydata(1,2014)
data2 = mydata(1,2015)
data3 = mydata(1,2016)
data4 = mydata(1,2017)
data5 = mydata(1,2018)
data6 = mydata(1,2019)
data7 = mydata(1,2020)
data = pd.concat([data1,data2,data3,data4,data5,data6,data7])
data = data.loc[:,['tm','ta','rn','dsnw']]
data=data.fillna(0)
data=data.astype({'ta':'int','rn':'int','dsnw':'int'})
import datetime

def cdate(x):
    format = '%Y-%m-%d %H:%M'
    x=datetime.datetime.strptime(x,format)
    return x
data['tm']=data['tm'].apply(cdate)
data.to_csv('final_weather.csv',index=False)