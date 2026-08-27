
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Customer Risk Explorer")
st.caption("Explore individual customers and filtered applicant records.")
df = add_common_filters(df, "p20")

st.subheader("Customer Search")
if "SK_ID_CURR" in df:
    q=st.text_input("Search SK_ID_CURR")
    if q.strip():
        try:
            sid=int(q.strip())
            match=df[df.SK_ID_CURR==sid]
        except:
            match=df.iloc[0:0]
    else:
        match=df.iloc[0:0]
else:
    match=df.iloc[0:0]

if len(match):
    row=match.iloc[0]
    st.success(f"Customer {row.SK_ID_CURR} found")
    a,b,c,d=st.columns(4)
    a.metric("TARGET",int(row.TARGET))
    b.metric("Age",f"{row.AGE:.1f}")
    c.metric("Income",f"{row.AMT_INCOME_TOTAL:,.0f}")
    d.metric("Credit",f"{row.AMT_CREDIT:,.0f}")
    profile_cols=[c for c in ["SK_ID_CURR","TARGET","AGE","CODE_GENDER","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY","NAME_EDUCATION_TYPE","OCCUPATION_TYPE","NAME_FAMILY_STATUS","CNT_CHILDREN","NAME_HOUSING_TYPE","EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3","AVERAGE_EXTERNAL_SCORE","CREDIT_INCOME_RATIO","ANNUITY_INCOME_RATIO","CREDIT_GOODS_RATIO","EMPLOYMENT_YEARS"] if c in df.columns]
    st.dataframe(match[profile_cols].T.rename(columns={match.index[0]:"Value"}),use_container_width=True)
else:
    st.info("Enter an SK_ID_CURR to view a customer profile.")

st.subheader("Filtered Applicant Data")
st.dataframe(df.head(500),use_container_width=True)

def csv_bytes(x):
    return x.to_csv(index=False).encode("utf-8")

c1,c2,c3,c4=st.columns(4)
c1.download_button("Download Filtered Customers",csv_bytes(df),"filtered_customers.csv","text/csv")
defaults=df[df.TARGET==1] if "TARGET" in df else df.iloc[0:0]
c2.download_button("Download Default Customers",csv_bytes(defaults),"default_customers.csv","text/csv")
high=df[df.CREDIT_INCOME_RATIO>6] if "CREDIT_INCOME_RATIO" in df else df.iloc[0:0]
c3.download_button("Download High-Risk Customers",csv_bytes(high),"high_risk_customers.csv","text/csv")
summary=pd.DataFrame({"Metric":["Applications","Defaults","Default Rate %","Average Income","Average Credit"],"Value":[len(df),int((df.TARGET==1).sum()),df.TARGET.mean()*100,df.AMT_INCOME_TOTAL.mean(),df.AMT_CREDIT.mean()]})
c4.download_button("Download Summary CSV",csv_bytes(summary),"summary.csv","text/csv")
