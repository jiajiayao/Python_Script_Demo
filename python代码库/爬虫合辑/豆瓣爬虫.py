import requests
import bs4
import openpyxl

wb = openpyxl.Workbook()
ws = wb.worksheets[0]
# print(targets)
lin = ["电影", "评分", "资料"]
ws.append(lin)

def exported(a,b,c):
    length=len(a)
    for i in range(length):
        line=[a[i],b[i],c[i]]
        ws.append(line)

def opeanurl(url):
    headers={'User-Agent':
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/74.0.3729.131 Safari/537.36'}
    res=requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    return res
# 总页面数为10
def find_depth(res):
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    depth=soup.find('span',class_="next").previous_sibling.previous_sibling.text
    return int(depth)

def find_movies(res):
    soup=bs4.BeautifulSoup(res.text,'html.parser')

    #电影名
    movies=[]
    targets=soup.find_all("div",class_="hd")
    for each in targets:
        movies.append(each.a.span.text)

    #评分
    ranks=[]
    targets=soup.find_all("span",class_="rating_num")
    for each in targets:
        ranks.append('评分：%s'% each.text)

    #资料
    messages=[]
    targets=soup.find_all("div",class_="bd")
    for each in targets:
        try:
            messages.append(each.p.text.split('\n')[1].strip()+each.p.text.split('\n')[2].strip())
        except:
            continue
   # print(messages)
    exported(movies,ranks,messages)
    result=[]
    length =len(movies)
    for i in range(length):
        result.append(movies[i]+ranks[i]+messages[i]+'\n')

    return result
def main():
    url_t2="https://www.bilibili.com/ranking"
    urs_t1="https://www.taobao.com"
    host="https://movie.douban.com/top250"
    res=opeanurl(host)
    print(opeanurl("https://user.qzone.qq.com/2074688761/main?_t_=0.9995540349303984").text)
    depth=find_depth(res)

    result=[]
    for i in range(depth):
       url=host+'/?start='+str(25*i)
       res=opeanurl(url)
       result.extend(find_movies(res))
    print(result)
    wb.save("豆瓣_t.xlsx")
    with open("233.txt","w",encoding="utf-8")as f:
        for each in result:
            f.write(each)

if __name__ == '__main__':
    main()