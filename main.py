from search_manager import SearchManager

def main():
    manager = SearchManager()
    
    query = "最近几天热点新闻"
    
    print("\n正在搜索所有平台...")
    results = manager.search(query)
    
    for platform, result in results.items():
        print(f"\n=== {platform} 搜索结果 ===")
        if not result.get('success'):
            print(f"错误码: {result.get('error_code')}")
            print(f"错误信息: {result.get('error_message')}")
        else:
            print(result)

if __name__ == "__main__":
    main()