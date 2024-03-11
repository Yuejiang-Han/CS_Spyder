import requests
from bs4 import BeautifulSoup
import time  # 预防网络问题

def what_in_url(url):
    res = requests.get(url)
    html_content = res.content

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 提取所有带有class="qj_bmfw_li"的内容
    qj_bmfw_li = soup.find_all('div', class_='qj_bmfw_li')

    # 遍历提取的内容
    link_set = []
    for item in qj_bmfw_li:
        link = "https://www.hunan.gov.cn" + item.a['href']
        text = item.a.span.get_text()  # 注意：这里提取了text但没有使用
        link_set.append(link)
    return link_set

def save_html_content(url, file_name, output_dir="/home/enoc2/hyj/html_one"):
    try:
        res = requests.get(url)
        res.raise_for_status()  # 如果请求不成功，会抛出异常
        html_content = res.content
        full_path = f"{output_dir}/{file_name}"  # 构建完整的文件路径
        with open(full_path, 'wb') as file:
            file.write(html_content)
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时出现异常: {e}")

url = "https://www.hunan.gov.cn/topic/yjsycb/bszn/index.html"
link_set = what_in_url(url)

for index, link in enumerate(link_set):
    file_name = f'html_content_{index}.html'
    save_html_content(link, file_name)
    time.sleep(1)  # 在每次请求之间添加1秒的延迟

