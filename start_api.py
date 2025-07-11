#!/usr/bin/env python3
"""
LangChain API Server Startup Script
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please make sure you have a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment check passed")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting LangChain API Server...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("\n📋 Available endpoints:")
    print("  • http://localhost:8000/          - Health check")
    print("  • http://localhost:8000/ui        - Web UI")
    print("  • http://localhost:8000/docs      - API documentation")
    print("  • http://localhost:8000/chat      - Chat API")
    print("  • http://localhost:8000/document-qa - Document Q&A API")
    print("  • http://localhost:8000/code/analyze - Code analysis API")
    print("  • http://localhost:8000/code/generate - Code generation API")
    
    print("\n🎯 Quick Start:")
    print("  1. Open http://localhost:8000/ui in your browser")
    print("  2. Or use the API directly with curl/Postman")
    print("  3. Check http://localhost:8000/docs for full API docs")
    
    print("\n" + "=" * 50)
    print("Starting server... (Press Ctrl+C to stop)")
    
    try:
        uvicorn.run(
            "api_app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 