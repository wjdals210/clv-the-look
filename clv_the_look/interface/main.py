import pandas as pd
from lifetimes.utils import calibration_and_holdout_data
from data import *
from model import *

def cal_hold_separation(clean_df):
    '''
    A function to separate the time dataframe into calibration and holdout (train and test) datasets
    '''

    # Define the calibration and holdout ranges
    cal_start = pd.to_datetime('2019-01-01')
    cal_end = pd.to_datetime('2020-12-31')
    hold_end = pd.to_datetime('2021-03-31')

    # get the subset of the data, restricted by calibration period plus holdout period
    clean_df_subset = clean_df[(clean_df.created_at>=cal_start) & (clean_df.created_at<=hold_end)]

    # use the calibration_and_holdout_data method in lifetimes package to separate the time series data
    separated_df = calibration_and_holdout_data(transactions=clean_df_subset,
                                                customer_id_col="user_id",
                                                datetime_col = "created_at",
                                                monetary_value_col= 'sale_price',
                                                calibration_period_end=cal_end,
                                                observation_period_end=hold_end)

    return separated_df


def clv(gg_model,bg_model,rfm_df):
    '''
    Function to output the 'customer lifetime value' for the next 3 months given:
    an input rfm dataframe;
    a gamma-gamma model; and
    a beta-geo model
    '''
    gg_model.customer_lifetime_value(bg_model,
                                     rfm_df['frequency'],
                                     rfm_df['recency'],
                                     rfm_df['T'],
                                     rfm_df['monetary_value'],
                                     time = 3,# In months
                                     )
