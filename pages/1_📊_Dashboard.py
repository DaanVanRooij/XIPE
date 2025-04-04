import streamlit as st
import pandas as pd
import numpy as np
from streamlit import session_state as ss
import plotly.express as px


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

st.header("XIPE Dashboard")
st.write("""To use the tool, please fill in all information requested on this page. The information requested on this page is all that is needed
         to make a first estimation of emission changes.
         \n **Do you want to make an estimation using your own emission factors or other specific variables? A more detailed analysis can be performed 
         by changing specific variables, all variables used in the calculations can be adjused in the 'Variables' pages, which can be accessed by using the menu on the left.**  
         \nThe estimated changes in emissions due to the introdiction of shared mobility are displayed at the bottom of this
         dashboard.""")


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
#car_year = st.selectbox(
#    "Average manufacturing year of the car fleet:",
#    year_list,
#    key="car_year"
#)

# Percentage diesel in ICE car fleet and save in session state 
#diesel_perc = st.slider("Diesel percentage of the ICE car fleet", 
#                        min_value=0, 
#                        max_value=100,
#                        step=1,
#                        key="diesel_perc" 
#)

# get values for vehicle age and fuel shares from dataframe imported in introduction
# car age
car_age = ss.car_acea.loc[ss.car_acea["country"] == ss.country, "average_age_acea"].values[0]

# fuel distribution of cars based on country
perc_petrol = ss.car_acea.loc[ss.car_acea["country"] == ss.country, "perc_petrol"].values[0]
perc_diesel = ss.car_acea.loc[ss.car_acea["country"] == ss.country, "perc_diesel"].values[0]
perc_ev = ss.car_acea.loc[ss.car_acea["country"] == ss.country, "perc_ev"].values[0]

# other is all minus petrol, diesel and EV
perc_other = 1-perc_petrol-perc_diesel-perc_ev

#collect data for pie chart
pie_data = {"Fuel": ["Petrol", "Diesel", "EV", "Other"], "Values":[perc_petrol, perc_diesel, perc_ev, perc_other]}

# Preserve category order
pie_data['Fuel'] = pd.Categorical(pie_data['Fuel'], categories=pie_data['Fuel'], ordered=True)

# Create Pie Chart
fig = px.pie(pie_data, names="Fuel", values='Values', title=f"Share of cars by fuel in {ss.country} (ACEA)", 
             category_orders={"Fuel": pie_data["Fuel"].tolist()}) # Explicit order

# Display in Streamlit
a, b = st.columns([1,1])
with a:
    st.write("")
    st.write("")
    if ss.country == "Bulgaria" or ss.country == "Malta":
        st.metric(f"**The average car age in {ss.country} is**", f"{car_age} years*")
        st.write(f"\* *ACEA has no data available for {ss.country}, therefore the average EU value is used. Same for the share of cars by fuel.*")
    else:
        st.metric(f"**The average car age in {ss.country} is**", f"{car_age} years")
    st.write("Replacing an older car fleet with new shared mobility modes has a higher impact on the emissions because older cars are in "
    "general more polluting.")
    st.markdown("The type of fuel is used to estimate savings in NOx en PM emissions. As with all variables, these can be"
    "replaced with your own values in the 'Variables' pages.")
with b:
    st.plotly_chart(fig)


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


############################################################################################################################
######### Number of NMS and EV percentage editable table ###################################################################
############################################################################################################################

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

###################################################################################################################################
###################### Change variable default variables ##########################################################################
###################################################################################################################################

### General Variables
# get default values based on country selected in dashboard and include in dataframe
default_elec_co2 = ss.elec_co2_country.loc[0, ss.country]
ss.var_general.at[0, "default"] = default_elec_co2
ss.var_general.at[2, "default"] = car_age
ss.var_general.at[3, "default"] = perc_petrol * 100
ss.var_general.at[4, "default"] = perc_diesel * 100
ss.var_general.at[5, "default"] = perc_ev * 100

