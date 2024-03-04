from lifetimes import BetaGeoFitter

def train_model(cleaned_rfm_train_df):
    '''
    Function to fit the Beta-Geometric model on the cleaned, training dataset (which has been converted to rfm)
    '''
    pen_coef_ = 0.001
    model = BetaGeoFitter(penalizer_coef=pen_coef_)
    model.fit(cleaned_rfm_train_df['frequency_train'],
              cleaned_rfm_train_df['recency_train'],
              cleaned_rfm_train_df['T_train'])
    print("✅ Model initialized")
    return model
