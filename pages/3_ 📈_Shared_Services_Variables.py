from st_aggrid import AgGrid
import pandas as pd
import streamlit as st
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

#CNL Logo and HTML scaling
st.logo("images/cenexNL_logo.png", size="large")
st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
##################################################################################
###################### Functions #################################################
##################################################################################

# Save edits by copying edited dataframes to "original" slots in session state
def save_edits(old_ss, edited_ss):
    old_ss.update(edited_ss.copy())

###################################################################################
################### Display variable tables #######################################
###################################################################################

# all the tables are set up with an editable user input column and followed by a button to save these inputs so the session state.

#Intoduction text
st.header("Shared Modes Variables")
st.write("""On this page the variables and factors of the shared services are displayed per mode. All variables on this page have default 
         values displayed. If the user has specific variable values they can fill these in the User Input column, this will override 
         the default values in the calculations.""")
st.write("""Calculations will use the whole User Input column. Therefore, when using user input be sure to fill in all user input cells, 
         copy default values where needed.""")
st.warning("Don't forget to click the save buttons to save the data in the table.") 

# Display new shared modes ICE car table
st.subheader("Shared ICE Car")
ss.var_nms_ICEcar_edited = st.data_editor(ss.var_nms_ICEcar, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save ICE Car Variables", type="primary", on_click=save_edits, args=(ss.var_nms_ICEcar, ss.var_nms_ICEcar_edited)) 

# Display new shared modes ICE moped table
st.subheader("Shared ICE Moped")
ss.var_nms_ICEmoped_edited = st.data_editor(ss.var_nms_ICEmoped, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save ICE Moped Variables", type="primary", on_click=save_edits, args=(ss.var_nms_ICEmoped, ss.var_nms_ICEmoped_edited))

# Display new shared modes bike table
st.subheader("Shared bike")
ss.var_nms_bike_edited = st.data_editor(ss.var_nms_bike, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save Shared Bike Variables", type="primary", on_click=save_edits, args=(ss.var_nms_bike, ss.var_nms_bike_edited))

# Display new shared modes ev table
st.subheader("Shared e-Car")
ss.var_nms_ev_edited = st.data_editor(ss.var_nms_ev, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save e-Car Variables", type="primary", on_click=save_edits, args=(ss.var_nms_ev, ss.var_nms_ev_edited))

# Display new shared modes ebike table
st.subheader("Shared e-bike")
ss.var_nms_ebike_edited = st.data_editor(ss.var_nms_ebike, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        num_rows=["fixed"],
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save e-Bike Variables", type="primary", on_click=save_edits, args=(ss.var_nms_ebike, ss.var_nms_ebike_edited))

# Display new shared modes emoped table
st.subheader("Shared e-Moped")
ss.var_nms_emoped_edited = st.data_editor(ss.var_nms_emoped, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },                                      
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save e-Moped Variables", type="primary", on_click=save_edits, args=(ss.var_nms_emoped, ss.var_nms_emoped_edited))

# Display new shared modes escooter table
st.subheader("Shared e-Scooter")
ss.var_nms_escooter_edited = st.data_editor(ss.var_nms_escooter, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.2f"
                                            )
                                        },
                                        column_order=["variable", "user_input", "default"],
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save e-Scooter Variables", type="primary", on_click=save_edits, args=(ss.var_nms_escooter, ss.var_nms_escooter_edited))

# Display new shared modes escooter table
# first define variable name, edited by editing shared mobility services table in Dashboard
other_name = ss.shared_modes["shared_modes"].values[4]

# display table new shared modes other
st.subheader(f"Shared {other_name}")
st.write("Please use these tables to insert a shared mode not available in the tool, this table should be used to add an ICE vehicle, while the next an electric vehicle.")
ss.var_nms_other_edited = st.data_editor(ss.var_nms_other, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.3f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.3f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button(f"Save {other_name} Variables", type="primary", on_click=save_edits, args=(ss.var_nms_other, ss.var_nms_other_edited))

# display table new shared modes other
st.subheader(f"Shared e-{other_name}")
ss.var_nms_eother_edited = st.data_editor(ss.var_nms_eother, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.3f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.3f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button(f"Save e-{other_name} Variables", type="primary", on_click=save_edits, args=(ss.var_nms_eother, ss.var_nms_eother_edited))