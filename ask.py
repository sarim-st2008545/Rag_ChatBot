import chromadb
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "document_qa"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"  
def setup_chroma():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    return chroma_client.get_collection(name=COLLECTION_NAME)

def get_groq_response(question, context):
    client = Groq(api_key=GROQ_API_KEY)
    
    # Try primary model first, fallback to alternate if needed
    for model in [MODEL_NAME]:
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"""Answer ONLY based on this context about gardening/agriculture. DOnt use internet
                        If the question is unrelated or answer isn't in context, say "I can only answer gardening questions".
                        
                        Context: {context}"""
                    },
                    {"role": "user", "content": question}
                ],
                model=model,
                temperature=0.1,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Tried model {model}, error: {e}")
            continue
    
    return "Sorry, I couldn't process your request. Please try again later."

def main():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not found in .env file")
        return
    
    collection = setup_chroma()
    
    print("Gardening Expert Chatbot (type 'exit' to quit)")
    print("--------------------------------------------")
    print("Note: I can only answer questions about gardening and agriculture\n")
    
    while True:
        question = input("\nYour gardening question: ")
        
        if question.lower() == 'exit':
            break
            
        try:
            results = collection.query(
                query_texts=[question],
                n_results=3
            )
            
            if not results['documents']:
                print("No relevant gardening information found")
                continue
                
            context = "\n\n".join(results['documents'][0])
            answer = get_groq_response(question, context)
            
            print("\nAnswer:")
            print(answer)
            print("\nRelevant gardening information:")
            for i, doc in enumerate(results['documents'][0], 1):
                print(f"{i}. {doc[:150]}...")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()