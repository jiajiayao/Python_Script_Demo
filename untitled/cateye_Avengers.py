import requests
import time
import csv
headers_url={'User-Agent':
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/74.0.3729.131 Safari/537.36'}
#返回评论数据api
com_url="http://m.maoyan.com/mmdb/comments/movie/248172.json?_v_=yes&startTime=2019-05-05%2015%3A19%3A05&offset="
def get_com(url):
    res=get_res(url)
    return res
def  get_res(url):
    mv_id=0
    params_url = {
        '_v_': 'yes',
        'startTime': '2019-05-06%2015%3A19%3A05',
        'offset': mv_id # 视频id
    }
    global com_url
    data=[]
    data.append(["昵称","评论","时间"])
    url=com_url+'0'
    while(1):
        res=res=requests.get(url,headers=headers_url).json()
        total=res['total']
        if total==0:
            break
        cmts=res['cmts']
        for each in cmts:
            nickName=each['nickName']
            content=each['content']
            startTime=each['startTime']
            data.append([nickName,content,startTime])
        data.append(mv_id)
        print("第%d页"%mv_id)
        url=com_url+str(mv_id)
        mv_id=mv_id+1
    return data
def main():
    result=get_com(com_url)
    with open("233444444.txt","w",encoding="utf-8")as f:
        for each in result:
            f.write(str(each)+"\n")
if __name__ == '__main__':
    main()