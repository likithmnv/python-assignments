
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Housing & Asset Analysis")
st.caption("Analyze property and vehicle ownership.")
df = add_common_filters(df, "p14")

car=df.FLAG_OWN_CAR.eq("Y") if "FLAG_OWN_CAR" in df else pd.Series(False,index=df.index)
realty=df.FLAG_OWN_REALTY.eq("Y") if "FLAG_OWN_REALTY" in df else pd.Series(False,index=df.index)
a,b,c,d=st.columns(4)
a.metric("Car Owners",f"{car.sum():,}")
b.metric("Property Owners",f"{realty.sum():,}")
c.metric("Owning Both",f"{(car & realty).sum():,}")
d.metric("Default Rate of Property Owners",f"{df.loc[realty,'TARGET'].mean()*100:.2f}%")
for col,title in [("FLAG_OWN_CAR","Car Ownership Distribution"),("FLAG_OWN_REALTY","Property Ownership Distribution"),("NAME_HOUSING_TYPE","Applicants by Housing Type")]:
    if col in df:
        x=df[col].value_counts().reset_index()
        st.plotly_chart(px.bar(x,x=col,y="count",title=title),use_container_width=True)
for col,title in [("FLAG_OWN_CAR","Default Rate by Car Ownership"),("FLAG_OWN_REALTY","Default Rate by Property Ownership"),("NAME_HOUSING_TYPE","Default Rate by Housing Type")]:
    if col in df:
        x=df.groupby(col)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
        st.plotly_chart(px.bar(x,x=col,y="Default Rate %",title=title),use_container_width=True)
