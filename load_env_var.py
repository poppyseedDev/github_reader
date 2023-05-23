from dotenv import load_dotenv
import os

# load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'YourAPIKey')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV', 'us-east1-gcp') # You may need to switch with your env
