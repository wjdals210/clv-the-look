import numpy as np
import pandas as pd


#from sklearn.pipeline import make_pipeline
#from sklearn.compose import ColumnTransformer, make_column_transformer
#from sklearn.preprocessing import OneHotEncoder, FunctionTransformer

from data import data_cleaning, select_user_columns, order_features, create_y_actual

def preprocess_data(order_items_df, orders_df, users_df, split_date):

# This function performs data cleaning, feature engineering, and selection of user columns

    # Clean the data
    cleaned_data = data_cleaning(order_items_df, orders_df)

    # Select user columns
    selected_users = select_user_columns(users_df, split_date)

    # Create target variable (actual next 90 days revenue)
    y_actual = create_y_actual(order_items_df, split_date)

    # Calculate order features
    order_feats = order_features(cleaned_data, order_items_df, split_date)

    return selected_users, order_feats, y_actual
