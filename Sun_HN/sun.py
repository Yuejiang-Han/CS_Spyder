import requests
from bs4 import BeautifulSoup
import json
from lxml import html

url = "https://zwfw-new.hunan.gov.cn/onething/sungovaffairs/item_list_1.jsp?areaCode=439900000000&jgname=&flag=&pager.offset="
base = "https://zwfw-new.hunan.gov.cn"

def responsibility_list_url(url,base):
    """
    整理阳光政务权责清单的所有链接
    """
    sun_url = []
    for offset in range(1441):
        url_n = url + str(offset)
        response = requests.get(url_n)
        soup = BeautifulSoup(response.content, "html.parser")
        tr_tags = soup.find_all("tr", {"style": "cursor:hand;"})
        for tr in tr_tags:
            href = tr.a["href"]
            sun_url.append(base + href)
    return sun_url


# 定义url_list
url_list = responsibility_list_url(url,base)

result = {}

# # 遍历url_list
# for url in url_list:
#     response = requests.get(url)
#     if response.status_code == 200:
#         page_content = response.content
#         tree = html.fromstring(page_content)

#         # 使用XPath提取数据
#         key_elements = tree.xpath("/html/body/div[8]/div/div[2]/div/table/tbody//td[1]")
#         value_elements = tree.xpath("/html/body/div[8]/div/div[2]/div/table/tbody//td[2]")

#         data = {}
#         for key_element, value_element in zip(key_elements, value_elements):
#             key = key_element.text_content().strip()
#             value = value_element.text_content().strip()
#             data[key] = value

#         result[url] = data

# # 将结果保存为JSON文件
# output_filename = 'CS_Sun.json' 
# with open(output_filename, "w", encoding="utf-8") as json_file:
#     json.dump(result, json_file, ensure_ascii=False, indent=4)

# print(f"结果已保存到{output_filename}")