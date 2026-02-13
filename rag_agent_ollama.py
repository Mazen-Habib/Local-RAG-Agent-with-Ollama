"""
RAG Agent with Ollama - Local LLM Implementation
Updated version using Ollama instead of Gemini
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from supabase import create_client, Client
import numpy as np

from config import (
    SUPABASE_URL,
    SUPABASE_API_KEY,
    SUPABASE_TABLE_NAME,
    SUPABASE_QUERY_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_DOCUMENTS,
    SYSTEM_PROMPT,
)

from ollama_config import (
    OLLAMA_BASE_URL,
    OLLAMA_LLM_MODEL,
    OLLAMA_EMBEDDING_MODEL,
    OLLAMA_TEMPERATURE,
    OLLAMA_MAX_TOKENS,
    OLLAMA_SYSTEM_PROMPT,
)


class RAGAgentOllama:
    """
    RAG Agent using Ollama for local LLM inference
    """
    
    def __init__(self):
        """Initialize the RAG agent with Ollama"""
        print("🚀 Initializing RAG Agent with Ollama...")
        
        # Initialize Ollama embeddings
        self.embeddings = OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
        print(f"✅ Ollama embeddings initialized ({OLLAMA_EMBEDDING_MODEL})")
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=OLLAMA_LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=OLLAMA_TEMPERATURE,
        )
        print(f"✅ Ollama LLM initialized ({OLLAMA_LLM_MODEL})")
        
        # Initialize Supabase client
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        print(f"✅ Supabase client initialized")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        print(f"✅ Text splitter initialized (chunk_size={CHUNK_SIZE})")
        
        print("✅ RAG Agent ready!\n")
    
    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        Load and parse a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Document objects
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"📄 Loading PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages from PDF")
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of chunked documents
        """
        print(f"✂️  Splitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Ollama
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        print(f"🧮 Generating embeddings for {len(texts)} texts...")
        embeddings = self.embeddings.embed_documents(texts)
        print(f"✅ Generated {len(embeddings)} embeddings")
        
        return embeddings
    
    def store_in_supabase(
        self,
        chunks: List[Document],
        source_file: str,
        batch_size: int = 10
    ) -> int:
        """
        Store document chunks with embeddings in Supabase
        
        Args:
            chunks: List of document chunks
            source_file: Original file name
            batch_size: Number of chunks to process at once
            
        Returns:
            Number of chunks stored
        """
        print(f"💾 Storing {len(chunks)} chunks in Supabase...")
        
        total_stored = 0
        
        # Process in batches to avoid overwhelming the API
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            # Extract texts from chunks
            texts = [chunk.page_content for chunk in batch]
            
            # Generate embeddings for this batch
            embeddings = self.generate_embeddings(texts)
            
            # Prepare data for insertion
            records = []
            for chunk, embedding in zip(batch, embeddings):
                metadata = {
                    "source": source_file,
                    "page": chunk.metadata.get("page", 0),
                    **chunk.metadata
                }
                
                record = {
                    "content": chunk.page_content,
                    "metadata": metadata,
                    "embedding": embedding
                }
                records.append(record)
            
            # Insert batch into Supabase
            try:
                result = self.supabase.table(SUPABASE_TABLE_NAME).insert(records).execute()
                total_stored += len(records)
                print(f"  ✅ Stored batch {i//batch_size + 1} ({len(records)} chunks)")
            except Exception as e:
                print(f"  ❌ Error storing batch {i//batch_size + 1}: {str(e)}")
                raise
        
        print(f"✅ Successfully stored {total_stored} chunks in Supabase")
        return total_stored
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: Load PDF, chunk, embed, and store
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with processing results
        """
        print("\n" + "="*60)
        print(f"🔄 Processing PDF: {pdf_path}")
        print("="*60)
        
        # Get source file name
        source_file = os.path.basename(pdf_path)
        
        # Step 1: Load PDF
        documents = self.load_pdf(pdf_path)
        
        # Step 2: Split into chunks
        chunks = self.split_documents(documents)
        
        # Step 3: Store in Supabase (includes embedding generation)
        num_stored = self.store_in_supabase(chunks, source_file)
        
        result = {
            "source_file": source_file,
            "num_pages": len(documents),
            "num_chunks": len(chunks),
            "num_stored": num_stored,
            "status": "success"
        }
        
        print("="*60)
        print("✅ PDF Processing Complete!")
        print(f"   Pages: {result['num_pages']}")
        print(f"   Chunks: {result['num_chunks']}")
        print(f"   Stored: {result['num_stored']}")
        print("="*60 + "\n")
        
        return result
    
    def similarity_search(
        self,
        query: str,
        top_k: int = TOP_K_DOCUMENTS
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents in Supabase using vector similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of similar documents with metadata
        """
        print(f"🔍 Searching for: '{query}'")
        
        # Generate embedding for query using Ollama
        query_embedding = self.embeddings.embed_query(query)
        
        # Call Supabase RPC function for similarity search
        try:
            result = self.supabase.rpc(
                SUPABASE_QUERY_NAME,
                {
                    "query_embedding": query_embedding,
                    "match_count": top_k
                }
            ).execute()
            
            documents = result.data
            print(f"✅ Found {len(documents)} relevant documents")
            
            return documents
            
        except Exception as e:
            print(f"❌ Error during similarity search: {str(e)}")
            raise
    
    def answer_question(
        self,
        question: str,
        top_k: int = TOP_K_DOCUMENTS
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG with Ollama
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and source documents
        """
        print("\n" + "="*60)
        print(f"❓ Question: {question}")
        print("="*60)
        
        # Step 1: Retrieve relevant documents
        documents = self.similarity_search(question, top_k)
        
        if not documents:
            return {
                "question": question,
                "answer": "I couldn't find any relevant information in the documents.",
                "sources": []
            }
        
        # Step 2: Prepare context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(documents)
        ])
        
        # Step 3: Create prompt with context
        prompt = f"""{OLLAMA_SYSTEM_PROMPT}

Context from documents:
{context}

Question: {question}

Answer:"""
        
        # Step 4: Generate answer using Ollama
        print("🤖 Generating answer with Ollama...")
        answer = self.llm.invoke(prompt)
        
        result = {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "similarity": doc.get("similarity", 0)
                }
                for doc in documents
            ],
            "num_sources": len(documents)
        }
        
        print("="*60)
        print(f"✅ Answer Generated")
        print("="*60)
        print(f"\n{answer}\n")
        print(f"📚 Used {len(documents)} source document(s)")
        print("="*60 + "\n")
        
        return result
    
    def check_supabase_connection(self) -> bool:
        """
        Test Supabase connection
        
        Returns:
            True if connection is successful
        """
        try:
            # Try to query the table
            result = self.supabase.table(SUPABASE_TABLE_NAME).select("id").limit(1).execute()
            print("✅ Supabase connection successful")
            return True
        except Exception as e:
            print(f"❌ Supabase connection failed: {str(e)}")
            return False
    
    def get_document_count(self) -> int:
        """
        Get total number of documents in Supabase
        
        Returns:
            Count of documents
        """
        try:
            result = self.supabase.table(SUPABASE_TABLE_NAME).select("id", count="exact").execute()
            count = result.count
            print(f"📊 Total documents in database: {count}")
            return count
        except Exception as e:
            print(f"❌ Error getting document count: {str(e)}")
            return 0


def main():
    """Main function for testing"""
    from config import validate_config
    from ollama_config import validate_ollama_config
    
    # Validate configuration
    if not validate_config():
        return
    
    if not validate_ollama_config():
        print("\n⚠️  Ollama is not properly configured")
        print("   Please install required models and start Ollama")
        return
    
    # Initialize RAG agent with Ollama
    agent = RAGAgentOllama()
    
    # Test connection
    agent.check_supabase_connection()
    
    # Get document count
    agent.get_document_count()


if __name__ == "__main__":
    main()
