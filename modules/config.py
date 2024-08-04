import os

class Config:
    MONGO_URI = "mongodb://localhost:27017"
    STORAGE_PATH = "/path/to/storage"
    VECTOR_DB_URI = "milvus://localhost:19530"
    LANGCHAIN_API_KEY = "your_langchain_api_key"
    QWEN_MODEL = "qwen-max"
    QWEN_API = "sk-1fb7773985734d488ec71309a8e71ae6"
    QWEN_CHAT_MODEL = "qwen2-7b-instruct"
    DEEPSEEK_MODEL = "deepseek-chat"
    DEEPSEEK_API= "sk-3dad314c294d41e7b4b07591298dd9ca"
    GLM_MODEL = "glm-4"
    GLM_API = "d36be7fa64e2eb36584501f4f5f0f0fd.iYAkbh6Qc7V6R9Di"
    DASHSCOPE_MAX_BATCH_SIZE = 25