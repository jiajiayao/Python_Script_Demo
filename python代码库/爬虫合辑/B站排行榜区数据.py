import bs4,requests
import openpyxl
url="https://www.bilibili.com/ranking"
res=requests.get(url)
res.encoding='utf-8'
soup=bs4.BeautifulSoup(res.text,"html.parser")

#print(soup.text)
targets=soup.find_all(class_="rank-item")
wb=openpyxl.Workbook()
ws=wb.worksheets[0]
#print(targets)
lin =["排序","作品名称","播放量","up主"]
ws.append(lin)
for each in targets:
    num=each.find(class_="num").text
    print(num)
    print("稿件名称：")
    name=each.findAll("a")[1].text
    print(name)
    times=each.findAll('span')[0].text
    print(times)
    print("up主：")
    up=each.findAll('span')[2].text
    print(up)
    line=[num,name,times,up]
    ws.append(line)
    wb.save('234.xls')
