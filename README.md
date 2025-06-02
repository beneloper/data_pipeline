# Real-Time Data Pipeline

This project simulates real-time data pipeline.  It uses pandas transformation (.melt, .pivot_table, moving average).  It uses asyncio for async processing.  In addition, it uses FastAPI to create REST endpoints for custom data views.

## Setup
```bash
git clone https://github.com/beneloper/data_pipeline.git
cd data_pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # use pip3 for MacOS
uvicorn app.main:app --reload
```

## Design
### Overview
This application simulates a rea-time data stream, processes the data using pandas, and serves the results through an asynchronous REST API built with FastAPI.  The architecture supports concurrent ingestion, transformation, and querying operations. 
### Architecture
                +---------------------------+
                |   Simulated Data Source   |
                | (JSON with timestamp, ID) |
                +------------+--------------+
                             |
                             v
                +---------------------------+
                |       Async Queue         |
                | (asyncio.Queue instance)  |
                +------------+--------------+
                             |
                             v
                +---------------------------+
                |   Processing Pipeline     |
                | (pandas transformations)  |
                +------------+--------------+
                             |
                  +----------+----------+
                  |                     |
        +---------v--------+ +----------v---------+
        | Latest Processed | | Aggregated Results |
        | DataFrame (dict) | |   (melt/pivot/MA)  |
        +------------------+ +--------------------+
                             |
                             v
                   +--------------------+
                   |   FastAPI Web API  |
                   +--------+-----------+
                            |
          +----------------+----------------+
          |                                 |
+---------v--------+           +------------v-------------+
| GET /latest      |           | GET /query?start=...     |
| Returns latest   |           | Filter by time window    |
| processed data   |           | on 'timestamp' field     |
+------------------+           +--------------------------+


### Key Components
__1. Simulated Data Ingestion (app/data_source.py)__
* Generate JSON objects with:

    * timestamp: current local time (could be changed to use UTC)
    * id: random UUID
    * value: random float between 10.xx - 99.xx
* Pushed data to an asyncio.Queue at 1-sec intervals

__2. Async Data Processing (app/consume.py and app/process.py)__
* Consumes data in batches of 10 items
* Performs:
    * DataFrame creation
    * .melt() to normalize data
    * .pivot() for aggregation
    * Time-based rolling average
* Updates shared results dict with transformed data

__3. REST API (app/main.py)__
* GET /trigger: prints info of pipeline was triggered at startup
* GET /latest: returns the latest processed batch
* GET /query?start&end: filters results by timestamp range (optional, returns latest of not provided).  Example:

    * /query?start=2025-06-01T21:15:07&end=2025-06-01T21:15:08
    * /query?start=2025-06-01T21:15:07
    * /query?end=2025-06-01T21:15:08
    * /query   (___This is the same as /latest___)

__4. Data Store__
* results: In-memory dictionary holding latest processed DataFrames, serialized as lists of dicts

__5. Concurrency Strategy__
* asyncio.Queue is used for thread-safe data transfer between consuming and processing
* asyncio.create_task enables concurrent ingestion and processing during FastAPI's startup event

__6. Assumption__
* Data volume is small, in-memory storage
* Processed results reset with every 10 new message
* System is designed for demo only

__7. Limitations__
* No persistent storage (data is lost on start and reset for new messages)
* Fixed batch size of 10, no dynamic tuning
* No authentication or reate-limiting on the API's
