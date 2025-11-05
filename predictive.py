#%% ---- Load Packages ----
import sqlite3 #Daten einholen

import pandas as pd #Daten analysieren
import numpy as np #Daten analysieren

import matplotlib.pyplot as plt #Daten visualisieren
import seaborn as sns #Daten visualisieren
import plotly.express as px #Daten visualisieren
import plotly.graph_objects as go #Daten visualisieren

from datetime import datetime #Daten formatieren

from sklearn.linear_model import LinearRegression #Machine Learning
import statsmodels.api as sm  #Statistische Modelle
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing #Time Series Analysis
import statsmodels.tsa.api as tsa #Time Series Analysis 


# %%
# ---- Get Data from Database ----
con = sqlite3.connect('oth_shpm.db')

customer = pd.read_sql_query("SELECT * FROM customer", con)
plant = pd.read_sql_query("SELECT * FROM plant", con)
shipment = pd.read_sql_query("SELECT * FROM shipment", con)

con.close()

# %% ---- Data wrangling ----
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

shpm_ts = (
    shpm
    .groupby ('del_date', as_index=False)
    .agg ( GWkg = ('GWkg', lambda x: x.sum (skipna=True)))
)


plt.figure (figsize=(10, 5))
sns.lineplot(data=shpm_ts, x='del_date', y='GWkg', marker='o')


# %% ---- Simple Linear Regression ----
shpm_ts['wdays'] = np.arange(1, len(shpm_ts)+1)

y = shpm_ts['GWkg']
X= shpm_ts [['wdays']]
# %%
