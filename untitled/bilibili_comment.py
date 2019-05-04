import requests
import json
import bs4
headers_url={'User-Agent':
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/74.0.3729.131 Safari/537.36'}
#返回评论数据api
com_url="https://api.bilibili.com/x/v2/reply"

#返回评论的页数
def get_depth(av_id):
    params_url={
        'jsonp': 'jsonp',
          # 页数从0开始的所以要+1
        'type': '1',
        'oid': av_id,  # 视频id
        'sort': '0'
    }
    res=requests.get(com_url,params=params_url,headers=headers_url).json()['data']['page']
    count=res['count']
    size=res['size']
    depth=count/size
    if depth>int(depth):
        depth=int(depth)+1
    print("共%d页"%depth)

    return depth

#获取评论
def get_commment(av_id):
    depth=get_depth(av_id)
    result=[]
    for i in range(depth):
        print("第%d页"%(i+1))
        params_url = {
            'jsonp': 'jsonp',
            # 页数从0开始的所以要+1
            'type': '1',
            'pn':i+1,
            'oid': av_id,  # 视频id
            'sort': '1'
        }
        res = requests.get(com_url, params=params_url, headers=headers_url).json()['data']['replies']
        for comment in res:
            #第一层的回复
            rep_a=comment['content']['message']
            #用户相关
            rep_user=comment['member']
            name=rep_user['uname']
            sex=rep_user['sex']
            lever=rep_user['level_info']['current_level']

            result.append([name,sex,lever,rep_a])
            try:
                t=comment['replies']
                #print(len(t))
                #print(t)
                for i in range(len(t)):
                    rep_user = t[i]['member']
                    name = rep_user['uname']
                    sex = rep_user['sex']
                    lever = rep_user['level_info']['current_level']
                    rep_b=t[i]['content']['message']
                    result.append([name,sex,lever,rep_b])
            except:
                continue
    print(result)

    with open(str(av_id)+".txt","w",encoding="utf-8")as f:
        for each in result:
            f.write(str(each)+'\n')




if __name__ == '__main__':
    get_commment(50276557)