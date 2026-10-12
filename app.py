import pandas as pd
import streamlit as st
@st.cache_data
def load_data():
    return pd.read_csv("data/risks.csv")

#Page config
st.set_page_config(
    page_title="Clinical Study Strategy & Scenario Simulator",
    layout="wide"
)

st.title("Clinical Study Strategy & Scenario Simulator")
st.caption("Explore site selection strategies and their trade-offs using synthetic clinical trial data")

data = load_data()
st.write("Total sites available:", len(data))