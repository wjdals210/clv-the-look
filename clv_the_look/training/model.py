import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import calibration_and_holdout_data

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

def train_bg_model(cleaned_separated_rfm_df):
    '''
    Function to fit the Beta-Geometric model on the cleaned, calibration/holdout dataset
    (which has been converted to rfm)
    '''

    pen_coef_ = 0.001
    bg_model = BetaGeoFitter(penalizer_coef=pen_coef_)
    bg_model.fit(cleaned_separated_rfm_df['frequency_cal'],
                 cleaned_separated_rfm_df['recency_cal'],
                 cleaned_separated_rfm_df['T_cal'])

    print("✅ ß-Geo Model trained")

    return bg_model

def train_gg_model(filtered_rfm_df):
    '''
    Function to fit the gamma-gamma model to the calibration/holdout dataset (with zeros removed)
    '''

    gg_model = GammaGammaFitter()
    gg_model.fit(filtered_rfm_df['frequency_cal'], filtered_rfm_df['monetary_value_cal'])

    print("✅ γγ Model trained")

    return gg_model
