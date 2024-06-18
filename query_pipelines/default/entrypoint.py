import chromadb
from chromadb.utils import embedding_functions
import sqlite3

import requests
import os
from dotenv import load_dotenv

def default_entrypoint(chat,history):


    similar_entries = fetch_similar_entries(chat)

    prompt = """
You are an AI assistant who is expert at web 3 and blockchain. You work for web3kerala community and you help answer users queries about web3 in general.

Given below is the users questions:
{chat}

Given below is the chat history :
{history}

Here are a few similar questions that might help you in answering the users questions: {similar_entries}

Respond to the user in a a very friendly and helpful manner.
Your response should be very concise and direct.
""".format(chat=chat, history=history, similar_entries=similar_entries)
                
    endpoint = 'https://api.together.xyz/inference'

    load_dotenv()

    response = requests.post(
    url=endpoint,
    headers={
        "Authorization": f"Bearer {os.getenv('TOGETHER_AI_KEY')}",
        "Content-Type": "application/json"
    },                
    json={
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "max_tokens": 6000,
        "temperature": 0.2,
        "messages": [
            {
                "content": prompt,
                "role": "user"
            }
        ]
    },)

    if response.status_code == 200:
        content = response.json()
        return content["output"]["choices"][0]["text"]
    else:
        raise Exception(f"Request failed with status code {response.status_code}")
    

def fetch_similar_entries(query):

    def init_vdb_items():
        client = chromadb.PersistentClient(path="./databases/default_pipeline_vdb")
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-en-v1.5",device="cuda")
        collection = client.get_or_create_collection(name="default_pipeline_vdb",embedding_function=embedding_func,metadata={"hnsw:space": "cosine"})

        return client,embedding_func,collection

    def query_vdb(question,collection):
        fetched_doc = collection.query(
            query_texts=question,
            n_results=3
        )

        conn = sqlite3.connect("databases/master/master.db")
        cursor = conn.cursor()
        result = []

        for pair_id in fetched_doc["ids"][0]:
            cursor.execute("SELECT question, answer FROM question_answer_pairs WHERE id = ?", (pair_id,))
            row = cursor.fetchone()
            result.append({"question": row[0], "answer": row[1]})

        conn.close()

        return result

        # DEFAULT EMBEDDING DB
    _,_,collection = init_vdb_items()
    return query_vdb(query,collection)