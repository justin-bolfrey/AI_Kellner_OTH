#%%
import pandas as pd
import plotnine as p9 
from create_db import get_data

customer, plant, shipment = get_data()



# %%
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

# %%
shpm.head(5)


# %%
shpm.tail(10)


# %%
shpm.info()


# %%
eda_plant = shpm [['Plant']].drop_duplicates()


#%%
filtered_shpm = shpm[shpm['Plant'] == 'DE17']
# %%
eda_shpm_tons= shpm.assign(tons=shpm['GWkg']/1000)
# %%
