#!/usr/bin/env python3
"""
简洁地列出所有EPUB文件
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import get_all_epub_files

def list_all_epubs():
    """列出Downloads目录中的所有EPUB文件"""
    downloads_path = "/Users/xudongqi/Downloads"
    
    try:
        epub_files = get_all_epub_files(downloads_path)
        
        print(f"📚 在 {downloads_path} 目录中找到 {len(epub_files)} 个EPUB文件：")
        print("=" * 80)
        
        for i, epub_file in enumerate(epub_files, 1):
            filename = os.path.basename(epub_file)
            print(f"{i:2d}. {filename}")
            
        print("\n" + "=" * 80)
        print(f"总计：{len(epub_files)} 个EPUB文件")
        
        # 按类别分类
        categories = {
            "经济学/商业": [],
            "文学/小说": [],
            "科技/设计": [],
            "心理学/自我提升": [],
            "历史/社会": [],
            "其他": []
        }
        
        for epub_file in epub_files:
            filename = os.path.basename(epub_file).lower()
            if any(keyword in filename for keyword in ["经济", "商业", "零售", "创业", "投资", "牛奶可乐", "克鲁格曼", "穷查理"]):
                categories["经济学/商业"].append(epub_file)
            elif any(keyword in filename for keyword in ["盖茨比", "水浒", "大奉", "全频带", "素书"]):
                categories["文学/小说"].append(epub_file)
            elif any(keyword in filename for keyword in ["科技", "设计", "技术"]):
                categories["科技/设计"].append(epub_file)
            elif any(keyword in filename for keyword in ["情绪", "心理", "潜能", "脑筋"]):
                categories["心理学/自我提升"].append(epub_file)
            elif any(keyword in filename for keyword in ["枪炮", "病菌", "钢铁", "历史", "社会"]):
                categories["历史/社会"].append(epub_file)
            else:
                categories["其他"].append(epub_file)
        
        print("\n📂 按类别分类：")
        print("-" * 80)
        for category, files in categories.items():
            if files:
                print(f"\n{category} ({len(files)}个):")
                for file in files:
                    filename = os.path.basename(file)
                    print(f"  • {filename}")
                    
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    list_all_epubs()