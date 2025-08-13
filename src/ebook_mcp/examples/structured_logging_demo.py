#!/usr/bin/env python3
"""
Structured Logging Demo

This script demonstrates the enhanced structured logging capabilities
of the ebook-mcp system.
"""

import os
import sys
import tempfile

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ebook_mcp.tools.logger_config import setup_logger, get_logger, log_operation
from ebook_mcp.tools.epub_helper import get_toc, get_meta
from ebook_mcp.tools.pdf_helper import get_toc as get_pdf_toc, get_meta as get_pdf_meta

def demo_basic_logging():
    """Demonstrate basic structured logging"""
    print("=== Basic Structured Logging Demo ===")
    
    # Setup logger
    setup_logger(level="DEBUG", log_file="demo.log")
    logger = get_logger("demo")
    
    # Log with context
    logger.info("Starting demo application", 
                operation="demo_start", 
                version="1.0.0")
    
    logger.debug("Processing user request", 
                 user_id="12345", 
                 request_type="epub_metadata")
    
    logger.warning("Deprecated feature used", 
                   feature="old_parser", 
                   recommendation="use_new_parser")
    
    logger.error("Failed to connect to database", 
                 database="epub_store", 
                 error_code="CONN_001")

def demo_operation_logging():
    """Demonstrate operation logging with timing"""
    print("\n=== Operation Logging Demo ===")
    
    @log_operation("demo_epub_processing")
    def process_epub_file(file_path):
        """Simulate EPUB processing"""
        import time
        time.sleep(0.1)  # Simulate processing time
        return {"pages": 150, "chapters": 12}
    
    # This will automatically log start, success, and timing
    result = process_epub_file("/path/to/sample.epub")
    print(f"Processing result: {result}")

def demo_error_logging():
    """Demonstrate error logging with context"""
    print("\n=== Error Logging Demo ===")
    
    @log_operation("demo_error_handling")
    def process_with_error():
        """Simulate an operation that fails"""
        raise ValueError("Simulated processing error")
    
    try:
        process_with_error()
    except ValueError as e:
        print(f"Caught expected error: {e}")

def demo_epub_logging():
    """Demonstrate EPUB-specific logging"""
    print("\n=== EPUB Logging Demo ===")
    
    # Create a temporary EPUB-like file for demo
    with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as f:
        temp_epub = f.name
    
    try:
        # This will trigger the structured logging in epub_helper
        logger = get_logger("epub_demo")
        logger.info("Attempting EPUB operations", file_path=temp_epub)
        
        # Note: This will fail since it's not a real EPUB, but will show error logging
        try:
            get_toc(temp_epub)
        except Exception as e:
            logger.error("EPUB operation failed", 
                        file_path=temp_epub, 
                        operation="toc_extraction",
                        error_type=type(e).__name__,
                        error_details=str(e))
    
    finally:
        # Clean up
        if os.path.exists(temp_epub):
            os.unlink(temp_epub)

def show_log_file():
    """Show the generated log file"""
    print("\n=== Generated Log File Content ===")
    log_file = os.path.join("src", "ebook_mcp", "logs", "demo.log")
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                print(line.strip())
    else:
        print("Log file not found. Check the logs directory.")

def main():
    """Run the structured logging demo"""
    print("Structured Logging Demo for ebook-mcp")
    print("=" * 50)
    
    # Run demos
    demo_basic_logging()
    demo_operation_logging()
    demo_error_logging()
    demo_epub_logging()
    
    # Show the log file
    show_log_file()
    
    print("\n" + "=" * 50)
    print("Demo completed! Check the log file for structured JSON logs.")

if __name__ == "__main__":
    main()
