#!/usr/bin/env python3
"""
Debug script to analyze anchor structure in EPUB files
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import read_epub
from bs4 import BeautifulSoup

def analyze_chapter_anchors(epub_path, chapter_file):
    """Analyze the anchor structure in a specific chapter file"""
    print(f"🔍 Analyzing anchors in: {chapter_file}")
    print("=" * 60)
    
    try:
        book = read_epub(epub_path)
        item = book.get_item_with_href(chapter_file)
        
        if item is None:
            print(f"❌ Chapter file not found: {chapter_file}")
            return
        
        content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        
        print(f"📄 File size: {len(content)} characters")
        print(f"📄 HTML structure preview:")
        print(content[:500] + "..." if len(content) > 500 else content)
        print("\n" + "="*60)
        
        # Find all elements with id attributes
        elements_with_id = soup.find_all(attrs={"id": True})
        print(f"\n🎯 Elements with 'id' attributes ({len(elements_with_id)} found):")
        for i, elem in enumerate(elements_with_id):
            print(f"  [{i+1}] <{elem.name}> id='{elem.get('id')}' - {elem.get_text()[:50]}...")
        
        # Find all anchor tags
        anchor_tags = soup.find_all('a')
        print(f"\n🔗 Anchor tags (<a>) found ({len(anchor_tags)} found):")
        for i, anchor in enumerate(anchor_tags):
            href = anchor.get('href', '')
            name = anchor.get('name', '')
            id_attr = anchor.get('id', '')
            text = anchor.get_text()[:30]
            print(f"  [{i+1}] href='{href}' name='{name}' id='{id_attr}' text='{text}...'")
        
        # Find all elements with name attributes
        elements_with_name = soup.find_all(attrs={"name": True})
        print(f"\n📛 Elements with 'name' attributes ({len(elements_with_name)} found):")
        for i, elem in enumerate(elements_with_name):
            print(f"  [{i+1}] <{elem.name}> name='{elem.get('name')}' - {elem.get_text()[:50]}...")
        
        # Find all heading tags
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print(f"\n📝 Heading tags found ({len(headings)} found):")
        for i, heading in enumerate(headings):
            id_attr = heading.get('id', '')
            name_attr = heading.get('name', '')
            text = heading.get_text()[:50]
            print(f"  [{i+1}] <{heading.name}> id='{id_attr}' name='{name_attr}' text='{text}...'")
        
        # Look for potential anchor patterns
        print(f"\n🔍 Searching for potential anchor patterns:")
        
        # Look for elements containing "6" in various attributes
        potential_anchors = []
        for elem in soup.find_all():
            if elem.get('id') == '6' or elem.get('name') == '6':
                potential_anchors.append(('exact', elem))
            elif '6' in str(elem.get('id', '')) or '6' in str(elem.get('name', '')):
                potential_anchors.append(('contains', elem))
        
        if potential_anchors:
            print(f"  Found {len(potential_anchors)} potential matches for anchor '6':")
            for match_type, elem in potential_anchors:
                print(f"    {match_type}: <{elem.name}> id='{elem.get('id')}' name='{elem.get('name')}' text='{elem.get_text()[:30]}...'")
        else:
            print("  ❌ No elements found with id or name containing '6'")
        
        # Check for numbered patterns
        print(f"\n🔢 Looking for numbered elements (1-10):")
        for num in range(1, 11):
            num_str = str(num)
            found_elements = soup.find_all(attrs={"id": num_str}) + soup.find_all(attrs={"name": num_str})
            if found_elements:
                for elem in found_elements:
                    print(f"  Found #{num}: <{elem.name}> id='{elem.get('id')}' name='{elem.get('name')}' text='{elem.get_text()[:30]}...'")
        
    except Exception as e:
        print(f"❌ Error analyzing chapter: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_anchor_structure.py <epub_path> [chapter_file]")
        print("Example: python debug_anchor_structure.py book.epub text/part0013.html")
        return
    
    epub_path = sys.argv[1]
    chapter_file = sys.argv[2] if len(sys.argv) > 2 else "text/part0013.html"
    
    if not os.path.exists(epub_path):
        print(f"❌ EPUB file not found: {epub_path}")
        return
    
    analyze_chapter_anchors(epub_path, chapter_file)

if __name__ == "__main__":
    main()