### Private Car Variables
# get default CO2 emission factor based on country and average car year selected in dashboard
# check if there is user input
if ss.var_general.at[2, "user_input"] == 0.0:
    ss.car_year = round(2024 - car_age,0)

# get index by substracting selected year by max year
# values <= 2020 are NEDC values and > 2020 are WLTP measurements
# NEDC and WLTP values underestimate real world CO2 emission by resepectively 40% and 14%, this is accounted for in the calculation below
default_co2_car = ss.car_co2.loc[(max(year_list) - ss.car_year) ,ss.country]
if ss.car_year <= 2020:
    default_co2_car = default_co2_car *1.4
else:
    default_co2_car = default_co2_car * 1.14


# get default NOx and PM emission factor based on country and share of fuels
# get petrol and diesel factors from air emissions based on year
petrol_nox = ss.car_air_emission.loc[(max(year_list) - ss.car_year) ,"petrol_nox"]
diesel_nox = ss.car_air_emission.loc[(max(year_list) - ss.car_year) ,"diesel_nox"]
petrol_pm = ss.car_air_emission.loc[(max(year_list) - ss.car_year) ,"petrol_pm"]
diesel_pm = ss.car_air_emission.loc[(max(year_list) - ss.car_year) ,"diesel_pm"]

# defaul emission factor based on percentage of fuel used in fleet, with EV emittion zero so not included in calculation, other fuels are disregarded as well
# e.g. fleet = 76.5% petrol, 8.4% diesel, 14% EV -->default_nox_car = 0.765 * petrol_nox + 0.084 * diesel nox + 0 * 14% 
default_nox_car = (perc_petrol * petrol_nox + perc_diesel * diesel_nox) * 1000 #calculate default NOx emission factor in mg/km
default_pm_car = (perc_petrol * petrol_pm + perc_diesel * diesel_pm) * 1000 #calculate default PM emission factor in mg/km

# set the default value based on country default when country is changed
ss.var_private_car.at[0, "default"] = default_co2_car
ss.var_private_car.at[1, "default"] = default_nox_car
ss.var_private_car.at[2, "default"] = default_pm_car

###################################################################################################################################
################################ Present Results ##################################################################################
###################################################################################################################################

#######  Set up calculation DataFrames ####### 
###### Create one table with all NMS Variables ######

# Dictionary with all NMS variable dataframes
var_nms_all = {"ICEcar":ss.var_nms_ICEcar, "ICEmoped":ss.var_nms_ICEmoped, "bike":ss.var_nms_bike, "ecar":ss.var_nms_ev, "ebike":ss.var_nms_ebike, "emoped":ss.var_nms_emoped, "escooter":ss.var_nms_escooter, "other":ss.var_nms_other, "eother":ss.var_nms_eother}

# Create a master template DataFrame with all unique variable names
df_template = pd.DataFrame({"variable": ss.lst_var_nms})  # Master template

var_nms_inputs = {}

# replace user input column with defaults if there is no input
for name, df in var_nms_all.items():
    df_new = df.copy()  # Copy original DataFrame
    df_new["variable"] = df_new["variable"].str.strip()

    if df_new["user_input"].sum() == 0:
        df_new["user_input"] = df_new["default"]

    df_new = df_new.drop(columns=["default"])  # Drop defaults
    df_new = df_new.rename(columns={"user_input":name})  # Rename columns
   
    # Merge with template to ensure alignment based on Variable
    df_merged = df_template.merge(df_new, on="variable", how="left")  # Left join to preserve all variable values
    var_nms_inputs[name] = df_merged  # Store processed DataFrame


# Combine all DataFrames into one based on variable column
df_var_nms = df_template.copy()  # Start with the template
for df in var_nms_inputs.values():
    df_var_nms = df_var_nms.merge(df, on="variable", how="left")  # Merge all on Col1

###### Create one table with all Tradional Modes Variables ######

# create separte walking and biking dataframes out of active variables
var_cyc = ss.var_act.iloc[:1].copy()
var_cyc.iloc[0,0] = "Emission factor for life-cycle phases excluding use phase (gCO2/km)"

