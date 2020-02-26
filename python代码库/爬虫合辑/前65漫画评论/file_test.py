import requests
import bs4
def get_result(url,params):
    headers_url = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/74.0.3729.131 Safari/537.36'}
    print("请求的url为:%s"%url)
    res=requests.get(url,headers=headers_url,params=params,timeout=10)
    return res
def main():
    res=get_result('https://upload-images.jianshu.io/upload_images/5419313-3363a09e0553cd84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700',{})
    f=open('233.jpg','wb')
    f.write(res.content)
    f.close()
if __name__ == '__main__':
    main()
