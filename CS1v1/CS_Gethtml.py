import requests
from bs4 import BeautifulSoup
import time
import os

def what_in_url(url):
    res = requests.get(url)
    html_content = res.content
    soup = BeautifulSoup(html_content, "html.parser")
    qj_bmfw_li = soup.find_all('div', class_='qj_bmfw_li')
    link_set = []
    for item in qj_bmfw_li:
        link = "https://www.hunan.gov.cn" + item.a['href']
        link_set.append(link)
    return link_set

def save_html_content(url, output_dir="/home/enoc2/hyj/CS_single_version/CS1v1_html", max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            res = requests.get(url)
            res.raise_for_status()  # 检查请求是否成功
            html_content = res.content
            
            # 确保目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 将URL中的'/'名字符替换为'~'
            filename = url.replace('/', '~')
            full_path = os.path.join(output_dir, filename)
            
            # 检查文件是否已存在
            if os.path.exists(full_path):
                print(f"File already exists: {full_path}, skipping...")
                break  # 文件已存在，跳过保存
            
            with open(full_path, 'wb') as file:
                file.write(html_content)
            print(f"Saved: {full_path}")
            break  # 成功后退出循环
        except requests.exceptions.RequestException as e:
            print(f"Error requesting {url}: {e}, retrying... {retries+1}/{max_retries}")
            time.sleep(2)  # 等待2秒再重试
            retries += 1
    
    if retries == max_retries:
        print(f"Failed to fetch {url} after {max_retries} attempts.")

# 示例用法
url = "https://www.hunan.gov.cn/topic/yjsycb/bszn/index.html"
link_set = what_in_url(url)

for link in link_set:
    save_html_content(link)
    time.sleep(1)  # 防止因请求过快而被服务器限制
