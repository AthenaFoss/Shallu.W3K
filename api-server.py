import chromadb
from chromadb.utils import embedding_functions

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import uuid

from support_ticket import support_ticket_router

from query_pipelines.default.entrypoint import default_entrypoint

app = FastAPI()
app.include_router(support_ticket_router)


class ChatRequest(BaseModel):
    user_query: str
    history: Optional[str] = None
    pipeline: Optional[str] = "default_pipeline"

class ChatResponse(BaseModel):
    response: str

class DatabaseEntry(BaseModel):
    question: str
    answer: str

# ChatAPI endpoint
@app.get("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = execute_pipeline(request.pipeline, request.user_query, request.history)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def execute_pipeline(pipeline_name, user_query, history):
    
    if pipeline_name == "default_pipeline":
        return default_entrypoint(user_query, history)
    else:
        raise ValueError(f"Invalid pipeline name: {pipeline_name}")

# DatabaseAPI endpoint
@app.post("/db/add")
def add_database_entry(entry: DatabaseEntry):
    try:
        entry_id = add_to_master_db(entry.question, entry.answer)
        update_downstream_dbs(entry.question, entry.answer, entry_id)
        return {"message": "Entry added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def add_to_master_db(question, answer):
    conn = sqlite3.connect("databases/master/master.db")
    entry_id = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO question_answer_pairs (id, question, answer) VALUES (?, ?, ?)", (entry_id, question, answer))
    conn.commit()
    conn.close()
    return entry_id

def update_downstream_dbs(question, answer, entry_id):

    def init_vdb_items():

        # have a logic where , if table/collection not exist , seed from master table

        client = chromadb.PersistentClient(path="./databases/default_pipeline_vdb")
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-en-v1.5",device="cuda")
        collection = client.get_or_create_collection(name="default_pipeline_vdb",embedding_function=embedding_func,metadata={"hnsw:space": "cosine"})

        return client,embedding_func,collection

    def add_qn_vdb(question,entry_id,collection,embedding_func):
        embed_data = embedding_func( [question] )    
        ids_list = [entry_id]
        collection.add(
            embeddings=embed_data,
            ids=ids_list
        )

    client,embedding_func,collection = init_vdb_items()
    add_qn_vdb(question,entry_id,collection,embedding_func)