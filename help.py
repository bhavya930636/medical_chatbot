from src.helper import download_google_embeddings
import os
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("GEMINI_API_KEY"))
print(os.getenv("GEMINI_API_KEY"))
emb = download_google_embeddings()

vec = emb.embed_query(
    "hello",
    output_dimensionality=768
)

print(len(vec))