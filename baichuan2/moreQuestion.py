import pandas as pd
import time
from openai import OpenAI
from retrying import retry

# 设置OpenAI API
openai_api_key = "EMPTY"
openai_api_base = "http://43.225.216.221:2080/v1"

@retry(stop_max_attempt_number=3, wait_fixed=2000)  # 最多重试3次，每次重试间隔2秒
def process_question(question):
    try:
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )

        chat_response = client.chat.completions.create(
            model="baichuan-inc/Baichuan2-7B-Chat",
            messages=[
                {"role": "system", "content": "You are a helpful teacher."},
                {"role": "user", "content": question},
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"处理问题时发生错误：{e}")
        raise

def process_questions(input_file, output_file):
    results = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for question in file:
            question = question.strip()
            if not question:
                continue
            start_time = time.time()
            try:
                answer = process_question(question)
            except Exception as e:
                print(f"问题处理失败：{e}")
                answer = "处理失败"
            end_time = time.time()
            processing_time = end_time - start_time
            results.append([question, answer, processing_time])

    df = pd.DataFrame(results, columns=[
                      'Question', 'Answer', 'Processing Time'])

    df.to_excel(output_file, index=False)

def main(input_filename, output_filename):
    process_questions(input_filename, output_filename)

if __name__ == '__main__':
    input_filename = 'questions.txt'  # 输入文件名
    output_filename = 'processed_questions.xlsx'  # 输出文件名
    main(input_filename, output_filename)
