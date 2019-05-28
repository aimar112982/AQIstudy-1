from selenium import webdriver
from bs4 import BeautifulSoup
import time, csv, os


class AqiStudy():
    '''
    爬取地级市日度空气质量数据并保存为 .csv格式
    '''
    
    
    # 初始化浏览器
    def __init__(self, browser):
        self._browser = browser
    
    
    # 模拟chrome打开网页
    def open_web(self, url):
        self._browser.get(url)
        time.sleep(0.5)
        html = self._browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        return soup
    
    
    # 爬取城市列表
    def get_city(self):
        citylist = []
        city_url = 'https://www.aqistudy.cn/historydata/'
        city_soup = self.open_web(city_url).find('div', class_='all').find_all('li')
        for li in city_soup:
            city = li.a.string.strip()
            citylist.append(city)
            
        return citylist
    
    
    # 爬取主要城市列表
    def get_maincity(self):
        maincity = []
        maincity_url = 'https://www.aqistudy.cn/historydata/'
        maincity_soup = self.open_web(maincity_url).find_all('ul', class_="unstyled")[-1].find_all('li')
        for li in maincity_soup:
            city = li.a.string.strip()
            maincity.append(city)
            
        return maincity
    
    
    # 爬取月份列表
    def get_month(self):
        monthlist = []
        month_url = 'https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8C%97%E4%BA%AC'
        month_soup = self.open_web(month_url).find('ul', class_='unstyled1').find_all('li')
        for li in month_soup:
            month_str = li.a.string.strip()
            month = f'{month_str[:4]}-{month_str[5:-1]}'
            monthlist.append(month)
            
        return monthlist
    
    
    # 创建保存图片的文件夹
    def create_folder(self):
        if not os.path.exists('AQIdata'):
            os.mkdir('AQIdata')
        os.chdir('AQIdata')
    
    
    def main(self):
        print('爬虫程序启动')
        monthlist = self.get_month()[1:61]
        citylist = self.get_maincity()
        self.create_folder()
        
        for city in citylist:
            #设置表头#
            heads = ['date', 'AQI', '质量等级', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h']
            with open(f'{city}.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(heads)
            print(f'正在爬取{city}的空气质量数据...')
            
            for month in monthlist:
                url = f'https://www.aqistudy.cn/historydata/daydata.php?city={city}&month={month}'
                soup = self.open_web(url)
                table = soup.find('tbody').find_all('tr')[1:]
                while not table:  # 判断页面是否完全加载
                    soup = self.open_web(url)
                    table = soup.find('tbody').find_all('tr')[1:]
                for tr in table:
                    tds = tr.find_all('td')
                    data = []
                    for i in tds:
                        data.append(i.string)
                    with open(f'{city}.csv', 'a', newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(data)
            print(f'{city}数据爬取完毕')
        print('全部数据爬取完毕')
        


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    aqi = AqiStudy(browser=chrome)
    aqi.main()
    chrome.quit()