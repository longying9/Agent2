import pandas as pd
import os 
from langchain_core.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

_datafram=None


@tool(description="加载文档数据")
def load_datas(file_path:str)->str:
    global _datafram
    try:
        df=pd.read_csv(file_path)
        _datafram=df
        return f"数据加载成功,形状为{df.shape}"
    except Exception as e:
        return f"数据加载失败，错误{str(e)}"
    
@tool(description="分析数据") 
def query_data(query:str)->str:
    global _datafram
    
    if _datafram is None:
        return f"请先加载数据"
    
    df= _datafram

    try:
        if "最高" in query or "最大" in query:
            idx =df["revenue"].idxmax()
            return f'最高收入产品:{df.loc[idx,"product"]},金额:{df.loc[idx,"revenue"]}'
            
        elif"总" in query:
            g=df.groupby("product")["revenue"].sum()
            return f"总收入最高产品:{g.idxmax()},金额:{g.max()}"
        
        elif"平均"in query:
            return f'平均收入:{df["revenue"].mean()}'
        
        elif"城市"in query:
            c=df.groupby("local")["revenue"].sum()
            return f"消费最高的城市:{c.idxmax()},金额:{c.max()}"
        
        else:
            return f"暂不支持查询"
        
    except Exception as e:
        return f"出现错误，{str(e)}"
    
@tool(description="保存分析内容")   
def generate_report(filename:str,content:str)->str:
    global _datafram
    
    df=_datafram
    
    if df is None:
        return f"请先加载数据"
    try:    
        with open(filename,"w",encoding="utf-8")as f:
            f.write(content)
            return f"文件已经保存为{os.path.abspath(filename)}"
    except Exception as e:
        return f"保存文件失败，错误{str(e)}"
    
    
model=ChatTongyi(model="qwen-max") # type: ignore

memory=MemorySaver()

agent=create_agent(
    model=model,
    tools=[load_datas,query_data,generate_report],
    system_prompt="""
你是电商数据分析助手：
1. 数据问题必须用工具
2. 自动理解上下文
3. 不编造数据
""",
    checkpointer=memory
)

config:RunnableConfig={"configurable":{"thread_id":"user_session_1"}}


user_input="你好，帮我分析一下此目录下的销售数据.csv文件，并将每个城市的平均收入数据分析一下并整理成txt文档发给我"

result=agent.invoke({
    "messages":[
        {"role":"user","content":user_input}]},
    config=config
    )

for message in result["messages"]:
    print(message.content)