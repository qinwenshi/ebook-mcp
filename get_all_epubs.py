#!/usr/bin/env python3
"""
获取所有EPUB文件
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import get_all_epub_files

def get_epubs_from_downloads():
    """从Downloads目录获取所有EPUB文件"""
    downloads_path = "/Users/xudongqi/Downloads"
    
    try:
        print("📚 正在搜索EPUB文件...")
        print("=" * 60)
        
        epub_files = get_all_epub_files(downloads_path)
        
        if epub_files:
            print(f"✅ 找到 {len(epub_files)} 个EPUB文件：\n")
            
            for i, epub_file in enumerate(epub_files, 1):
                # 获取文件名（不包含路径）
                filename = os.path.basename(epub_file)
                # 获取文件大小
                try:
                    file_size = os.path.getsize(epub_file)
                    size_mb = file_size / (1024 * 1024)
                    print(f"{i:2d}. {filename}")
                    print(f"    📁 路径: {epub_file}")
                    print(f"    📊 大小: {size_mb:.2f} MB")
                    print()
                except OSError:
                    print(f"{i:2d}. {filename}")
                    print(f"    📁 路径: {epub_file}")
                    print(f"    ⚠️  无法获取文件大小")
                    print()
        else:
            print("❌ 未找到任何EPUB文件")
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

def get_epubs_from_current_dir():
    """从当前目录获取EPUB文件"""
    current_path = os.getcwd()
    
    try:
        print(f"\n🔍 在当前目录搜索EPUB文件: {current_path}")
        print("-" * 60)
        
        epub_files = get_all_epub_files(current_path)
        
        if epub_files:
            print(f"✅ 找到 {len(epub_files)} 个EPUB文件：\n")
            
            for i, epub_file in enumerate(epub_files, 1):
                filename = os.path.basename(epub_file)
                print(f"{i:2d}. {filename}")
                print(f"    📁 {epub_file}")
        else:
            print("❌ 当前目录未找到EPUB文件")
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    # 搜索Downloads目录
    get_epubs_from_downloads()
    
    # 搜索当前目录
    get_epubs_from_current_dir()