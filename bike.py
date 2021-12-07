# -*- coding: utf-8 -*- 

# 폴더안에 있는 csv 파일들을  하나의 데이터프레임으로 합치는 작업
import pandas as pd
import os 
import collections as co 
path = '/Users/ilho/Desktop/학교수업/2021-2학기/빅데이터프로그래밍/데이터/'
file_list = os.listdir(path)

file_list_py = [file for file in file_list if file.endswith('.csv')]
total=co.deque([])  
for i in file_list_py:
    print(i)
    data = pd.read_csv(path + i,header=None)
    print(len(data))
    total.append(data)
final_data = pd.concat(total) 

#데이터 전처리 시작

final_data = final_data.astype({'자전거번호':'string',"대여일시":'string','대여소번호':'string','대여대여소명':'string','반납일시':'string'
                         ,'반납대여소번호':'string','반납대여소명':'string'})

#nan값이 포함된 모든 레코드 제거
final_data= final_data.dropna(axis=0)
# '와"제거
def forReplace(x):
    x=x.replace("'","").replace('"','')
    return x
final_data['자전거번호']=final_data['자전거번호'].apply(forReplace)
final_data['대여일시']=final_data['대여일시'].apply(forReplace)
final_data['대여소번호']=final_data['대여소번호'].apply(forReplace)
final_data['대여대여소명']=final_data['대여대여소명'].apply(forReplace)
final_data['반납일시']=final_data['반납일시'].apply(forReplace)
final_data['반납대여소번호']=final_data['반납대여소번호'].apply(forReplace)
final_data['반납대여소명']=final_data['반납대여소명'].apply(forReplace)

# 자전거번호에  번호가 아닌 것이 포함된 레코드 제거
idx=final_data[final_data['자전거번호']=='자전거번호'].index
final_data=final_data.drop(idx)

#날짜 포멧 통일 
import datetime
def cdate(x):
    if len(x)>17:
        x = x[0:-3]
    x= x.replace('.','-')
    format = '%Y-%m-%d %H:%M'
    x=datetime.datetime.strptime(x,format)
    return x
final_data['대여일시']=final_data['대여일시'].apply(cdate)
final_data['반납일시']=final_data['반납일시'].apply(cdate)

final_data=final_data.astype({'자전거번호':'string','대여대여소명':'string','반납대여소명':'string'})
# 대여소번호 말고 이름으로 존재하는 레코드들 제거
idx=final_data[final_data['대여소번호']=='상암센터 정비실'].index
final_data=final_data.drop(idx)
idx1=final_data[final_data['대여소번호']=='위트콤공장'].index
final_data=final_data.drop(idx1)
idx2=final_data[final_data['대여소번호']=='중랑센터'].index
final_data=final_data.drop(idx2)
idx3=final_data[final_data['대여소번호']=='위트콤'].index
final_data=final_data.drop(idx3)
idx4=final_data[final_data['대여소번호']=='중랑정비팀test 1005'].index
final_data=final_data.drop(idx4)
idx=final_data[final_data['반납대여소번호']=='상암센터 정비실'].index
final_data=final_data.drop(idx)
idx1=final_data[final_data['반납대여소번호']=='위트콤공장'].index
final_data=final_data.drop(idx1)
idx2=final_data[final_data['반납대여소번호']=='중랑센터'].index
final_data=final_data.drop(idx2)
idx3=final_data[final_data['반납대여소번호']=='위트콤'].index
final_data=final_data.drop(idx3)
idx4=final_data[final_data['반납대여소번호']=='중랑정비팀test 1005'].index
final_data=final_data.drop(idx4)

#마지막으로 데이터 타입 지정
final_data=final_data.astype({'대여소번호':'float'})
final_data=final_data.astype({'대여소번호':'int'})
final_data=final_data.astype({'반납대여소번호':'float'})
final_data=final_data.astype({'반납대여소번호':'int'})
final_data=final_data.astype({'이용시간':'float'})
final_data=final_data.astype({'이용시간':'int'})
final_data=final_data.astype({'이용거리':'float'})
final_data=final_data.astype({'이용거리':'int'})
final_data=final_data.astype({'대여거치대':'float'})
final_data=final_data.astype({'대여거치대':'int'})
final_data=final_data.astype({'반납거치대':'float'})
final_data=final_data.astype({'반납거치대':'int'})

#csv저장
final_data.to_csv('/Users/ilho/Desktop/학교수업/2021-2학기/빅데이터프로그래밍/데이터/final_bike.csv',encoding='utf-8',index=False)
