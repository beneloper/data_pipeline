import asyncio
import random
import datetime
import uuid

async def stream_data(queue, interval: int):
    while True:
        data = {
            "timestamp": datetime.datetime.now(),
            "id": uuid.uuid4(), 
            "value": round(random.uniform(10.0, 100.0), 2)
        }
        await queue.put(data)
        await asyncio.sleep(interval) # simulate n-seconds intervals