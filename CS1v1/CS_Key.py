import requests
from bs4 import BeautifulSoup
import json
import unicodedata #用于decode
import re #用于正则整理key格式
import time #预防网络问题

# 发送请求获取网页内容
def what_in_url(url):
    res = requests.get(url)
    html_content = res.content

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 提取所有带有class="qj_bmfw_li"的内容
    qj_bmfw_li = soup.find_all('div', class_='qj_bmfw_li')

    # 遍历提取的内容
    n = 0
    link_set = []
    for item in qj_bmfw_li:
        n+=1
        link = "https://www.hunan.gov.cn" + item.a['href']
        text = item.a.span.get_text()
        link_set.append(link)
    return(link_set)

def get_key(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=True)
            soup = BeautifulSoup(response.content, 'html.parser')
            bold_tags = [tag.text for tag in soup.find_all(['b', 'strong', 'span']) if tag.parent.name == 'p']
            cleaned_result = [re.sub(r'^\s+|\s+$', '', unicodedata.normalize('NFKC', x)) for x in bold_tags]
            pattern = r'^(1?\d|1?[0-9]|[一二三四五六七八九十十一十二十三十四十五十六十七十八十九二十]+)[、.]'
            matched_result = [x for x in cleaned_result if re.search(pattern, x)]
            return matched_result
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError occurred: {e}")
            print("Retrying...")
            time.sleep(5)
            retries += 1
    print("Max retries reached, unable to retrieve data.")
    return []


url = "https://www.hunan.gov.cn/topic/yjsycb/bszn/index.html"
link_set = what_in_url(url)
json_key = []
for i in link_set:
    data = {
        "url": i,
        "key":get_key(i)
    }
    json_key.append(data)

with open('tttt.json', 'w', encoding='utf-8') as f:
    json.dump(json_key, f, ensure_ascii=False, indent=4)