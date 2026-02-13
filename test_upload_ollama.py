"""
Upload PDFs using Ollama embeddings
"""

import os
import sys
from pathlib import Path

from rag_agent_ollama import RAGAgentOllama
from config import PDF_UPLOAD_FOLDER


def upload_pdf_with_ollama(pdf_path: str):
    """Upload a single PDF with Ollama embeddings"""
    
    print("\n" + "="*60)
    print("📤 Uploading PDF with Ollama Embeddings")
    print("="*60)
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"✅ PDF found: {pdf_path}")
    
    # Initialize RAG agent with Ollama
    print("\n🤖 Initializing RAG agent with Ollama...")
    agent = RAGAgentOllama()
    
    # Process PDF
    result = agent.process_pdf(pdf_path)
    
    if result["status"] == "success":
        print("\n✅ Upload Complete!")
        print(f"   File: {result['source_file']}")
        print(f"   Pages: {result['num_pages']}")
        print(f"   Chunks: {result['num_chunks']}")
        print(f"   Stored: {result['num_stored']}")
        print(f"   Embedding Model: nomic-embed-text (768 dims)")
        return True
    else:
        print("❌ Upload failed")
        return False


def upload_all_pdfs_in_folder(folder: str = PDF_UPLOAD_FOLDER):
    """Upload all PDFs in a folder"""
    
    pdf_files = list(Path(folder).glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in {folder}")
        print(f"   Please add PDF files to the folder")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")
    
    # Initialize agent once
    print(f"\n🤖 Initializing RAG agent with Ollama...")
    agent = RAGAgentOllama()
    
    # Process each PDF
    success_count = 0
    for pdf_path in pdf_files:
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*60}")
        
        try:
            result = agent.process_pdf(str(pdf_path))
            print(f"✅ {pdf_path.name} uploaded successfully!")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to upload {pdf_path.name}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Batch upload complete!")
    print(f"   Successful: {success_count}/{len(pdf_files)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    from ollama_config import validate_ollama_config
    from config import validate_config
    
    # Validate configurations
    print("\n🔍 Validating configuration...")
    if not validate_config():
        print("❌ Configuration validation failed")
        exit(1)
    
    if not validate_ollama_config():
        print("❌ Ollama configuration validation failed")
        print("   Make sure Ollama is running and models are downloaded")
        exit(1)
    
    print("✅ Configuration validated\n")
    
    # Upload PDFs
    if len(sys.argv) > 1:
        # Upload specific PDF
        pdf_path = sys.argv[1]
        upload_pdf_with_ollama(pdf_path)
    else:
        # Upload all PDFs in folder
        upload_all_pdfs_in_folder()
