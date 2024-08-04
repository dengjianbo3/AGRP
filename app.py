# app.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional, Any
import os
import numpy as np
import pandas as pd 

from modules.loader import DocxDocLoader, RapidOCRPDFLoader, RapidOCRLoader
from modules.embedding import EmbeddingModel
from modules.vector_db import MilvusHelper
from modules.table_analysis import TableAnalysis
from modules.utils import read_file_to_df, save_df_to_pickle
from modules.model_call import QwenCall, DeepseekCall, GlmCall

import tempfile
import base64

import json 

app = FastAPI()

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)


# 设置保存pickle文件的路径
PICKLE_FOLDER = 'pickles'
if not os.path.exists(PICKLE_FOLDER):
    os.makedirs(PICKLE_FOLDER)

# 初始化 EmbeddingModel 和 MilvusHelper
embedding_model = EmbeddingModel()
milvus_helper = MilvusHelper()

qwen = QwenCall()
deepseek = DeepseekCall()
glm = GlmCall()

# 存储上传的文本和向量
uploaded_data = {
    "texts": [],
    "embeddings": []
}

@app.post("/upload_file/upload_doc", summary="Upload doc files and split docs into chunks and insert to vector database")
async def upload_doc(db_name: str = Form(...),
                     chunk_size: int = Form(...),
                     chunk_overlap: int = Form(...),
                     files: List[UploadFile] = File(...)) -> Dict[str, str]:
    """
    Upload doc files and split docs into chunks and insert to vector database.
    
    :param db_name: Name of the database.
    :param collection_name: Name of the collection.
    :param chunk_size: Size of each chunk.
    :param chunk_overlap: Overlap between chunks.
    :param files: List of uploaded files.
    :return: Dictionary containing a success message.
    """
    uploaded_files = []
    
    for file in files:
        tmp_file_path = None
        try:
            # Save the uploaded file to a temporary file
            print(f"{file.filename} uploading ")
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(await file.read())
                tmp_file_path = tmp_file.name
            
            # Get the file extension from the original filename
            org_name, file_extension = os.path.splitext(file.filename)
            file_extension = file_extension.lower().lstrip('.')
            
            if file_extension in ["doc", "docx"]:
                loader = DocxDocLoader(tmp_file_path, file_name=file.filename, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            elif file_extension == "pdf":
                loader = RapidOCRPDFLoader(tmp_file_path, file_name=file.filename, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                loader = RapidOCRLoader(file_path=tmp_file_path)
            else:
                os.unlink(tmp_file_path)
                raise HTTPException(status_code=400, detail=f"{file_extension} type not supported yet, only support doc, docx, pdf, png, jpg, jpeg for now")
            
            docs = loader.load()
            
            # Insert each row of data into the vector database
            texts = [str(doc.page_content) for doc in docs]
            embeddings = embedding_model.embed_with_list_of_str(texts)
            
            client = milvus_helper.get_milvus_client(db_name)
            milvus_helper.create_collection(client, org_name)
            milvus_helper.insert_data(client, org_name, texts, [embedding['embedding'] for embedding in embeddings['output']['embeddings']])
            
            # Delete the temporary file
            os.unlink(tmp_file_path)
            
            uploaded_files.append(file.filename)
            print(f"{file.filename} uploaded")
        
        except Exception as e:
            # Delete the temporary file if it exists
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            raise HTTPException(status_code=400, detail=f"Error loading {file.filename}: {e}")
    
    return {"message": f"Files {', '.join(uploaded_files)} uploaded successfully"}

@app.get("/search")
async def search(db_name: str, collection_name: str, query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search in the vector database.

    :param db_name: Name of the database.
    :param collection_name: Name of the collection.
    :param query: Query string.
    :param top_k: Number of top results to return.
    :return: Search results.
    """
    return {"document_result": process_document_file(query, db_name, collection_name)}


@app.post("/upload_file/upload_excel_or_csv", summary="Upload Excel or CSV file and save as pickle")
async def upload_excel_or_csv(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Upload an Excel or CSV file, convert to DataFrame, and save as pickle file.
    
    :param file: Uploaded Excel or CSV file.
    :return: Dictionary containing a success message.
    """
    tmp_file_path = None
    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await file.read())
            tmp_file_path = tmp_file.name
        
        _, file_extension = os.path.splitext(file.filename)
        # Read the file into DataFrame
        df = read_file_to_df(tmp_file_path, file_extension)
        # Get the original file name without extension
        file_name = os.path.splitext(file.filename)[0]
        
        # Save DataFrame to pickle file
        save_df_to_pickle(df, file_name, PICKLE_FOLDER)
        
        # Delete the temporary file
        os.unlink(tmp_file_path)

        return {"message": f"File '{file.filename}' has been uploaded and saved as pickle."}
    
    except Exception as e:
        # Delete the temporary file if it exists
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error processing {file.filename}: {e}")
    

@app.post("/query", summary="Query with table and document")
async def query_table_and_document(query: str = Form(...), 
                                   db_name: str = Form(...),
                                   table_file_name: Optional[str] = Form(None), 
                                   doc_file_name: Optional[str] = Form(None)) -> Dict[str, Any]:
    """
    Query with a table and document file name. If table_file_name is provided, use TableAnalysis.
    If doc_file_name is provided, search in the vector database.

    :param query: Query string.
    :param table_file_name: Name of the table file in pickles folder.
    :param doc_file_name: Name of the document file in vector database.
    :return: Combined result from table analysis and document search.
    """
    final_result = {}
    import time 
    start_time = time.time()
    # Process table file if provided
    if table_file_name:
        final_result['table_result'] = process_table_file(query, table_file_name)

    # Process document file if provided
    if doc_file_name:
        final_result['document_result'] = process_document_file(query, db_name, doc_file_name)

    final_result_time = time.time()
    print(f"Time to generate tools result: {final_result_time - start_time} seconds")
    print(final_result)
    table_result = final_result.get("table_result")
    
    if table_result and table_result.startswith('"') and table_result.endswith('"'):
        table_result = json.loads(table_result)

    if table_result and table_result.endswith(".png"):
        with open(table_result, "rb") as image_file:
            base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return {"query": query, "answer": None, "results": None, "image": base64_encoded_image}
    
    else:
        from prompts.final_answer_prompt import final_answer_prompt
        prompt = final_answer_prompt.format(query=query, final_result=final_result)
        # answer = deepseek.get_response(prompt)
        answer = qwen.get_response(prompt)
        # answer = glm.get_response(prompt)

        output_time = time.time()
        print(f"Time to get response from model Call: {output_time - final_result_time} seconds")

        return {"query": query, "answer": answer, "results": final_result, "image": None}


@app.delete("/delete_data", summary="Delete all files in milvus_db and pickles")
async def delete_all_data() -> Dict[str, str]:
    """
    Delete all files in milvus_db and pickles folders.
    
    :return: Dictionary containing a success message.
    """
    try:
        # Delete all files in pickles folder
        milvus_folder = "milvus_db"
        for file in os.listdir(milvus_folder):
            file_path = os.path.join(milvus_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Delete all files in pickles folder
        for file in os.listdir(PICKLE_FOLDER):
            file_path = os.path.join(PICKLE_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return {"message": "All data in milvus_db and pickles folders have been deleted."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting data: {e}")


def process_table_file(query: str, table_file_name: str) -> str:
    """
    Process table file for the given query and return the result as a JSON string.

    :param query: Query string.
    :param table_file_name: Name of the table file in pickles folder.
    :return: JSON string result from table analysis.
    """
    try:
        pickle_path = os.path.join(PICKLE_FOLDER, f"{table_file_name}.pkl")

        if not os.path.exists(pickle_path):
            raise HTTPException(status_code=404, detail=f"Pickle file '{table_file_name}.pkl' not found")

        # Load DataFrame from pickle file
        df = pd.read_pickle(pickle_path)
        for column in df.select_dtypes(include=['datetime', 'datetimetz']):
            df[column] = df[column].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x) else '')

        ta_chat = TableAnalysis(df)
        table_result = ta_chat.call_with_messages(query)

        return json.dumps(table_result, ensure_ascii=False)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing table file '{table_file_name}': {e}")
    

def process_document_file(query: str, db_name: str, doc_file_name: str) -> str:
    """
    Process document file for the given query and return the result as a JSON string.

    :param query: Query string.
    :param db_name: Name of the database.
    :param doc_file_name: Name of the document file in vector database.
    :return: JSON string result from document search.
    """
    try:
        query_embedding = embedding_model.embed_with_list_of_str([query])
        query_vector = np.array([query_embedding['output']['embeddings'][0]['embedding']]).astype('float32')
        client = milvus_helper.get_milvus_client(db_name)

        results = milvus_helper.search(client, doc_file_name, query_vector, top_k=5)
        search_results = []
        for result in results[0]:
            search_results.append({
                "text": result['entity']['text'],
                "distance": result['distance']
            })

        return json.dumps(search_results, ensure_ascii=False)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing document file '{doc_file_name}': {e}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