var_walk = ss.var_act.iloc[1:].copy()
var_walk.iloc[0,0] = "Emission factor for life-cycle phases excluding use phase (gCO2/km)"

# Dictionary with all Traditional Modes Variable dataframes, including seperate cycling and walking
var_trad_lst = [ss.var_private_car, ss.var_road, ss.var_rail, var_cyc, var_walk]
var_trad_all = dict(zip(ss.trad_types, var_trad_lst))

# Create a master template DataFrame with all unique variable names
df_template = pd.DataFrame({"variable": ss.lst_var_trad})  # Master template

var_trad_inputs = {}

for name, df in var_trad_all.items():
    df_new = df.copy()  # Copy original DataFrame
    df_new["variable"] = df_new["variable"].str.strip()
    df_new["user_input"] = np.where(df_new["user_input"] == 0, df_new["default"], df_new["user_input"])  # Replace zeros
    df_new = df_new.drop(columns=["default"])  # Drop defaults
    df_new = df_new.rename(columns={"user_input":name})  # Rename columns

    # Merge with template to ensure alignment based on Variable
    df_merged = df_template.merge(df_new, on="variable", how="left")  # Left join to preserve all variable values
    
    var_trad_inputs[name] = df_merged  # Store processed DataFrame

# Combine all DataFrames into one based on variable column
df_var_trad = df_template.copy()  # Start with the template
for df in var_trad_inputs.values():
    df_var_trad = df_var_trad.merge(df, on="variable", how="left")  # Merge all on Col1

###### create table with general value s######

df_var_gen = ss.var_general.copy()  # Copy original DataFrame
df_var_gen["variable"] = df_var_gen["variable"].str.strip()
df_var_gen["user_input"] = np.where(df_var_gen["user_input"] == 0, df_var_gen["default"], df_var_gen["user_input"])  # Replace zeros
df_var_gen = df_var_gen.drop(columns=["default"])  # Drop defaults
df_var_gen = df_var_gen.rename(columns={"user_input":"general"})  # Rename columns



# Calculate the number of vehicles from the dashboard table for Shared Mobility
number_ICEcar = ss.shared_modes.num_veh[0] * ((100-ss.shared_modes.perc_EV[0])/100)
number_ICEmoped = ss.shared_modes.num_veh[2] * ((100-ss.shared_modes.perc_EV[2])/100)
number_bike = ss.shared_modes.num_veh[1] * ((100-ss.shared_modes.perc_EV[1])/100)
number_ecar = ss.shared_modes.num_veh[0] * (ss.shared_modes.perc_EV[0]/100)
number_ebike = ss.shared_modes.num_veh[1] * (ss.shared_modes.perc_EV[1]/100)
number_emoped = ss.shared_modes.num_veh[2] * (ss.shared_modes.perc_EV[2]/100)
number_escooter = ss.shared_modes.num_veh[3] # escooter is always electric so no need to multiply with percentage
number_other = ss.shared_modes.num_veh[4] * ((100-ss.shared_modes.perc_EV[4])/100)
number_eother = ss.shared_modes.num_veh[4] * (ss.shared_modes.perc_EV[4]/100)

# save all vehicle number variables in a dictionary
numbers_nms = {"variable": "Number of vehicles","ICEcar": number_ICEcar, "ICEmoped": number_ICEmoped, "bike": number_bike, "ecar": number_ecar, "ebike": number_ebike, "emoped": number_emoped, "escooter": number_escooter, "other": number_other, "eother": number_eother}

# Add the dictionary to the top row of the nms variable data frame
df_numbers_nms = pd.DataFrame([numbers_nms])
df_var_nms = pd.concat([df_numbers_nms, df_var_nms], ignore_index=True)


#######  Result calculations ####### 
####### CO2 use phase #########

# create empty dataframe to store results
column_names = df_var_nms.columns.tolist()
df_calc = pd.DataFrame(columns=column_names)

# calculate total trips
total_trips = df_var_nms.iloc[0, 1:] * df_var_nms.iloc[1, 1:]
new_row = pd.concat([pd.Series({"variable":"total_trips"}), total_trips])
df_calc.loc[len(df_calc)] = new_row


