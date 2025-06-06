from typing import List
import pandas as pd

def process_data(data: List[dict]) -> tuple:
    """
    Summary:  Process the input data to create a DataFrame, melted DataFrame, and pivoted DataFrame.\n
    Description: This function takes a list of dictionaries containing 'timestamp', 'id', and 'value',
    converts it into a DataFrame, and performs several transformations including melting and pivoting.\n
    It also calculates a moving average of the 'value' column based on the 'timestamp'.
    The resulting DataFrame, melted DataFrame, and pivoted DataFrame are returned as a tuple.
    Args:
        data (list of dict): Input data where each dict contains 'timestamp', 'id', and 'value'.
    Returns:
        tuple: A tuple containing:
            - df (DataFrame): The original data as a DataFrame with 'timestamp' converted to datetime.
            - melted (DataFrame): The melted version of the DataFrame.
            - pivoted (DataFrame): The pivoted version of the DataFrame.
    """

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']) # for easy query by timestamp

    # Transformations
    melted = df.melt(id_vars=['id'], value_name='val')
    pivoted = df.pivot_table(index='id', values=['id', 'value', 'timestamp'], aggfunc='mean')

    # Moving average (by timestamp)
    df.set_index('timestamp', inplace=True)
    df['moving_avg'] = df['value'].rolling('5s').mean()

    # Reset index for the final DataFrame
    return df.reset_index(), melted, pivoted



if __name__ == "__main__":
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

    main()
    