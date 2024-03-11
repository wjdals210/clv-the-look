<<<<<<< HEAD
import pandas as pd
from sklearn.pipeline import make_pipeline, make_union
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.preprocessing import RobustScaler
from sklearn.compose import make_column_selector

def pipeline_scaler(X):
    num_transformer = make_pipeline(RobustScaler())
    num_col = make_column_selector(dtype_include=['float64'])

    preproc_basic = make_column_transformer(
        (num_transformer, num_col),
        # (cat_transformer, cat_col),
        remainder='passthrough'
    )

    preproc_full = make_union(preproc_basic)
    return pd.DataFrame(preproc_full.fit_transform(X),
                        columns=[i.replace('columntransformer__pipeline__','').replace('columntransformer__remainder__','')
                                 for i in preproc_full.get_feature_names_out()]
            )
=======
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
>>>>>>> 27c11883a4b47a0be90d2ce419f7dbe303a39534
