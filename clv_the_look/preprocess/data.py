import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data

def data_cleaning(order_items_df, orders_df):
    '''
    This function takes the order_items and the orders tables, aggregates the order_items table,
    merges the tables, cleans the datatypes and returns the cleaned dataframe
    '''

    # Agreegate the sale_price by order_id and merge the orders table
    order_sales = order_items_df[['order_id','sale_price']].groupby(by='order_id').sum('sale_price').reset_index()

    cleaned_order_sales = orders_df.merge(order_sales, on='order_id', how='left')

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

def select_user_columns(users_df, split_date):

    df = users_df[['id','age','country','created_at']].rename(columns={'id':'user_id'})
    # Filter users only for last 2 years from split date
    min_date = split_date - pd.DateOffset(days=365*2)
    df['created_at'] = pd.to_datetime(df['created_at'], format='mixed').dt.tz_localize(None)
    df = df[(df['created_at'] <= split_date) & (df['created_at'] > min_date)]

    return df

def order_features(orders_df, order_items_df, split_date):
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
    orders_df = orders_df[(orders_df.days_to_split_date >= 0) & (orders_df.days_to_split_date < 365*3)]

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
    f_30 = df_30[['user_id','order_id']].groupby(by='user_id').count().fillna(0).rename(columns={'order_id': 'orders_30d'})
    f_60 = df_60[['user_id','order_id']].groupby(by='user_id').count().fillna(0).rename(columns={'order_id': 'orders_60d'})
    f_120 = df_120[['user_id','order_id']].groupby(by='user_id').count().fillna(0).rename(columns={'order_id': 'orders_120d'})
    f_240 = df_240[['user_id','order_id']].groupby(by='user_id').count().fillna(0).rename(columns={'order_id': 'orders_240d'})
    f_480 = df_480[['user_id','order_id']].groupby(by='user_id').count().fillna(0).rename(columns={'order_id': 'orders_480d'})

    # Frequency Joined to base dataset
    base = base.merge(f_30,on='user_id',how='left')
    base = base.merge(f_60,on='user_id',how='left')
    base = base.merge(f_120,on='user_id',how='left')
    base = base.merge(f_240,on='user_id',how='left')
    base = base.merge(f_480,on='user_id',how='left')

    # orders per different timeframe
    m_30 = df_30[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_30d'})
    m_60 = df_60[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_60d'})
    m_120 = df_120[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_120d'})
    m_240 = df_240[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_240d'})
    m_480 = df_480[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_480d'})
    m_total = orders_df[['user_id','sale_price']].groupby(by='user_id').sum().fillna(0).rename(columns={'sale_price': 'revenue_total'})

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

    # Fill NA with 0 for selected columns
    selected_columns = ['orders_total',
              'orders_30d',
              'orders_60d',
              'orders_120d',
              'orders_240d',
              'orders_480d',
              'revenue_30d',
              'revenue_60d',
              'revenue_120d',
              'revenue_240d',
              'revenue_480d']

    base[selected_columns] = base[selected_columns].fillna(0)

    return base

def join_tables_item_level(order_items_df, products_df):
    '''
    Joins order-item & product
    '''
    order_items_df = order_items_df[['id',
                                     'order_id',
                                     'user_id',
                                     'product_id',
                                     'inventory_item_id',
                                     # 'status',
                                     'created_at',
                                     # 'shipped_at',
                                     # 'delivered_at',
                                     # 'returned_at',
                                     'sale_price']].rename(columns={'id':'order_item_id'})

    order_items_df['created_at'] = pd.to_datetime(order_items_df['created_at'],
                                                       format='mixed').dt.tz_localize(None)
    products_df = products_df[['id',
                               'cost',
                               'category',
                               'name',
                               'brand',
                               'retail_price',
                               # 'department',
                               # 'sku',
                               'distribution_center_id']]


    df_joined = order_items_df.merge(products_df, left_on='product_id', right_on='id', how='left')
    df_joined = df_joined.drop(columns=['id']) # duplicate product id

    return df_joined

def calc_product_features(item_level_df, split_date):
    '''
    takes item-level dataframe and calculate features to user level.
    '''

    # filter data only for last 2 years
    min_date = split_date - pd.DateOffset(days=365*3)
    item_level_df = item_level_df[(item_level_df['created_at'] <= split_date) & (item_level_df['created_at'] > min_date)].copy()

    # Calculate the first orders
    item_level_df['order_rank'] = item_level_df.groupby('user_id')['created_at'].rank().astype(int) # calculating the order of orders
    item_level_df['order_rank_desc'] = item_level_df.groupby('user_id')['created_at'].rank(method='max').astype(int) # calculating the order of orders

    base = item_level_df[['user_id','order_item_id']].groupby('user_id').count().fillna(0).rename(columns={'order_item_id':'num_order_item'})

    # # taking value for the very first order
    # intial_values = item_level_df[item_level_df['order_rank']==1][['user_id','category','brand']].rename(columns={'category':'categ_initial',
    #                                                                                                               'brand':'brand_initial'})
    # base = base.merge(intial_values, on='user_id', how='left')

    # # taking value for the very last order
    # last_values = item_level_df[item_level_df['order_rank_desc']==1][['user_id','category','brand']].rename(columns={'category':'categ_last',
    #                                                                                                               'brand':'brand_last'})
    # base = base.merge(last_values, on='user_id', how='left')

    # item_level_df = item_level_df.rename(columns={'created_at':'order_item_created_at'})

    # Most frequent brand
    count_brands = item_level_df.groupby(['user_id', 'brand']).size().reset_index(name='count')
    idx = count_brands.groupby(['user_id'])['count'].transform('max') == count_brands['count']
    preffered_brand = count_brands[idx].drop(columns='count').rename(columns={'brand':'brand_preffered'})

    base = base.merge(preffered_brand, on='user_id', how='left')

    # Most frequent category
    count_cat = item_level_df.groupby(['user_id', 'category']).size().reset_index(name='count')
    idx = count_cat.groupby(['user_id'])['count'].transform('max') == count_cat['count']
    preffered_cat = count_cat[idx].drop(columns='count').rename(columns={'category':'category_preffered'})

    base = base.merge(preffered_cat, on='user_id', how='left')

    return base

def select_user_columns(users_df, split_date):

    df = users_df[['id','age','country','created_at']].rename(columns={'id':'user_id','created_at':'user_created_at'})
    # Filter users only for last 2 years from split date
    # min_date = split_date - pd.DateOffset(days=365*5)
    df['user_created_at'] = pd.to_datetime(df['user_created_at'], format='mixed').dt.tz_localize(None)
    df = df[(df['user_created_at'] <= split_date)]

    return df

def create_y_actual(order_items_df, split_date):
    df = order_items_df[['id','user_id','created_at','sale_price']].copy().rename(columns={'id':'order_item_id'})
    df['order_created_at'] = pd.to_datetime(df['created_at'], format='mixed').dt.tz_localize(None)

    # select next 90 days of revenue from split_date
    max_date = split_date + pd.DateOffset(days=90)
    df = df[(df['order_created_at'] <= max_date) & (df['order_created_at'] > split_date)]

    df_agg = df[['user_id','sale_price']].groupby('user_id').sum().fillna(0).rename(columns={'sale_price':'revenue_next_90d'})

    return df_agg


def prep_input_dataset(df_user, df_order, df_item, df_y_actual):
    '''
    joins all preprocessed user-level-df
    '''

    final_df = df_user.merge(df_order, on='user_id', how='left')
    final_df = final_df.merge(df_item, on='user_id', how='left')
    final_df = final_df.merge(df_y_actual, on='user_id', how='left')

    final_df = final_df[final_df['orders_total']>0].copy()

    final_df = final_df.reset_index()

    return final_df
