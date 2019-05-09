import requests
############导入和导出##########
#导出类
#导出txt
def out_txt(data,name):
    with open(name+".txt","w",encoding="utf-8")as f:
        for each in data:
            f.write(str(each)+'\n')
    print('导出%s.txt成功'%name)

#导入类
#导入txt
def opean_txt(file_name):
    Data = []
    with open(file_name,encoding="utf-8") as txtData:
        lines = txtData.readlines()
        for line in lines:
            lineData = line.strip()  # 去除空白和逗号“,”
            Data.append(eval(lineData))  # 测试数据集

    return Data
###############################
def get_target_value(key, dic, tmp_list):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    else:
        for value in dic.values():  # 传入数据不符合则对其value值进行遍历
            if isinstance(value, dict):
                get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list

def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身



def get_result(url,params):
    headers_url = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/74.0.3729.131 Safari/537.36'}
    #print("请求的url为:%s"%url)
    res=requests.get(url,headers=headers_url,params=params,timeout=1)
    return res

def get_depth(av_id):
    params_url={
        'jsonp': 'jsonp',
          # 页数从0开始的所以要+1
        'type': '22',#漫画评论区
        'oid': av_id,  # 视频id
        'sort': '0',
        'nohot': '1'
    }
    com_url = "https://api.bilibili.com/x/v2/reply"
    res=get_result(com_url,params_url).json()['data']['page']
    count=res['count']
    size=res['size']
    acount=res['acount']
    depth=count/size
    if depth>int(depth):
        depth=int(depth)+1
    print("共%d页 共%d条"%(depth,acount))

    return depth

def get_comment(av_id):
    com_url = "https://api.bilibili.com/x/v2/reply"
    depth=get_depth(av_id)
    data=[]
    for i in range(depth):
        params_url = {
            'jsonp': 'jsonp',
            # 页数从0开始的所以要+1
            'type': '22',  # 漫画评论区
            'oid': av_id,  # 视频id
            'sort': '0',
            'nohot': '1',
            'pn': i + 1
        }
        try:
            res=get_result(com_url,params_url).json()
            item = get_target_value('ctime', res['data'], [])
            data.append(item)
        except:
            print("爬取错误第%d页"%i)
            continue
    return data
def oneindata(data):
    t=[]
    for each in data:
        for item in each:
            t.append(item)
    return t
def AnalysisData():

def main():
    #out_txt(get_comment(24793),'五等分的花嫁ctime')
    '''
    out_txt(get_comment(25966), '史莱姆ctime')
    out_txt(get_comment(25717), '鬼灭ctime')
    out_txt(get_comment(26009), '大小姐ctime')
    out_txt(get_comment(25497), 'jojoctime')
    out_txt(get_comment(25504), '斗罗ctime')
    out_txt(get_comment(25447), '英雄学院ctime')
    out_txt(get_comment(25969), '碧蓝ctime')
    out_txt(get_comment(25506), '大师兄ctime')
    out_txt(get_comment(25746), '灵能百分百ctime')
    out_txt(get_comment(25467), '食戟之灵ctime')
    '''
    Name_id=opean_txt('b站漫画前69.txt')
    print(Name_id[1])
    for each in Name_id:
        out_txt(get_comment(each['season_id']),each['title'])
    #data=opean_txt('五等分的花嫁ctime.txt')
    #data_1=oneindata(data)

if __name__ == '__main__':
    main()