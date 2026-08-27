
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Regional Risk Analysis")
st.caption("Analyze regional and city mismatch indicators.")
df = add_common_filters(df, "p17")

a,b,c=st.columns(3)
a.metric("Most Common Region Rating",str(df.REGION_RATING_CLIENT.mode().iloc[0]) if "REGION_RATING_CLIENT" in df else "—")
r=df.groupby("REGION_RATING_CLIENT")["TARGET"].mean() if "REGION_RATING_CLIENT" in df else pd.Series()
b.metric("Highest Risk Region Rating",str(r.idxmax()) if len(r) else "—")
c.metric("Avg Regional Population Indicator",f"{df.REGION_POPULATION_RELATIVE.mean():.4f}" if "REGION_POPULATION_RELATIVE" in df else "—")
for col,title in [("REGION_RATING_CLIENT","Customers by Region Rating"),("REGION_RATING_CLIENT_W_CITY","Default Rate by Region Rating with City"),("REGION_POPULATION_RELATIVE","Regional Population Indicator")]:
    if col in df:
        if col.startswith("REGION_RATING"):
            x=df.groupby(col)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
            st.plotly_chart(px.bar(x,x=col,y="Default Rate %",title=title),use_container_width=True)
        else:
            st.plotly_chart(px.histogram(df,x=col,nbins=50,title=title),use_container_width=True)
for col in ["REG_REGION_NOT_LIVE_REGION","REG_REGION_NOT_WORK_REGION","REG_CITY_NOT_LIVE_CITY","REG_CITY_NOT_WORK_CITY"]:
    if col in df:
        x=df.groupby(col)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
        st.plotly_chart(px.bar(x,x=col,y="Default Rate %",title=f"Mismatch vs Default: {col}"),use_container_width=True)
