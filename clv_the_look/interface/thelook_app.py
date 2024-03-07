import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

# import plotly.express as px  #interactive charts

currentfile = os.path.abspath(__file__)
currentdir = os.path.dirname(currentfile)

eventsfile = os.path.join(currentdir, "..", "..", "raw_data", "events.csv")
d_centersfile =os.path.join(currentdir, "..", "..", "raw_data", "distribution_centers.csv")
inventoryfile=os.path.join(currentdir, "..", "..", "raw_data", "inventory_items.csv")
order_itemsfile=os.path.join(currentdir, "..", "..", "raw_data", "order_items.csv")
ordersfile=os.path.join(currentdir, "..", "..", "raw_data", "orders.csv")
usersfile=os.path.join(currentdir, "..", "..", "raw_data", "users.csv")
productsfile=os.path.join(currentdir, "..", "..", "raw_data", "products.csv")

# Load the dataset
@st.cache_resource
def load_data():
     data = {

         "Events":pd.read_csv(eventsfile),
         "Inventory_items": pd.read_csv(inventoryfile),
         "Order_items": pd.read_csv(order_itemsfile),
         "D_centers": pd.read_csv(d_centersfile),
         "Orders": pd.read_csv(ordersfile),
         "Users": pd.read_csv(usersfile),
         "Products": pd.read_csv(productsfile)
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
    st.markdown("<h1 style='text-align: center; color: white;'>TheLook eCommerce Dataset Explorer </h1>", unsafe_allow_html=True)
    #st.title("TheLook eCommerce Dataset Explorer")

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





#create your figure and get the figure object returned
#fig = plt.figure(figsize=(8, 6))

fig = plt.figure(figsize=(8, 6))

plt.plot([1, 2, 3, 4, 5])

st.pyplot(fig)
