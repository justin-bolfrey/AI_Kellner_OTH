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

model = LinearRegression()
model.fit (X, y) 

print(" Linear Regression Model:")
print(f"Intercept: {model.intercept_}, Coefficient: {model.coef_[0]}")


# ---- Predict Future Values ----
new_days = pd.DataFrame ({'wdays': [253,254,255]})
pred_01= model.predict (new_days)
print("Predictions:" , pred_01)

plt.figure (figsize=(10, 5))
sns.lineplot(data=shpm_ts, x='del_date', y='GWkg', marker='o', label= 'Actual Values')
plt.plot(shpm_ts['del_date'], model.predict(X), color='red', label= 'Fitted Values')
plt.legend()
plt.show()

# %% -- Multiple Linear Regression

us_change = pd.read_csv("oth_data/us_change.csv", sep=";", decimal =",")

x = us_change [["Income","Production","Savings","Unemployment"]]
y = us_change ["Consumption"]

x= sm.add_constant (x)
mlr_model= sm.OLS(y,x).fit()
print(mlr_model.summary())


new_data= pd.DataFrame ({'Income': [1,2,3], 'Production': [1,2,3], 'Savings': [1,2,3], 'Unemployment': [1,2,3]})

new_data= sm.add_constant (new_data)
pred_02= mlr_model.predict (new_data)
print("Multiple Linear Regression Predictions:" , pred_02)
# %%
