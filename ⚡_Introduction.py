import streamlit as st
import pandas as pd
import streamlit as st
from streamlit import session_state as ss

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

#Sidebar title and text
#st.sidebar.header("Introduction")
#st.sidebar.write("")

#Title and text main body
st.title("The Cross Impact Performance Emissions (XIPE) model for shared mobility")
st.write(
    """The XIPE model was developed by Cenex Nederland as part of the GEMINI project and 
    estimates the effect shared mobility has on CO2 and air pollution emissions in a city 
    or region. It aims to be easy to use while also being flexible and customisable to reflect 
    real world situations or different scenarios. This is achieved by making all default 
    variables, which are prefilled from literature and previous research, adjustable by the user."""
)

#GEMINI and EU logo after text of screen
st.image("images/GEMINI_BANNER2.png",use_column_width="auto")

st.write("Version: beta")
st.write("Published: 2025")


# Load country specific data from csv's
car_co2 = pd.read_csv("data/co2_emissions_new_cars_EU.csv")
car_acea = pd.read_csv("data/acea_vehicle_data.csv")
car_air_emission = pd.read_csv("data/air_emission_limits.csv")

if "car_co2" not in ss:
    ss.car_co2 = car_co2

if "car_acea" not in ss:
    ss.car_acea = car_acea

if "car_air_emission" not in ss:
    ss.car_air_emission = car_air_emission

#####################################################################################################################################################################
###### initialise general session states ###########################################################################################################################
#####################################################################################################################################################################


# Create list of all EU countries and manufacturing years from data list and save 
# as session state to be able access it in all pages
country_list = car_co2.columns.tolist()[1:-1]
year_list = car_co2[car_co2.columns[0]]

if "country_list" not in ss:
    ss["country_list"] = country_list

if "year_list" not in ss:
    ss["year_list"] = year_list
    

### electricity emissions per country
# Electricty emission intensity electricity production taken from EEA, same order as country list
elec_co2 = [96, 145, 422, 133, 589, 400, 103, 658, 66, 68, 366, 416, 180, 310, 252, 86, 180, 52, 347, 321, 666, 173, 247, 115, 208, 205, 7, 251]

# create dataframe from values and transpose to have countries as column headers
df_elec_co2_country = pd.DataFrame.from_dict(dict(zip(ss.country_list, elec_co2)), orient='index')
df_elec_co2_country = df_elec_co2_country.T

if "elec_co2_country" not in ss:
    ss.elec_co2_country = df_elec_co2_country

# create variable lists
if "lst_var_dash" not in ss:
    ss.lst_var_dash = ["country", "city_name", "inhabitants", "car_year", "diesel_perc"
                       ]

if "lst_var_nms" not in ss:
    ss.lst_var_nms = ["Average number of trips per day", "Average Tank-to-Wheel CO2 emissions (g/km)","Average NOx emissions (mg/km)",
                      "Average PM emissions (mg/km)",  "Average efficiency of the electric vehicle (kWh/km)", "Emission factor for life-cycle phases excluding use phase (gCO2/km)", 
                      "Replaces private car by (%)", "Replaces PT road by (%)", "Replaces PT rail by (%)", "Replaces cycling by (%)", "Replaces walking by (%)", 
                      "Average trip distance of the shared mode when replacing car (km)", "Average trip distance of the shared mode when replacing PT road (km)", "Average trip distance of the shared mode when replacing PT rail (km)", 
                      "Average trip distance of the shared mode when replacing cycling (km)", "Average trip distance of the shared mode when replacing walking (km)"
                      ]

if "lst_var_trad" not in ss:
    ss.lst_var_trad = ["CO2 emission factors Tank-to-Wheel (gr/km)", "Average NOx emissions (mg/km)", "Average PM emissions (mg/km)",
                       "Average efficiency of public transport rail (kWh/km)", "Emission factor for life-cycle phases excluding use phase (gCO2/km)"
                       ]

if "lst_var_act" not in ss:
    ss.lst_var_act = ["Cycling, emission factor for life-cycle phases excluding use phase (gCO2/km)", "Walking, emission factor for life-cycle phases excluding use phase (gCO2/km"]

if "var_nms_types" not in ss:
    ss.var_nms_types = ["var_nms_ICEcar", "var_nms_ICEmoped", "var_nms_bike", "var_nms_ev", "var_nms_ebike", "var_nms_emoped", "var_nms_escooter", "var_nms_other", "var_nms_eother"
                        ]

if "trad_types" not in ss:
    ss.trad_types = ["private_car", "pt_road", "pt_rail", "cycling", "walking"]

if "nms_types" not in ss:
    ss.nms_types = ["Car", "Bike", "Moped", "e-Scooter", "Other"]

### session states for dashboard inputs
# country
if "country" not in ss:
    ss.country = country_list[0]

# number of inhabitants, minimum is 1 to prevent devision by zero
if "inhabitants" not in ss:
    ss.inhabitants = 1

# average car year of the fleet, default is Austria as it is the default country
if "car_year" not in ss:
    ss.car_year = 2015

#percentage of the fleet that is diesel
#if "diesel_perc" not in ss:
#    ss.diesel_perc = 0

