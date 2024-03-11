from langchain_openai import ChatOpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://43.225.216.221:2080/v1"
model_name = "Qwen/Qwen1.5-14B-Chat"

llm = ChatOpenAI(model_name=model_name,
                 openai_api_key=openai_api_key,
                 openai_api_base=openai_api_base)

response = llm.invoke("讲解一下大语言模型")
print(response)
