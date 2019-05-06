import requests
import json
import time, datetime
import openpyxl
import csv
wb = openpyxl.Workbook()
ws = wb.worksheets[0]
ws.append(['name','type','value','date'])
headers_url={'User-Agent':
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/74.0.3729.131 Safari/537.36'}
def get_dm_av(url):
    res = requests.get(url,headers=headers_url).json()['result']['main_section']['episodes']
    data=[]
    for each in res:
        data.append(each['aid'])

    return data
#返回的结果
result_back=[]
#返回评论数据api
com_url="https://api.bilibili.com/x/v2/reply"
num_yihua=0
num_ernai=0
num_sanjiu=0
num_siyue=0
num_wuyue=0
#返回评论的页数
def get_depth(av_id):
    params_url={
        'jsonp': 'jsonp',
          # 页数从0开始的所以要+1
        'type': '1',
        'oid': av_id,  # 视频id
        'sort': '0'
    }
    res=requests.get(com_url,params=params_url,headers=headers_url,timeout=1).json()['data']['page']
    count=res['count']
    size=res['size']
    acount=res['acount']
    depth=count/size
    if depth>int(depth):
        depth=int(depth)+1
    print("共%d页 共%d条"%(depth,acount))

    return depth

#获取评论
def get_commment(av_id):
    global result_back
    depth=get_depth(av_id)
    #depth=20
    result=[]
    for i in range(depth):
        try:
            print("第%d页"%(i+1))
            params_url = {
                'jsonp': 'jsonp',
                # 页数从0开始的所以要+1
                'type': '1',
                'pn':i+1,
                'oid': av_id,  # 视频id
                'sort': '0'
            }

            res = requests.get(com_url, params=params_url, headers=headers_url, timeout=1).json()['data']['replies']
            for comment in res:
                try:
                    # 第一层的回复
                    _time = comment['ctime']
                    timeArray = time.localtime(_time)
                    _time = time.strftime("%Y/%m/%d", timeArray)

                    rep_a = comment['content']['message']
                    # 用户相关
                    rep_user = comment['member']
                    name = rep_user['uname']
                    sex = rep_user['sex']
                    lever = rep_user['level_info']['current_level']
                    # print(_time)

                    result_back.append([name, sex, lever, rep_a, _time])
                    #print(comment['replies'])
                    if str(comment['replies'])!='None':
                        t=comment['replies']
                        #print("评论区深入\n")
                    #print(len(t))
                    #print(t)
                        for j in range(len(t)):

                            _time = t[j]['ctime']
                            timeArray = time.localtime(_time)
                            _time = time.strftime("%Y/%m/%d", timeArray)
                            #print(_time)
                            rep_user = t[j]['member']
                            name = rep_user['uname']
                            sex = rep_user['sex']
                            lever = rep_user['level_info']['current_level']
                            rep_b=t[j]['content']['message']
                            result_back.append([name,sex,lever,rep_b,_time])
                except:
                    print("爬取失败")
                    continue
        except:
            print("爬取错误第%d页"%i)
            continue
    return result_back
def out_txt(result):
    with open(str(av_id)+".txt","w",encoding="utf-8")as f:
        for each in result:
            f.write(str(each)+'\n')

def sm_analyse(result):
    global num_yihua
    global num_ernai
    global num_sanjiu
    global num_siyue
    global num_wuyue
    data=[]
    head=["name","type","value","date"]
    for each in result:
        words=each[0]
        num_yihua=word_count_in_str(words,'一花')
        data.append(['一花-评论','一花',num_yihua,each[1]])
        num_ernai=word_count_in_str(words,'二乃')
        data.append(['二乃-评论', '二乃', num_ernai, each[1]])
        num_sanjiu=word_count_in_str(words,'三玖')
        data.append(['三玖-评论', '三玖', num_sanjiu, each[1]])
        num_siyue=word_count_in_str(words,'四叶')
        data.append(['四叶-评论', '四叶', num_siyue, each[1]])
        num_wuyue=word_count_in_str(words,'五月')
        data.append(['五月-评论', '五月', num_wuyue, each[1]])
    print(data)
    with open("五等分的花嫁评论_day.csv", 'w',newline='',encoding='utf8') as t:  # numline是来控制空的行数的
        writer = csv.writer(t)  # 这一步是创建一个csv的写入器（个人理解）
        writer.writerow(head)  # 写入标签
        writer.writerows(data)  # 写入样本数据
        #print(each[3])
    #count=num_wuyue+num_siyue+num_sanjiu+num_ernai+num_yihua
    #print("一花：%0.2f%%二乃：%0.2f%%三玖：%0.2f%%四叶：%0.2f%%五月：%0.2f%%" % (num_yihua/count*100, num_ernai/count*100, num_sanjiu/count*100, num_siyue/count*100, num_wuyue/count*100))
    #print("一花：%d二乃：%d三玖：%d四叶：%d五月：%d"%(num_yihua,num_ernai,num_sanjiu,num_siyue,num_wuyue))
    #ws.append([page_cout,num_yihua/count*100, num_ernai/count*100, num_sanjiu/count*100, num_siyue/count*100, num_wuyue/count*100])

def word_count_in_str(string, keyword):
    return len(string.split(keyword))-1
def time_data(result):
    time_key=[]
    for each in result:
        time_key.append(each[4])
    time_key=list(set(time_key))
    time_key=sorted(time_key)
    comment=[]
    for each in time_key:
        temp=''
        for item in result:
            if each==item[4]:
                temp+=item[3]
        comment.append([temp,each])
    #print(comment)
    #print(time_key)
    return comment

if __name__ == '__main__':
    avs=get_dm_av("https://api.bilibili.com/pgc/web/season/section?season_id=26283")
    t=0
    print("获取番剧av号")
    for each in avs:
        t+=get_depth(each)
    print(t)
    i=0
    print("爬取中。。。")
    for each in avs:
        try:
            i=i+1
            print("第%d集："%i)
            res=get_commment(each)
        except:
            print("爬取失败第%d集av %s"%(i,each))
            print(res)
            result = time_data(res)
            # 评论加时间
            print(result)
            sm_analyse(result)
            continue



    #print(res)
    result=time_data(res)
    #评论加时间
    print(result)
    sm_analyse(result)
    #print(len(result))
    #wb.save(str(av_id)+".csv")
    #sm_analyse(result)

