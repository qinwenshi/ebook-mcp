import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Mock external dependencies
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock PyPDF2
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = Mock()

# Mock PyMuPDF
try:
    import fitz
except ImportError:
    fitz = Mock()

from ebook_mcp.tools.pdf_helper import (
    get_all_pdf_files,
    get_meta,
    get_toc,
    extract_page_text,
    extract_page_markdown,
    get_chapter_content
)


class TestPdfHelper:
    """Test PDF helper functions"""
    
    def test_get_all_pdf_files_empty_directory(self):
        """Test get_all_pdf_files with empty directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = get_all_pdf_files(temp_dir)
            assert result == []
    
    def test_get_all_pdf_files_with_pdf_files(self):
        """Test get_all_pdf_files with PDF files present"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock PDF files
            pdf_files = ["document1.pdf", "document2.pdf", "text.txt"]
            for file in pdf_files:
                with open(os.path.join(temp_dir, file), 'w') as f:
                    f.write("mock content")
            
            result = get_all_pdf_files(temp_dir)
            assert set(result) == {"document1.pdf", "document2.pdf"}
    
    @patch('ebook_mcp.tools.pdf_helper.PdfReader')
    def test_get_meta_success(self, mock_pdf_reader):
        """Test get_meta successful case"""
        # Mock PDF reader with metadata
        mock_reader = Mock()
        mock_reader.metadata = {
            '/Title': 'Test PDF',
            '/Author': 'Test Author',
            '/Subject': 'Test Subject',
            '/Creator': 'Test Creator',
            '/Producer': 'Test Producer',
            '/CreationDate': '2023-01-01',
            '/ModDate': '2023-01-02'
        }
        mock_reader.pages = [Mock(), Mock(), Mock()]  # 3 pages
        mock_pdf_reader.return_value = mock_reader
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_meta(pdf_path)
            expected = {
                'title': 'Test PDF',
                'author': 'Test Author',
                'subject': 'Test Subject',
                'creator': 'Test Creator',
                'producer': 'Test Producer',
                'creation_date': '2023-01-01',
                'modification_date': '2023-01-02',
                'pages': 3
            }
            assert result == expected
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.PdfReader')
    def test_get_meta_no_metadata(self, mock_pdf_reader):
        """Test get_meta with no metadata"""
        # Mock PDF reader without metadata
        mock_reader = Mock()
        mock_reader.metadata = None
        mock_reader.pages = [Mock(), Mock()]  # 2 pages
        mock_pdf_reader.return_value = mock_reader
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_meta(pdf_path)
            expected = {'pages': 2}
            assert result == expected
        finally:
            os.unlink(pdf_path)
    
    def test_get_meta_file_not_found(self):
        """Test get_meta with non-existent file"""
        with pytest.raises(FileNotFoundError):
            get_meta("/path/to/nonexistent.pdf")
    
    @patch('ebook_mcp.tools.pdf_helper.PdfReader')
    def test_get_meta_parsing_error(self, mock_pdf_reader):
        """Test get_meta with parsing error"""
        mock_pdf_reader.side_effect = Exception("PDF parsing error")
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            with pytest.raises(Exception):
                get_meta(pdf_path)
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_toc_success(self, mock_fitz_open):
        """Test get_toc successful case"""
        # Mock PyMuPDF document with TOC
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1", 1),
            (1, "Chapter 2", 5),
            (2, "Subchapter 2.1", 7)
        ]
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_toc(pdf_path)
            expected = [
                ("Chapter 1", 1),
                ("Chapter 2", 5),
                ("Subchapter 2.1", 7)
            ]
            assert result == expected
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_toc_empty(self, mock_fitz_open):
        """Test get_toc with empty TOC"""
        # Mock PyMuPDF document with empty TOC
        mock_doc = Mock()
        mock_doc.get_toc.return_value = []
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_toc(pdf_path)
            assert result == []
        finally:
            os.unlink(pdf_path)
    
    def test_get_toc_file_not_found(self):
        """Test get_toc with non-existent file"""
        with pytest.raises(FileNotFoundError):
            get_toc("/path/to/nonexistent.pdf")
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_toc_parsing_error(self, mock_fitz_open):
        """Test get_toc with parsing error"""
        mock_fitz_open.side_effect = Exception("PDF parsing error")
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            with pytest.raises(Exception):
                get_toc(pdf_path)
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_extract_page_text_success(self, mock_fitz_open):
        """Test extract_page_text successful case"""
        # Mock PyMuPDF document and page
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_text.return_value = "This is page 1 content."
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = extract_page_text(pdf_path, 1)
            assert result == "This is page 1 content."
            mock_doc.__getitem__.assert_called_once_with(0)  # 0-based index
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_extract_page_text_page_not_found(self, mock_fitz_open):
        """Test extract_page_text with page not found"""
        # Mock PyMuPDF document with IndexError
        mock_doc = Mock()
        mock_doc.__getitem__.side_effect = IndexError("Page not found")
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            with pytest.raises(Exception):
                extract_page_text(pdf_path, 999)
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_extract_page_markdown_success(self, mock_fitz_open):
        """Test extract_page_markdown successful case"""
        # Mock PyMuPDF document and page
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_text.return_value = "This is page 1 content."
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = extract_page_markdown(pdf_path, 1)
            # Should contain page number and content
            assert "Page 1" in result
            assert "This is page 1 content." in result
            mock_doc.__getitem__.assert_called_once_with(0)  # 0-based index
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_extract_page_markdown_with_formatting(self, mock_fitz_open):
        """Test extract_page_markdown with formatted content"""
        # Mock PyMuPDF document and page with formatted text
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_text.return_value = "Title\n\nThis is content with\nmultiple lines."
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = extract_page_markdown(pdf_path, 1)
            # Should format as markdown
            assert "# Page 1" in result
            assert "Title" in result
            assert "This is content with" in result
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_chapter_content_success(self, mock_fitz_open):
        """Test get_chapter_content successful case"""
        # Mock PyMuPDF document with TOC and pages
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1", 1),
            (1, "Chapter 2", 3),
            (1, "Chapter 3", 5)
        ]
        
        # Mock pages
        mock_page1 = Mock()
        mock_page1.get_text.return_value = "Chapter 1 content"
        mock_page2 = Mock()
        mock_page2.get_text.return_value = "Chapter 1 continued"
        mock_page3 = Mock()
        mock_page3.get_text.return_value = "Chapter 2 content"
        
        mock_doc.__getitem__.side_effect = [mock_page1, mock_page2, mock_page3]
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_chapter_content(pdf_path, "Chapter 1")
            content, page_numbers = result
            
            # Should contain chapter content
            assert "Chapter 1 content" in content
            assert "Chapter 1 continued" in content
            # Should return correct page numbers (1-based)
            assert page_numbers == [1, 2]
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_chapter_content_chapter_not_found(self, mock_fitz_open):
        """Test get_chapter_content with chapter not found"""
        # Mock PyMuPDF document with TOC
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1", 1),
            (1, "Chapter 2", 3)
        ]
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            with pytest.raises(Exception):
                get_chapter_content(pdf_path, "Nonexistent Chapter")
        finally:
            os.unlink(pdf_path)
    
    @patch('ebook_mcp.tools.pdf_helper.fitz.open')
    def test_get_chapter_content_single_page(self, mock_fitz_open):
        """Test get_chapter_content with single page chapter"""
        # Mock PyMuPDF document with TOC
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1", 1),
            (1, "Chapter 2", 2)
        ]
        
        # Mock single page
        mock_page = Mock()
        mock_page.get_text.return_value = "Single page chapter content"
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b"mock pdf content")
            pdf_path = f.name
        
        try:
            result = get_chapter_content(pdf_path, "Chapter 1")
            content, page_numbers = result
            
            assert "Single page chapter content" in content
            assert page_numbers == [1]
        finally:
            os.unlink(pdf_path) 