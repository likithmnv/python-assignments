
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Education Analysis")
st.caption("Analyze applicants by education level.")
df = add_common_filters(df, "p11")

g=df.groupby("NAME_EDUCATION_TYPE").agg(Customers=("TARGET","size"),Default_Rate=("TARGET","mean"),Avg_Income=("AMT_INCOME_TOTAL","mean"),Avg_Credit=("AMT_CREDIT","mean"),Avg_Annuity=("AMT_ANNUITY","mean"),Avg_Credit_Income=("CREDIT_INCOME_RATIO","mean")).reset_index()
g["Default_Rate"]*=100
a,b,c,d=st.columns(4)
a.metric("Most Common Education",str(df.NAME_EDUCATION_TYPE.mode().iloc[0]))
b.metric("Highest Income Education",str(g.loc[g.Avg_Income.idxmax(),"NAME_EDUCATION_TYPE"]))
c.metric("Lowest Default Education",str(g.loc[g.Default_Rate.idxmin(),"NAME_EDUCATION_TYPE"]))
d.metric("Highest Default Education",str(g.loc[g.Default_Rate.idxmax(),"NAME_EDUCATION_TYPE"]))
for y,title in [("Customers","Customers by Education"),("Default_Rate","Default Rate by Education"),("Avg_Income","Income by Education"),("Avg_Credit","Credit by Education"),("Avg_Annuity","Annuity by Education"),("Avg_Credit_Income","Credit-to-Income Ratio by Education")]:
    st.plotly_chart(px.bar(g,x="NAME_EDUCATION_TYPE",y=y,title=title),use_container_width=True)
