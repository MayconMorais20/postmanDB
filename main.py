from typing import Optional
from db import Db
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
import jwt, base64
from body import SQLBody, Token
from encode import Secret
app = FastAPI()

@app.get("/readme", tags=["SQL Query"])
def rules():
    return { "Regras de sintaxe:": [["1 - as tabelas devem ter a database como prefixo","Ex.: SELECT * FROM database.table"],
    ["2 - definir pelo menos uma vez a base de dados com: $ (inicio e fim)","Ex.: SELECT * FROM $database$"],
    ["3 - definir pelo menos uma vez a tabela com: @ (inicio e fim)","Ex.: SELECT * FROM $database$.@table@"]]}

@app.post("/token", tags=["SQL Query"])
def Generate_an_access_token_for_database_connection(token: Token):
    try:
        sct = Secret()
        sct.set_secret(token.secret)
        return {"token":jwt.encode(token.credentials, token.secret, algorithm="HS256"), "secretencode":sct.show}
    except Exception as e:
        print(e)
        return {"message:": e}

@app.post("/execute", tags=["SQL Query"])
def execute_query(sql_body: SQLBody):
    db = Db(sql_body, sql_body.local)
    print(">>>",db.error)
    if not db.error == None:
        raise HTTPException(status_code=400, detail={"erro":db.error})

    result = db.execute(sql_body.query)
    if result["data"]["query_status"] == "FAIL":
        raise HTTPException(status_code=400, detail={"query": sql_body.query, "error": result["data"]})
    return {"query": sql_body.query, "result": result}
