# AgentGo rapid process

## API 接口文档

### 1. 上传文档文件并分块插入向量数据库

**接口地址**: `/upload_file/upload_doc`

**请求方式**: `POST`

**请求参数**:
- `db_name` (表单字段): 数据库名称
- `chunk_size` (表单字段): 每个块的大小
- `chunk_overlap` (表单字段): 块之间的重叠大小
- `files` (文件字段): 上传的文件列表

**返回示例**:
```json
{
  "message": "Files {file1, file2, ...} uploaded successfully"
}
```

**代码调用示例**:
```python
import requests

url = "http://localhost:5000/upload_file/upload_doc"
data = {
    'db_name': 'test_db',
    'chunk_size': 250,
    'chunk_overlap': 100
}
files = {'files': open('example.docx', 'rb')}
response = requests.post(url, data=data, files=files)
print(response.json())
```

### 2. 搜索向量数据库

**接口地址**: `/search`

**请求方式**: `GET`

**请求参数**:
- `db_name` (查询参数): 数据库名称
- `collection_name` (查询参数): 集合名称
- `query` (查询参数): 查询字符串
- `top_k` (查询参数): 返回的结果数量 (默认值: 5)

**返回示例**:
```json
{
  "document_result": [
    {
      "text": "Document content",
      "distance": 0.123
    },
    ...
  ]
}
```

**代码调用示例**:
```python
import requests

url = "http://localhost:5000/search"
params = {
    'db_name': 'test_db',
    'collection_name': 'test_collection',
    'query': 'example query',
    'top_k': 5
}
response = requests.get(url, params=params)
print(response.json())
```

### 3. 上传 Excel 或 CSV 文件并保存为 pickle

**接口地址**: `/upload_file/upload_excel_or_csv`

**请求方式**: `POST`

**请求参数**:
- `file` (文件字段): 上传的 Excel 或 CSV 文件

**返回示例**:
```json
{
  "message": "File 'example.csv' has been uploaded and saved as pickle."
}
```

**代码调用示例**:
```python
import requests

url = "http://localhost:5000/upload_file/upload_excel_or_csv"
files = {'file': open('example.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### 4. 查询表格和文档

**接口地址**: `/query`

**请求方式**: `POST`

**请求参数**:
- `query` (表单字段): 查询字符串
- `db_name` (表单字段): 数据库名称
- `table_file_name` (表单字段, 可选): 表格文件名称
- `doc_file_name` (表单字段, 可选): 文档文件名称

**返回示例**:
```json
{
  "query": "example query",
  "answer": "example answer",
  "results": {
    "table_result": "table analysis result",
    "document_result": "document search result"
  },
  "image": "base64_encoded_image"
}
```

**代码调用示例**:
```python
import requests

url = "http://localhost:5000/query"
data = {
    'query': 'example query',
    'db_name': 'test_db',
    'table_file_name': 'example_table',
    'doc_file_name': 'example_doc'
}
response = requests.post(url, data=data)
print(response.json())
```

### 5. 删除所有数据

**接口地址**: `/delete_data`

**请求方式**: `DELETE`

**请求参数**: 无

**返回示例**:
```json
{
  "message": "All data in milvus_db and pickles folders have been deleted."
}
```

**代码调用示例**:
```python
import requests

url = "http://localhost:5000/delete_data"
response = requests.delete(url)
print(response.json())
```

### 6. 处理表格文件

**函数**: `process_table_file`

**参数**:
- `query` (字符串): 查询字符串
- `table_file_name` (字符串): 表格文件名称

**返回**: JSON 字符串结果

**代码调用示例**:
```python
result = process_table_file('example query', 'example_table')
print(result)
```

### 7. 处理文档文件

**函数**: `process_document_file`

**参数**:
- `query` (字符串): 查询字符串
- `db_name` (字符串): 数据库名称
- `doc_file_name` (字符串): 文档文件名称

**返回**: JSON 字符串结果

**代码调用示例**:
```python
result = process_document_file('example query', 'test_db', 'example_doc')
print(result)
```