# calculate replaced trips
for i, name in zip(range(7, 12), ss.trad_types):
    result = df_calc.iloc[0, 1:] * (df_var_nms.iloc[i, 1:]/100)
    new_row = pd.concat([pd.Series({"variable":f"replaced_trip_{name}"}), result])
    df_calc.loc[len(df_calc)] = new_row

# calculate decreased mileage from private modes
for i, name in zip(range(0,5), ss.trad_types):
    result = df_calc.iloc[i+1, 1:] * df_var_nms.iloc[i+12, 1:]*- 1
    new_row = pd.concat([pd.Series({"variable":f"decreased_distance_{name}"}), result])
    df_calc.loc[len(df_calc)] = new_row


# calculate emission factor rail from inputs
emission_factor_rail = df_var_gen.iloc[0, 1] * df_var_trad.iloc[3, 3]

# calculate CO2 emission TTW 
co2_factors = df_var_trad.iloc[0, 1:].to_list()
co2_factors[2] = emission_factor_rail


for i, name in zip(range(0,6), ss.trad_types):
    result = (df_calc.iloc[i+6, 1:] * co2_factors[i])/1000
    if i <= 1:
        new_row = pd.concat([pd.Series({"variable":f"co2_saved_TTW_{name}"}), result])
        df_calc.loc[len(df_calc)] = new_row
    else:
        new_row = pd.concat([pd.Series({"variable":f"co2_saved_WTT_{name}"}), result])
        df_calc.loc[len(df_calc)] = new_row

# calculate CO2 emission WTW
for i, name in zip(range(0,2), ss.trad_types):
    result = df_calc.iloc[i+11, 1:] * ((1/(1-(df_var_gen.iloc[1,1]/100)))-1) 
    new_row = pd.concat([pd.Series({"variable":f"co2_saved_WTT_{name}"}), result])
    df_calc.loc[len(df_calc)] = new_row

# calculate kilometres travelled by NMS
trips = df_calc.iloc[1:6, 1:].reset_index(drop=True)
trip_dist = df_var_nms.iloc[12:17, 1:].reset_index(drop=True)

total_km_travelled = (trips * trip_dist).sum()
new_row = pd.concat([pd.Series({"variable":"total_km_travelled"}), total_km_travelled])
df_calc.loc[len(df_calc)] = new_row

### calculate emissions from NMS
# calculate average emission factor shared EVs
avg_co2_nms = df_var_gen.iloc[0,1] * df_var_nms.iloc[5, 1:]
new_row = pd.concat([pd.Series({"variable":"ev_emission_factor"}), avg_co2_nms])
df_calc.loc[len(df_calc)] = new_row

# calculate ttw CO2
ttw_ice_co2 = (df_calc.iloc[18, 1:] * df_var_nms.iloc[2, 1:])/1000
new_row = pd.concat([pd.Series({"variable":"ttw_co2"}), ttw_ice_co2])
df_calc.loc[len(df_calc)] = new_row

# calculate wtt CO2
wtt_ice_co2 = ttw_ice_co2 * ((1/(1-(df_var_gen.iloc[1,1]/100)))-1)
wtt_ev_co2 = (df_calc.iloc[18, 1:] * df_calc.iloc[19, 1:])/1000

#combine wtt in one row, replacing none and zero values
# set both sets to float before combining them, got warning without astype
wtt_ev_co2 = wtt_ev_co2.astype("float64")
wtt_ice_co2 = wtt_ice_co2.astype("float64")

wtt_co2 = wtt_ev_co2.where(wtt_ev_co2.ne(0.0)).fillna(wtt_ice_co2).infer_objects(copy=False)
new_row = pd.concat([pd.Series({"variable":"wtt_co2"}), wtt_co2])
df_calc.loc[len(df_calc)] = new_row

# make dafaframe to hold results 
df_results = pd.DataFrame(columns=column_names)

