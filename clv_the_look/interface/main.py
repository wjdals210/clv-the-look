import pandas as pd
from clv_the_look.preprocess.data import *
from clv_the_look.training.model import *
from clv_the_look.training.registry import *

# call the load_models function which loads the two pickled models, required for the baseline:
# beta-geo model and gamma-gamma model
rf_pipeline = load_rf_model()

##################  TEST WITH A NEW USER  ##################

new_user = pd.read_csv('/Users/Ian/Downloads/input_X_test.csv').iloc[6:7,:]
print(new_user)
print(rf_pipeline.predict(new_user))

############################################################

# new_user = pd.DataFrame(columns=['sale_price', 'user_id', 'created_at'])
# new_user.loc[0] = {'sale_price':45,'user_id':'X','created_at':'2020-08-30 08:26:00'}
# new_user.loc[1] = {'sale_price':70,'user_id':'X','created_at':'2020-09-07 08:26:00'}
# new_user_rfm = rfm(new_user)

############################################################

# new_CLV = trained_gg_model.customer_lifetime_value(trained_bg_model,
#                                                    new_user_rfm['frequency'],
#                                                    new_user_rfm['recency'],
#                                                    new_user_rfm['T'],
#                                                    new_user_rfm['monetary_value'],
#                                                    time = 3,# In months
#                                                    )

# print(f"\nEstimated value of this user in the next three months is {round(new_CLV[0],2)}\n")

############################################################
