from lifetimes.utils import calibration_and_holdout_data

def cal_hold_separation(clean_df):
    '''
    A function to separate the time dataframe into calibration and holdout (train and test) datasets
    '''
    time_diff = clean_df['created_at'].max() - \
                clean_df['created_at'].min()  # work out how many days range in the dataset
    train_test_ratio = 0.25  # choose the fraction to use as test

    # work out the last date for the train dataset (the date to split the data)
    train_date_end = clean_df['created_at'].min() + \
                     time_diff * (1-train_test_ratio)

    # use the calibration_and_holdout_data method in lifetimes package to separate the time series data
    separated_df = calibration_and_holdout_data(transactions=clean_df,
                                                customer_id_col="user_id",
                                                datetime_col = "created_at",
                                                monetary_value_col= 'sale_price',
                                                calibration_period_end=train_date_end,
                                                observation_period_end=clean_df.created_at.max())

    return separated_df
