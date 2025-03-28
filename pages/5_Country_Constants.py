from st_aggrid import AgGrid
import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Tells streamlit that all of your session state values 
# have been set manually, so they should be persisted even if 
# you change pages. ADD TO EVERY PAGE
for k, v in st.session_state.items():
    st.session_state[k] = v

# Website header
st.set_page_config(
    page_title="XIPE model",
    page_icon="⚡", 
)
#CNL Logo and HTML sclaing
st.logo("images/cenexNL_logo.png", size="large")
st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)


##################################################################################
####################### COUNTRY CONSTANTS ########################################
###################################################################################

# use csv read in introduction to make table
# For loop setting number format for the table
column_names = ss.car_co2.columns

col_format = {}
for name in column_names:
    col_format.update({name : st.column_config.NumberColumn(format="%.1f")})
col_format.update({"Year" : st.column_config.NumberColumn(format = "%d")})


# display dataframe in app
st.subheader('Average CO2 emissions per km from new passenger cars \n Source: EuroStat')
st.write("""Up to 2020 the NEDC measuring method was used, which was replaced by the WLTP from 2021 onwards. NEDC and WLTP values 
         underestimate real world CO2 emission by resepectively 40% and 14%. These factors are included to calculate the average 
         Tank-to-Wheel values for ICE cars.""")
car_co2_country_edited = st.dataframe(ss.car_co2,
                           column_config=col_format,
                           hide_index=True,
)

# display dataframe
st.subheader('2023 GHG emission intensity of electricity production (gCO2e/kWh)  \n Source: EEA')

st.dataframe(ss.elec_co2_country,
             hide_index=True)

