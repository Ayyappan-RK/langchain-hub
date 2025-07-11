# LangChain API Server

A FastAPI-based REST API that exposes all your LangChain examples as web services with a beautiful web interface.

## 🚀 Quick Start

### 1. Start the Server
```bash
python start_api.py
```

### 2. Access the Web Interface
Open your browser and go to: **http://localhost:8000/ui**

### 3. Or Use the API Directly
- API Documentation: **http://localhost:8000/docs**
- Health Check: **http://localhost:8000/**

## 📋 Available Endpoints

### 1. **Chat API** - `/chat`
**POST** - Chat with AI using conversation memory

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "session_id": "optional-session-id"
  }'
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "session_id": "generated-session-id"
}
```

### 2. **Document Q&A API** - `/document-qa`
**POST** - Ask questions about documents

```bash
curl -X POST "http://localhost:8000/document-qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is LangChain?",
    "document_text": "Optional document text..."
  }'
```

**Response:**
```json
{
  "answer": "LangChain is a framework for developing applications powered by language models...",
  "question": "What is LangChain?"
}
```

### 3. **Code Analysis API** - `/code/analyze`
**POST** - Analyze code and get insights

```bash
curl -X POST "http://localhost:8000/code/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello_world():\n    print(\"Hello, World!\")"
  }'
```

**Response:**
```json
{
  "language": "Python",
  "complexity": "simple",
  "suggestions": [
    "Add docstring for better documentation",
    "Consider adding type hints"
  ],
  "explanation": "This is a simple Python function that prints 'Hello, World!'"
}
```

### 4. **Code Generation API** - `/code/generate`
**POST** - Generate code from description

```bash
curl -X POST "http://localhost:8000/code/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Create a function to calculate fibonacci numbers"
  }'
```

**Response:**
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "explanation": "This function calculates the nth Fibonacci number using recursion."
}
```

### 5. **Session Management** - `/sessions`
**GET** - List active chat sessions

```bash
curl "http://localhost:8000/sessions"
```

**Response:**
```json
{
  "active_sessions": ["session-id-1", "session-id-2"],
  "session_count": 2
}
```

### 6. **Reset Chat Session** - `/chat/reset/{session_id}`
**POST** - Reset a chat session (clear memory)

```bash
curl -X POST "http://localhost:8000/chat/reset/session-id-here"
```

## 🎨 Web Interface Features

The web interface at **http://localhost:8000/ui** provides:

### 💬 **Chat Tab**
- Interactive chat with AI
- Conversation memory across sessions
- Reset chat functionality
- Real-time responses

### 📚 **Document Q&A Tab**
- Ask questions about documents
- Use default LangChain documentation
- Upload custom document text
- Semantic search capabilities

### 🔍 **Code Analysis Tab**
- Analyze code for language detection
- Get complexity assessment
- Receive improvement suggestions
- Code explanation

### ⚡ **Code Generation Tab**
- Generate code from descriptions
- Get explanations of generated code
- Syntax highlighting
- Copy-to-clipboard functionality

## 🛠️ Development

### Project Structure
```
langchain-training1/
├── api_app.py              # Main FastAPI application
├── start_api.py            # Startup script
├── static/
│   └── index.html          # Web interface
├── .env                    # Environment variables
├── chatbot_example.py      # Original CLI examples
├── document_qa_example.py
├── code_assistant_example.py
└── README.md
```

### Environment Setup
1. **Install Dependencies:**
```bash
pip install fastapi uvicorn langchain langchain-openai python-dotenv faiss-cpu pydantic
```

2. **Set up Environment Variables:**
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Running in Development Mode
```bash
python start_api.py
```

The server will:
- Auto-reload on code changes
- Show detailed logs
- Check environment variables
- Display available endpoints

### Production Deployment
For production, you might want to use:
```bash
uvicorn api_app:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### API Configuration
- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 8000
- **CORS**: Enabled for all origins
- **Auto-reload**: Enabled in development

## 📊 API Testing

### Using curl
```bash
# Test chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Test document Q&A
curl -X POST "http://localhost:8000/document-qa" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is LangChain?"}'
```

### Using Python requests
```python
import requests

# Chat
response = requests.post("http://localhost:8000/chat", json={
    "message": "Hello!"
})
print(response.json())

# Document Q&A
response = requests.post("http://localhost:8000/document-qa", json={
    "question": "What is LangChain?"
})
print(response.json())
```

### Using Postman
1. Import the collection from `/docs`
2. Set base URL to `http://localhost:8000`
3. Test each endpoint

## 🚨 Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: Server-side errors
- **Detailed error messages** for debugging

### Common Errors
1. **Missing API Key**: Check your `.env` file
2. **Invalid JSON**: Ensure proper JSON format
3. **Network Issues**: Check if server is running

## 🔒 Security Considerations

- **API Key Security**: Never expose API keys in client-side code
- **Input Validation**: All inputs are validated using Pydantic
- **CORS**: Configured for development (adjust for production)
- **Rate Limiting**: Consider adding rate limiting for production

## 📈 Monitoring

### Health Check
```bash
curl http://localhost:8000/
```

### Session Monitoring
```bash
curl http://localhost:8000/sessions
```

## 🎯 Use Cases

### 1. **Customer Support Chatbot**
- Integrate with your website
- Handle FAQs automatically
- Route complex issues to humans

### 2. **Document Analysis System**
- Process legal documents
- Analyze research papers
- Create knowledge bases

### 3. **Code Review Assistant**
- Analyze pull requests
- Generate documentation
- Suggest improvements

### 4. **Content Generation**
- Generate blog posts
- Create marketing copy
- Write documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- **Documentation**: http://localhost:8000/docs
- **Web Interface**: http://localhost:8000/ui
- **Health Check**: http://localhost:8000/

## 🎉 What You've Built

You now have a complete **LangChain API server** with:

✅ **REST API endpoints** for all LangChain features  
✅ **Beautiful web interface** for easy testing  
✅ **Session management** for chat memory  
✅ **Document processing** with semantic search  
✅ **Code analysis and generation**  
✅ **Auto-generated API documentation**  
✅ **Production-ready** FastAPI application  

This is a fully functional AI application that can be deployed, integrated, and extended for real-world use cases! 