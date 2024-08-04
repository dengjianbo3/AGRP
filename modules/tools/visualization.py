import plotly.express as px
import pandas as pd
import os
import random

# 创建临时目录以保存图像
if not os.path.exists('tmp'):
    os.makedirs('tmp')

# # 全局设置
# px.defaults.template = "plotly_white"

# 生成随机颜色
def generate_random_color():
    r = lambda: random.randint(0, 255)
    return f'#{r():02x}{r():02x}{r():02x}'

# 绘制折线图的工具
def plot_line_chart(df, col_name):
    try:
        fig = px.line(
            df, 
            x=df.index, 
            y=col_name, 
            title=f'Line Chart of {col_name}',
            labels={'index': 'Index', col_name: col_name},
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12))
        )
        png_path = os.path.join('tmp', f'{col_name}_line_chart.png')
        fig.write_image(png_path)
        return png_path
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 绘制竖向柱状图的工具
def plot_bar_chart(df, col_name):
    try:
        fig = px.bar(
            df, 
            x=df.index, 
            y=col_name, 
            title=f'Bar Chart of {col_name}',
            labels={'index': 'Index', col_name: col_name},
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12))
        )
        png_path = os.path.join('tmp', f'{col_name}_bar_chart.png')
        fig.write_image(png_path)
        return png_path
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 绘制散点图的工具
def plot_scatter_chart(df, x_col, y_col):
    try:
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col, 
            title=f'Scatter Plot of {x_col} vs {y_col}',
            labels={x_col: x_col, y_col: y_col},
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12))
        )
        png_path = os.path.join('tmp', f'{x_col}_vs_{y_col}_scatter_plot.png')
        fig.write_image(png_path)
        return png_path
    except KeyError as e:
        return f"Column '{str(e)}' does not exist in the dataframe."

# 绘制直方图的工具
def plot_histogram(df, col_name, bins=5):
    try:
        fig = px.histogram(
            df, 
            x=col_name, 
            nbins=bins, 
            title=f'Histogram of {col_name}',
            labels={col_name: col_name},
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12))
        )
        png_path = os.path.join('tmp', f'{col_name}_histogram.png')
        fig.write_image(png_path)
        return png_path
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."

# 绘制箱线图的工具
def plot_box_plot(df, col_name):
    try:
        fig = px.box(
            df, 
            y=col_name, 
            title=f'Box Plot of {col_name}',
            labels={col_name: col_name},
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_traces(boxmean='sd')
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12))
        )
        png_path = os.path.join('tmp', f'{col_name}_box_plot.png')
        fig.write_image(png_path)
        return png_path
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."
    

# 绘制饼状图的工具
def plot_pie_chart(df, col_name):
    try:
        fig = px.pie(
            df, 
            names=col_name, 
            title=f'Pie Chart of {col_name}',
            color_discrete_sequence=[generate_random_color()]
        )
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5)
        )
        png_path = os.path.join('tmp', f'{col_name}_pie_chart.png')
        fig.write_image(png_path)
        return png_path
    except KeyError:
        return f"Column '{col_name}' does not exist in the dataframe."