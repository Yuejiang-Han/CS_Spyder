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

def get_img(url):
    try:
        # 设置超时时间为10秒
        res = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, verify=True, timeout=10)
    except requests.exceptions.Timeout:
        # 如果超时，尝试再次请求，最多尝试4次
        for i in range(4):
            try:
                res = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, verify=True, timeout=20)
                if res.status_code == 200:
                    break
            except requests.exceptions.Timeout:
                pass  # 继续尝试直到达到最大尝试次数

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(res.content, "html.parser")

    url_prefixes = {
        "第一批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/lb/201907/",
        "第一批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/db/201907/",
        "第二批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/lb2/201912/",
        "第二批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/db2/201912/",
        "第三批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/dsplbyjs/202104/",
        "第三批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/dspdbyjs/202104/"
    }
    
    # 提取所有<p>标签内的图片链接
    image_links = []
    for p_tag in soup.find_all('p'):
        img_tag = p_tag.find('img')
        if img_tag:
            # 根据"ColumnName" content选择相应的URL前缀
            column_name = soup.find('meta', attrs={'name': 'ColumnName'})['content']
            url_prefix = url_prefixes.get(column_name, "")
            if url_prefix:
                image_links.append(url_prefix + img_tag['src'])
                
    return image_links

url = "https://www.hunan.gov.cn/topic/yjsycb/bszn/index.html"
link_set = what_in_url(url)

for i in link_set:
    img_urls = get_img(i)
    for img_url in img_urls:
        try:
            # 发送请求获取图片内容
            res = requests.get(img_url, headers={"User-Agent":"Mozilla/5.0"}, verify=True, timeout=10)
            if res.status_code == 200:
                # 从链接中提取图片名称
                img_name = img_url.split('/')[-1]
                # 保存图片为二进制格式
                with open(img_name, 'wb') as f:
                    f.write(res.content)
                print(f"图片 {img_name} 保存成功")
            else:
                print(f"图片 {img_url} 下载失败")
        except requests.exceptions.RequestException as e:
            print(f"图片 {img_url} 下载失败: {e}")