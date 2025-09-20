#!/usr/bin/env python3
"""
Debug script to inspect EPUB TOC structure and chapter ID matching
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import read_epub
from typing import Any

def debug_toc_structure(book: Any):
    """Debug the TOC structure to understand how chapter IDs are organized"""
    print("🔍 Debugging TOC Structure")
    print("=" * 50)
    
    print("\n📚 Raw TOC structure:")
    for i, item in enumerate(book.toc):
        print(f"  [{i}] Type: {type(item)}")
        if isinstance(item, tuple):
            chapter = item[0]
            print(f"      Main Chapter: '{chapter.title}' -> '{chapter.href}'")
            if len(item) > 1:
                print(f"      Subchapters ({len(item[1])}):")
                for j, sub_item in enumerate(item[1]):
                    if isinstance(sub_item, tuple):
                        print(f"        [{j}] '{sub_item[0].title}' -> '{sub_item[0].href}'")
                    else:
                        print(f"        [{j}] '{sub_item.title}' -> '{sub_item.href}'")
        else:
            print(f"      Chapter: '{item.title}' -> '{item.href}'")
    
    print("\n📋 Flattened TOC entries:")
    toc_entries = []
    for item in book.toc:
        if isinstance(item, tuple):
            chapter = item[0]
            toc_entries.append((chapter.title, chapter.href, 1))
            for sub_item in item[1]:
                if isinstance(sub_item, tuple):
                    toc_entries.append((sub_item[0].title, sub_item[0].href, 2))
                else:
                    toc_entries.append((sub_item.title, sub_item.href, 2))
        else:
            toc_entries.append((item.title, item.href, 1))
    
    for i, (title, href, level) in enumerate(toc_entries):
        indent = "  " * level
        print(f"  [{i}] {indent}'{title}' -> '{href}' (level {level})")
    
    return toc_entries

def test_chapter_matching(toc_entries, test_chapter_id):
    """Test how the chapter matching logic works"""
    print(f"\n🎯 Testing chapter matching for: '{test_chapter_id}'")
    print("=" * 50)
    
    # Test exact match
    print("\n1️⃣ Testing exact match:")
    for i, (title, toc_href, level) in enumerate(toc_entries):
        if toc_href == test_chapter_id:
            print(f"  ✅ EXACT MATCH found at index {i}: '{title}' -> '{toc_href}'")
            return i
    print(f"  ❌ No exact match found for '{test_chapter_id}'")
    
    # Test partial match (current logic)
    print("\n2️⃣ Testing partial match (current logic):")
    for i, (title, toc_href, level) in enumerate(toc_entries):
        if test_chapter_id in toc_href and '#' in test_chapter_id:
            print(f"  ✅ PARTIAL MATCH found at index {i}: '{title}' -> '{toc_href}'")
            return i
    print(f"  ❌ No partial match found for '{test_chapter_id}'")
    
    # Test reverse partial match
    print("\n3️⃣ Testing reverse partial match:")
    for i, (title, toc_href, level) in enumerate(toc_entries):
        if toc_href in test_chapter_id:
            print(f"  ✅ REVERSE PARTIAL MATCH found at index {i}: '{title}' -> '{toc_href}'")
            return i
    print(f"  ❌ No reverse partial match found for '{test_chapter_id}'")
    
    # Test file part match (without anchor)
    print("\n4️⃣ Testing file part match (without anchor):")
    test_file = test_chapter_id.split('#')[0] if '#' in test_chapter_id else test_chapter_id
    for i, (title, toc_href, level) in enumerate(toc_entries):
        toc_file = toc_href.split('#')[0] if '#' in toc_href else toc_href
        if toc_file == test_file:
            print(f"  ✅ FILE MATCH found at index {i}: '{title}' -> '{toc_href}' (file: {toc_file})")
            return i
    print(f"  ❌ No file match found for '{test_file}'")
    
    return None

def suggest_fixes(toc_entries, test_chapter_id):
    """Suggest possible fixes for the matching logic"""
    print(f"\n💡 Suggestions for fixing chapter matching:")
    print("=" * 50)
    
    test_file = test_chapter_id.split('#')[0] if '#' in test_chapter_id else test_chapter_id
    test_anchor = test_chapter_id.split('#')[1] if '#' in test_chapter_id else None
    
    print(f"Target file: '{test_file}'")
    print(f"Target anchor: '{test_anchor}'")
    
    # Find all entries with the same file
    matching_files = []
    for i, (title, toc_href, level) in enumerate(toc_entries):
        toc_file = toc_href.split('#')[0] if '#' in toc_href else toc_href
        if toc_file == test_file:
            matching_files.append((i, title, toc_href, level))
    
    if matching_files:
        print(f"\n📁 Found {len(matching_files)} entries with matching file '{test_file}':")
        for i, title, href, level in matching_files:
            print(f"  [{i}] '{title}' -> '{href}' (level {level})")
        
        if test_anchor:
            print(f"\n🔗 Looking for anchor '{test_anchor}' in the file content...")
            print("Suggestion: Use the first matching file entry and search for the anchor within the HTML content")
    else:
        print(f"❌ No entries found with file '{test_file}'")
        print("Suggestion: Check if the file path format is different (e.g., with/without 'text/' prefix)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_toc_matching.py <epub_file> [chapter_id]")
        print("Example: python debug_toc_matching.py book.epub 'text/part0013.html#6'")
        sys.exit(1)
    
    epub_path = sys.argv[1]
    test_chapter_id = sys.argv[2] if len(sys.argv) > 2 else "text/part0013.html#6"
    
    if not os.path.exists(epub_path):
        print(f"❌ EPUB file not found: {epub_path}")
        sys.exit(1)
    
    print(f"📖 Analyzing EPUB: {epub_path}")
    print(f"🎯 Test chapter ID: {test_chapter_id}")
    
    try:
        book = read_epub(epub_path)
        toc_entries = debug_toc_structure(book)
        match_index = test_chapter_matching(toc_entries, test_chapter_id)
        
        if match_index is None:
            suggest_fixes(toc_entries, test_chapter_id)
        else:
            print(f"\n✅ Chapter found at index {match_index}")
            
    except Exception as e:
        print(f"❌ Error analyzing EPUB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()