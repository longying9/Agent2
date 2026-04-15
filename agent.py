from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from tools import load_datas,quety_data,calculate,search_web,save_report

model=ChatTongyi(model="qwen-max") # type: ignore

agent=create_agent(
    model=model,
    tools=[load_datas,quety_data,calculate,search_web,save_report],
    system_prompt="""你是一家电商公司的数据助理，可以使用工具来回答用户的提问，
    如果已经给出过某个信息，不要重复陈述相同的内容
    绝对不要重复用户的问题或重复你自己的上一轮输出"""
)

_datafram=None

while True:
    user_input=input("请输入你的问题")
    if user_input=="quit":
        break
    result=agent.invoke({"messages":[HumanMessage(content=user_input)]})
    for message in result["messages"]:
        print(f"{message.type},{message.content}")