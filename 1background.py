import streamlit as st
import pandas as pd

country_constants = pd.read_csv("data/co2_emissions_new_cars_EU.csv")

"""
# Session State of country list to be used in multiple pages
country_list = country_constants.columns.tolist()[1:]

if "country_list" not in st.session_state:
    st.session_state["country_list"] = []

st.write(st.session_state["country_list"])

st.session_state["country_list"]
"""