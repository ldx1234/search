import requests
import json
from config import Config
from exceptions import BaiduAPIError

class BaiduSearchClient:
    def __init__(self):
        self.api_key = Config.BAIDU_API_KEY
        self.secret_key = Config.BAIDU_SECRET_KEY
        self.token_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.search_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugins/websearch"
        self.access_token = None
    
    def _get_access_token(self):
        if not self.api_key or not self.secret_key:
            raise ValueError("百度API Key或Secret Key未配置")
        
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        try:
            response = requests.post(self.token_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'error' in result:
                error_code = result.get('error_code', 0)
                error_msg = result.get('error_description', result.get('error', '未知错误'))
                raise BaiduAPIError(error_code, error_msg, response)
            
            self.access_token = result.get("access_token")
            if not self.access_token:
                raise BaiduAPIError(0, "获取access_token失败", response)
            
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise BaiduAPIError(500, str(e))
    
    def search(self, query, size=10):
        if not self.access_token:
            self._get_access_token()
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "query": query,
            "size": size
        }
        
        params = {
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(self.search_url, headers=headers, params=params, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            
            if 'error_code' in result:
                error_code = result.get('error_code', 0)
                error_msg = result.get('error_msg', '未知错误')
                raise BaiduAPIError(error_code, error_msg, response)
            
            return result
        except requests.exceptions.RequestException as e:
            raise BaiduAPIError(500, str(e))