from fastapi import FastAPI
from fastapi import UploadFile, File
import json
import pandas as pd
from clv_the_look.training.registry import *
from clv_the_look.preprocess.data import *

app = FastAPI()

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello - retesting the local")
    # $CHA_END

@app.post('/predict')
def upload_file(file: UploadFile = File(...)):
    contents = file.file.read() # Reading content of 'myfile' in bytes
    # print(contents)
    decoded_str = contents.decode('utf-8') # Decoding contents into str type
    # decoded_str = StringIO(contents.decode('utf-8')) # Alternative using StringIO
    df_json = json.loads(decoded_str) # Reading string and converting to json (dictionary)
    df = pd.DataFrame(df_json) # Reading dictionary and converting into dataframe
    bg_model, gg_model = load_models()
    df_rfm = rfm(df)

    new_CLV = gg_model.customer_lifetime_value(bg_model,
                                                   df_rfm['frequency'],
                                                   df_rfm['recency'],
                                                   df_rfm['T'],
                                                   df_rfm['monetary_value'],
                                                   time = 3,# In months
                                                   )
    prediction = float(new_CLV.iloc[0])
    results = {
        'Prediction' : round(prediction, 2)
        }
    return results

@app.post('/gbpredict')
def upload_file(file: UploadFile = File(...)):
    contents = file.file.read() # Reading content of 'myfile' in bytes
    decoded_str = contents.decode('utf-8') # Decoding contents into str type
    # decoded_str = StringIO(contents.decode('utf-8')) # Alternative using StringIO
    df_json = json.loads(decoded_str) # Reading string and converting to json (dictionary)
    df = pd.DataFrame(df_json) # Reading dictionary and converting into dataframe
    rf_pipeline = load_rf_model()
    prediction = rf_pipeline.predict(df)

    if prediction[0] == 0:
        outcome = "This customer will not purchase with us again"
    elif prediction[0] == 1:
        outcome = "This customer should purchase with us again"

    results = {
        'Prediction' : outcome
        }
    return results
