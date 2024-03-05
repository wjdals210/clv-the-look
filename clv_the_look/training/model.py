from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

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
