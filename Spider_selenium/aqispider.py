from bs4 import BeautifulSoup
from selenium import webdriver
import time, csv


def open_url(url, browser):#模拟chrome打开网页#
    browser.get(url)
    time.sleep(0.5)#间隔0.5s,表格中没有数据就设置长一点#
    html = chrome.page_source
    soup = BeautifulSoup(html, features='lxml')

    return soup


def get_month():#爬取月份#
    monthlist = []
    for i in range(1, 10):
        monthlist.append(f'2017-0{i}')
    for i in range(10, 13):
        monthlist.append(f'2017-{i}')
    for i in range(1, 10):
        monthlist.append(f'2018-0{i}')
    monthlist.append(f'2018-10')

    return monthlist


def get_city():#爬取城市#
    citylist = []
    cityurl = 'https://www.aqistudy.cn/historydata/'
    citysoup = open_url(cityurl, chrome)
    cityset = citysoup.findAll('div', {'class':'all'})[0].findAll('li')
    for city in cityset:
        city = city.text.strip()
        citylist.append(city)

    return citylist


def main():
    monthlist = get_month()
    citylist = get_city()

    for city in citylist:
        #表头#
        heads = ['date', 'AQI', '质量等级', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h']
        with open(f'{city}.csv', 'a', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(heads)

        for month in monthlist:
            url = f'https://www.aqistudy.cn/historydata/daydata.php?city={city}&month={month}'
            soup = open_url(url, chrome)
            table = soup.find('table')

            num = str(table).count('<tr')
            for i in range(num):
                if i != 0:
                    tdata = table.find_all('tr')[i].find_all('td')
                    data = []
                    for i in tdata:
                        data.append(i.text)
                    with open(f'{city}.csv', 'a', newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(data)

    chrome.quit()


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    main()