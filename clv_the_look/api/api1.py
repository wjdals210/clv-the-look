from fastapi import FastAPI
from fastapi import UploadFile, File
from pathlib import Path
import json
import pandas as pd
from clv_the_look.training.registry import *
from clv_the_look.preprocess.data import *

app = FastAPI()



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


# preproces
# load model
# predict

# @app.get("/predict_again")
# async def read_csv():
    # Path to your CSV file
    csv_file = "orders.csv"

    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert DataFrame to JSON format
    data = df.to_json(orient="records")

    return {"data": data}

# @app.post("/users/")
# async def create_user(name: str, email: str):
    # Create a new user in the database with the provided name and email
    # Return the newly created user information
    return {"name": name, "email": email}
