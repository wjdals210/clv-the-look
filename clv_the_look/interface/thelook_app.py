import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
#from preprocess.preprocessor import preprocess_data  # Import preprocessing function
#from training import predict_clv  # Import predict_clv function
#from training.model import load_model  # Import load_model function

def main():
    st.markdown("<h1 style='text-align: center; color: white;'>TheLook eCommerce Dataset Explorer </h1>", unsafe_allow_html=True)
    #st.title("TheLook eCommerce Dataset Explorer")

    # File upload section
    st.sidebar.header("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    # Check if file is uploaded
    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded data:")
        st.write(df)

        url = 'https://clvimage-k2idjtgthq-oe.a.run.app/predict'
        df_new = df.to_json().encode()
        response = requests.post(url, files={'file' : df_new})

        # Display predictions
        st.write("Predictions:")
        st.write(response.json())

        # Plot CLV distribution
        st.write("CLV Distribution Plot:")
        plot_clv_distribution(predictions)

    # When no file is uploaded
    else:
        st.write("Please upload a CSV file.")

def plot_clv_distribution(predictions):
    # Generate fake data for plotting
    np.random.seed(0)
    data = np.random.normal(1000, 200, 1000)


    # Plot CLV distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(predictions['Predicted CLV'], kde=True)
    plt.xlabel('Predicted CLV')
    plt.ylabel('Frequency')
    plt.title('Distribution of Predicted CLV')
    st.pyplot()

if __name__ == "__main__":
    main()
