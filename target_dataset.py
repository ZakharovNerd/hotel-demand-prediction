import pandas as pd
from etna.datasets import TSDataset


def f(row):
    if row['hotel_id'] == 1 or row['hotel_id'] == 2 or row['hotel_id'] == 3 or row['hotel_id'] == 4:
        val = 1 #Economy 
    elif row['hotel_id'] == 5 or row['hotel_id'] == 6 or row['hotel_id'] == 7 or row['hotel_id'] == 8:
        val = 2 # Standart
    else:
        val = 3 # Luxury
    return val


def load_data(source):
    df = pd.read_csv(source)

    df['hotel_id'] = df.apply(f, axis=1)

    # Convert 'order_date' to datetime and ensure it's the index alongside 'hotel_id'
    df['order_date'] = pd.to_datetime(df['order_date'])

    df['order_date'] = df['order_date'] - pd.Timedelta(days=2*365 + 180)

    grouped = df.groupby(['order_date', 'hotel_id']).size().reset_index(name='target')

    grouped['segment'] = grouped['hotel_id'] # Convert order_date to datetime
    grouped.drop(columns=["hotel_id"], inplace=True)

    grouped['timestamp'] = pd.to_datetime(grouped['order_date'])
    grouped.drop(columns=["order_date"], inplace=True)


    # Convert the grouped DataFrame to a TSDataset
    ts_dataset = TSDataset.to_dataset(grouped)
    return ts_dataset