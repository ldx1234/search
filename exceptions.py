class SearchAPIError(Exception):
    def __init__(self, platform, error_code, error_message, response=None):
        self.platform = platform
        self.error_code = error_code
        self.error_message = error_message
        self.response = response
        super().__init__(f"[{platform}] Error {error_code}: {error_message}")

class BaiduAPIError(SearchAPIError):
    ERROR_CODES = {
        100: "请求格式错误",
        101: "API Key不存在",
        102: "API Key已过期",
        103: "API Key已被禁用",
        104: "签名错误",
        105: "请求参数缺失",
        106: "请求参数格式错误",
        107: "请求体过大",
        108: "请求频率超限",
        109: "账户余额不足",
        110: "IP白名单限制",
        111: "权限不足",
        200: "服务器内部错误",
        201: "服务暂不可用",
        202: "任务队列已满",
        300: "资源不存在",
        301: "资源已被删除",
        302: "资源已存在",
        400: "参数错误",
        401: "未授权",
        403: "禁止访问",
        404: "资源未找到",
        500: "服务器内部错误"
    }
    
    def __init__(self, error_code, error_message, response=None):
        code_desc = self.ERROR_CODES.get(error_code, "未知错误")
        super().__init__("Baidu", error_code, f"{code_desc} - {error_message}", response)

class VolcAPIError(SearchAPIError):
    ERROR_CODES = {
        400: "请求参数错误",
        401: "未授权或签名错误",
        403: "禁止访问",
        404: "资源未找到",
        408: "请求超时",
        429: "请求频率超限",
        500: "服务器内部错误",
        502: "网关错误",
        503: "服务不可用",
        504: "网关超时",
        10001: "API Key不存在",
        10002: "API Key已过期",
        10003: "签名错误",
        10004: "权限不足",
        10005: "账户余额不足",
        10006: "请求频率超限",
        20001: "搜索服务异常",
        20002: "索引不存在",
        20003: "查询语法错误"
    }
    
    def __init__(self, error_code, error_message, response=None):
        code_desc = self.ERROR_CODES.get(error_code, "未知错误")
        super().__init__("Volc", error_code, f"{code_desc} - {error_message}", response)

class AliyunAPIError(SearchAPIError):
    ERROR_CODES = {
        "InvalidAccessKeyId.NotFound": "Access Key ID不存在",
        "InvalidAccessKeyId": "Access Key ID无效",
        "SignatureDoesNotMatch": "签名不匹配",
        "AccessDenied": "访问被拒绝",
        "InvalidAction": "无效的Action",
        "InvalidParameter": "参数无效",
        "MissingParameter": "缺少必要参数",
        "InvalidVersion": "API版本无效",
        "Throttling": "请求频率超限",
        "InternalError": "服务器内部错误",
        "ServiceUnavailable": "服务不可用",
        "ResourceNotFound": "资源未找到",
        "ResourceAlreadyExists": "资源已存在"
    }
    
    def __init__(self, error_code, error_message, response=None):
        code_desc = self.ERROR_CODES.get(error_code, "未知错误")
        super().__init__("Aliyun", error_code, f"{code_desc} - {error_message}", response)