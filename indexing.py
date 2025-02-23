import os
from dotenv import load_dotenv
import openai
from llama_index.core import StorageContext, readers
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
#from llama_index.readers.file import (PDFReader)

#Load environment variables
load_dotenv()

# Read OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
# raise ValueError("API key not found. Ensure OPENAI_API_KEY is set in your environment variables.")

#  # Set OpenAI API key
openai.api_key = api_key

# Print partial API key for verification
if api_key:
    print("API key: " + api_key[0:6])
else:
    print("API key not found")

# PDF Reader with `SimpleDirectoryReader`
# parser = PDFReader()
# file_extractor = {"pdf": parser}
documents = SimpleDirectoryReader("pdf").load_data()
#file_extractor=file_extractor
# Load documents from the "pdf" directory
# reader = SimpleDirectoryReader(input_dir="pdf")
# documents = reader.load_data()  # This returns a list of documents


# Create the index from the documents
index = VectorStoreIndex.from_documents(documents)

# # Create an index
# index = VectorStoreIndex.from_documents(documents)
#engine=index.as_query_engine()
#result=engine.query("What are the strengths of R over Python?")
#print(result)
# # Save the index 
index.storage_context.persist("faq_index")
#index.storage_context.persist("ml_index")




# persist_dir = "pdf"
# if not os.path.exists(os.path.join(persist_dir, "")):
#     raise FileNotFoundError(f"Missing required file in {persist_dir}. Please regenerate the index.")
# context = StorageContext.from_defaults(persist_dir=persist_dir)


# completion = openai.ChatCompletion.create(
#     model="gpt-4",
#      messages=[
#          {"role": "user", "content": "Write about AI"}
#      ]
#  )
# print(completion.choices[0].message["content"])