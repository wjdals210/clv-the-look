import pandas as pd
import lifetimes

def data_cleaning(order_items_df):
    '''
    This function takes the order_items dataframe, cleans the data and returns the cleaned dataframe
    '''

    # Convert the created_at column from object to datetime
    order_items_df['created_at'] = pd.to_datetime(order_items_df.created_at,format='mixed')

    return order_items_df

def rfm(cleaned_order_units_df):
    '''
    This function takes the cleaned order_items dataframe and outputs the Recency, Frequency and Tenure dataframe
    '''
    return summary_data_from_transaction_data(transactions = df,
                                              customer_id_col = 'user_id',
                                              datetime_col = 'created_at',
                                              monetary_value_col = 'sale_price')
