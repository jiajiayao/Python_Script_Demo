import requests
import bs4

def opeanurl(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    res=requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    return res
def find_depth(res):
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    depth=soup.find('span',class_="next").previous_sibling.previous_sibling.text
    return depth
def main():
    url_t2="https://www.bilibili.com/ranking"
    urs_t1="https://www.taobao.com"
    url="https://movie.douban.com/top250"
    res=opeanurl(url)
    depth=find_depth(res)
    print(depth)
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    #print(soup.text)


if __name__ == '__main__':
    main()