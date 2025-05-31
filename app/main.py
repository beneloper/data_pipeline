from fastapi import FastAPI

app = FastAPI()

@app.get('/trigger')
async def trigger():
    return {"message": "Data pipeline was triggered."}

@app.get('/latest')
async def get_latest():
    return {"result": []}

@app.get('/query')
async def query_data():
    return {"result": []}