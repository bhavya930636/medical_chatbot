from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv

from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings
import os
load_dotenv()


extracted_data = load_pdf_files("data")
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(minimal_docs)
embedding = download_embeddings()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key = pinecone_api_key)
index_name = "medical-chatbot"
if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "cosine",
        spec = ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents = texts_chunk,
    embedding = embedding,
    index_name = index_name
)

# import os
# import time
# from dotenv import load_dotenv

# from pinecone import Pinecone, ServerlessSpec
# from langchain_pinecone import PineconeVectorStore

# from src.helper import (
#     load_pdf_files,
#     filter_to_minimal_docs,
#     text_split,
#     download_google_embeddings,
# )

# load_dotenv()

# # ==========================
# # Load & Split Documents
# # ==========================
# print("Loading PDFs...")
# extracted_data = load_pdf_files("data")

# minimal_docs = filter_to_minimal_docs(extracted_data)

# texts_chunk = text_split(minimal_docs)

# print(f"Total chunks: {len(texts_chunk)}")

# # ==========================
# # Embedding Model
# # ==========================
# embedding = download_google_embeddings()

# # ==========================
# # Pinecone
# # ==========================
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# pc = Pinecone(api_key=PINECONE_API_KEY)

# index_name = "medical-chatbot"

# # IMPORTANT:
# # Replace dimension with the correct value for your embedding model.
# EMBEDDING_DIMENSION = 768

# if not pc.has_index(index_name):
#     pc.create_index(
#         name=index_name,
#         dimension=EMBEDDING_DIMENSION,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1",
#         ),
#     )

# index = pc.Index(index_name)

# vectorstore = PineconeVectorStore(
#     index=index,
#     embedding=embedding,
# )

# # ==========================
# # Upload in Batches
# # ==========================
# BATCH_SIZE = 50

# for start in range(0, len(texts_chunk), BATCH_SIZE):

#     end = min(start + BATCH_SIZE, len(texts_chunk))
#     batch = texts_chunk[start:end]

#     while True:

#         try:

#             vectorstore.add_documents(batch)

#             print(
#                 f"Uploaded batch {start//BATCH_SIZE + 1} "
#                 f"({end}/{len(texts_chunk)} chunks)"
#             )

#             # small delay to reduce rate limit
#             time.sleep(2)

#             break

#         except Exception as e:

#             if "429" in str(e) or "ResourceExhausted" in str(e):

#                 print("Rate limit reached. Waiting 20 seconds...")
#                 time.sleep(20)

#             else:
#                 raise e

# print("\n✅ All documents uploaded successfully!")