import pandas as pd

def data_cleaning(order_items_df):
    '''
    This function takes the order_items dataframe, cleans the data and returns the cleaned dataframe
    '''

    # Convert the created_at column from object to datetime
    order_items_df['created_at'] = pd.to_datetime(order_items_df.created_at,format='mixed')

    return order_items_df
