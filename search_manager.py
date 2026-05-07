from search_clients import BaiduSearchClient, VolcSearchClient, AliyunSearchClient
from exceptions import SearchAPIError

class SearchManager:
    def __init__(self):
        self.clients = {
            'baidu': BaiduSearchClient(),
            'volc': VolcSearchClient(),
            'aliyun': AliyunSearchClient()
        }
    
    def search(self, query, platforms=None, size=10):
        if platforms is None:
            platforms = list(self.clients.keys())
        
        results = {}
        for platform in platforms:
            if platform in self.clients:
                try:
                    client = self.clients[platform]
                    result = client.search(query, size)
                    results[platform] = {'success': True, 'data': result}
                except SearchAPIError as e:
                    results[platform] = {
                        'success': False,
                        'error_code': e.error_code,
                        'error_message': e.error_message,
                        'platform': e.platform,
                        'detail': str(e)
                    }
                except ValueError as e:
                    results[platform] = {
                        'success': False,
                        'error_code': 'CONFIG_ERROR',
                        'error_message': str(e),
                        'platform': platform,
                        'detail': str(e)
                    }
                except Exception as e:
                    results[platform] = {
                        'success': False,
                        'error_code': 'UNKNOWN_ERROR',
                        'error_message': str(e),
                        'platform': platform,
                        'detail': str(e)
                    }
        
        return results
    
    def search_baidu(self, query, size=10):
        return self.clients['baidu'].search(query, size)
    
    def search_volc(self, query, size=10):
        return self.clients['volc'].search(query, size)
    
    def search_aliyun(self, query, size=10):
        return self.clients['aliyun'].search(query, size)