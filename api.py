from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from backend.llm_handler import LLMHandler
from backend.sql_utils import clean_sql

app = FastAPI(title="SQL LLM Chatbot API")

@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}


class SQLRequest(BaseModel):
    schema: str
    user_query: str
    model_name: str
    sql_dialect: Optional[str] = "PostgreSQL"
    temperature: Optional[float] = 0.2


@app.post("/generate_sql")
def generate_sql(request: SQLRequest, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="HuggingFace token missing in Authorization header!")
    
    hf_token = authorization.split(" ")[1]

    if not hf_token:
        raise HTTPException(status_code=401, detail="HuggingFace token missing!")

    try:
        # Initialize LLM handler
        llm = LLMHandler(hf_token=hf_token, model_name=request.model_name)

        # Generate SQL
        sql_query = llm.generate_sql(
            schema=request.schema,
            user_query=request.user_query,
            sql_dialect=request.sql_dialect,
            temperature=request.temperature
        )

        sql_query = clean_sql(sql_query)
        return {"sql_query": sql_query}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
