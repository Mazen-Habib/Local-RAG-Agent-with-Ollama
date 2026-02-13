"""
Test Script - Question Answering
Tests the RAG question answering capability
"""

import sys
from rag_agent import RAGAgent
from config import validate_config


def test_single_question(question: str):
    """
    Test answering a single question
    
    Args:
        question: Question to ask
    """
    print("\n" + "="*60)
    print("🧪 TEST: Question Answering")
    print("="*60)
    
    # Validate config
    if not validate_config():
        return False
    
    # Initialize agent
    try:
        agent = RAGAgent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        return False
    
    # Check if there are documents in the database
    doc_count = agent.get_document_count()
    if doc_count == 0:
        print("\n⚠️  No documents found in database!")
        print("   Please upload some PDFs first using: python test_upload.py")
        return False
    
    # Answer question
    try:
        result = agent.answer_question(question)
        
        print("\n✅ TEST PASSED!")
        print(f"\n📝 Sources used: {result['num_sources']}")
        
        # Display source snippets
        print("\n📚 Source Documents:")
        for i, source in enumerate(result['sources'][:3], 1):  # Show top 3
            print(f"\n   Source {i} (similarity: {source['similarity']:.3f}):")
            print(f"   {source['content'][:200]}...")
            if 'source' in source['metadata']:
                print(f"   From: {source['metadata']['source']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during question answering: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def interactive_qa():
    """
    Interactive Q&A session
    """
    print("\n" + "="*60)
    print("🤖 Interactive RAG Q&A Session")
    print("="*60)
    print("Type 'exit' or 'quit' to end the session")
    print("="*60)
    
    # Validate config
    if not validate_config():
        return
    
    # Initialize agent
    print("\nInitializing RAG agent...")
    try:
        agent = RAGAgent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        return
    
    # Check document count
    doc_count = agent.get_document_count()
    if doc_count == 0:
        print("\n⚠️  No documents found in database!")
        print("   Please upload some PDFs first using: python test_upload.py")
        return
    
    print(f"\n✅ Ready! Database has {doc_count} document chunks")
    print("\n" + "="*60 + "\n")
    
    # Q&A loop
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Answer question
            result = agent.answer_question(question)
            
            print(f"\n💡 Answer:\n{result['answer']}\n")
            print(f"📚 (Based on {result['num_sources']} source document(s))\n")
            print("-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def test_sample_questions():
    """
    Test with a set of sample questions
    """
    print("\n" + "="*60)
    print("🧪 TEST: Sample Questions")
    print("="*60)
    
    sample_questions = [
        "What is this document about?",
        "What are the main topics discussed?",
        "Can you summarize the key points?",
    ]
    
    # Initialize agent
    agent = RAGAgent()
    
    # Check document count
    doc_count = agent.get_document_count()
    if doc_count == 0:
        print("\n⚠️  No documents found in database!")
        print("   Please upload some PDFs first")
        return False
    
    print(f"\nTesting with {len(sample_questions)} sample questions...\n")
    
    # Test each question
    for i, question in enumerate(sample_questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}/{len(sample_questions)}")
        print(f"{'='*60}")
        
        try:
            result = agent.answer_question(question)
            print(f"✅ Question answered successfully")
            print(f"   Sources used: {result['num_sources']}")
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ Sample Questions Test Complete")
    print("="*60)


def main():
    """Main test function"""
    if len(sys.argv) > 1:
        # Test specific question
        question = " ".join(sys.argv[1:])
        test_single_question(question)
    else:
        # Interactive mode
        print("\nChoose mode:")
        print("1. Interactive Q&A")
        print("2. Test with sample questions")
        print("3. Quick test with custom question")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            interactive_qa()
        elif choice == "2":
            test_sample_questions()
        elif choice == "3":
            question = input("Enter your question: ").strip()
            if question:
                test_single_question(question)
        else:
            print("Invalid choice. Starting interactive mode...")
            interactive_qa()


if __name__ == "__main__":
    main()
