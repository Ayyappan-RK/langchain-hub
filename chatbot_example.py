import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

def create_chatbot():
    """Create a simple chatbot with memory"""
    
    # Initialize the chat model
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create memory for conversation history
    memory = ConversationBufferMemory()
    
    # Create conversation chain
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    return conversation

def chat_with_bot():
    """Interactive chat session"""
    print("🤖 Welcome to the LangChain Chatbot!")
    print("Type 'quit' to exit\n")
    
    conversation = create_chatbot()
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🤖 Goodbye! Thanks for chatting!")
            break
        
        try:
            response = conversation.predict(input=user_input)
            print(f"🤖 {response}")
        except Exception as e:
            print(f"🤖 Sorry, I encountered an error: {e}")

if __name__ == "__main__":
    chat_with_bot() 