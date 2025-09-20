#!/usr/bin/env python3
"""
提取《情绪勒索》的目录和金句
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import get_toc, extract_chapter_from_epub

def extract_emotional_blackmail_toc():
    """提取《情绪勒索》的目录结构"""
    epub_path = "/Users/xudongqi/Downloads/情緒勒索〔全球暢銷20年經典〕：遇到利用恐懼、責任與罪惡感控制你的人，該怎麼辦？ = Emotional Blackmail When the People in Your Life Use Fear, Obligation, and Gui... (Z-Library).epub"
    
    try:
        print("📚 《情绪勒索》目录结构")
        print("=" * 80)
        
        toc = get_toc(epub_path)
        
        for i, item in enumerate(toc, 1):
            if isinstance(item, tuple) and len(item) >= 2:
                title, href = item[0], item[1]
            else:
                title = str(item)
                href = ''
            print(f"{i:2d}. {title}")
            if href:
                print(f"    📄 {href}")
            print()
            
        print(f"\n总计：{len(toc)} 个章节")
        return toc
        
    except Exception as e:
        print(f"❌ 提取目录时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def extract_key_content_for_quotes(toc):
    """提取关键章节内容寻找金句"""
    epub_path = "/Users/xudongqi/Downloads/情緒勒索〔全球暢銷20年經典〕：遇到利用恐懼、責任與罪惡感控制你的人，該怎麼辦？ = Emotional Blackmail When the People in Your Life Use Fear, Obligation, and Gui... (Z-Library).epub"
    
    # 选择可能包含金句的关键章节（前言、第1章、第2章、结论等）
    key_chapters = []
    for item in toc[:5]:  # 前5个章节
        key_chapters.append(item)
    
    # 也包含最后几个章节
    if len(toc) > 5:
        key_chapters.extend(toc[-3:])  # 最后3个章节
    
    print("\n🔍 正在提取关键章节内容寻找金句...")
    print("=" * 80)
    
    all_quotes = []
    
    for chapter in key_chapters:
        if isinstance(chapter, tuple) and len(chapter) >= 2:
            title, href = chapter[0], chapter[1]
        else:
            title = str(chapter)
            href = ''
        
        if not href:
            continue
            
        try:
            print(f"\n📖 正在分析: {title}")
            print("-" * 60)
            
            content = extract_chapter_from_epub(epub_path, href)
            
            if content:
                # 寻找可能的金句（包含关键词的句子）
                quotes = find_golden_quotes_in_text(content, title)
                all_quotes.extend(quotes)
                
                # 显示章节摘要
                lines = content.split('\n')
                clean_lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]
                
                if clean_lines:
                    print(f"章节摘要（前3句）:")
                    for i, line in enumerate(clean_lines[:3]):
                        if len(line) > 100:
                            line = line[:100] + "..."
                        print(f"  • {line}")
                
        except Exception as e:
            print(f"  ❌ 提取章节内容失败: {str(e)}")
    
    return all_quotes

def find_golden_quotes_in_text(text, chapter_title):
    """从文本中寻找金句"""
    quotes = []
    
    # 关键词列表，用于识别可能的金句
    keywords = [
        "情绪勒索", "恐惧", "责任", "罪恶感", "控制", "操纵", "边界", "自我保护",
        "健康关系", "沟通", "拒绝", "自尊", "独立", "选择", "权力", "尊重",
        "爱", "关系", "心理", "情感", "压力", "焦虑", "愧疚", "自由"
    ]
    
    # 分割文本为句子
    sentences = []
    for delimiter in ['。', '！', '？', '.', '!', '?']:
        text = text.replace(delimiter, delimiter + '|SPLIT|')
    
    raw_sentences = text.split('|SPLIT|')
    
    for sentence in raw_sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and len(sentence) < 200:  # 合适长度的句子
            # 检查是否包含关键词
            for keyword in keywords:
                if keyword in sentence:
                    # 进一步筛选有价值的句子
                    if any(indicator in sentence for indicator in ['是', '要', '应该', '必须', '可以', '能够', '需要', '重要', '关键']):
                        quotes.append({
                            'text': sentence,
                            'chapter': chapter_title,
                            'keyword': keyword
                        })
                        break
    
    return quotes

def display_golden_quotes(quotes):
    """显示整理后的金句"""
    if not quotes:
        print("\n❌ 未找到明显的金句")
        return
    
    print(f"\n✨ 《情绪勒索》金句集锦 ({len(quotes)}条)")
    print("=" * 80)
    
    # 按章节分组
    quotes_by_chapter = {}
    for quote in quotes:
        chapter = quote['chapter']
        if chapter not in quotes_by_chapter:
            quotes_by_chapter[chapter] = []
        quotes_by_chapter[chapter].append(quote)
    
    for chapter, chapter_quotes in quotes_by_chapter.items():
        print(f"\n📖 {chapter}")
        print("-" * 60)
        
        for i, quote in enumerate(chapter_quotes[:3], 1):  # 每章最多显示3条
            text = quote['text']
            keyword = quote['keyword']
            print(f"{i}. 「{text}」")
            print(f"   🔑 关键词: {keyword}")
            print()

if __name__ == "__main__":
    # 1. 提取目录
    toc = extract_emotional_blackmail_toc()
    
    if toc:
        # 2. 提取关键内容寻找金句
        quotes = extract_key_content_for_quotes(toc)
        
        # 3. 显示金句
        display_golden_quotes(quotes)