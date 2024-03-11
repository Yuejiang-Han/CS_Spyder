import json
import re
import requests
from bs4 import BeautifulSoup
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_img(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=True, timeout=10)
    except requests.exceptions.Timeout:
        for i in range(4):
            try:
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=True, timeout=20)
                if res.status_code == 200:
                    break
            except requests.exceptions.Timeout:
                pass

    soup = BeautifulSoup(res.content, "html.parser")

    url_prefixes = {
        "第一批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/lb/201907/",
        "第一批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/db/201907/",
        "第二批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/lb2/201912/",
        "第二批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/db2/201912/",
        "第三批联办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/dsplbyjs/202104/",
        "第三批单办一件事": "https://www.hunan.gov.cn/topic/yjsycb/bszn/dspdbyjs/202104/"
    }

    image_links = []
    for p_tag in soup.find_all('p'):
        img_tag = p_tag.find('img')
        if img_tag:
            column_name = soup.find('meta', attrs={'name': 'ColumnName'})['content']
            url_prefix = url_prefixes.get(column_name, "")
            if url_prefix:
                full_img_url = url_prefix + img_tag['src']
                image_links.append(full_img_url)

    return image_links

def read_json_file(filename):
    """读取并解析JSON文件"""
    with open(filename, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    return data_list

def fetch_and_parse_html(url, max_retries=3):
    """获取指定URL的HTML内容，并使用BeautifulSoup进行解析，最多尝试max_retries次"""
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                html_content = soup.get_text()
                return html_content, soup
            else:
                print(f"请求{url}失败，状态码：{response.status_code}")
        except requests.RequestException as e:
            print(f"请求{url}异常: {e}")
        retries += 1
        print(f"重试{retries}/{max_retries}...")
    return None, None

def extract_content_between_keys(html_content, keys, end_of_content="相关附件\n\n"):
    """在HTML内容中提取每个key之间的内容，最后一个key截止到特定的字符串"""
    results = {}
    for i in range(len(keys)):
        start_key = re.escape(keys[i].rstrip(':'))
        if i + 1 < len(keys):
            end_key = re.escape(keys[i + 1].rstrip(':'))
            pattern = f"{start_key}[:：]?\\s*(.*?){end_key}[:：]?\\s*"
        else:
            pattern = f"{start_key}[:：]?\\s*(.*?){re.escape(end_of_content)}"
        
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            results[keys[i]] = match.group(1).strip()
        else:
            if i == len(keys) - 1:
                pattern = f"{start_key}[:：]?\\s*(.*)"
                match = re.search(pattern, html_content, re.DOTALL)
                if match:
                    results[keys[i]] = match.group(1).strip()
    return results

def save_image(img_url, save_dir='/home/enoc2/hyj/images', max_retries=3):
    """从给定的图片URL下载图片，并保存到指定目录，最多重试max_retries次"""
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(img_url, timeout=10)
        if response.status_code == 200:
            os.makedirs(save_dir, exist_ok=True)
            img_name = os.path.basename(img_url)
            save_path = os.path.join(save_dir, img_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return save_path
        else:
            print(f"Failed to download image {img_url} - Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return None

def process_urls(json_filename):
    """主函数，遍历所有URL并处理它们"""
    data_list = read_json_file(json_filename)
    results_list = []

    for data in data_list:
        url = data["url"]
        keys = [key.rstrip(':') for key in list(data.keys())[1:]]  # 移除键中的冒号
        
        html_content, _ = fetch_and_parse_html(url)
        img_urls = get_img(url)  # 使用get_img函数获取图片URLs
        image_paths = [save_image(img_url) for img_url in img_urls]  # 下载图片并获取路径
        
        if html_content:
            extracted_content = extract_content_between_keys(html_content, keys)
            results_list.append({"url": url, **extracted_content, "images": image_paths})
        else:
            results_list.append({"url": url, "error": "Failed to fetch or parse HTML content"})

    return results_list

# 使用示例
json_filename = 'updated_CS_Key+.json' 
results = process_urls(json_filename)

# 将结果保存到output.json文件中
output_filename = 'CS_DATA.json'  # 指定输出文件名
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print(f"结果已保存到{output_filename}")