# calculate the average co2 emission change for TTW and WTT for trad and nms vehicles
avg_co2_TTW_trad = df_calc.iloc[11:13, 1:].sum()
avg_co2_WTT_trad = df_calc.iloc[13:18, 1:].sum()
avg_co2_TTW_nms = ttw_ice_co2
avg_co2_WTT_nms = wtt_co2

results_dict = {"avg_co2_TTW_trad": avg_co2_TTW_trad, "avg_co2_WTT_trad": avg_co2_WTT_trad, "avg_co2_TTW_nms": avg_co2_TTW_nms, "avg_co2_WTT_nms": avg_co2_WTT_nms}

for name, result in results_dict.items():
    new_row = pd.concat([pd.Series({"variable": name}), result])
    df_results.loc[len(df_results)] = new_row

# calculate total estimated CO2 emission change for each of the nms
avg_co2_total = df_results.iloc[:,1:].sum(min_count=1)

####### CO2 LCA phase ########

# Get distances and emission factors and multiply them
decreased_distance = df_calc.iloc[6:11, 1:].reset_index(drop=True)
emission_fact_lca = df_var_trad.iloc[4, 1:].reset_index(drop=True)

avg_co2_lca = decreased_distance.mul((emission_fact_lca/1000), axis=0)

km_by_nms = df_calc.iloc[18, 1:].reset_index(drop=True)
emission_fact_lca_nms = df_var_nms.iloc[6, 1:].reset_index(drop=True)

avg_co2_lca_nms = (emission_fact_lca_nms.values * total_km_travelled.values)/1000
avg_co2_lca.loc[len(avg_co2_lca)] = avg_co2_lca_nms


####### NOx and PM use phase #########
# NOx calculations
emission_fact_nox = df_var_trad.iloc[1, 1:].reset_index(drop=True)
avg_nox = decreased_distance.mul((emission_fact_nox/1000), axis=0)
emission_fact_nox_nms = df_var_nms.iloc[3, 1:].reset_index(drop=True)
avg_nox_nms = (emission_fact_nox_nms.values * total_km_travelled.values)/1000
avg_nox.loc[len(avg_nox)] = avg_nox_nms

# PM calculations
emission_fact_pm = df_var_trad.iloc[2, 1:].reset_index(drop=True)
avg_pm = decreased_distance.mul((emission_fact_pm/1000), axis=0)
emission_fact_pm_nms = df_var_nms.iloc[4, 1:].reset_index(drop=True)
avg_pm_nms = (emission_fact_pm_nms.values * total_km_travelled.values)/1000
avg_pm.loc[len(avg_pm)] = avg_pm_nms

#######  Table presentation ####### 

# sum the emission changes over the base nms types
df_presentation = pd.DataFrame(columns=ss.nms_types)
df_presentation.insert(0, "Estimated CO2 change",["Tank-to-Wheel (kg/day)", "Well-to-Tank (kg/day)", "Additional life-cycle emissions (kg/day)", "TOTAL (kg/day)"])

for types in ss.nms_types:
    # CO2 use phase
    sum = df_results.filter(regex=types.lower()).sum(axis=1)
    ttw_total = sum.iloc[0] + sum.iloc[2]
    wtt_total = sum.iloc[1] + sum.iloc[3]
    df_presentation.loc[0, types] = ttw_total
    df_presentation.loc[1, types] = wtt_total
    # CO2 LCA
    sum_lca = avg_co2_lca.filter(regex=types.lower()).sum(axis=1)
    lca_total = sum_lca.sum()
    df_presentation.loc[2, types] = lca_total

df_presentation.iloc[3, 1:] = df_presentation.iloc[0:3, 1:].sum()

df_presentation_air = pd.DataFrame(columns=ss.nms_types)
df_presentation_air.insert(0, "Estimated air quality emission change",["NOx (g/day)", "PM (g/day)"])

for types in ss.nms_types:
    # NOx
    sum_nox = avg_nox.filter(regex=types.lower()).sum(axis=1)
    nox_total = sum_nox.sum()
    df_presentation_air.loc[0, types] = nox_total
    # PM
    sum_pm = avg_pm.filter(regex=types.lower()).sum(axis=1)
    pm_total = sum_pm.sum()
    df_presentation_air.loc[1, types] = pm_total

