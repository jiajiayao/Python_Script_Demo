import bs4
import requests
import json
import csv
def opean_txt(file_name):
    Data = []
    with open(file_name,encoding="utf-8") as txtData:
        lines = txtData.readlines()
        for line in lines:
            lineData = line.strip()  # 去除空白和逗号“,”
            Data.append(eval(lineData))  # 测试数据集

    return Data
def out_csv(data):
    with open("漫画排行_6.csv", 'w',newline='',encoding='utf8') as t:  # numline是来控制空的行数的
        writer = csv.writer(t)  # 这一步是创建一个csv的写入器（个人理解）
        writer.writerow(["name","type","value","date"])  # 写入标签
        writer.writerows(data)  # 写入样本数据
def out_txt(data,name):
    with open(name+".txt","w",encoding="utf-8")as f:
        for each in data:
            f.write(str(each)+'\n')
def post_res(url,cartoon_data):
    headers = {
        'content-type': 'application/json',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/74.0.3729.131 Safari/537.36'
    }
    print(type(cartoon_data))
    res=requests.post(url,data=json.dumps(cartoon_data),headers=headers)
    return res.json()
def main():
    url='http://manga.bilibili.com/twirp/comic.v1.Comic/ClassPage'
    cartoon_data = {
        "style_id": -1,
        "area_id": -1,
        "is_finish": -1,
        "order": 2,
        "page_num": 1,
        "page_size": 69
    }
    res=post_res(url,cartoon_data)['data']
    #res=opean_txt("b站漫画前100.txt")
    cartoons=[]
    for each in res:
        cartoons.append({'title':each['title'],'season_id':each['season_id']})
    print(cartoons)
    #out_txt(cartoons)
    out_txt(cartoons,'b站漫画前69')

if __name__ == '__main__':
    main()
