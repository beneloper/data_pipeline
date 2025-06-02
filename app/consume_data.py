
from asyncio import Queue

from app.process_data import process_data

async def consume_data(queue: Queue, results: dict) -> None:
    """
    Summary: Consume data from the queue and process it in batches.\n
    Description: This function continuously consumes data from the provided asyncio queue.\n
    It collects data in batches of 10, processes each batch, and updates the results\n
    dictionary with the latest, melted, and pivoted data.

    Args:
        queue (Queue): The asyncio queue from which data will be consumed.
        results (dict): A dictionary to store the processed results, including 'latest', 'melted', and 'pivoted' data.
    Returns:
        None
    """    
    
    buffer = []
    while True:
        data = await queue.get()
        buffer.append(data)

        if len(buffer) >= 10:
            processed = process_data(buffer)
            results['latest'] = processed[0].to_dict(orient='records')
            results['melted'] = processed[1].to_dict(orient='records')
            results['pivoted'] = processed[2].to_dict(orient='records')
            buffer.clear() 