# Create table with total values
df_presentation_total = pd.DataFrame(columns=["Total", "Tank-to-Wheel", "Well-to-Tank", "Life-cyle"])
df_presentation_total.insert(0, "Estimated CO2 change",["kg/day", "ton/year", "ton/year/1,000 inhabitants"])
for i in range(0,4):
    df_presentation_total.iloc[0,i+1] = df_presentation.iloc[i, 1:].sum()

df_presentation_total.iloc[1,1:] = df_presentation_total.iloc[0,1:] / 1000 * 365.25
df_presentation_total.iloc[2,1:] = df_presentation_total.iloc[1,1:] / ss.inhabitants * 1000

# Shift values to start with total
# Get all columns except the first
cols_to_shift = df_presentation_total.columns[1:]

# Shift each row's values (excluding first column)
df_presentation_total[cols_to_shift] = df_presentation_total[cols_to_shift].apply(
    lambda row: pd.Series([row.iloc[-1]] + row.iloc[:-1].tolist(), index=row.index),
    axis=1
)

# Create table with total values NOx and PM
df_presentation_total_air = pd.DataFrame(columns=["NOx", "PM"])
df_presentation_total_air.insert(0, "Estimated air quality emission change",["g/day", "kg/year", "kg/year/1,000 inhabitants"])
for i in range(0,2):
    df_presentation_total_air.iloc[0,i+1] = df_presentation_air.iloc[i, 1:].sum()

df_presentation_total_air.iloc[1,1:] = df_presentation_total_air.iloc[0,1:] / 1000 * 365.25
df_presentation_total_air.iloc[2,1:] = df_presentation_total_air.iloc[1,1:] / ss.inhabitants * 1000


#### Presentation table configuration before presenting
# Function to color cells based on value red when positive, green when negative, yellow when zero
def color_positive_negative(val):
    if val < 0:
        return 'background-color: lightgreen'
    elif val > 0:
        return 'background-color: salmon'
    else:
        return 'background-color: lightyellow'

# Apply style to all numeric columns
styled_df_presentation = df_presentation.style.map(color_positive_negative, subset=df_presentation.columns[1:])
styled_df_presentation_air = df_presentation_air.style.map(color_positive_negative, subset=df_presentation_air.columns[1:])
styled_df_presentation_total = df_presentation_total.style.map(color_positive_negative, subset=df_presentation_total.columns[1:])
styled_df_presentation_total_air = df_presentation_total_air.style.map(color_positive_negative, subset=df_presentation_total_air.columns[1:])

column_config = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in df_presentation.columns[1:]
}

column_config_air = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in df_presentation_air.columns[1:]
}

column_config_total = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in df_presentation_total.columns[1:]
}

column_config_total_air = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in df_presentation_total_air.columns[1:]
}

# present result tables
# Title and explanation
st.header("Results of the analysis")
st.write("""The tables below show the emission changes due to the introduction of shared mobility. The first table shows the changes per shared mode,
         the second table the total values per day, year and per 1000 inhabitants.
         :green-background[Green cells] are a decrease in emissions, :red-background[red cells] are an increase in emissions and :orange-background[yellow cells] have no changes.
         \nPlease remember, you can recalculate the emission changes using your own emission factors or other variables by accessing the 'Variables' pages accessible on the left!""")
st.subheader(f"Estimated emission change per shared mode in {ss.city_name}")

st.dataframe(styled_df_presentation,
             hide_index=True,
             column_config=column_config,
             use_container_width=True
             )

st.dataframe(styled_df_presentation_air,
             hide_index=True,
             column_config=column_config_air,
             use_container_width=True
             )

st.subheader(f"Estimated total emission change in {ss.city_name}")
st.dataframe(styled_df_presentation_total,
             hide_index=True,
             column_config=column_config_total,
             use_container_width=True
             )

st.dataframe(styled_df_presentation_total_air,
             hide_index=True,
             column_config=column_config_total_air,
             use_container_width=True
             )