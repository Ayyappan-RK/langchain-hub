import os
import uuid
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LangChain API",
    description="REST API for LangChain examples including chatbot, document Q&A, and code assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global storage for conversation sessions
conversation_sessions: Dict[str, ConversationChain] = {}

# Pydantic models for requests and responses
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation memory")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response")
    session_id: str = Field(..., description="Session ID for future requests")

class DocumentQARequest(BaseModel):
    question: str = Field(..., description="Question about the document")
    document_text: Optional[str] = Field(None, description="Document text to analyze")

class DocumentQAResponse(BaseModel):
    answer: str = Field(..., description="Answer to the question")
    question: str = Field(..., description="Original question")

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code to analyze")

class CodeAnalysisResponse(BaseModel):
    language: str = Field(..., description="Programming language detected")
    complexity: str = Field(..., description="Code complexity level")
    suggestions: List[str] = Field(..., description="Improvement suggestions")
    explanation: str = Field(..., description="What the code does")

class CodeGenerationRequest(BaseModel):
    requirement: str = Field(..., description="Description of code to generate")

class CodeGenerationResponse(BaseModel):
    code: str = Field(..., description="Generated code")
    explanation: str = Field(..., description="Explanation of the generated code")

class HealthResponse(BaseModel):
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Status message")

# Initialize LangChain components
def get_llm():
    """Get OpenAI LLM instance"""
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def get_qa_llm():
    """Get OpenAI LLM for Q&A with lower temperature"""
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# API Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="LangChain API is running! Check /docs for API documentation."
    )

@app.get("/ui")
async def get_ui():
    """Serve the HTML UI"""
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with AI using conversation memory"""
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in conversation_sessions:
            # Create new conversation
            llm = get_llm()
            memory = ConversationBufferMemory()
            conversation = ConversationChain(
                llm=llm,
                memory=memory,
                verbose=False
            )
            conversation_sessions[session_id] = conversation
        else:
            conversation = conversation_sessions[session_id]
        
        # Get response
        response = conversation.predict(input=request.message)
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/chat/reset/{session_id}")
async def reset_chat_session(session_id: str):
    """Reset a chat session (clear memory)"""
    try:
        if session_id in conversation_sessions:
            del conversation_sessions[session_id]
        return {"message": f"Session {session_id} reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset error: {str(e)}")

@app.post("/document-qa", response_model=DocumentQAResponse)
async def document_qa(request: DocumentQARequest):
    """Ask questions about documents"""
    try:
        # Create sample document if no text provided
        if not request.document_text:
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
            """
            document_text = sample_text
        else:
            document_text = request.document_text
        
        # Create temporary file
        temp_file = f"temp_doc_{uuid.uuid4()}.txt"
        with open(temp_file, "w") as f:
            f.write(document_text)
        
        try:
            # Load and process document
            loader = TextLoader(temp_file)
            documents = loader.load()
            
            # Split documents
            text_splitter = CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            vectorstore = FAISS.from_documents(texts, embeddings)
            
            # Create QA chain
            llm = get_qa_llm()
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )
            
            # Get answer
            answer = qa_chain.run(request.question)
            
            return DocumentQAResponse(
                answer=answer,
                question=request.question
            )
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document Q&A error: {str(e)}")

@app.post("/code/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code and provide insights"""
    try:
        llm = get_qa_llm()
        
        # Create output parser
        parser = PydanticOutputParser(pydantic_object=CodeAnalysisResponse)
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer and programmer. 
            Analyze the provided code and provide insights about:
            1. Programming language
            2. Code complexity (simple, moderate, complex)
            3. Improvement suggestions
            4. What the code does
            
            {format_instructions}"""),
            ("user", "Analyze this code:\n{code}")
        ])
        
        # Create chain
        chain = prompt | llm | parser
        
        # Get analysis
        result = chain.invoke({
            "code": request.code,
            "format_instructions": parser.get_format_instructions()
        })
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code analysis error: {str(e)}")

@app.post("/code/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code from description"""
    try:
        llm = get_llm()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert programmer. Generate clean, well-documented code based on the user's requirements. Also provide a brief explanation of what the code does."),
            ("user", "Generate code for: {requirement}")
        ])
        
        chain = prompt | llm
        
        response = chain.invoke({"requirement": request.requirement})
        
        # Simple parsing to separate code and explanation
        content = response.content
        lines = content.split('\n')
        
        # Try to find code block
        code_lines = []
        explanation_lines = []
        in_code_block = False
        
        for line in lines:
            if '```' in line:
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_lines.append(line)
            else:
                explanation_lines.append(line)
        
        code = '\n'.join(code_lines).strip()
        explanation = '\n'.join(explanation_lines).strip()
        
        if not code:
            # If no code block found, treat everything as code
            code = content
            explanation = "Generated code based on your requirements."
        
        return CodeGenerationResponse(
            code=code,
            explanation=explanation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation error: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    """List all active chat sessions"""
    return {
        "active_sessions": list(conversation_sessions.keys()),
        "session_count": len(conversation_sessions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 