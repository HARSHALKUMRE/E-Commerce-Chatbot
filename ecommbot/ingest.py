from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import BedrockEmbeddings
from dotenv import load_dotenv
import os
import boto3
import pandas as pd
from ecommbot.data_converter import dataconverter

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")

## bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name = "us-east-1")

## Get embedding model
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)


def ingestdata(status):
    vstore = AstraDBVectorStore(
        embedding=bedrock_embeddings,
        collection_name="chatbotecom1",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    
    storage = status
    
    if storage == None:
        docs = dataconverter()
        inserted_ids = vstore.add_documents(docs)
    else:
        return vstore
    return vstore, inserted_ids


if __name__=='__main__':
    vstore,inserted_ids=ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")