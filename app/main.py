import asyncio
from typing import Annotated
from fastapi import FastAPI, Query
import pandas as pd

from models import QueryFilter
from consume_data import consume_data
from data_source import stream_data

app = FastAPI()
data_queue = asyncio.Queue()
results = {}

@app.get('/trigger')
async def trigger():
    asyncio.create_task(stream_data(data_queue, 1))
    asyncio.create_task(consume_data(data_queue, results))
    return {"message": "Data pipeline was triggered."}

@app.get('/latest')
def get_latest():
    return results['latest']

@app.get('/melted')
def get_melted():
    return results['melted']

@app.get('/pivoted')
def get_pivoted():
    return results['pivoted']

@app.get('/query')
async def query_data(query_filter: Annotated[QueryFilter, Query()]):
    start = query_filter.start
    end = query_filter.end

    if start == None and end == None:
        return get_latest()
    
    df = pd.DataFrame(results.get("latest", []))
    if df.empty:
        return []

    df['timestamp'] = pd.to_datetime(df['timestamp'])


    if start and end:
        mask = (df['timestamp'] >= pd.to_datetime(start)) & (df['timestamp'] <= pd.to_datetime(end))
    elif start:
        mask = df['timestamp'] >= pd.to_datetime(start)
    else:
        mask = df['timestamp'] <= pd.to_datetime(end)

    return df[mask].to_dict(orient='records')