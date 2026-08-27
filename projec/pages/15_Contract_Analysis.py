
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Contract Type Analysis")
st.caption("Analyze loan applications by contract type.")
df = add_common_filters(df, "p15")

g=df.groupby("NAME_CONTRACT_TYPE").agg(Applications=("TARGET","size"),Default_Rate=("TARGET","mean"),Avg_Credit=("AMT_CREDIT","mean"),Avg_Income=("AMT_INCOME_TOTAL","mean"),Avg_Annuity=("AMT_ANNUITY","mean"),Avg_CIR=("CREDIT_INCOME_RATIO","mean")).reset_index()
g["Default_Rate"]*=100
a,b,c,d=st.columns(4)
for box,label,row in [(a,"Cash Loan Applications","Cash loans"),(b,"Revolving Loan Applications","Revolving loans")]:
    v=g.loc[g.NAME_CONTRACT_TYPE==row,"Applications"]
    box.metric(label,f"{int(v.iloc[0]):,}" if len(v) else "0")
for row,label,box in [("Cash loans","Cash Loan Default Rate",c),("Revolving loans","Revolving Loan Default Rate",d)]:
    v=g.loc[g.NAME_CONTRACT_TYPE==row,"Default_Rate"]
    box.metric(label,f"{v.iloc[0]:.2f}%" if len(v) else "—")
for y,title in [("Applications","Applications by Contract Type"),("Default_Rate","Default Rate by Contract Type"),("Avg_Credit","Average Credit by Contract Type"),("Avg_Income","Average Income by Contract Type"),("Avg_Annuity","Average Annuity by Contract Type"),("Avg_CIR","Credit-to-Income Ratio by Contract Type")]:
    st.plotly_chart(px.bar(g,x="NAME_CONTRACT_TYPE",y=y,title=title),use_container_width=True)
