#!/usr/bin/env python3
"""
PyMuPDF 元数据提取演示

这个示例展示了如何使用 PyMuPDF 提取 PDF 文件的元数据，
并与 PyPDF2 进行对比。
"""

import os
import sys
from typing import Dict, Union, List

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from ebook_mcp.tools.pdf_helper import get_meta, get_meta_pypdf2
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"导入错误: {e}")
    DEPENDENCIES_AVAILABLE = False

def print_metadata_comparison(pdf_path: str):
    """
    比较 PyMuPDF 和 PyPDF2 的元数据提取结果
    
    Args:
        pdf_path: PDF 文件路径
    """
    if not DEPENDENCIES_AVAILABLE:
        print("❌ 依赖库不可用，无法运行演示")
        return
    
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        return
    
    print(f"📄 分析 PDF 文件: {pdf_path}")
    print("=" * 60)
    
    try:
        # 使用 PyMuPDF 提取元数据
        print("🔍 使用 PyMuPDF 提取元数据:")
        pymupdf_meta = get_meta(pdf_path)
        
        print("PyMuPDF 提取的字段:")
        for key, value in pymupdf_meta.items():
            print(f"  {key}: {value}")
        
        print("\n" + "-" * 40)
        
        # 使用 PyPDF2 提取元数据
        print("🔍 使用 PyPDF2 提取元数据:")
        pypdf2_meta = get_meta_pypdf2(pdf_path)
        
        print("PyPDF2 提取的字段:")
        for key, value in pypdf2_meta.items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        
        # 比较结果
        print("📊 对比分析:")
        print(f"PyMuPDF 提取字段数: {len(pymupdf_meta)}")
        print(f"PyPDF2 提取字段数: {len(pypdf2_meta)}")
        
        # PyMuPDF 独有的字段
        pymupdf_only = set(pymupdf_meta.keys()) - set(pypdf2_meta.keys())
        if pymupdf_only:
            print(f"PyMuPDF 独有字段: {', '.join(pymupdf_only)}")
        
        # PyPDF2 独有的字段
        pypdf2_only = set(pypdf2_meta.keys()) - set(pymupdf_meta.keys())
        if pypdf2_only:
            print(f"PyPDF2 独有字段: {', '.join(pypdf2_only)}")
        
        # 共同字段
        common_fields = set(pymupdf_meta.keys()) & set(pypdf2_meta.keys())
        if common_fields:
            print(f"共同字段: {', '.join(common_fields)}")
            
            # 检查共同字段的值是否一致
            differences = []
            for field in common_fields:
                if pymupdf_meta[field] != pypdf2_meta[field]:
                    differences.append(field)
            
            if differences:
                print(f"值不一致的字段: {', '.join(differences)}")
            else:
                print("✅ 共同字段的值完全一致")
        
    except Exception as e:
        print(f"❌ 提取元数据时出错: {e}")

def demonstrate_pymupdf_advantages():
    """
    演示 PyMuPDF 的优势
    """
    print("\n🚀 PyMuPDF 的优势:")
    print("1. 📏 页面尺寸信息: 可以获取页面的宽度和高度")
    print("2. 🔐 加密状态: 可以检测 PDF 是否加密")
    print("3. 📊 PDF 版本: 获取 PDF 文件版本信息")
    print("4. 📁 文件大小: 获取文件大小信息")
    print("5. 🏷️ 关键词: 提取 PDF 关键词信息")
    print("6. 📝 格式信息: 获取文档格式信息")
    print("7. ⚡ 性能: 更快的处理速度")
    print("8. 🛠️ 功能丰富: 支持更多 PDF 操作")

def main():
    """主函数"""
    print("🎯 PyMuPDF vs PyPDF2 元数据提取对比演示")
    print("=" * 60)
    
    # 演示 PyMuPDF 的优势
    demonstrate_pymupdf_advantages()
    
    # 如果有命令行参数，使用指定的 PDF 文件
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print_metadata_comparison(pdf_path)
    else:
        print("\n💡 使用方法:")
        print("python pymupdf_metadata_demo.py <PDF文件路径>")
        print("\n例如:")
        print("python pymupdf_metadata_demo.py /path/to/your/document.pdf")
        
        # 尝试在常见位置查找 PDF 文件
        common_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
            "."
        ]
        
        pdf_files = []
        for path in common_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(path, file))
        
        if pdf_files:
            print(f"\n📁 在常见位置找到 {len(pdf_files)} 个 PDF 文件:")
            for i, pdf_file in enumerate(pdf_files[:5], 1):  # 只显示前5个
                print(f"  {i}. {pdf_file}")
            
            if len(pdf_files) > 5:
                print(f"  ... 还有 {len(pdf_files) - 5} 个文件")
            
            print(f"\n💡 可以运行: python pymupdf_metadata_demo.py '{pdf_files[0]}'")
        else:
            print("\n❌ 未找到 PDF 文件")

if __name__ == "__main__":
    main() 