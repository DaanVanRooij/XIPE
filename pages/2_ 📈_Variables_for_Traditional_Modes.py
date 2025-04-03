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

# Function to save edits by copying edited dataframes to "original" slots in session state
def save_edits(old_ss, edited_ss):
    old_ss.update(edited_ss.copy())

#################################################################################
################### Display variable tables #####################################
#################################################################################

# all the tables are set up with an editable user input column and followed by a button to save these inputs so the session state.

#Intoduction text
st.header("Traditional Modes Variables")
st.write("""On this page the variables and factors of the traditional modes are displayed per mode. All variables on this page have default 
         values displayed. If the user has specific variable values they can fill these in the User Input column, this will override 
         the default values in the calculations.
         \n**Calculations will use the whole User Input column. Therefore, when using user input be sure to fill in all user input cells, 
         copy default values where needed.**
         \nChanges on the Variables pages will directly change the Estimated Emission Change tables displayed on the Dashboard page.""")

st.warning("Don't forget to click the save buttons to save the data in the table.") 

# Display General variables table
st.subheader("General variables")
ss.var_general_edited = st.data_editor(ss.var_general, 
                                        hide_index=True, 
                                        column_config={
                                            "variable": st.column_config.TextColumn(
                                                label= ""
                                            ),
                                            "user_input": st.column_config.NumberColumn(
                                                label="User Input",
                                                min_value=0,
                                                step=0.001,
                                                format="%.1f"
                                            ),
                                            "default": st.column_config.NumberColumn(
                                                label="Default Value",
                                                min_value=0,
                                                step=0.001,
                                                format="%.1f"
                                            )
                                        },
                                        disabled=["variable", "default"],
                                        use_container_width=True
                                        )

st.button("Save General Variables", type="primary", on_click=save_edits, args=(ss.var_general, ss.var_general_edited)) 

# Display private car variables table
st.subheader("Private Car (per vehicle km)")
ss.var_private_car_edited = st.data_editor(ss.var_private_car, 
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

st.button("Save Private Car Variables", type="primary", on_click=save_edits, args=(ss.var_private_car, ss.var_private_car_edited))

# Display PT Road variables table
st.subheader("Public Transport Road (per passenger km)")
ss.var_road_edited = st.data_editor(ss.var_road, 
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

st.button("Save Public Transport Road Variables", type="primary", on_click=save_edits, args=(ss.var_road, ss.var_road_edited))

# Display PT Rail variables table
st.subheader("Public Transport Rail (per passenger km)")
ss.var_rail_edited = st.data_editor(ss.var_rail, 
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

st.button("Save Public Transport Rail Variables", type="primary", on_click=save_edits, args=(ss.var_rail, ss.var_rail_edited))

# Display Active variables table
st.subheader("Active Transport (per vehicle km)")
ss.var_act_edited = st.data_editor(ss.var_act, 
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

st.button("Save Active Transport Variables", type="primary", on_click=save_edits, args=(ss.var_act, ss.var_act_edited))