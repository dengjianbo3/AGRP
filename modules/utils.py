import pandas as pd 
import os 

# 读取Excel或CSV文件并转换为DataFrame
def read_file_to_df(file_path: str, file_extension) -> pd.DataFrame:
    if file_extension == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")
    return df

# 将DataFrame保存为pickle文件
def save_df_to_pickle(df: pd.DataFrame, file_name: str, file_path: str):
    pickle_path = os.path.join(file_path, f"{file_name}.pkl")
    df.to_pickle(pickle_path)


# 读取Excel或CSV文件并转换为DataFrame
def read_file_to_df(file_path: str, file_extension) -> pd.DataFrame:
    if file_extension == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")
    return df

# 将DataFrame保存为pickle文件
def save_df_to_pickle(df: pd.DataFrame, file_name: str, file_path: str):
    pickle_path = os.path.join(file_path, f"{file_name}.pkl")
    df.to_pickle(pickle_path)


# 注册工具函数
def update_tools_with_columns(df):
    tool_list = []
    columns = df.columns.tolist()
    column_names = ", ".join(columns)

    describe_description = f"对指定DataFrame列进行基本数据描述性分析，包括最大值、最小值、均值、方差、分位数等。可以问例如：'请描述列A的统计信息'，或者'列B的平均值是多少？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "describe_column",
                "description": describe_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要进行描述性分析的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    dataframe_description = "对整个DataFrame进行基本数据描述性分析，包括最大值、最小值、均值、方差、分位数等。可以问例如：'请描述整个数据框的统计信息'，或者'数据框的基本统计数据是什么？'。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "describe_dataframe",
                "description": dataframe_description,
                "parameters": {}
            }
        }
    )

    correlation_description = f"计算两列之间的相关性。可以问例如：'列A和列B之间的相关性是多少？'，或者'列C和列D的相关系数是多少？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_correlation",
                "description": correlation_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col1": {
                            "type": "string",
                            "description": "第一列的列名。"
                        },
                        "col2": {
                            "type": "string",
                            "description": "第二列的列名。"
                        }
                    },
                    "required": ["col1", "col2"]
                }
            }
        }
    )

    covariance_description = f"计算两列之间的协方差。可以问例如：'列A和列B的协方差是多少？'，或者'列C和列D之间的协方差是什么？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_covariance",
                "description": covariance_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col1": {
                            "type": "string",
                            "description": "第一列的列名。"
                        },
                        "col2": {
                            "type": "string",
                            "description": "第二列的列名。"
                        }
                    },
                    "required": ["col1", "col2"]
                }
            }
        }
    )

    skewness_description = f"计算一列的偏度。可以问例如：'列A的偏度是多少？'，或者'列B的数据分布是否偏斜？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_skewness",
                "description": skewness_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算偏度的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    kurtosis_description = f"计算一列的峰度。可以问例如：'列A的峰度是多少？'，或者'列B的数据分布是否具有尖峰？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_kurtosis",
                "description": kurtosis_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算峰度的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    percentile_description = f"计算一列的指定百分位数。可以问例如：'列A的第90百分位数是多少？'，或者'列B的中位数是多少？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_percentile",
                "description": percentile_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算百分位数的列名。"
                        },
                        "percentile": {
                            "type": "number",
                            "description": "需要计算的百分位数值。"
                        }
                    },
                    "required": ["col_name", "percentile"]
                }
            }
        }
    )

    cv_description = f"计算一列的变异系数。可以问例如：'列A的变异系数是多少？'，或者'列B的数据分散程度如何？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_coefficient_of_variation",
                "description": cv_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算变异系数的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    missing_value_description = f"计算一列的缺失值比例。可以问例如：'列A的缺失值比例是多少？'，或者'列B有多少缺失值？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_missing_value_ratio",
                "description": missing_value_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算缺失值比例的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    unique_values_description = f"计算一列的唯一值个数。可以问例如：'列A有多少个唯一值？'，或者'列B的唯一值个数是多少？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_unique_values",
                "description": unique_values_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算唯一值个数的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    mode_description = f"计算一列的最常见值（众数）。可以问例如：'列A的众数是多少？'，或者'列B中最常见的值是什么？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "calculate_mode",
                "description": mode_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要计算众数的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )


    locate_description = f"根据指定条件查找某行的所有列数据。可以问例如：'请给我销售人员为李华的所有数据'，或者'我想查看王芳在南区的所有数据'。可用的列名有：{column_names}。"

    # 注册 locate_specific_value 工具
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "locate_specific_value",
                "description": locate_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name_condition": {
                            "type": "string",
                            "description": "用于查找条件的列名，例如'销售人员'。"
                        },
                        "condition_value": {
                            "type": "string",
                            "description": "要匹配的条件值，例如'李华'。"
                        }
                    },
                    "required": ["col_name_condition", "condition_value"]
                }
            }
        }
    )

        # 查找大于特定值的描述
    locate_greater_description = f"查找大于指定值的行的所有列数据。可以问例如：'请给我收入大于3500的所有数据'，或者'我想查看售出单位大于200的所有数据'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "locate_greater_than_value",
                "description": locate_greater_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name_condition": {
                            "type": "string",
                            "description": "用于查找条件的列名，例如'收入'。"
                        },
                        "condition_value": {
                            "type": "number",
                            "description": "要比较的条件值，例如'3500'。"
                        }
                    },
                    "required": ["col_name_condition", "condition_value"]
                }
            }
        }
    )

    # 查找小于特定值的描述
    locate_less_description = f"查找小于指定值的行的所有列数据。可以问例如：'请给我售出单位小于160的所有数据'，或者'我想查看收入小于3000的所有数据'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "locate_less_than_value",
                "description": locate_less_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name_condition": {
                            "type": "string",
                            "description": "用于查找条件的列名，例如'售出单位'。"
                        },
                        "condition_value": {
                            "type": "number",
                            "description": "要比较的条件值，例如'160'。"
                        }
                    },
                    "required": ["col_name_condition", "condition_value"]
                }
            }
        }
    )

    line_plot_description = f"绘制指定DataFrame列的折线图。可以问例如：'请绘制列A的折线图'，或者'列B的趋势图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_line_chart",
                "description": line_plot_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要绘制折线图的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    bar_plot_description = f"绘制指定DataFrame列的柱状图。可以问例如：'请绘制列A的柱状图'，或者'列B的柱状图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_bar_chart",
                "description": bar_plot_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要绘制柱状图的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    scatter_plot_description = f"绘制指定DataFrame列之间的散点图。可以问例如：'请绘制列A和列B的散点图'，或者'列C和列D的关系图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_scatter_chart",
                "description": scatter_plot_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x_col": {
                            "type": "string",
                            "description": "需要作为x轴的列名。"
                        },
                        "y_col": {
                            "type": "string",
                            "description": "需要作为y轴的列名。"
                        }
                    },
                    "required": ["x_col", "y_col"]
                }
            }
        }
    )

    histogram_description = f"绘制指定DataFrame列的直方图。可以问例如：'请绘制列A的直方图'，或者'列B的频率分布图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_histogram",
                "description": histogram_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要绘制直方图的列名。"
                        },
                        "bins": {
                            "type": "integer",
                            "description": "直方图的bins数目。",
                            "default": 10
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    box_plot_description = f"绘制指定DataFrame列的箱线图。可以问例如：'请绘制列A的箱线图'，或者'列B的分布范围图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_box_plot",
                "description": box_plot_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要绘制箱线图的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    pie_chart_description = f"绘制指定DataFrame列的饼状图。可以问例如：'请绘制列A的饼状图'，或者'列B的比例图是什么样的？'。可用的列名有：{column_names}。"
    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "plot_pie_chart",
                "description": pie_chart_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "col_name": {
                            "type": "string",
                            "description": "需要绘制饼状图的列名。"
                        }
                    },
                    "required": ["col_name"]
                }
            }
        }
    )

    tool_list.append(
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "当你想知道现在的时间时非常有用，包括日期，时间，季节等，凡是和时间相关的都可以调用。可以问例如：'现在的时间是什么？'，或者'今天是几号？'。",
                "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
            }
        }
    )

    return tool_list