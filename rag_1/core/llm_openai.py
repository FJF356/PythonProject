from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="GLM-4.7",
    temperature=0.3,
    streaming=True,
    base_url = "https://open.bigmodel.cn/api/coding/paas/v4"
)

while True:
    question = input("输入你的问题:")
    if question == "q":
        break
    for chunk in llm.stream(question):
        print(chunk.content, end="", flush=True)
    print()