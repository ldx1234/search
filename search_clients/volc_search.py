import requests
import json
import time
import hashlib
import hmac
from config import Config
from exceptions import VolcAPIError

class VolcSearchClient:
    def __init__(self):
        self.api_key = Config.VOLC_API_KEY
        self.secret_key = Config.VOLC_SECRET_KEY
        self.host = "search.bytedance.net"
        self.search_url = f"https://{self.host}/api/search"
    
    def _generate_signature(self, method, path, params, timestamp):
        canonical_querystring = "&".join([f"{k}={params[k]}" for k in sorted(params.keys())])
        string_to_sign = f"{method}\n{self.host}\n{path}\n{canonical_querystring}"
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def search(self, query, size=10):
        if not self.api_key or not self.secret_key:
            raise ValueError("火山引擎API Key或Secret Key未配置")
        
        timestamp = int(time.time())
        path = "/api/search"
        
        params = {
            "query": query,
            "size": size,
            "api_key": self.api_key,
            "timestamp": timestamp
        }
        
        signature = self._generate_signature("GET", path, params, timestamp)
        params["signature"] = signature
        
        try:
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'code' in result and result['code'] != 0:
                error_code = result.get('code', 0)
                error_msg = result.get('msg', result.get('message', '未知错误'))
                raise VolcAPIError(error_code, error_msg, response)
            
            return result
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', 500)
            raise VolcAPIError(status_code, str(e))