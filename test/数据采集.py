import datetime
import time
from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd
import json
def get_html_text(url):

    headers = {"User-Agent" : "Mozila 5.0.0.4"}
    #Sends a GET request.
    html=requests.get(url,headers=headers,timeout=60)
    html.raise_for_status
    html.encoding=html.apparent_encoding
    return html.text

def parseHtml(rank_info,html):

    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
        #找到属性和内容
        if isinstance(tr,bs4.element.Tag):
            tds=tr('td')
            rank_info.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string,tds[4].string,tds[5].string,tds[6].string,
                              tds[7].string,tds[8].string,tds[9].string,tds[10].string,tds[11].string])


def save_contents(rank_info):
    name = ["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered",
            "Active Cases","Serious Critical","Tot Cases/1M pop","Deaths/1M pop","Total Tests",
            "Tests/1M pop"]
    test = pd.DataFrame(columns = name,data = rank_info)
    test.to_csv('疫情数据世界{}.csv'.format(time.strftime("%Y-%m-%d",time.localtime())))
if __name__ == "__main__":
    
    url = "https://www.worldometers.info/coronavirus/"
    rank_info=[]
    html=get_html_text(url)
    parseHtml(rank_info,html)
    rank_info = rank_info[7:]
    save_contents(rank_info)

# =============================================================================
# 爬取中国
# =============================================================================

# 请求的URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'

# 伪装请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'referer': 'https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0'
}

# 抓取数据
r = requests.get(url % time.time(), headers=headers)

data = json.loads(r.text)
data = json.loads(data['data'])

lastUpdateTime = data['lastUpdateTime']
print('数据更新时间 ' + str(lastUpdateTime))

areaTree = data['areaTree']

col_names =  ['省', '市', '确认' , '死亡', '治愈']
my_df  = pd.DataFrame(columns = col_names)

for item in areaTree:
    if item['name'] == '中国':
        item_ps = item['children']
        for item_p in item_ps:
            province = item_p['name']
            # print(province)
            item_cs = item_p['children']
            for item_c in item_cs:
                prefecture = item_c['name']
                confirm = item_c['total']['confirm']
                death = item_c['total']['dead']
                heal = item_c['total']['heal']
                # 向df添加数据
                data_dict = {'省': province, '市':prefecture, '确认': confirm, '死亡': death, '治愈': heal}
                my_df.loc[len(my_df)] = data_dict

# 保存数据
my_df.to_csv(r'china_status_{}.csv'.format(str(lastUpdateTime).split()[0]), encoding='utf_8_sig', header='true')

print('Success')    