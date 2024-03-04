from lifetimes import BetaGeoFitter

def train_model(cleaned_df_rfm_train):
    '''
    Function to fit the Beta-Geometric model using the training dataset which has been converted to rfm
    '''
    pen_coef_ = 0.001
    model = BetaGeoFitter(penalizer_coef=pen_coef_)
    model.fit(cleaned_df_rfm_train['frequency'],
            cleaned_df_rfm_train['recency'],
            cleaned_df_rfm_train['T'])
    print("✅ Model initialized")
    return model