# General Variables DataDrame
if 'var_general' not in ss:
    ss.var_general = pd.DataFrame({
        "variable": ["Average CO2 emission intensity for electricity generation (gCO2/kWh)", "Well-to-Tank emissions fraction of Well-to-Wheel emissions ICE cars (%)", "Average age of the car fleet (years)", "Percentage of petrol cars in the current fleet (%)","Percentage of diesel cars in the current fleet (%)", "Percentage of electric cars in the current fleet (%)"],
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [96.0, 20.0, 9.3, 42.2, 49.9, 7.8]
    })
    ss.var_general_edited = ss.var_general.copy()

#####################################################################################################################################################################
###### initialise Trad session states ###########################################################################################################################
#####################################################################################################################################################################

if 'var_private_car' not in ss:
    ss.var_private_car = pd.DataFrame({
        "variable": ss.lst_var_trad[0:3] + ss.lst_var_trad[4:], #linked to variable list
        "user_input": [0.0, 0.0, 0.0, 0.0],
        "default": [118.6, 69.00, 4.5, 55.00]
    })
    ss.var_private_car_edited = ss.var_private_car.copy()

# Public Transport Variables Road & Rail
# Public Transport Variables Road
if 'var_road' not in ss:
    ss.var_road = pd.DataFrame({
        "variable": ss.lst_var_trad[0:3] + ss.lst_var_trad[4:], #linked to variable list
        "user_input": [0.0, 0.0, 0.0, 0.0],
        "default": [63.00, 30.67, 0.67, 20.00]
    })
    ss.var_road_edited = ss.var_road.copy()

# Public Transport Variables Rail
if 'var_rail' not in ss:
    ss.var_rail = pd.DataFrame({
        "variable": ss.lst_var_trad[3:], #linked to variable list
        "user_input": [0.0, 0.0],
        "default": [0.09, 13.00]
    })
    ss.var_rail_edited = ss.var_rail.copy()

# Active modes
if 'var_act' not in ss:
    ss.var_act = pd.DataFrame({
        "variable": ss.lst_var_act, #linked to variable list
        "user_input": [0.0, 0.0],
        "default": [17.00, 0.00]
    })
    ss.var_act_edited = ss.var_act.copy()

#####################################################################################################################################################################
###### initialise NMS session states ###########################################################################################################################
#####################################################################################################################################################################

# shared modes input table
if 'shared_modes' not in ss:
    ss.shared_modes = pd.DataFrame({
        "shared_modes": ss.nms_types,
        "num_veh": [0, 0, 0, 0, 0],
        "perc_EV": [0.0, 0.0, 0.0, 100, 0.0]
    })
    ss.shared_modes_edited = ss.shared_modes.copy()

# shared ICE car
if 'var_nms_ICEcar' not in ss:
    ss.var_nms_ICEcar = pd.DataFrame({
        "variable": (ss.lst_var_nms[:4] + ss.lst_var_nms[5:]), #linked to variable list
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_ICEcar_edited = ss.var_nms_ICEcar.copy()

# shared ICE moped
if 'var_nms_ICEmoped' not in ss:
    ss.var_nms_ICEmoped = pd.DataFrame({
        "variable": (ss.lst_var_nms[:4] + ss.lst_var_nms[5:]), #linked to variable list
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001] #last default 0.001 to prevent error in table rendering, replaced automatically
    })
    ss.var_nms_ICEmoped_edited = ss.var_nms_ICEmoped.copy()

# shared bike
if 'var_nms_bike' not in ss:
    ss.var_nms_bike = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[5:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_bike_edited = ss.var_nms_bike.copy()

# shared ev
if 'var_nms_ev' not in ss:
    ss.var_nms_ev = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[4:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_ev_edited = ss.var_nms_ev.copy()

# shared ebike
if 'var_nms_ebike' not in ss:
    ss.var_nms_ebike = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[4:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_ebike_edited = ss.var_nms_ebike.copy()

# shared emoped
if 'var_nms_emoped' not in ss:
    ss.var_nms_emoped = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[4:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.1, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #first defaults 0.01 to prevent error in table rendering, replaced automatically
    })
    ss.var_nms_emoped_edited = ss.var_nms_emoped.copy()

# shared escooter
if 'var_nms_escooter' not in ss:
    ss.var_nms_escooter = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[4:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #first defaults 0.02 to prevent error in table rendering, replaced automatically
    })
    ss.var_nms_escooter_edited = ss.var_nms_escooter.copy()

# shared other mode
if 'var_nms_other' not in ss:
    ss.var_nms_other = pd.DataFrame({
        "variable": (ss.lst_var_nms[:4] + ss.lst_var_nms[5:]), #linked to variable list
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_other_edited = ss.var_nms_other.copy()

    # shared e-other mode
if 'var_nms_eother' not in ss:
    ss.var_nms_eother = pd.DataFrame({
        "variable": (ss.lst_var_nms[:1] + ss.lst_var_nms[4:]), #linked to variable list,
        "user_input": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "default": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    })
    ss.var_nms_other_edited = ss.var_nms_eother.copy()
