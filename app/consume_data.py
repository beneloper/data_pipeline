
import asyncio

from app.process_data import process_data

async def consume_data(queue: asyncio.Queue, results: dict) -> None:
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

if __name__ == "__main__":
    async def main():
        queue = asyncio.Queue()
        results = {'latest': [], 'melted': [], 'pivoted': []}

        # Simulate data being added to the queue
        for i in range(25):
            await queue.put({
                'timestamp': f'2025-06-01T19:35:1{i}.740112+00:00',
                'id': f'b808737a-ca42-4812-8d96-7c8efa8ea6b{i}',
                'value': i * 10.0
            })

        await consume_data(queue, results)
        print(results)

    asyncio.run(main())