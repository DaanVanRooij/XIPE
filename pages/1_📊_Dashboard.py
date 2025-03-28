import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from streamlit import session_state as ss
from streamlit_extras.grid import grid


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

#CNL Logo and HTML scaling
st.logo("images/cenexNL_logo.png", size="large")
st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)

#save country and year list from session state initialised in introduction
country_list = ss["country_list"]
year_list = ss["year_list"]

###############################################################################
###################### City inputs ############################################
###############################################################################

######### Select country and save in session state and df
# initiate session state widget and save in session state
country = st.selectbox(
    "Select your country:",
    country_list,
    key="country_key"
)
ss.country = country

######### City name and save in session state
# initiate session state
city_name = st.text_input("City name", 
                      placeholder="Type the name of the city",
                      key="city_name")

######### Number of inhabitants and save in session state
inhabitants = st.number_input(
    "Number of inhabitants:", 
    placeholder="Type a number...",
    min_value=1, 
    format="%0.1d",
    key="inhabitants"
)

### Select average age car fleet and save index in session state 
car_year = st.selectbox(
    "Average manufacturing year of the car fleet:",
    year_list,
    key="car_year"
)

# Percentage diesel in ICE car fleet and save in session state 
diesel_perc = st.slider("Diesel percentage of the ICE car fleet", 
                        min_value=0, 
                        max_value=100,
                        step=1,
                        key="diesel_perc" 
)

###################################################################################
######### City modal split and trip distance editable table #######################
###################################################################################

# Modal split and distances set up as session states
var_ms = {"ms_pcar": 0.0, "ms_road": 0.0, "ms_rail": 0.0, "ms_pt": 0.0, "ms_walk": 0.0, "ms_cyc": 0.0, "ms_act": 0.0}
var_dist = {"dist_pcar": 0.0, "dist_road": 0.0, "dist_rail": 0.0, "dist_pt": 0.0, "dist_walk": 0.0, "dist_cyc": 0.0, "dist_act": 0.0}

var_ms_dist = var_ms | var_dist

for var in var_ms_dist:
    if var not in ss:
        ss[var] = var_ms_dist[var]

ss["ms_pt"] = ss["ms_road"] + ss["ms_rail"]
ss["dist_pt"] = (ss["dist_road"] + ss["dist_rail"])/2
ss["ms_act"] = ss["ms_walk"] + ss["ms_cyc"]
ss["dist_act"] = (ss["dist_walk"] + ss["dist_cyc"])/2

### Modal split and trip distance input table
# Title and explanation
st.header("City modal split and average trip distance")
st.write("""Please fill in the current modal split and average trip distance in the city. 
         Modal split for public transport and active modes is a summation of its sub-modes. 
         Average trip distance for public transport and active modes is the average of its sub-modes.""") 

# Column Headers
with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.write("")
    c2.subheader("Modal Split (%)")
    c3.subheader("Average Trip Distance (km)")

