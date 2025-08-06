import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from ebook_mcp.tools.pdf_helper import get_meta, get_meta_pypdf2
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

class TestPDFMetadataComparison:
    """Test comparison between PyMuPDF and PyPDF2 metadata extraction"""
    
    @pytest.mark.skipif(not DEPENDENCIES_AVAILABLE, reason="Dependencies not available")
    def test_pymupdf_metadata_extraction(self):
        """Test PyMuPDF metadata extraction functionality"""
        with patch('ebook_mcp.tools.pdf_helper.fitz.open') as mock_fitz_open, \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024000):
            
            # Mock PyMuPDF document
            mock_doc = Mock()
            mock_doc.metadata = {
                'title': 'Test PDF Title',
                'author': 'Test Author',
                'subject': 'Test Subject',
                'creator': 'Test Creator',
                'producer': 'Test Producer',
                'creationDate': '2024-01-01T00:00:00Z',
                'modDate': '2024-01-02T00:00:00Z',
                'keywords': 'test, pdf, metadata',
                'format': 'PDF'
            }
            mock_doc.page_count = 10
            # Mock version attributes - some versions may not have these
            mock_doc.version_major = 1
            mock_doc.version_minor = 7
            mock_doc.is_encrypted = False
            
            # Mock first page for dimensions
            mock_page = Mock()
            mock_rect = Mock()
            mock_rect.width = 595.0
            mock_rect.height = 842.0
            mock_page.rect = mock_rect
            
            # Properly mock the __getitem__ method
            mock_doc.__getitem__ = Mock(return_value=mock_page)
            
            mock_fitz_open.return_value = mock_doc
            
            result = get_meta('/path/to/test.pdf')
            
            # Verify PyMuPDF specific fields
            assert result['title'] == 'Test PDF Title'
            assert result['author'] == 'Test Author'
            assert result['pages'] == 10
            assert result['pdf_version'] == '1.7'
            assert result['is_encrypted'] == False
            assert result['file_size'] == 1024000
            assert result['page_width'] == 595.0
            assert result['page_height'] == 842.0
            assert 'keywords' in result
            assert 'format' in result
    
    @pytest.mark.skipif(not DEPENDENCIES_AVAILABLE, reason="Dependencies not available")
    def test_pypdf2_metadata_extraction(self):
        """Test PyPDF2 metadata extraction functionality"""
        with patch('ebook_mcp.tools.pdf_helper.PdfReader') as mock_pdf_reader, \
             patch('os.path.exists', return_value=True):
            
            # Mock PyPDF2 reader
            mock_reader = Mock()
            mock_reader.metadata = {
                '/Title': 'Test PDF Title',
                '/Author': 'Test Author',
                '/Subject': 'Test Subject',
                '/Creator': 'Test Creator',
                '/Producer': 'Test Producer',
                '/CreationDate': '2024-01-01T00:00:00Z',
                '/ModDate': '2024-01-02T00:00:00Z'
            }
            mock_reader.pages = [Mock() for _ in range(10)]
            mock_pdf_reader.return_value = mock_reader
            
            result = get_meta_pypdf2('/path/to/test.pdf')
            
            # Verify PyPDF2 specific fields
            assert result['title'] == 'Test PDF Title'
            assert result['author'] == 'Test Author'
            assert result['pages'] == 10
            # PyPDF2 doesn't provide these fields
            assert 'pdf_version' not in result
            assert 'is_encrypted' not in result
            assert 'file_size' not in result
            assert 'page_width' not in result
            assert 'page_height' not in result
    
    @pytest.mark.skipif(not DEPENDENCIES_AVAILABLE, reason="Dependencies not available")
    def test_pymupdf_vs_pypdf2_comparison(self):
        """Compare metadata extraction capabilities between PyMuPDF and PyPDF2"""
        with patch('ebook_mcp.tools.pdf_helper.fitz.open') as mock_fitz_open, \
             patch('ebook_mcp.tools.pdf_helper.PdfReader') as mock_pdf_reader, \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024000):
            
            # Mock PyMuPDF document
            mock_doc = Mock()
            mock_doc.metadata = {
                'title': 'Test PDF Title',
                'author': 'Test Author',
                'subject': 'Test Subject',
                'creator': 'Test Creator',
                'producer': 'Test Producer',
                'creationDate': '2024-01-01T00:00:00Z',
                'modDate': '2024-01-02T00:00:00Z',
                'keywords': 'test, pdf, metadata',
                'format': 'PDF'
            }
            mock_doc.page_count = 10
            mock_doc.version_major = 1
            mock_doc.version_minor = 7
            mock_doc.is_encrypted = False
            
            mock_page = Mock()
            mock_rect = Mock()
            mock_rect.width = 595.0
            mock_rect.height = 842.0
            mock_page.rect = mock_rect
            mock_doc.__getitem__ = Mock(return_value=mock_page)
            mock_fitz_open.return_value = mock_doc
            
            # Mock PyPDF2 reader
            mock_reader = Mock()
            mock_reader.metadata = {
                '/Title': 'Test PDF Title',
                '/Author': 'Test Author',
                '/Subject': 'Test Subject',
                '/Creator': 'Test Creator',
                '/Producer': 'Test Producer',
                '/CreationDate': '2024-01-01T00:00:00Z',
                '/ModDate': '2024-01-02T00:00:00Z'
            }
            mock_reader.pages = [Mock() for _ in range(10)]
            mock_pdf_reader.return_value = mock_reader
            
            # Get results from both methods
            pymupdf_result = get_meta('/path/to/test.pdf')
            pypdf2_result = get_meta_pypdf2('/path/to/test.pdf')
            
            # Compare common fields
            assert pymupdf_result['title'] == pypdf2_result['title']
            assert pymupdf_result['author'] == pypdf2_result['author']
            assert pymupdf_result['pages'] == pypdf2_result['pages']
            
            # PyMuPDF provides more information
            assert len(pymupdf_result) > len(pypdf2_result)
            assert 'pdf_version' in pymupdf_result
            assert 'is_encrypted' in pymupdf_result
            assert 'file_size' in pymupdf_result
            assert 'page_width' in pymupdf_result
            assert 'page_height' in pymupdf_result
            assert 'keywords' in pymupdf_result
            assert 'format' in pymupdf_result
    
    @pytest.mark.skipif(not DEPENDENCIES_AVAILABLE, reason="Dependencies not available")
    def test_pymupdf_encrypted_pdf_handling(self):
        """Test PyMuPDF handling of encrypted PDFs"""
        with patch('ebook_mcp.tools.pdf_helper.fitz.open') as mock_fitz_open, \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=512000):
            
            mock_doc = Mock()
            mock_doc.metadata = {'title': 'Encrypted PDF'}
            mock_doc.page_count = 5
            mock_doc.version_major = 1
            mock_doc.version_minor = 6
            mock_doc.is_encrypted = True
            
            # Mock first page for dimensions
            mock_page = Mock()
            mock_rect = Mock()
            mock_rect.width = 595.0
            mock_rect.height = 842.0
            mock_page.rect = mock_rect
            mock_doc.__getitem__ = Mock(return_value=mock_page)
            
            mock_fitz_open.return_value = mock_doc
            
            result = get_meta('/path/to/encrypted.pdf')
            
            assert result['is_encrypted'] == True
            assert result['title'] == 'Encrypted PDF'
    
    @pytest.mark.skipif(not DEPENDENCIES_AVAILABLE, reason="Dependencies not available")
    def test_pymupdf_empty_metadata_handling(self):
        """Test PyMuPDF handling of PDFs with minimal metadata"""
        with patch('ebook_mcp.tools.pdf_helper.fitz.open') as mock_fitz_open, \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=512000):
            
            mock_doc = Mock()
            mock_doc.metadata = {}  # Empty metadata
            mock_doc.page_count = 3
            mock_doc.version_major = 1
            mock_doc.version_minor = 4
            mock_doc.is_encrypted = False
            
            mock_page = Mock()
            mock_rect = Mock()
            mock_rect.width = 612.0
            mock_rect.height = 792.0
            mock_page.rect = mock_rect
            mock_doc.__getitem__ = Mock(return_value=mock_page)
            mock_fitz_open.return_value = mock_doc
            
            result = get_meta('/path/to/minimal.pdf')
            
            # Should still provide basic information
            assert result['pages'] == 3
            assert result['pdf_version'] == '1.4'
            assert result['is_encrypted'] == False
            assert result['file_size'] == 512000
            assert result['page_width'] == 612.0
            assert result['page_height'] == 792.0
            
            # Metadata fields should not be present
            assert 'title' not in result
            assert 'author' not in result 