import pandas as pd
import numpy as np

# 对某列进行基本数据描述性分析的工具
def describe_column(df, col_name):
    try:
        description = df[col_name].describe().to_dict()
        return description
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 对整个数据框进行总体描述的工具
def describe_dataframe(df):
    try:
        description = df.describe().to_dict()
        return description
    except Exception as e:
        return str(e)

# 计算两列之间的相关性
def calculate_correlation(df, col1, col2):
    try:
        correlation = df[col1].corr(df[col2])
        return {f'Correlation between {col1} and {col2}': correlation}
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."

# 计算两列之间的协方差
def calculate_covariance(df, col1, col2):
    try:
        covariance = df[[col1, col2]].cov().iloc[0, 1]
        return {f'Covariance between {col1} and {col2}': covariance}
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."

# 计算一列的偏度
def calculate_skewness(df, col_name):
    try:
        skewness = df[col_name].skew()
        return {f'Skewness of {col_name}': skewness}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的峰度
def calculate_kurtosis(df, col_name):
    try:
        kurtosis = df[col_name].kurt()
        return {f'Kurtosis of {col_name}': kurtosis}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的百分位数
def calculate_percentile(df, col_name, percentile):
    try:
        percentile_value = np.percentile(df[col_name].dropna(), percentile)
        return {f'{percentile}th percentile of {col_name}': percentile_value}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的变异系数
def calculate_coefficient_of_variation(df, col_name):
    try:
        mean = df[col_name].mean()
        std = df[col_name].std()
        cv = std / mean if mean != 0 else float('inf')
        return {f'Coefficient of Variation of {col_name}': cv}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的缺失值比例
def calculate_missing_value_ratio(df, col_name):
    try:
        missing_ratio = df[col_name].isna().mean()
        return {f'Missing Value Ratio of {col_name}': missing_ratio}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的唯一值个数
def calculate_unique_values(df, col_name):
    try:
        unique_values_count = df[col_name].nunique()
        return {f'Unique Values Count of {col_name}': unique_values_count}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 计算一列的最常见值（众数）
def calculate_mode(df, col_name):
    try:
        mode_value = df[col_name].mode().iloc[0]
        return {f'Mode of {col_name}': mode_value}
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."
    except IndexError:
        return f"No mode found for column '{col_name}'. The column might be empty."
    

# 定位特定行的所有列数据的工具
def locate_specific_value(df, col_name_condition, condition_value):
    try:
        specific_value = df.loc[df[col_name_condition] == condition_value]
        if specific_value.empty:
            return f"No matching rows found for the given condition: {col_name_condition} = {condition_value}"
        return specific_value.to_dict(orient='records')
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."
    except Exception as e:
        return str(e)
    

# 查找大于特定值的行的所有列数据的工具
def locate_greater_than_value(df, col_name_condition, condition_value):
    try:
        specific_value = df.loc[df[col_name_condition] > condition_value]
        if specific_value.empty:
            return f"No matching rows found for the given condition: {col_name_condition} > {condition_value}"
        return specific_value.to_dict(orient='records')
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."
    except Exception as e:
        return str(e)
    
# 查找小于特定值的行的所有列数据的工具
def locate_less_than_value(df, col_name_condition, condition_value):
    try:
        specific_value = df.loc[df[col_name_condition] < condition_value]
        if specific_value.empty:
            return f"No matching rows found for the given condition: {col_name_condition} < {condition_value}"
        return specific_value.to_dict(orient='records')
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."
    except Exception as e:
        return str(e)