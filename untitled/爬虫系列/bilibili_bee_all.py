import requests
import bs4
import json

def get_result(url,params):
    headers_url = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/74.0.3729.131 Safari/537.36'}
    print("请求的url为:%s"%url)
    res=requests.get(url,headers=headers_url,params=params,timeout=10)
    return res
############导入和导出##########
#导出类
#导出txt
def out_txt(data,name):
    with open(name+".txt","w",encoding="utf-8")as f:
        for each in data:
            f.write(str(each)+'\n')

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

############搜素###############
#导出主站搜素的结果--目前为导出av号
def get_search(words,pagecount):
    print("搜素的词为：%s"%words)
    url='https://search.bilibili.com/all'
    data=[]
    for i in range(pagecount):
        print('第%d页'%(i+1))
        params={
        'keyword':words,#输入的搜素类容
        'order': 'click',#排序方式--最多点击
        'duration': '0',#视频时长
        'tids_1': '0',#分区
        'page': i+1,#页数
        }
        res=get_result(url,params)
        item_data=get_search_data(res)
        for each in item_data:
            data.append(each)
    out_txt(data,'搜素'+words+'结果'+str(pagecount)+'页')
    print(data)
    print(len(data))

def get_search_data(res):
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    avs=[]
    targerts=soup.find_all('span',class_='type avid')
    for each in targerts:
        avs.append(each.text)
    print(avs)
    titles=[]
    looks=[]
    targerts=soup.find_all('span',class_="so-icon watch-num")
    for each in targerts:
        looks.append(each.text.split())
    times=[]
    targerts=soup.find_all('span',class_='so-icon time')
    for each in targerts:
        times.append(each.text.split())
    print(times)
    ups=[]
    ##########
    data=[]
    for i in range(len(times)):
        data.append({'av':avs[i],'time':times[i],'look':looks[i]})
    print(data)
    return data
    #print(soup)
##############################
#############评论-############

def main():
    #get_search('复仇者联盟',50)
    search_data=opean_txt('搜素复仇者联盟结果50页.txt')
    avs=[]
    for each in search_data:
        avs.append(each['av'])
    print(avs)
if __name__ == '__main__':
    main()

