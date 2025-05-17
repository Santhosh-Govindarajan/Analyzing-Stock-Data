import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

# Function to connect to MySQL database
@st.cache_resource
def get_connection():
    engine = create_engine(
        "mysql+mysqlconnector://31byymmafmh6WEp.root:KU0Fz7gGZcxq5XwF"
        "@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/stocks"
    )
    return engine

# Load data from a given table
@st.cache_data
def load_data(table_name):
    engine = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    return df


with st.sidebar:
    st.image("E:\MiniProject\SYMBOL.jpeg",width=300)


# with col1:#--------------------------------> Put the IMDb badge in the top-left corner of the first column
st.markdown("""
        <div style='
        display: inline-block;
        background-color: #96f222;
        color: Black;
        font-weight: bold;
        font-size: 35px;
        padding: 6px 16px;
        border-radius: 3px;
        font-family: Arial, sans-serif;
        '>
         STOCK ANALYSIS
        </div>
    """, unsafe_allow_html=True)   

# Sidebar for selecting visualization
option = st.sidebar.selectbox(
    "Choose a visualization",
    (
        "Top 10 Green Stocks",
        "Top 10 Loss Stocks",
        "Market Status Pie Chart",
        "Volatility Summary",
        "Cumulative Returns of Top 5",
        "Sector-wise Average Return",
        "Stock Correlation Heatmap",
        "Monthly Top Gainers & Losers"
    )
)

# Visualization logic
if option == "Top 10 Green Stocks":
    df = load_data("top_10_green")
    st.subheader("Top 10 Green Stocks")
    fig = px.bar(df, x='Ticker', y='Overall Return (%)', color='Ticker', title="Top 10 Green Stocks")
    st.plotly_chart(fig, use_container_width=True)
    
elif option == "Top 10 Loss Stocks":
    df = load_data("top_10_loss")
    st.subheader("Top 10 Loss Stocks")
    fig = px.bar(df, x='Ticker', y='Overall Return (%)', color='Ticker', title="Top 10 Loss Stocks", color_discrete_sequence=["red"])
    st.plotly_chart(fig, use_container_width=True)

elif option == "Market Status Pie Chart":
    df = load_data("stock_status")
    st.subheader("Market Status Overview")
    fig = px.pie(df, names='Status', values='Count', title='Market Status: Green vs Red vs No Change')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Sector-wise Average Return":
    df = load_data("sector_returns")
    st.subheader("Sector-wise Average Return")
    fig = px.bar(df, x='sector', y='Overall Return (%)', color='sector', title='Sector Average Return')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Cumulative Returns of Top 5":
    df = load_data("top5_cumulative")
    st.subheader("Cumulative Returns of Top 5 Stocks")
    fig = px.line(df, x='date', y='cumulative_return', color='Ticker', title='Cumulative Returns Over Time')
    st.plotly_chart(fig, use_container_width=True)


elif option == "Volatility Summary":
    df = load_data("volatility_summary")
    st.subheader("Volatility Summary")
    fig = px.bar(df, x='Ticker', y='volatility', title='Volatility of Stocks')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Stock Correlation Heatmap":
    df = load_data("correlation_matrix")
    st.subheader("Stock Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(df.set_index(df.columns[0]), cmap='coolwarm', annot=False, linewidths=0.5)
    st.pyplot(fig)

elif option == "Monthly Top Gainers & Losers":
    df = load_data("monthly_movers")
    st.subheader("Monthly Top Gainers & Losers")
    selected_month = st.selectbox("Select Month", df['Month'].unique())
    month_df = df[df['Month'] == selected_month]
    fig = px.bar(month_df, x='Ticker', y='Monthly Return (%)', color='Type',
                 title=f"Top Movers for {selected_month}", orientation='v',
                 color_discrete_map={'Top Gainers': 'green', 'Top Losers': 'red'})
    st.plotly_chart(fig, use_container_width=True)


