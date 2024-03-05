import streamlit as st
import pandas as pd
# import plotly.express as px  #interactive charts


# Load the dataset
#@st.cache
@st.cache_resource
#@st.cache_data(ttl=3600) #Streamlit invalidates any cached values after 1 hour

def load_data():
     data = {

         "Events": pd.read_csv(r'/home/datascience/code/wjdals210/clv-the-look/raw_data/events.csv'),
         "Inventory_items": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/inventory_items.csv"),
         "Order_items": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/order_items.csv"),
         "D_centers": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/distribution_centers.csv"),
         "Orders": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/orders.csv"),
         "Users": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/users.csv"),
         "Products": pd.read_csv(r"/home/datascience/code/wjdals210/clv-the-look/raw_data/products.csv")
     }
     return data

 # Display the data
def display_data(data, table_name, columns, filter_column, filter_value):
    df = data[table_name]

     # Filter data
    if filter_column and filter_value:
        df = df[df[filter_column] == filter_value]

     # Select columns
    if columns:
        df = df[columns]
    # Display first few rows of the DataFrame
    st.write(f"First few rows of {table_name}:")
    st.write(df.head())

def main():
    st.title("TheLook eCommerce Dataset Explorer")

     # Load data
    data = load_data()
     # Sidebar - Table selection
    table_name = st.sidebar.selectbox("Select Table", list(data.keys()))

     # Sidebar - Column selection
    columns = st.sidebar.multiselect("Select Columns", data[table_name].columns)
#     # Sidebar - Filter
    filter_column = st.sidebar.selectbox("Filter Column (Optional)", data[table_name].columns.insert(0, ""))
    filter_value = st.sidebar.text_input("Filter Value")
#     # Display data
    if st.sidebar.button("Refresh Data"):
        data = load_data()  # Reload data
    display_data(data, table_name, columns, filter_column or None, filter_value or None)
if __name__ == "__main__":
    main()
