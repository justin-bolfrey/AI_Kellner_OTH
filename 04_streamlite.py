#%%
import streamlit as st
import pandas as pd
import plotnine as p9
from create_db import get_data

st.set_page_config(page_title="OTH AI Projekt - Angewandte KI und KI Literacy", page_icon="🤙🏾",layout="wide")




#%%
st.write("# OTH AI Projekt - Angewandte KI und KI Literacy 🤙🏾")

st.write("## Step 1: Load Data")
customer, plant, shipment = get_data()

st.dataframe(customer)

st.write("## Step 2: Prepare Data")
shpm= (
    shipment
    .merge(customer, left_on='Ship-to2', right_on='ID', suffixes=('','_customer'))
    .merge(plant, left_on='Plant', right_on='ID', suffixes=('_customer','_plant'))
    .assign(del_date = lambda df: pd.to_datetime(
        df['Delivery_day'].astype(str).str.strip(),
        format="%d.%m.%Y",
        errors="coerce"
    )) 
)

data = (
    shpm
    .groupby ('del_date', as_index=False)
    .agg (
        pal = ('Pallets', lambda x: x.sum (skipna=True)),
    )
)

st.dataframe(data)


#Hier wird dann der Teil eingefügt den wir in den Stunden folgend auf den 29.10.2025 gemacht haben.

st.write("## Step 3: Visualize Data")
plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal'), color='red') +
    p9.theme_bw() +
    p9.labs(title='Pallets by Delivery Date')
)

plot.draw()
st.pyplot(plot.draw())