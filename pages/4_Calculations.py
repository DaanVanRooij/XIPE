from st_aggrid import AgGrid
import pandas as pd
import streamlit as st
import numpy as np
from streamlit import session_state as ss

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

#################################################################################################
########################### Set up calculation DataFrames #######################################
#################################################################################################


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

######################################################################################################
######################## Result calculations #########################################################
######################################################################################################

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


######################################################################################################
######################## Table presentation ##########################################################
######################################################################################################

# sum the emission changes over the base nms types
df_presentation = pd.DataFrame(columns=ss.nms_types)
df_presentation.insert(0, "",["Estimated CO2 change Tank-to-Wheel (kg/day)", "Estimated CO2 change Well-to-Tank (kg/day)", "Estimated additional life-cycle CO2 change (kg/day)", "Estimated CO2 change TOTAL (kg/day)"])
i=0
for types in ss.nms_types:
    i+=1
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

# Create table with total values
df_presentation_total = pd.DataFrame(columns=["Total", "Tank-to-Wheel", "Well-to-Tank", "Life-cyle"])
df_presentation_total.insert(0, "Estimated CO2 reduction",["kg/day", "ton/year", "ton/year/1,000 inhabitants"])
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
styled_df_presentation_total = df_presentation_total.style.map(color_positive_negative, subset=df_presentation_total.columns[1:])

# configure numbers to be two decimals
column_config = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in ss.nms_types
}

column_config_total = {
    col: st.column_config.NumberColumn(col, format="%.2f")
    for col in ["Total", "Tank-to-Wheel", "Well-to-Tank", "Life-cyle"]
}


# present result tables
# Title and explanation
st.header("Estimated Emission Change")
st.write("""The tables below show the emission changes due to the introduction of shared mobility. The first table shows the changes per shared mode,
         the second table the total values per day, year and per 1000 inhabitants""")
st.subheader("Estimated emission change per shared mode")
st.dataframe(styled_df_presentation,
             hide_index=True,
             column_config=column_config,
             use_container_width=True
             )


st.subheader("Total estimated emission changes")
st.dataframe(styled_df_presentation_total,
             hide_index=True,
             column_config=column_config_total,
             use_container_width=True
             )
#####################################################################################################
######################## testing and outputs ########################################################
#####################################################################################################
