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
