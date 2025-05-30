from data_source import stream_data

def main():
    stream_data(interval=2, total_records=50)
    
if __name__ == "__main__":
    main()