from os import listdir,getenv,walk
from genericpath import getctime
from json import load
from msvcrt import getch
from time import sleep
#输入需求
path=f'{getenv('APPDATA')}\\ETS'
homeworklist=listdir(path)
newestn=0
newestdate=0
for i in range(len(homeworklist)):
    print(f'{i}.',homeworklist[i])
    if newestdate<getctime(path+'\\'+homeworklist[i]):
        newestn=i
        newestdate=getctime(path+'\\'+homeworklist[i])
print(f'最新试卷:{newestn}')
print('选择要解析的试卷')
path+=f'\\{homeworklist[int(input())]}'

#获取json dict
data=[]
ls1=0#判断是否为第一个
ls2=0#计数
for i,j,k in walk(path):
    #print(i)
    if i[-6]=='e':
        break
    if i[-1]!='l' and ls1:
        #file.append(open(i+'\\content.json','r').read())
        with open(i+'\\content2.json','r',encoding='utf-8') as op:
            data.append(load(op))
    ls1=1
    ls2+=1
    if ls2>=21:
        break

#print(data[4]['info']['question'][0]['ask'][0])

#解析
choose=[]
role=[]
picture=[]
for i in data:
    if i['structure_type']=='collector.choose':
        diary={"num":int(i['info']['xtlist'][0]['xt_nr'][0]),
               'ans1':i['info']['xtlist'][0]['answer'],
               'ans2':i['info']['xtlist'][1]['answer']}
        choose.append(diary)
    elif i['structure_type']=='collector.role':
        if len(i['info']['question'])==1:
            diary={"num":int(i['info']['question'][0]['ask'][0]),
                   'ans1':i['info']['question'][0]['std'][0]['value']}
        else:
            diary={"num":int(i['info']['question'][0]['ask'][0]),
                   'ans1':i['info']['question'][0]['std'][0]['value'],
                   'ans2':i['info']['question'][1]['std'][1]['value']}
        role.append(diary)
    elif i['structure_type']=='collector.picture':
        diary={'ans1':i['info']['std'][0]['value']}
        picture.append(diary)
choose=sorted(choose,key=lambda x:x['num'])
role=sorted(role,key=lambda x:x['num'])

#输出
print('听后选择:')
if len(choose)==0:
    print('    无')
for i in choose:
    print(f'    {i["num"]}.{i["ans1"]}')
    print(f'    {i["num"]+1}.{i["ans2"]}')
print('听后回答：')
if len(role)==0:
    print('    无')
for i in role:
    print(f'    {i["num"]}.{i["ans1"]}')
    if 'ans2' in i:
        print(f'    {i["num"]+1}.{i["ans2"]}')
print('听后转述：')
if len(picture)==0:
    print('    无')
for i in picture:
    print(f'    {i["ans1"]}')


print('请按任意键退出...')
getch()
