from fastapi import FastAPI
from pydantic import BaseModel
from models.llm import question_to_sql
from utils.query_executor import execute_sql
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    try:
        sql = question_to_sql(query.question)
        result, columns = execute_sql(sql) 
        return {
            "question": query.question,
            "generated_sql": sql,
            "columns": columns,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}


