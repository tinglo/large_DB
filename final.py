import requests
import time
import datetime
from bs4 import BeautifulSoup

req=requests.get('http://www.stockq.org/stock/history/')
soup=BeautifulSoup(req.content.decode("utf-8"),'html.parser')

ISOTIMEFORMAT='%Y-%m-%d-%X-%a'
total=time.strftime(ISOTIMEFORMAT,time.localtime())
total_split=total.split('-')
year=total_split[0]
mon=total_split[1]
day=total_split[2]
week=total_split[4]

timing=total_split[3]
timing_split=timing.split(':')
connect=''
count=1
result_name=[]
result_total=[]
result_updown=[]
result_persent=[]
result_time=[]
post=[]
num_list=[]
def get_date(count):
        yday=datetime.date.today() - datetime.timedelta(days=count)
        arr=yday.strftime(ISOTIMEFORMAT)
        return arr
while True:
        connect='/stock/history/'+year+'/'+mon+'/'+year+mon+day+'_tc.php'
        name=soup.find("a",{"href":connect})
        if int(timing_split[0])>=18 or int(timing_split[0])<7:
                if week=='Sat':
                        total3=get_date(1)
                if week=='Sun':
                        total3=get_date(2)
                if week !='Sat' and week !='Sun':
                        total3=get_date(0)
                total3_split=total3.split('-')
                year=total3_split[0]
                mon=total3_split[1]
                day=total3_split[2]
                name='sth'
                connect=''
        if name==None:
#                yday=datetime.date.today() - datetime.timedelta(days=count)
#                total2=yday.strftime(ISOTIMEFORMAT)
#                total_split2=total2.split('-')
                total2=get_date(count)
                total_split2=total2.split('-')
                year=total_split2[0]
                mon=total_split2[1]
                day=total_split2[2]
                count+=1
        else:
                print(year,end='-')
                print(mon,end='-')
                print(day)
                req2=requests.get('http://www.stockq.org'+connect)
                soup2=BeautifulSoup(req2.content.decode("utf-8"),'html.parser')
                name2=soup2.find("table",{"class":"marketdatatable"})
                split=name2.text.split('\n')
                for item in range(0,31,1):
                        persent_split=split[11+7*item+3].split('%')
                        num_list.append(str(float(persent_split[0])))
                        post.append(split[11+7*item]+' '+str(split[11+7*item+1])+' '+str(float(split[11+7*item+2]))+' '+str(float(persent_split[0]))+'%'+' '+str(split[11+7*item+4]))
                break

num_list=[float(x) for x in num_list]
sort_list=sorted(num_list)
bottom=0
#print(post)
print(sort_list)
def get_list(test_list, result_list):
        top=0
        for x in test_list:
                if top==5:
                        return result_list
                for y in post:
                        post_split=y.split(' ')
                        ss=post_split[3]
                        s=ss.split('%')
 #                       if x==float(s[0]):
                        if x==float(s[0]):
                                save=0
                                for i in result_list:
                                        item_split=i.split(' ')                                
                                        if post_split[0] == item_split[0] :
                                                save=1
                                                break  
                                if save==0:
                                        result_list.append(y)
                                        top+=1
                                        break
              #  break
best=[]
worst=[]
worst=get_list(sort_list,worst)
sort_list.reverse()
best=get_list(sort_list,best)
#print(best)
#print(worst)
print(best)
print(worst)
best.extend(worst)
ok=0
for a in best:
        print(a)
        payload={'robot_id':'108143422899450' , 'content': a , 'lng':'123','lat':'123' }
        req2=requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
        if req2.status_code == 200:
                ok+=1
print(ok)

