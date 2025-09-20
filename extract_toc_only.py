#!/usr/bin/env python3
"""
只提取《情绪勒索》的目录结构
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import get_toc

def extract_toc_only():
    """提取《情绪勒索》的完整目录结构"""
    epub_path = "/Users/xudongqi/Downloads/情緒勒索〔全球暢銷20年經典〕：遇到利用恐懼、責任與罪惡感控制你的人，該怎麼辦？ = Emotional Blackmail When the People in Your Life Use Fear, Obligation, and Gui... (Z-Library).epub"
    
    try:
        print("📚 《情绪勒索》完整目录结构")
        print("=" * 80)
        
        toc = get_toc(epub_path)
        
        for i, item in enumerate(toc, 1):
            if isinstance(item, tuple) and len(item) >= 2:
                title, href = item[0], item[1]
            else:
                title = str(item)
                href = ''
            print(f"{i:2d}. {title}")
            
        print(f"\n总计：{len(toc)} 个章节")
        
    except Exception as e:
        print(f"❌ 提取目录时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_toc_only()