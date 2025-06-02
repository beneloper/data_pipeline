import pandas as pd

def process_data(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']) # for easy query by timestamp

    # Transformations
    melted = df.melt(id_vars=['id'], value_name='val')
    pivoted = df.pivot_table(index='id', values='value', aggfunc='mean')

    # Moving average (by timestamp)
    df.set_index('timestamp', inplace=True)
    df['moving_avg'] = df['value'].rolling('5s').mean()

    return df.reset_index(), melted, pivoted

def main():
    data = [
        {'timestamp': '2025-06-01T19:35:12.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b1', 'value': 79.72},
        {'timestamp': '2025-06-01T19:35:13.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b2', 'value': 60.92},
        {'timestamp': '2025-06-01T19:35:14.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b3', 'value': 70.91},
        {'timestamp': '2025-06-01T19:35:15.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b4', 'value': 12.66},
        {'timestamp': '2025-06-01T19:35:16.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b5', 'value': 22.64},
        {'timestamp': '2025-06-01T19:35:17.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b6', 'value': 82.25},
        {'timestamp': '2025-06-01T19:35:18.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b7', 'value': 46.23},
        {'timestamp': '2025-06-01T19:35:19.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b8', 'value': 74.36},
        {'timestamp': '2025-06-01T19:35:20.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b9', 'value': 35.57},
        {'timestamp': '2025-06-01T19:35:21.740112+00:00', 'id': 'b808737a-ca42-4812-8d96-7c8efa8ea6b0', 'value': 39.88}
    ] 
    df, melted, pivoted = process_data(data)
    print(df.to_string()) 
    print('------------------')
    print(melted.to_string())
    print('------------------')
    print(pivoted.to_string())

if __name__ == "__main__":
    main()
    