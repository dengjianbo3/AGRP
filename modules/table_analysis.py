from dashscope import Generation
from .config import Config

from .tools.basic_tools import *
from .tools.tabular_analysis import *
from .tools.visualization import *

from .utils import read_file_to_df, update_tools_with_columns

import random
import json

class TableAnalysis():
    def __init__(self,
                 dataframe):
        self.dataframe = dataframe
        self.tools = update_tools_with_columns(dataframe)
        self.tool_function_mapping = {
            'get_current_time': lambda: get_current_time(),
            # 定位函数
            'locate_specific_value': lambda args: locate_specific_value(self.dataframe, args['col_name_condition'], args['condition_value']),
            'locate_greater_than_value': lambda args: locate_greater_than_value(self.dataframe, args['col_name_condition'], args['condition_value']),
            'locate_less_than_value': lambda args: locate_less_than_value(self.dataframe, args['col_name_condition'], args['condition_value']),
            # 描述函数
            'describe_column': lambda args: describe_column(self.dataframe, args['col_name']),
            'describe_dataframe': lambda args: describe_dataframe(self.dataframe),
            # 计算函数
            'calculate_correlation': lambda args: calculate_correlation(self.dataframe, args['col1'], args['col2']),
            'calculate_covariance': lambda args: calculate_covariance(self.dataframe, args['col1'], args['col2']),
            'calculate_skewness': lambda args: calculate_skewness(self.dataframe, args['col_name']),
            'calculate_kurtosis': lambda args: calculate_kurtosis(self.dataframe, args['col_name']),
            'calculate_percentile': lambda args: calculate_percentile(self.dataframe, args['col_name'], args['percentile']),
            'calculate_coefficient_of_variation': lambda args: calculate_coefficient_of_variation(self.dataframe, args['col_name']),
            'calculate_missing_value_ratio': lambda args: calculate_missing_value_ratio(self.dataframe, args['col_name']),
            'calculate_unique_values': lambda args: calculate_unique_values(self.dataframe, args['col_name']),
            'calculate_mode': lambda args: calculate_mode(self.dataframe, args['col_name']),
            # 可视化函数
            'plot_line_chart': lambda args: plot_line_chart(self.dataframe, args['col_name']),
            'plot_bar_chart': lambda args: plot_bar_chart(self.dataframe, args['col_name']),
            'plot_scatter_chart': lambda args: plot_scatter_chart(self.dataframe, args['x_col'], args['y_col']),
            'plot_histogram': lambda args: plot_histogram(self.dataframe, args['col_name'], args.get('bins', 10)),
            'plot_box_plot': lambda args: plot_box_plot(self.dataframe, args['col_name']),
            'plot_pie_chart': lambda args: plot_pie_chart(self.dataframe, args['col_name']), 

        }

    def get_response(self, messages):
        response = Generation.call(
            model=Config.QWEN_MODEL,
            messages=messages,
            tools=self.tools,
            api_key=Config.QWEN_API,
            seed=random.randint(1, 10000),
            result_format='message'
        )
        return response
    
    def handle_tool_call(self,tool_name, tool_arguments):
        try:
            # 从字典中获取相应的函数，并传入参数执行
            tool_output = {
                "name": tool_name,
                "role": "tool",
                "content": self.tool_function_mapping[tool_name](tool_arguments)
            }
        except KeyError:
            tool_output = {"name": tool_name, "role": "tool", "content": f"Tool {tool_name} not found."}
        except Exception as e:
            tool_output = {"name": tool_name, "role": "tool", "content": str(e)}
        return tool_output
    
    def call_with_messages(self, user_input):
        messages = [{"content": user_input, "role": "user"}]
        # 模型的第一轮调用
        first_response = self.get_response(messages)

        assistant_output = first_response.output.choices[0].message
        messages.append(assistant_output)

        if 'tool_calls' not in assistant_output:
            return assistant_output['content']

        tool_call = assistant_output['tool_calls'][0]['function']
        tool_name = tool_call['name']
        tool_arguments = json.loads(tool_call['arguments'])

        tool_output = self.handle_tool_call(tool_name, tool_arguments)
        return tool_output['content']

            

if __name__ == '__main__':
    # 假设用户上传了一个包含销售额的Excel文件，实际应替换为用户上传文件的路径
    file_path = "/root/Documents/ascend_rag/example_data/index.csv"
    df = read_file_to_df(file_path)

    ta_chat = TableAnalysis(df)

    # 用户输入示例
    user_input = "帮我把销售金额的走势画出来看看"

    # 调用函数
    result = ta_chat.call_with_messages(user_input)
    print(result)
