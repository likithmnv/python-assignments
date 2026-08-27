
import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="Home Credit Default Risk Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💳 HOME CREDIT DEFAULT RISK ANALYTICS")
st.caption("Interactive credit-risk dashboard for Home Credit application_train.csv")

df = load_data()

with st.sidebar:
    st.header("Navigation")
    st.info("Use the pages in the sidebar to explore applicants, defaults, risk factors, and customer profiles.")
    st.markdown("---")
    st.write(f"**Rows:** {len(df):,}")
    st.write(f"**Columns:** {df.shape[1]:,}")

st.markdown("""
### Dashboard
Use the page navigation on the left to open the 20 analysis modules.

**Recommended starting point:** Executive Overview → Default Analysis → Income vs Credit → External Scores → Correlation & Risk Factors.
""")
