from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

def train_model(cleaned_rfm_train_df):
    '''
    Function to fit the Beta-Geometric model on the cleaned, training dataset (which has been converted to rfm)
    '''
    pen_coef_ = 0.001
    model = BetaGeoFitter(penalizer_coef=pen_coef_)
    model.fit(cleaned_rfm_train_df['frequency_cal'],
              cleaned_rfm_train_df['recency_cal'],
              cleaned_rfm_train_df['T_cal'])
    print("✅ ß-Geo Model trained")
    return model

def train_ggmodel(filtered_rfm_df):
    gg_model = GammaGammaFitter()
    gg_model.fit(filtered_rfm_df['frequency'], filtered_rfm_df['monetary_value'])
    print("✅ γγ Model trained")
    return gg_model
