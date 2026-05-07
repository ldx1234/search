from search_manager import SearchManager

def main():
    manager = SearchManager()
    
    query = input("请输入搜索关键词: ")
    
    print("\n正在搜索所有平台...")
    results = manager.search(query)
    
    for platform, result in results.items():
        print(f"\n=== {platform} 搜索结果 ===")
        if 'error' in result:
            print(f"错误: {result['error']}")
        else:


            print(result)

if __name__ == "__main__":
    main()