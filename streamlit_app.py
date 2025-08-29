# streamlit_app.py
import wbdata as wb
import pandas as pd
import datetime as dt
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="World Bank Explorer", layout="wide")

st.title("World Bank Data Explorer (wbdata + Streamlit)")

countries = st.multiselect("Countries (ISO3)", ["USA","GBR","DEU","IND","CHN","BRA","ZAF"], default=["USA","GBR","IND"])
indicator_code = st.text_input("Indicator code", "NY.GDP.PCAP.CD")
start_year, end_year = st.slider("Year range", 1990, dt.datetime.today().year, (2000, dt.datetime.today().year))

if st.button("Load data"):
    indicator = {indicator_code: "value"}
    df_raw = wb.get_dataframe(indicator, country=countries, data_date=(dt.datetime(start_year,1,1), dt.datetime(end_year,12,31)), convert_date=True)
    df = df_raw.reset_index().rename(columns={"country":"country","date":"date"}).sort_values(["country","date"])
    st.dataframe(df.head())
    if not df.empty:
        fig = px.line(df, x="date", y="value", color="country", title=f"{indicator_code}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Choose your options and click **Load data**.")
