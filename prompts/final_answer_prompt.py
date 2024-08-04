from langchain import PromptTemplate


final_answer_prompt = """
                    你是一个专业的文档分析师和数据分析师，你的工作职责就是根据搜索出来的结果数据，回答用户的问题
                    ——————————————————————————————————————————————————————————————————————————————————
                    用户问题: {query}\n, 
                    搜索出来的结果数据: {final_result}\n
                    ——————————————————————————————————————————————————————————————————————————————————
                    请根据用户问题和结果数据，进行回答
                    """

# 定义 Prompt Template
final_answer_prompt = PromptTemplate(
    input_variables=["query", "final_result"],
    template=final_answer_prompt
)
