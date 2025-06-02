import asyncio
import pandas as pd
from typing import Annotated, List
from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from app.models import QueryFilter
from app.consume_data import consume_data
from app.data_source import stream_data
from app.process_data import process_data

INTERVAL_IN_SEC: int = 1

data_queue = asyncio.Queue()
results = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Summary:  Lifespan event handler for the FastAPI application.\n
    Description: This function is called when the FastAPI application starts up and shuts down.\n
    It initializes the data streaming and consumption tasks, allowing the application to process data in real-time.\n
    It uses asyncio to create tasks for streaming data and consuming it from the queue.\n
    The tasks run concurrently, enabling the application to handle incoming data efficiently.

    Args:
        app (FastAPI): The FastAPI application instance.
    Returns:
        None
    Yields:
        None: This allows the application to run until it is stopped, at which point the tasks are cleaned up.
    """    

    print("Starting data streaming and consumption tasks...")
    asyncio.create_task(stream_data(data_queue, INTERVAL_IN_SEC))
    asyncio.create_task(consume_data(data_queue, results))

    yield  # This allows the application to run until it is stopped
    print("Stopping data streaming and consumption tasks...")

app = FastAPI(lifespan=lifespan)

@app.get('/trigger')
async def trigger() -> dict:
    print("Data pipeline is auto-started on app launch.")
    return {"message": "Data pipeline triggered (auto-started on app launch)"}

@app.get('/latest')
def get_latest() -> dict:
    """
    Summary: Get the latest records.
    Description: This endpoint retrieves the latest records processed by the data pipeline.
    Returns:
        dict: A dictionary containing the latest records, melted data, and pivoted data.
        If no data is available, an empty dictionary is returned.
    """

    return results

@app.get('/query')
async def query_data(query_filter: Annotated[QueryFilter, Query()]) -> dict:
    """
    Summary: Query data based on timestamp range.\n
    Description: This endpoint allows querying the data based on a specified timestamp range.\n
    It returns the records that fall within the provided start and end timestamps.  If no \n
    timestamps are provided, it defaults to returning the latest records. 

    Example:
        /query?start=2025-06-01T21:15:07&end=2025-06-01T21:15:08\n
        /query?start=2025-06-01T21:15:07\n
        /query?end=2025-06-01T21:15:08\n

    Args:
        start: str | None: The start timestamp for the query. If None, no lower bound is applied.
        end: str | None: The end timestamp for the query. If None, no upper bound is applied. 

    Returns:
        dict: A dictionary containing the latest, melted, and pivoted data within the specified timestamp range.\n
        If no data matches the criteria, an empty dictionary is returned.
    """    
    
    latest = results.get("latest", [])
    if not latest:
        return {}

    start = query_filter.start
    end = query_filter.end
    if start == None and end == None:
        return results 
    
    df = pd.DataFrame(latest)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if start and end:
        mask = (df['timestamp'] >= pd.to_datetime(start)) & (df['timestamp'] <= pd.to_datetime(end))
    elif start:
        mask = df['timestamp'] >= pd.to_datetime(start)
    else:
        mask = df['timestamp'] <= pd.to_datetime(end)

    mask_data = df[mask]
    if mask_data.empty:
        return {}

    filtered_data = mask_data.reset_index(drop=True)
    latest, melted, pivoted = process_data(filtered_data.to_dict(orient='records'))
    return {
        "latest": latest.to_dict(orient='records'),
        "melted": melted.to_dict(orient='records'), 
        "pivoted": pivoted.to_dict(orient='records')
    }