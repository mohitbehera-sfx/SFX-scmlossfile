import streamlit as st
import pandas as pd
import re

st.title("HOV & High Ageing Shipment Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def extract_days(val):
        match = re.search(r'\d+', str(val))
        return int(match.group()) if match else 0

    df['age_days'] = df['ageing_from_received'].apply(extract_days)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    hov = df[df['Price'] >= 1000]
    high_age = df[df['age_days'] >= 10]

    st.subheader("HOV Shipments")
    st.dataframe(hov[['AM','current_hub','awb_number','Price','order_status','age_days']])

    st.subheader("High Ageing Shipments")
    st.dataframe(high_age[['AM','current_hub','awb_number','Price','order_status','age_days']])

    st.subheader("AM Wise Summary")
    st.dataframe(hov.groupby(['AM','current_hub']).size().reset_index(name='count'))