# Private Car
with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.write("Private Car")
    c2.number_input("Private Car", max_value=100.0,min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed", key="ms_pcar")
    c3.number_input("dist_pcar", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed", key="dist_pcar")

# Public Transport
with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.write("Public Transport")
    c2.markdown(f":blue-background[{(ss.ms_pt/100):.1%}]" )
    c3.markdown(f":blue-background[{ss.dist_pt}]" )

with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.markdown('<div style="text-align: right;">Road</div>', unsafe_allow_html=True)
    c2.number_input("ms_road", max_value=100.0,min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed", key="ms_road")
    c3.number_input("dist_road", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed", key="dist_road")

with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.markdown('<div style="text-align: right;">Rail</div>', unsafe_allow_html=True)
    c2.number_input("ms_rail", max_value=100.0,min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed", key="ms_rail")
    c3.number_input("dist_rail", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed", key="dist_rail")

# Active modes
with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.write("Active modes")
    c2.markdown(f":blue-background[{(ss.ms_act/100):.1%}]" )
    c3.markdown(f":blue-background[{ss.dist_act}]" )

with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.markdown('<div style="text-align: right;">Cycling</div>', unsafe_allow_html=True)
    c2.number_input("ms_cyc", max_value=100.0, min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed", key="ms_cyc")
    c3.number_input("dist_cyc", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed", key="dist_cyc")

with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.markdown('<div style="text-align: right;">Walking</div>', unsafe_allow_html=True)
    c2.number_input("ms_walk", max_value=100.0,min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed", key="ms_walk")
    c3.number_input("dist_walk", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed", key="dist_walk")

with st.container():
    c1, c2, c3 = st.columns(3, vertical_alignment="center")
    c1.write("Total")
    if ((ss.ms_act + ss.ms_pt + ss.ms_pcar)/100) != 1:
        c2.markdown(f":red-background[{((ss.ms_act + ss.ms_pt + ss.ms_pcar)/100):.1%}]" )
        st.warning("Your modal split should add to 100%", icon="⚠️")
    else:
        c2.markdown(f":blue-background[{((ss.ms_act + ss.ms_pt + ss.ms_pcar)/100):.1%}]" )
    c3.write("")

### initiate and update default inputs in session state after updating dashboard
ss.default_inputs_ICEcar = ([5.00, 133.38, 60.00, 4.50, 55.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])
ss.default_inputs_ICEmoped = ([5.00, 37.00, 60.00, 4.50, 31.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])
# To prevent overestimation of bike distances, distances for car and PT are asumed to be the average cycling distances 
ss.default_inputs_bike = ([4.00, 58.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_cyc, ss.dist_cyc, ss.dist_cyc, ss.dist_cyc, ss.dist_walk])
ss.default_inputs_ev = ([5.00, 0.17, 81.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])
# To prevent overestimation of e-bike distances, distances for car and PT are asumed to be 1.5 times the average cycling distances 
ss.default_inputs_ebike = ([4.00, 0.0103, 71.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_cyc*1.5, ss.dist_cyc*1.5, ss.dist_cyc*1.5, ss.dist_cyc, ss.dist_walk])
ss.default_inputs_emoped = ([5.00, 0.033, 59.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])
# To prevent overestimation of escooter distances, distances for car and PT are asumed to be average cycling distances 
ss.default_inputs_escooter = ([5.00, 0.016, 100.00, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_cyc, ss.dist_cyc, ss.dist_cyc, ss.dist_cyc, ss.dist_walk])
ss.default_inputs_other = ([0.0, 0.0, 0.0, 0.0, 0.0, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])
ss.default_inputs_eother = ([0.0, 0.0, 0.0, ss.ms_pcar, ss.ms_road, ss.ms_rail, ss.ms_cyc, ss.ms_walk, ss.dist_pcar, ss.dist_road, ss.dist_rail, ss.dist_cyc, ss.dist_walk])

default_inputs_list = [ss.default_inputs_ICEcar, ss.default_inputs_ICEmoped, ss.default_inputs_bike, ss.default_inputs_ev, ss.default_inputs_ebike, ss.default_inputs_emoped, ss.default_inputs_escooter, ss.default_inputs_other, ss.default_inputs_eother]

### write the new default values to variable in session state
i=0
for types in ss.var_nms_types:
    if types in ss:
        ss[types]["default"] = default_inputs_list[i]
        i +=1

# Save edits by copying edited dataframes to "original" slots in session state
def save_edits():
    ss.shared_modes = ss.shared_modes_edited.copy()


###################################################################################
######### Number of NMS and EV percentage editable table ##########################
###################################################################################

### NMS input table
# Title and explanation
st.header("Shared Mobility Services")
st.write("""Please fill in the number of shared vehicles per mode and the percentage of them that is electric. 
         e-Scooters will always be electric and are therefore prefilled with 100%. Clink the Save Data button to 
         save the data in the table""")
         
ss.shared_modes_edited = st.data_editor(ss.shared_modes, 
                                        hide_index=True, 
                                        column_config={
                                            "shared_modes": st.column_config.TextColumn(
                                                label= "Shared Modes"
                                            ),
                                            "num_veh": st.column_config.NumberColumn(
                                                label="Number of Shared Vehicles",
                                                min_value=0,
                                                step=1,
                                                format="%d"
                                            ),
                                            "perc_EV": st.column_config.NumberColumn(
                                                label="Percentage Electric",
                                                min_value=0,
                                                max_value=100,
                                                step=1,
                                                format="%d %%"
                                            )
                                        },
                                        disabled=["default"],
                                        use_container_width=True
                                        )


st.button("Save Data", type="primary", on_click=save_edits)

##########################################################################################
###################### Change variable default variables #################################
##########################################################################################

### General Variables
# get default value based on country selected in dashboard and include in dataframe
default_elec_co2 = ss.elec_co2_country.loc[0, ss.country]
ss.var_general.at[0, "default"] = default_elec_co2

### Private Car Variables
# get default value based on country and average car year selected in dashboard
# get index by substracting selected year by max year
# values <= 2020 are NEDC values and > 2020 are WLTP measurements
# NEDC and WLTP values underestimate real world CO2 emission by resepectively 40% and 14%, this is accounted for in the calculation below

default_co2_car = ss.car_co2.loc[(max(year_list) - ss.car_year) ,ss.country]
if ss.car_year <= 2020:
    default_co2_car = default_co2_car *1.4
else:
    default_co2_car = default_co2_car * 1.14

# set the default value based on country default when country is changed
ss.var_private_car.at[0, "default"] = default_co2_car

################### Present Results #########################
#############################################################
