#!/usr/bin/env python3
"""
Debug script to analyze EPUB TOC structure and chapter paths
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ebook_mcp.tools.epub_helper import read_epub, get_toc
from ebooklib import epub

def analyze_epub_structure(epub_path, target_chapter=None):
    """Analyze the complete structure of an EPUB file"""
    print(f"🔍 Analyzing EPUB structure: {os.path.basename(epub_path)}")
    print("=" * 80)
    
    try:
        # Read the EPUB
        book = read_epub(epub_path)
        
        # Get TOC using our function
        print("\n📚 TOC from get_toc() function:")
        try:
            toc_entries = get_toc(epub_path)
            print(f"Found {len(toc_entries)} TOC entries:")
            for i, (title, href) in enumerate(toc_entries):
                marker = "🎯" if target_chapter and target_chapter.lower() in href.lower() else "  "
                print(f"{marker} [{i+1:2d}] '{title}' -> '{href}'")
        except Exception as e:
            print(f"❌ Error getting TOC: {e}")
        
        # Get all items in the EPUB
        print(f"\n📁 All items in EPUB:")
        items = list(book.get_items())
        print(f"Found {len(items)} total items:")
        
        for i, item in enumerate(items):
            item_type = "📄" if hasattr(item, 'get_type') and 'DOCUMENT' in str(item.get_type()) else "📎"
            marker = "🎯" if target_chapter and target_chapter.lower() in item.get_name().lower() else "  "
            print(f"{marker} [{i+1:2d}] {item_type} '{item.get_name()}' (type: {getattr(item, 'get_type', lambda: 'unknown')()})")
        
        # Get spine (reading order)
        print(f"\n📖 Spine (reading order):")
        spine_items = [item for item in book.spine]
        print(f"Found {len(spine_items)} spine items:")
        
        for i, (item_id, linear) in enumerate(spine_items):
            try:
                item = book.get_item_with_id(item_id)
                if item:
                    marker = "🎯" if target_chapter and target_chapter.lower() in item.get_name().lower() else "  "
                    print(f"{marker} [{i+1:2d}] ID: '{item_id}' -> '{item.get_name()}' (linear: {linear})")
                else:
                    print(f"  [{i+1:2d}] ID: '{item_id}' -> NOT FOUND")
            except Exception as e:
                print(f"  [{i+1:2d}] ID: '{item_id}' -> ERROR: {e}")
        
        # Search for target chapter if specified
        if target_chapter:
            print(f"\n🔍 Searching for '{target_chapter}':")
            
            # Exact matches
            exact_matches = []
            case_insensitive_matches = []
            partial_matches = []
            
            for item in items:
                item_name = item.get_name()
                if item_name == target_chapter:
                    exact_matches.append(item)
                elif item_name.lower() == target_chapter.lower():
                    case_insensitive_matches.append(item)
                elif target_chapter.lower() in item_name.lower():
                    partial_matches.append(item)
            
            if exact_matches:
                print(f"✅ Exact matches ({len(exact_matches)}):")
                for item in exact_matches:
                    print(f"    '{item.get_name()}'")
            
            if case_insensitive_matches:
                print(f"🔤 Case-insensitive matches ({len(case_insensitive_matches)}):")
                for item in case_insensitive_matches:
                    print(f"    '{item.get_name()}'")
            
            if partial_matches:
                print(f"🔍 Partial matches ({len(partial_matches)}):")
                for item in partial_matches:
                    print(f"    '{item.get_name()}'")
            
            if not exact_matches and not case_insensitive_matches and not partial_matches:
                print("❌ No matches found")
                
                # Suggest similar paths
                print(f"\n💡 Suggestions (files with similar patterns):")
                suggestions = []
                target_base = os.path.basename(target_chapter).lower()
                target_parts = target_base.replace('.xhtml', '').replace('.html', '').split('part')
                
                for item in items:
                    item_name = item.get_name().lower()
                    if 'part' in item_name and any(part in item_name for part in target_parts if part):
                        suggestions.append(item.get_name())
                
                if suggestions:
                    for suggestion in suggestions[:10]:  # Show top 10
                        print(f"    '{suggestion}'")
                else:
                    print("    No similar files found")
        
        # Check TOC navigation structure
        print(f"\n🧭 Navigation structure:")
        try:
            nav = book.get_item_with_id('nav') or book.get_item_with_id('ncx')
            if nav:
                print(f"Navigation file: '{nav.get_name()}'")
                content = nav.get_content().decode('utf-8')
                print(f"Content preview (first 500 chars):")
                print(content[:500] + "..." if len(content) > 500 else content)
            else:
                print("No navigation file found")
        except Exception as e:
            print(f"Error reading navigation: {e}")
            
    except Exception as e:
        print(f"❌ Error analyzing EPUB: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_epub_toc.py <epub_path> [target_chapter]")
        print("Example: python debug_epub_toc.py book.epub Text/part0035.xhtml")
        return
    
    epub_path = sys.argv[1]
    target_chapter = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(epub_path):
        print(f"❌ EPUB file not found: {epub_path}")
        return
    
    analyze_epub_structure(epub_path, target_chapter)

if __name__ == "__main__":
    main()