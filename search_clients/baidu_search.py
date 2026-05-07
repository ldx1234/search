import requests
import json
from config import Config
from exceptions import BaiduAPIError

class BaiduSearchClient:
    def __init__(self):
        self.api_key = Config.BAIDU_API_KEY
        self.search_url = "https://qianfan.baidubce.com/v2/ai_search/web_search"

    def search(self, query):
        
        headers = {
            "Content-Type": "application/json"
        }
        headers['Authorization']="Bearer"+ " "+self.api_key

        payload = json.dumps({
            "messages": [
                {
                   "role": "user",
                    "content": query
                }
            ],
            "edition": "standard",
            "search_source": "baidu_search_v2",
            "search_recency_filter": "week" ##网页发布时间
        }, ensure_ascii=False)

        try:
            response = requests.request("POST", self.search_url , headers=headers, data=payload.encode("utf-8"))
            result = response.json()

            if 'error_code' in result:
                error_code = result.get('error_code', 0)
                error_msg = result.get('error_msg', '未知错误')
                raise BaiduAPIError(error_code, error_msg, response)

            return result
        except requests.exceptions.RequestException as e:
            raise BaiduAPIError(500, str(e))
