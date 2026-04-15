import pandas as pd
import numpy as np
import os
from langchain_core.tools import tool
from tavily import TavilyClient


@tool(description="加载文件")
def load_datas(file_path: str) -> str:
    try:
        if file_path.endswith("csv"):
            df = pd.read_csv(file_path)
        else:
            return "请传入csv文件格式"
        global _datafram
        _datafram = df
        info = f"数据加载成功，形状:{df.shape}\n列名:{list(df.columns)}\n缺失值:{df.isnull().sum()}\n前五行{df.head().to_string}"
        return info
    except Exception as e:
        return f"出现错误，错误情况{str(e)}"


@tool(description="数据分析")
def quety_data() -> str:
    global _datafram
    if "_datafram" not in globals() or _datafram is None:
        return "错误，尚未加载数据，请先使用load_datas工具"

    try:
        df = _datafram
        df_max = df.revenue.max()  # 收入最高值
        idx=df.revenue.idxmax()
        df_product = df.loc[idx, "product"]  # 收入最高的产品
        df_mean = df.revenue.mean()  # 收入平均值
        df_describe = df.revenue.describe()  # 收入情况介绍

        return (
            str(df_max)
            + ","
            + str(df_product)
            + ","
            + str(df_mean)
            + ","
            + df_describe.to_string()
        )

    except Exception as e:
        return f"查询失败{str(e)}"


@tool(description="四则运算工具")
def calculate(query: str) -> str:
    try:
        result = eval(query)
        return result
    except Exception as e:
        return f"错误情况{str(e)}"


@tool(description="网上搜索")
def search_web(query: str) -> str:
    tavily = TavilyClient()
    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        if response.get("answer"):
            return response["answer"]
        else:
            return f"没有搜索到答案"
    except Exception as e:
        return f"出现了问题{str(e)}"


@tool(description="文件保存")
def save_report(filename: str, content: str) -> str:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            return f"文件已经保存为{os.path.abspath(filename)}"
    except Exception as e:
        return f"出现了错误{str(e)}"


# if __name__=="__main__":
#     result=load_datas("./销售数据.csv")
#     print(result)
