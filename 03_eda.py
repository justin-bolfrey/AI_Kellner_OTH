#%%
import sqlite3
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
eda_shpm_to= shpm.assign(tons=shpm['GWkg']/1000)
# %%
eda_temp = (
    eda_shpm_to
    .groupby('Plant', as_index=False)
    .agg (to=('tons', 'sum'))
    )
# %%
eda_temp_wider= eda_temp.pivot_table(index=None, columns='Plant', values='to').reset_index(drop=True)


# %%
eda_temp_longer = eda_temp_wider.melt(var_name='Plant', value_name='to')


# %%
eda_temp = (
    shpm
    .groupby ('del_date', as_index=False)
    .agg (pal = ('Pallets', lambda x: x.sum (skipna=True)))
)
eda_temp

# %%
eda_temp = (
    shpm
    .groupby (['del_date', 'Plant'], as_index=False)
    .agg (pal = ('Pallets', lambda x: x.sum (skipna=True)))
)

# %%
sum_gwkg = shpm ['GWkg'].sum()
min_gwkg = shpm ['GWkg'].min()
avg_gwkg = shpm ['GWkg'].mean()
max_gwkg = shpm ['GWkg'].max()

print( f"Sum of GWkg: {sum_gwkg}")
print( f"Min of GWkg: {min_gwkg}")
print( f"Mean of GWkg: {avg_gwkg}")
print( f"Max of GWkg: {max_gwkg}")

# %%
eda_temp = (
    eda_shpm_to
    .groupby('Plant', as_index=False)
    .agg (
        sum_to=('tons', lambda x: x.sum (skipna=True)),
        min_to=('tons', lambda x: x.min (skipna=True)),
        avg_to=('tons', lambda x: x.mean (skipna=True)),
        max_to=('tons', lambda x: x.max (skipna=True))
    )
)
eda_temp 

# %%
eda_temp.to_csv('eda_temp.csv', decimal=',' , sep =';' , index=False)
# %%
data = (
    shpm
    .groupby ('del_date', as_index=False)
    .agg (
        pal = ('Pallets', lambda x: x.sum (skipna=True)),
    )
)
data


# %%
plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal'), color='red') +
    p9.theme_bw() +
    p9.labs(x='Delivery Date', y='Pallets', title='Pallets by Delivery Date')
    
)

plot.draw()
# %%
data = (
    shpm
    .groupby (['del_date', 'Plant'], as_index=False)
    .agg (
        pal = ('Pallets', lambda x: x.sum (skipna=True)),
    )
)







plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal', color='Plant')) +
    p9.theme_bw() +
    p9.labs(x='Delivery Date', y='Pallets', title='Pallets by Delivery Date')
    
)

plot.draw()
# %%
plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal', color='Plant')) +
    p9.theme_bw() +
    p9.labs(x='Delivery Date', y='Pallets', title='Pallets by Delivery Date') +
    p9.facet_wrap('Plant', nrow=1)
)

plot.draw()
# %%
plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal')) +
    p9.theme_bw() +
    p9.labs(x='Delivery Date', y='Pallets', title='Pallets by Delivery Date') +
    p9.facet_wrap('Plant', nrow=1) +
    p9.geom_point( p9.aes(x='del_date', y='pal'), color = 'green')
)

plot.draw()
# %%
plot = (
    p9.ggplot(data) +
    p9.geom_line( p9.aes(x='del_date', y='pal')) +
    p9.theme_bw() +
    p9.labs(x='Delivery Date', y='Pallets', title='Pallets by Delivery Date') +
    p9.facet_wrap('Plant', nrow=1) +
    p9.geom_point( p9.aes(x='del_date', y='pal'), color = 'green') +
    p9.geom_violin( p9.aes(x='del_date', y='pal'), fill = 'blue', alpha = 0.5)
)

plot.draw()
# %%
