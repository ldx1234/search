import requests
import json
import time
import hmac
import hashlib
from urllib.parse import quote
from config import Config
from exceptions import AliyunAPIError

class AliyunSearchClient:
    def __init__(self):
        self.access_key_id = Config.ALIYUN_ACCESS_KEY_ID
        self.access_key_secret = Config.ALIYUN_ACCESS_KEY_SECRET
        self.endpoint = Config.ALIYUN_ENDPOINT
        self.instance_name = Config.ALIYUN_INSTANCE_NAME
        self.version = "2017-12-25"
    
    def _generate_signature(self, params):
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        canonical_querystring = "&".join([f"{k}={quote(str(v), safe='')}" for k, v in sorted_params])
        
        string_to_sign = f"GET\n/\n\n{canonical_querystring}"
        
        signature = hmac.new(
            self.access_key_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        return signature.hex()
    
    def search(self, query, size=10):
        if not self.access_key_id or not self.access_key_secret:
            raise ValueError("阿里云Access Key ID或Access Key Secret未配置")
        
        if not self.endpoint:
            raise ValueError("阿里云Endpoint未配置")
        
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        params = {
            "Action": "Search",
            "Version": self.version,
            "AccessKeyId": self.access_key_id,
            "Timestamp": timestamp,
            "SignatureMethod": "HMAC-SHA1",
            "SignatureVersion": "1.0",
            "SignatureNonce": str(int(time.time() * 1000)),
            "Query": query,
            "Size": size
        }
        
        if self.instance_name:
            params["InstanceName"] = self.instance_name
        
        signature = self._generate_signature(params)
        params["Signature"] = signature
        
        try:
            response = requests.get(self.endpoint, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'Error' in result:
                error_code = result['Error'].get('Code', 'Unknown')
                error_msg = result['Error'].get('Message', '未知错误')
                raise AliyunAPIError(error_code, error_msg, response)
            
            return result
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', 500)
            raise AliyunAPIError(status_code, str(e))