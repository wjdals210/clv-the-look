# Import libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="THE LOOK",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded")

def main():
    st.markdown("<h1 style='text-align: center;'> 📈The LooK</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>  We Know about you 👁️</h2>", unsafe_allow_html=True)

    #st.empty()  # Add an empty element to create space
    st.markdown("<br>", unsafe_allow_html=True)


    # Add content
    st.write("Welcome to The Look's Analytics page!")

    st.markdown("<br>", unsafe_allow_html=True)


    st.write("At The Look, we specialize in predictive analytics to help our business to understand our customers better.")

    st.markdown("<p style='text-align: center; font-size: 36px;'>👁️</p>", unsafe_allow_html=True)



    st.write("Our service focuses on predicting two key aspects:")

    st.markdown("- **Customer Retention**: We analyze customer data to predict whether a new customer will stay.")
    st.markdown("- **Future Purchase Impact**: We assess the potential impact of a customer's future purchases.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Using advanced machine learning algorithms and data analysis techniques, we provide actionable insights to optimize marketing strategies and enhance customer satisfaction.")
    st.write("🔔🔔 Stay tuned for our upcoming presentation 🔔🔔")

  # Define the data
    countries = ['China', 'United States', 'Brasil']
    customer_numbers = [15653, 10276, 6719]

    # Create a DataFrame
    df = pd.DataFrame({'Country': countries, 'Customer Numbers': customer_numbers})

    # Create a bar plot using Plotly Express
    fig = px.bar(df, x='Country', y='Customer', title='Top 3 Countries by Customer')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
