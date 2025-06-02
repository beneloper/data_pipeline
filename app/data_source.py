import asyncio
import random
import datetime
import uuid

async def stream_data(queue: asyncio.Queue, interval: int):
    """
    Summary:  Stream data into the queue at specified intervals.\n
    Description: This function generates random data and puts it into the provided asyncio\n
    queue.  The data consists of a timestamp, a unique ID, and a random value.

    Args:
        queue (asyncio.Queue): The asyncio queue where the data will be put.
        interval (int): The interval in seconds at which data will be generated and put into the queue.

    Returns:
        None
    """    
    while True:
        data = {
            "timestamp": datetime.datetime.now(),
            "id": uuid.uuid4(), 
            "value": round(random.uniform(10.0, 100.0), 2)
        }
        await queue.put(data)
        await asyncio.sleep(interval) # simulate n-seconds intervals