import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BAIDU_API_KEY = os.getenv('BAIDU_API_KEY', '')
    BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', '')
    
    VOLC_API_KEY = os.getenv('VOLC_API_KEY', '')
    VOLC_SECRET_KEY = os.getenv('VOLC_SECRET_KEY', '')
    
    ALIYUN_ACCESS_KEY_ID = os.getenv('ALIYUN_ACCESS_KEY_ID', '')
    ALIYUN_ACCESS_KEY_SECRET = os.getenv('ALIYUN_ACCESS_KEY_SECRET', '')
    ALIYUN_ENDPOINT = os.getenv('ALIYUN_ENDPOINT', '')
    ALIYUN_INSTANCE_NAME = os.getenv('ALIYUN_INSTANCE_NAME', '')