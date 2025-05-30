import json
import random
import time
import datetime

def generate_record(id: int):
    return {
        "timestamp": datetime.datetime.now().timestamp(),
        "id": id, 
        "value": round(random.uniform(10.0, 100.0), 2)
    }

def stream_data(interval=1.0, total_records=100):
    record_count = 1
    while record_count <= total_records:
        record = generate_record(record_count)
        print(json.dumps(record))  # Simulating real-time output
        time.sleep(interval)
        record_count += 1

if __name__ == "__main__":
    stream_data(interval=2, total_records=50)