import streamlit as st
from pages import a_form_page_1, b_results_page_2, c_charts_page_3

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# st.sidebar.success("Select a demo above.")

st.sidebar.markdown("### Navigation")
selected_demo = st.sidebar.radio(
    "Choose a demo",
    ("Form Page", "Results Page", "Charts Page")
)

# Check if a demo has been selected via form submission
if hasattr(st.session_state, 'selected_demo') and st.session_state.selected_demo == "Results Page":
    selected_demo = "Results Page"
    st.session_state.selected_demo = None  # Reset the selected_demo state

if selected_demo == "Form Page":
    a_form_page_1.form_page()
elif selected_demo == "Results Page":
    b_results_page_2.results_page()
else:
    c_charts_page_3.charts_page()
