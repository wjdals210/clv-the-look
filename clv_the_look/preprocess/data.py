import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data

def data_cleaning(order_items_df, orders_df):
    '''
    This function takes the order_items and the orders tables, aggregates the order_items table,
    merges the tables, cleans the datatypes and returns the cleaned dataframe
    '''

    # Agreegate the sale_price by order_id and merge the orders table
    order_sales = order_items_df[['order_id','sale_price']].groupby(by='order_id').sum('sale_price').reset_index()

    cleaned_order_sales = orders_df.merge(order_sales, on='order_id', how='left').set_index('order_id')

    # Convert the created_at column from 'object' to datetime64
    cleaned_order_sales['created_at'] = pd.to_datetime(cleaned_order_sales['created_at'],
                                                       format='mixed').dt.tz_localize(None)
    cleaned_order_sales['returned_at'] = pd.to_datetime(cleaned_order_sales['returned_at'],
                                                       format='mixed').dt.tz_localize(None)
    cleaned_order_sales['shipped_at'] = pd.to_datetime(cleaned_order_sales['shipped_at'],
                                                       format='mixed').dt.tz_localize(None)
    cleaned_order_sales['delivered_at'] = pd.to_datetime(cleaned_order_sales['delivered_at'],
                                                       format='mixed').dt.tz_localize(None)


    return cleaned_order_sales

def rfm(cleaned_order_sales):
    '''
    This function takes the cleaned orders dataframe and converts it a Recency-Frequency-Tenure dataframe
    This rfm dataframe is appropriate for passing to the Beta-Geometric model
    '''
    return summary_data_from_transaction_data(transactions = cleaned_order_sales,
                                              customer_id_col = 'user_id',
                                              datetime_col = 'created_at',
                                              monetary_value_col = 'sale_price')

def order_features(split_date, orders_df, order_items_df, products_df):
    '''
    Calculates features required for XBG
    inputs order_df, order_items_df, products_df
    Assumes revenue per order is already calculated in sale_price column,
    all the datetime fields and split_date should be in datetime format
    '''

    orders_df = data_cleaning(order_items_df, orders_df)

    # Days calculation
    orders_df['days_to_split_date'] = (split_date - orders_df['created_at']).dt.days
    orders_df['days_delivery'] = (orders_df['delivered_at'] - orders_df['created_at']).dt.days

    # Filter data only for last 2 years
    orders_df = orders_df[(orders_df.days_to_split_date >= 0) & (orders_df.days_to_split_date < 365*2)]

    # Base dataset : user level
    base = orders_df[['user_id','order_id']].groupby('user_id').count().rename(columns={'order_id': 'orders_total'})

    # Calculate first purchase, latest purchase
    first_purchase = orders_df[['user_id','created_at']].groupby('user_id').min().rename(columns={'created_at': 'min_created_at'})
    base = base.merge(first_purchase, on='user_id')
    latest_purchase = orders_df[['user_id','created_at']].groupby('user_id').max().rename(columns={'created_at': 'max_created_at'})
    base = base.merge(latest_purchase, on='user_id')


    # Days from first/last order (Recency, customer T)
    base['days_from_first_order'] =  (split_date - base['min_created_at']).dt.days
    base['days_from_last_order'] =  (split_date - base['max_created_at']).dt.days


    # Frequency, Monetary
    df_30 = orders_df[orders_df.days_to_split_date < 30]
    df_60 = orders_df[(orders_df.days_to_split_date >= 30) & (orders_df.days_to_split_date < 60)]
    df_120 = orders_df[(orders_df.days_to_split_date >= 60) & (orders_df.days_to_split_date < 120)]
    df_240 = orders_df[(orders_df.days_to_split_date >= 120) & (orders_df.days_to_split_date < 240)]
    df_480 = orders_df[(orders_df.days_to_split_date >= 240) & (orders_df.days_to_split_date < 480)]

    # orders per different timeframe
    f_30 = df_30[['user_id','order_id']].groupby(by='user_id').count().rename(columns={'order_id': 'orders_30d'})
    f_60 = df_60[['user_id','order_id']].groupby(by='user_id').count().rename(columns={'order_id': 'orders_60d'})
    f_120 = df_120[['user_id','order_id']].groupby(by='user_id').count().rename(columns={'order_id': 'orders_120d'})
    f_240 = df_240[['user_id','order_id']].groupby(by='user_id').count().rename(columns={'order_id': 'orders_240d'})
    f_480 = df_480[['user_id','order_id']].groupby(by='user_id').count().rename(columns={'order_id': 'orders_480d'})

    # Frequency Joined to base dataset
    base = base.merge(f_30,on='user_id',how='left')
    base = base.merge(f_60,on='user_id',how='left')
    base = base.merge(f_120,on='user_id',how='left')
    base = base.merge(f_240,on='user_id',how='left')
    base = base.merge(f_480,on='user_id',how='left')

    # orders per different timeframe
    m_30 = df_30[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_30d'})
    m_60 = df_60[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_60d'})
    m_120 = df_120[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_120d'})
    m_240 = df_240[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_240d'})
    m_480 = df_480[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_480d'})
    m_total = df[['user_id','sale_price']].groupby(by='user_id').sum().rename(columns={'sale_price': 'revenue_total'})

    # Monetary Joined to base dataset
    base = base.merge(m_30,on='user_id',how='left')
    base = base.merge(m_60,on='user_id',how='left')
    base = base.merge(m_120,on='user_id',how='left')
    base = base.merge(m_240,on='user_id',how='left')
    base = base.merge(m_480,on='user_id',how='left')
    base = base.merge(m_total,on='user_id',how='left')

    # ABV calculation
    base['abv'] = base['revenue_total']/base['orders_total']

    # Other calcs (delivery, num_items)
    avg_delivery_days = orders_df[['user_id','days_delivery']].groupby('user_id').mean().rename(columns={'days_delivery': 'avg_delivery_days'})
    base = base.merge(avg_delivery_days, on='user_id')
    avg_items_p_order = orders_df[['user_id','num_of_item']].groupby('user_id').mean().rename(columns={'num_of_item': 'avg_num_items'})
    base = base.merge(avg_items_p_order, on='user_id')

    return base
