#!/usr/bin/env python3
"""
Test script to verify the chapter ID matching fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_matching_logic():
    """Test the new matching logic with various scenarios"""
    print("🧪 Testing Chapter ID Matching Logic")
    print("=" * 50)
    
    # Mock TOC entries that might exist in an EPUB
    toc_entries = [
        ("Chapter 1", "text/part0001.html", 1),
        ("Section 1.1", "text/part0001.html#section1", 2),
        ("Chapter 2", "text/part0002.html", 1),
        ("Chapter 13", "text/part0013.html", 1),
        ("Section 13.1", "text/part0013.html#1", 2),
        ("Section 13.2", "text/part0013.html#2", 2),
        ("Section 13.6", "text/part0013.html#6", 2),
        ("Chapter 14", "text/part0014.html", 1),
    ]
    
    test_cases = [
        "text/part0013.html#6",  # The problematic case
        "text/part0013.html",    # File without anchor
        "text/part0001.html#section1",  # Different anchor format
        "part0013.html#6",       # Without text/ prefix
        "text/part0999.html",    # Non-existent file
    ]
    
    for test_case in test_cases:
        print(f"\n🎯 Testing: '{test_case}'")
        
        current_idx = None
        current_level = None
        fallback_idx = None
        fallback_level = None
        
        # Apply the new matching logic with priority
        for i, (title, toc_href, level) in enumerate(toc_entries):
            # Strategy 1: Exact match (highest priority)
            if toc_href == test_case:
                current_idx = i
                current_level = level
                print(f"  ✅ EXACT MATCH: [{i}] '{title}' -> '{toc_href}'")
                break
            
            # Strategy 2: TOC href is contained in the requested anchor_href (high priority)
            if toc_href in test_case:
                current_idx = i
                current_level = level
                print(f"  ✅ CONTAINS MATCH: [{i}] '{title}' -> '{toc_href}'")
                # Don't break - continue looking for exact matches
            
            # Strategy 3: File part matches (lower priority - use as fallback)
            if current_idx is None:  # Only consider if no better match found
                if '#' in test_case and '#' in toc_href:
                    anchor_file = test_case.split('#')[0]
                    toc_file = toc_href.split('#')[0]
                    if anchor_file == toc_file and fallback_idx is None:
                        fallback_idx = i
                        fallback_level = level
                        print(f"  🔄 FALLBACK: FILE MATCH (both have anchors): [{i}] '{title}' -> '{toc_href}'")
                elif '#' in test_case:
                    anchor_file = test_case.split('#')[0]
                    if anchor_file == toc_href and fallback_idx is None:
                        fallback_idx = i
                        fallback_level = level
                        print(f"  🔄 FALLBACK: FILE MATCH (test has anchor): [{i}] '{title}' -> '{toc_href}'")
                elif '#' in toc_href:
                    toc_file = toc_href.split('#')[0]
                    if toc_file == test_case and fallback_idx is None:
                        fallback_idx = i
                        fallback_level = level
                        print(f"  🔄 FALLBACK: FILE MATCH (toc has anchor): [{i}] '{title}' -> '{toc_href}'")
        
        # Use fallback if no better match was found
        if current_idx is None and fallback_idx is not None:
            current_idx = fallback_idx
            current_level = fallback_level
            print(f"  📋 Using fallback match")
        
        if current_idx is None:
            print(f"  ❌ NO MATCH FOUND")
        else:
            print(f"  📍 Result: Index {current_idx}, Level {current_level}")

def test_with_real_epub():
    """Test with a real EPUB file if provided"""
    if len(sys.argv) > 1:
        epub_path = sys.argv[1]
        test_chapter_id = sys.argv[2] if len(sys.argv) > 2 else "text/part0013.html#6"
        
        print(f"\n📖 Testing with real EPUB: {epub_path}")
        print(f"🎯 Chapter ID: {test_chapter_id}")
        
        try:
            from ebook_mcp.tools.epub_helper import read_epub, extract_chapter_markdown
            
            book = read_epub(epub_path)
            result = extract_chapter_markdown(book, test_chapter_id)
            
            print(f"✅ SUCCESS! Chapter content extracted ({len(result)} characters)")
            print(f"📝 Preview: {result[:200]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

def main():
    test_matching_logic()
    test_with_real_epub()

if __name__ == "__main__":
    main()