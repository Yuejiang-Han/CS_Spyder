import requests
from bs4 import BeautifulSoup
import json

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

def get_title(url):
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
            
    # 提取标题和内容
    title = soup.find('meta', attrs={'name': 'ArticleTitle'})['content']    

    return title

def get_content(url):
    
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


    # 发送GET请求获取网页内容
    response = requests.get(url,headers={"User-Agent":"Mozilla/5.0"}, verify=True)

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 初始化一个空的列表，用于存储value
    value_list = []

    # 初始化一个空的key
    current_key = None

    # 初始化result为一个空字典
    result = {}
    
    # 遍历每个<p>标签
    for p in soup.find_all('p'):
        # 找到<p>标签中的<b>或<strong>标签作为key
        if p.find('strong') or p.find('b'):
            current_key = p.find('strong').text if p.find('strong') else p.find('b').text
            # 如果key不在result中，则将其添加到result中
            if current_key not in result:
                result[current_key] = []
            # 获取下一个兄弟节点的文本
            next_sibling_text = p.find('strong').next_sibling if p.find('strong') else p.find('b').next_sibling
            result[current_key].append(next_sibling_text)
        else:
            # 将文本添加到对应的key中
            result[current_key].append(p.text.strip())

    
    return result

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

json_t = []
url =" https://www.hunan.gov.cn/topic/yjsycb/bszn/index.html"
link_set = what_in_url(url)

for i in link_set:
    data = {
        "title": get_title(i),
        "content": get_content(i),
        "image_links": get_img(i)
    }
    json_t.append(data)

    with open('0111.json', 'w', encoding='utf-8') as f:
        json.dump(json_t, f, ensure_ascii=False, indent=4)