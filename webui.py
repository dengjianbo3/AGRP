import gradio as gr
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import shutil

API_BASE_URL = "http://localhost:5000"  # 替换为你的API服务器地址

uploaded_files = {}

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    _, file_ext = os.path.splitext(file_name)

    if file_ext in ['.csv', '.xlsx', 'xls']:
        url = f"{API_BASE_URL}/upload_file/upload_excel_or_csv"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)
    elif file_ext in ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg']:
        url = f"{API_BASE_URL}/upload_file/upload_doc"
        files = {'files': open(file_path, 'rb')}
        data = {
            'db_name': 'test',  # 默认数据库名称
            'chunk_size': 250,  # 默认chunk大小
            'chunk_overlap': 100  # 默认chunk重叠大小
        }
        response = requests.post(url, data=data, files=files)
    else:
        return "Unsupported file type"

    print(f"Status Code: {response.status_code}")  # 打印状态码
    print(f"Response Text: {response.text}")  # 打印响应文本

    if response.status_code == 200:
        uploaded_files[file_name] = file_path
        return list(uploaded_files.keys())
    else:
        return f"Failed to upload file: {response.text}"

def query_api(query, table_file_name, doc_file_name):
    url = f"{API_BASE_URL}/query"
    data = {
        'query': query,
        'db_name': 'test',  # 默认数据库名称
        'table_file_name': table_file_name,
        'doc_file_name': doc_file_name,
    }
    response = requests.post(url, data=data)
    return response.json()

def respond(message, sources, chat_history):
    table_file_name = None
    doc_file_name = None
    for source in sources:
        _, file_ext = os.path.splitext(source)
        if file_ext in ['.csv', '.xlsx', 'xls']:
            table_file_name = os.path.splitext(source)[0]
        else:
            doc_file_name = os.path.splitext(source)[0]
    
    result = query_api(message, table_file_name, doc_file_name)
    
    if result.get('image'):
        # 解析Base64编码的图片
        image_data = base64.b64decode(result['image'])
        image = Image.open(BytesIO(image_data))
        chat_history.append((message, gr.Image(value=image, label="Result Image")))
    else:
        answer = result.get('answer', 'No answer received.')
        chat_history.append((message, answer))
    return "", chat_history

def validate_selection(selected_files):
    table_count = 0
    doc_count = 0
    for file in selected_files:
        _, file_ext = os.path.splitext(file)
        if file_ext in ['.csv', '.xlsx', 'xls']:
            table_count += 1
        else:
            doc_count += 1

    if len(selected_files) > 2:
        return gr.update(value=[], choices=list(uploaded_files.keys()), label="选择回答来源 (最多选择2个文件)")
    if table_count > 1 or doc_count > 1:
        return gr.update(value=[], choices=list(uploaded_files.keys()), label="选择回答来源 (最多一个表格文件和一个文档文件)")

    return gr.update(choices=list(uploaded_files.keys()))

def update_source(files, chat_history):
    global uploaded_files
    if chat_history is None:
        chat_history = []
    
    messages = []
    for file in files:
        upload_file(file.name)
        file_name = os.path.basename(file.name)
    return list(uploaded_files.keys()), chat_history

def clear_all_data():
    global uploaded_files
    # 清除Gradio缓存数据
    uploaded_files = {}
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')
        os.makedirs('tmp')

    # 调用服务器接口清除所有数据
    url = f"{API_BASE_URL}/delete_data"
    response = requests.delete(url)
    if response.status_code == 200:
        return "All data has been cleared."
    else:
        return f"Failed to clear data: {response.text}"

with gr.Blocks() as demo:
    gr.Markdown(
    """
    # AgentGO rapid processor 艾果
    """
    )

    chatbot = gr.Chatbot(
        avatar_images=(None, None),  # 如果有头像，可以在这里设置
        bubble_full_width=False, 
        height=400,
        show_copy_button=True,
    )
    
    with gr.Column():
        
        with gr.Row(equal_height=True):
            msg = gr.Textbox(show_label=False, placeholder="请输入你的问题", elem_classes="full-width", scale=9)
            submit_btn = gr.Button("GO", scale=1, min_width=5, size='sm', variant="primary")
            
        with gr.Row(equal_height=False):
            source = gr.CheckboxGroup(choices=[], label="选择回答来源文件", scale=9)
            clear_btn = gr.Button("清除数据", scale=1, min_width=10, size='sm')  # 添加清除数据按钮
        file_upload = gr.File(label="上传文件", file_count="multiple", type="filepath",
                              file_types=["doc", "docx", "pdf", "png", "jpg", "jpeg", "xlsx", "csv", "xls"], 
                              visible=True)
        

    def handle_upload(files, chat_history):
        return update_source(files, chat_history)
    
    file_upload.upload(handle_upload, inputs=[file_upload, chatbot], outputs=[source, chatbot])

    source.change(validate_selection, source, [source])
    msg.submit(respond, inputs=[msg, source, chatbot], outputs=[msg, chatbot])
    submit_btn.click(respond, inputs=[msg, source, chatbot], outputs=[msg, chatbot])
    clear_btn.click(clear_all_data, outputs=[])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=3389, share=True)
