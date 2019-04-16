import requests,json,re,os,time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)#禁用ssl警告
from img import ImgToPdf

class Download_free():
    def __init__(self):
        self.target_url=input('输入下载页面网址')
        self.max = 0
        # pdf类型的参数
        self.url_list = []
        self.aid=''
        self.token=''
        self.title=''
        #word类型的参数
        self.f = ''
        self.readLimit= ''
        self.furl = ''
        self.img = ''
        self.headers={'Accept':'*/*',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Connection':'keep-alive',
                    'Host':'view42.book118.com',
                    'Referer':'http://view42.book118.com/',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',}

    def scheduler(self):
        # 清理图片文件夹里残存文件
        self.cleaner('图片')

        self.aid = self.target_url.split('/')[-1].replace('.shtm', '')
        judge_url = 'https://max.book118.com/index.php?g=Home&m=View&a=viewUrl&cid=' + str(self.aid) + '&flag=1&mark=0&onlyread='
        response = requests.get(judge_url)
        if response.text == 'new':
            print('PDF类型文件')
            self.pdf_get_page()
            self.pdf_get_links(1)
        else:
            print('Word类型文件')
            self.pdf_get_page()#为了获取title
            link = 'http:' + str(response.text)
            try:
                self.word_get_page(link)
            except:
                self.word_get_page(link)
                print('word_get_page retry!')

            try:
                self.word_get_links()
            except:
                self.word_get_links()
                print('word_get_links retry!')

        #转p'd'f
        self.transfer()



    def cleaner(self,rootDir):
        for filename in os.listdir(rootDir):
            pathname = os.path.join(rootDir, filename)
            os.remove(pathname)

    def downloader(self,url_list):
        c=0
        for url in url_list:
            if url=='':
                print('重来一次！')
            c=c+1
            if str(url)[0:4]=='http':
                url=url
            else:
                url='http:'+str(url)
            print('下载中。。。第'+str(c)+'页')
            print(url)
            response=requests.get(url)
            with open('图片//'+str(self.title).split('.')[0]+str(c)+'.png','wb+')as f:
                f.write(response.content)
    def transfer(self):
        # 图片转pdf：
        print('转pdf中。。。')
        transfer = ImgToPdf()
        transfer.pmain(src_folder='图片',title=self.title)

    def word_get_page(self,url):
        response = requests.get(url, headers=self.headers,timeout=10)#headers=self.headers,
        soup = BeautifulSoup(response.content, 'lxml')
        self.f = soup.select('#Url')[0].attrs['value']
        self.readLimit = soup.select('#ReadLimit')[0].attrs['value']
        self.furl = soup.select('#Furl')[0].attrs['value']
        self.retry=1
        print('ok!开始获取图片链接，请稍等。。。')

    def word_get_links(self):
        img_list=[]
        while True:
            first_url = 'http://view42.book118.com/PW/GetPage?f=' + str(self.f) + '&img=' + str(
                self.img) + '&isMobile=false&readLimit=' + str(self.readLimit) + '&sn=0&furl=' + str(self.furl)
            response = requests.get(first_url, headers=self.headers)
            # try:
            data = json.loads(response.text)
            self.img = data['NextPage']
            PageIndex = data['PageIndex']
            PageCount = data['PageCount']

            img_list.append('http://view42.book118.com/img?img='+str(self.img))

            if PageIndex == PageCount:
                break
            # except:
            #     print(response.text)
        self.downloader(img_list)
    '''
    PDF类型下载模块
    '''
    def pdf_get_page(self):
        url = self.target_url
        response = requests.post(url, verify=False)
        i = r"view_token = '(.*?)';"
        token = re.findall(i, response.text)[0]
        self.token = token
        t = r'<title>(.*?)</title>'
        title = re.findall(t, response.text)[0]
        self.title = title

    def pdf_get_links(self,page):
        url='https://max.book118.com/index.php?g=Home&m=Ajax&a=getPreviewData'
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '71',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'max.book118.com',
            'Origin': 'https://max.book118.com',
            'Referer': 'https://max.book118.com/index.php?g=Home&m=NewView&a=index&aid=106712526',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
              }
        data={
            'aid': self.aid,
            'page_number': page,
            'view_token': self.token
        }
        response=requests.post(url,headers=headers,data=data,verify=False)
        data=json.loads(response.text)['data']
        page=json.loads(response.text)['page']
        for i in data:
            self.url_list.append(data[i])
            self.max = i
        print(max)
        if int(self.max)==int(page):
            print('结束！')
            self.downloader(self.url_list)
        else:
            page=str(int(self.max)+1)
            self.pdf_get_links(page)


if __name__ == '__main__':
    D=Download_free()
    D.scheduler()
