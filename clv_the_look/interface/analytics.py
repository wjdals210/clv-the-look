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

    st.markdown("- **Customer Retention**: We analyze customer data to predict whether a new customer will stay with your business.")
    st.markdown("- **Future Purchase Impact**: We assess the potential impact of a customer's future purchases on your business.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Using advanced machine learning algorithms and data analysis techniques, we provide actionable insights to optimize your marketing strategies and enhance customer satisfaction.")
    st.write("🔔🔔 Stay tuned for our upcoming presentation, where we'll delve deeper into our predictive analytics solutions and showcase how they can benefit your business! 🔔🔔")

    # Load sample data (replace this with your actual data)
    money = {
         'Month': ['1', '2', '3', '4', '5'],
         'Retention Rate': [30, 40, 90, 88, 100]
    }
    df = pd.DataFrame(money)

     # Create a bar chart using Plotly
    fig = px.bar(df, x='Month', y='Retention Rate', title='Customer Retention Rate Over Time',
                  labels={'Retention Rate': 'Retention Rate (%)', 'Month': 'Month'})

     # Customize layout
    fig.update_layout(xaxis=dict(title='Time'),
                       yaxis=dict(title='Retention Rate (%)'),
                       plot_bgcolor='rgba(0,0,0,0)')

#     # Display the bar chart
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
