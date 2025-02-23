import openai
import os
from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Query(BaseModel):
    question: str

# Load environment variables
load_dotenv()

# Read API key and configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key  # Ensure OpenAI library is configured

# Print first 6 characters of the API key for debugging
if api_key:
    print(f"API Key Loaded: {api_key[:6]}...")
else:
    print("API key not found")
    
# Load index from storage
persist_dir = "pdf"
context = StorageContext.from_defaults(persist_dir=persist_dir)
try:
    index = load_index_from_storage(context)
    print("Index loaded successfully.")
except FileNotFoundError:
    print(f"Index files not found in '{persist_dir}'. Building a new index...")
    # Create a new index if files are missing
    documents = SimpleDirectoryReader(persist_dir).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=persist_dir)
    print("Index built and persisted successfully.")

# Initialize query engine
engine = index.as_query_engine()

# FastAPI setup
app = FastAPI()

@app.post("/")
async def query(query: Query):
    result = engine.query(query.question)
    return {"response": str(result)}  # Ensure the result is serialized

# Run the server
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
#result = post(url="http://localhost:8080", json={"question": value})
