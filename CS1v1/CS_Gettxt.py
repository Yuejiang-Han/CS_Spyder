import json
import os

def save_individual_json_objects(file_path, output_directory):
    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)
    
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 遍历 JSON 对象
    for item in data:
        # 从 URL 中生成文件名
        filename = item["url"].replace('/', '~') + '.txt'
        # 构建完整的输出路径
        full_path = os.path.join(output_directory, filename)
        
        # 保存 JSON 对象到文本文件
        with open(full_path, 'w', encoding='utf-8') as output_file:
            # 将 JSON 对象转换为字符串格式
            json_str = json.dumps(item, ensure_ascii=False, indent=4)
            output_file.write(json_str)
        
        print(f"Saved: {full_path}")

# 文件路径和输出目录
file_path = 'CS_Data_1v1.json'  
output_directory = '/home/enoc2/hyj/CS_single_version/CS1v1_txt'

# 执行函数
save_individual_json_objects(file_path, output_directory)
