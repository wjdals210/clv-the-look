from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

def train_bgmodel(cleaned_rfm_train_df):
    '''
    Function to fit the Beta-Geometric model on the cleaned, training dataset (which has been converted to rfm)
    '''
    pen_coef_ = 0.001
    bg_model = BetaGeoFitter(penalizer_coef=pen_coef_)
    bg_model.fit(cleaned_rfm_train_df['frequency_cal'],
              cleaned_rfm_train_df['recency_cal'],
              cleaned_rfm_train_df['T_cal'])
    print("✅ ß-Geo Model trained")
    return bg_model

def train_ggmodel(filtered_rfm_df):
    gg_model = GammaGammaFitter()
    gg_model.fit(filtered_rfm_df['frequency'], filtered_rfm_df['monetary_value'])
    print("✅ γγ Model trained")
    return gg_model

def clv(gg_model,bg_model,rfm_df):
    '''
    Function to output the 'customer lifetime value' for the next 3 months given an input rfm dataframe
    '''
    gg_model.customer_lifetime_value(bg_model,
                                    rfm_df['frequency'],
                                    rfm_df['recency'],
                                    rfm_df['T'],
                                    rfm_df['monetary_value'],
                                    time = 3,# In months
                                    )
