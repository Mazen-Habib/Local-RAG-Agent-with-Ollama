"""
Test Script - Upload and Process PDFs
Tests the complete PDF processing pipeline
"""

import os
import sys
from pathlib import Path

from rag_agent import RAGAgent
from config import validate_config, PDF_UPLOAD_FOLDER


def test_pdf_upload(pdf_path: str):
    """
    Test uploading and processing a PDF
    
    Args:
        pdf_path: Path to PDF file
    """
    print("\n" + "="*60)
    print("🧪 TEST: PDF Upload and Processing")
    print("="*60)
    
    # Validate config
    if not validate_config():
        print("❌ Configuration validation failed")
        return False
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"✅ PDF found: {pdf_path}")
    print(f"   Size: {os.path.getsize(pdf_path) / 1024:.2f} KB")
    
    # Initialize RAG agent
    try:
        agent = RAGAgent()
    except Exception as e:
        print(f"❌ Failed to initialize RAG agent: {str(e)}")
        return False
    
    # Test Supabase connection
    if not agent.check_supabase_connection():
        print("❌ Supabase connection test failed")
        return False
    
    # Process PDF
    try:
        result = agent.process_pdf(pdf_path)
        
        if result["status"] == "success":
            print("\n✅ TEST PASSED!")
            print(f"   Processed: {result['source_file']}")
            print(f"   Pages: {result['num_pages']}")
            print(f"   Chunks created: {result['num_chunks']}")
            print(f"   Chunks stored: {result['num_stored']}")
            return True
        else:
            print("❌ Processing failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_pdfs(pdf_folder: str = PDF_UPLOAD_FOLDER):
    """
    Test processing multiple PDFs from a folder
    
    Args:
        pdf_folder: Folder containing PDFs
    """
    print("\n" + "="*60)
    print(f"🧪 TEST: Processing Multiple PDFs from {pdf_folder}")
    print("="*60)
    
    # Get all PDF files
    pdf_files = list(Path(pdf_folder).glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in {pdf_folder}")
        print(f"   Please place some PDF files in this folder")
        return False
    
    print(f"📄 Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")
    
    # Initialize agent
    agent = RAGAgent()
    
    # Process each PDF
    results = []
    for pdf_path in pdf_files:
        try:
            result = agent.process_pdf(str(pdf_path))
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to process {pdf_path.name}: {str(e)}")
            results.append({"status": "failed", "source_file": pdf_path.name})
    
    # Summary
    print("\n" + "="*60)
    print("📊 PROCESSING SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful
    
    print(f"Total PDFs: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if successful > 0:
        total_chunks = sum(r.get("num_chunks", 0) for r in results if r["status"] == "success")
        print(f"📦 Total chunks stored: {total_chunks}")
    
    print("="*60)
    
    return successful > 0


def create_sample_pdf():
    """Create a sample PDF for testing if none exists"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        sample_path = os.path.join(PDF_UPLOAD_FOLDER, "sample_test.pdf")
        
        # Create PDF
        c = canvas.Canvas(sample_path, pagesize=letter)
        
        # Page 1
        c.drawString(100, 750, "Sample Document for RAG Testing")
        c.drawString(100, 720, "")
        c.drawString(100, 700, "This is a sample document created for testing purposes.")
        c.drawString(100, 680, "")
        c.drawString(100, 660, "Topic: Artificial Intelligence")
        c.drawString(100, 640, "")
        c.drawString(100, 620, "Artificial Intelligence (AI) is the simulation of human intelligence")
        c.drawString(100, 600, "processes by machines, especially computer systems. These processes")
        c.drawString(100, 580, "include learning, reasoning, and self-correction.")
        c.showPage()
        
        # Page 2
        c.drawString(100, 750, "Applications of AI")
        c.drawString(100, 720, "")
        c.drawString(100, 700, "1. Natural Language Processing")
        c.drawString(100, 680, "2. Computer Vision")
        c.drawString(100, 660, "3. Robotics")
        c.drawString(100, 640, "4. Expert Systems")
        c.drawString(100, 620, "")
        c.drawString(100, 600, "AI has become increasingly important in modern technology and")
        c.drawString(100, 580, "is being used in various industries including healthcare,")
        c.drawString(100, 560, "finance, and transportation.")
        c.showPage()
        
        c.save()
        
        print(f"✅ Created sample PDF: {sample_path}")
        return sample_path
        
    except ImportError:
        print("⚠️  reportlab not installed. Cannot create sample PDF.")
        print("   Install with: pip install reportlab")
        return None


def main():
    """Main test function"""
    if len(sys.argv) > 1:
        # Test specific PDF
        pdf_path = sys.argv[1]
        test_pdf_upload(pdf_path)
    else:
        # Test all PDFs in folder
        pdf_folder = PDF_UPLOAD_FOLDER
        
        # Check if folder has PDFs
        pdf_files = list(Path(pdf_folder).glob("*.pdf"))
        
        if not pdf_files:
            print(f"\n⚠️  No PDFs found in {pdf_folder}")
            response = input("Would you like to create a sample PDF for testing? (y/n): ")
            
            if response.lower() == 'y':
                sample_path = create_sample_pdf()
                if sample_path:
                    test_pdf_upload(sample_path)
            else:
                print("\n📝 To test with your own PDF, run:")
                print(f"   python {sys.argv[0]} /path/to/your/file.pdf")
                print("\nOr place PDF files in:", pdf_folder)
        else:
            test_multiple_pdfs(pdf_folder)


if __name__ == "__main__":
    main()
