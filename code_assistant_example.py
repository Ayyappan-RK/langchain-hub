import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

class CodeAnalysis(BaseModel):
    """Structure for code analysis output"""
    language: str = Field(description="Programming language detected")
    complexity: str = Field(description="Code complexity level (simple, moderate, complex)")
    suggestions: List[str] = Field(description="List of improvement suggestions")
    explanation: str = Field(description="Brief explanation of what the code does")

def create_code_assistant():
    """Create a code analysis assistant"""
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create output parser
    parser = PydanticOutputParser(pydantic_object=CodeAnalysis)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert code reviewer and programmer. 
        Analyze the provided code and provide insights about:
        1. Programming language
        2. Code complexity
        3. Improvement suggestions
        4. What the code does
        
        {format_instructions}"""),
        ("user", "Analyze this code:\n{code}")
    ])
    
    # Create chain
    chain = prompt | llm | parser
    
    return chain

def code_generation_assistant():
    """Create a code generation assistant"""
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert programmer. Generate clean, well-documented code based on the user's requirements."),
        ("user", "Generate code for: {requirement}")
    ])
    
    chain = prompt | llm
    
    return chain

def interactive_code_assistant():
    """Interactive code assistant session"""
    print("💻 Code Assistant")
    print("1. Analyze existing code")
    print("2. Generate new code")
    print("3. Quit")
    
    analysis_chain = create_code_assistant()
    generation_chain = code_generation_assistant()
    
    while True:
        choice = input("\nChoose an option (1-3): ")
        
        if choice == "1":
            print("\n📝 Code Analysis Mode")
            print("Paste your code (type 'END' on a new line when done):")
            
            code_lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                code_lines.append(line)
            
            code = "\n".join(code_lines)
            
            if code.strip():
                try:
                    result = analysis_chain.invoke({
                        "code": code,
                        "format_instructions": analysis_chain.parser.get_format_instructions()
                    })
                    
                    print(f"\n🔍 Analysis Results:")
                    print(f"Language: {result.language}")
                    print(f"Complexity: {result.complexity}")
                    print(f"Explanation: {result.explanation}")
                    print(f"Suggestions:")
                    for suggestion in result.suggestions:
                        print(f"  • {suggestion}")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == "2":
            print("\n🚀 Code Generation Mode")
            requirement = input("Describe what code you want to generate: ")
            
            try:
                response = generation_chain.invoke({"requirement": requirement})
                print(f"\n💻 Generated Code:\n{response.content}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    interactive_code_assistant() 