import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()

def create_sample_document():
    """Create a sample document for demonstration"""
    sample_text = """
    LangChain is a framework for developing applications powered by language models.
    
    Key Features:
    1. Modular Components: LangChain provides modular components for working with language models.
    2. Memory: Built-in memory systems for maintaining conversation context.
    3. Chains: Combine multiple components to create complex workflows.
    4. Agents: Create autonomous agents that can use tools and make decisions.
    5. Document Loaders: Load documents from various sources (PDF, CSV, etc.).
    6. Vector Stores: Store and retrieve embeddings for semantic search.
    
    Common Use Cases:
    - Chatbots with memory
    - Document question answering
    - Code generation and analysis
    - Content creation and summarization
    - Data analysis and reporting
    
    Installation: pip install langchain openai python-dotenv
    """
    
    with open("sample_document.txt", "w") as f:
        f.write(sample_text)
    
    return "sample_document.txt"

def setup_document_qa():
    """Set up a document Q&A system"""
    
    # Create sample document
    doc_path = create_sample_document()
    
    # Load the document
    loader = TextLoader(doc_path)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Create QA chain
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa_chain

def ask_questions():
    """Interactive Q&A session"""
    print("📚 Document Q&A System")
    print("Ask questions about LangChain. Type 'quit' to exit\n")
    
    qa_chain = setup_document_qa()
    
    sample_questions = [
        "What is LangChain?",
        "What are the key features of LangChain?",
        "What are common use cases?",
        "How do you install LangChain?"
    ]
    
    print("Sample questions you can ask:")
    for i, question in enumerate(sample_questions, 1):
        print(f"{i}. {question}")
    print()
    
    while True:
        user_question = input("Your question: ")
        
        if user_question.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        try:
            answer = qa_chain.run(user_question)
            print(f"📖 Answer: {answer}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    ask_questions() 