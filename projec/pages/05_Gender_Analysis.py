
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Gender Analysis")
st.caption("Compare credit characteristics across genders.")
df = add_common_filters(df, "p5")

g=df.groupby("CODE_GENDER",dropna=False).agg(Customers=("TARGET","size"),Defaults=("TARGET","sum"),Default_Rate=("TARGET","mean"),Avg_Income=("AMT_INCOME_TOTAL","mean"),Avg_Credit=("AMT_CREDIT","mean"),Avg_Annuity=("AMT_ANNUITY","mean")).reset_index()
g["Default_Rate"]*=100
a,b,c,d=st.columns(4)
for box,label,col in [(a,"Male Applicants","M"),(b,"Female Applicants","F")]:
    box.metric(label,f"{(df.CODE_GENDER==col).sum():,}")
a.metric("Male Default Rate",f"{g.loc[g.CODE_GENDER=="M","Default_Rate"].iloc[0]:.2f}%" if (g.CODE_GENDER=="M").any() else "—")
b.metric("Female Default Rate",f"{g.loc[g.CODE_GENDER=="F","Default_Rate"].iloc[0]:.2f}%" if (g.CODE_GENDER=="F").any() else "—")
st.plotly_chart(px.bar(g,x="CODE_GENDER",y="Default_Rate",title="Default Rate by Gender"),use_container_width=True)
st.plotly_chart(px.bar(g,x="CODE_GENDER",y="Avg_Income",title="Average Income by Gender"),use_container_width=True)
st.plotly_chart(px.bar(g,x="CODE_GENDER",y="Avg_Credit",title="Average Credit by Gender"),use_container_width=True)
st.dataframe(g,use_container_width=True)
