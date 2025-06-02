
from process_data import process_data


async def consume_data(queue, results):
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