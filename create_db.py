# %% Imports
import sqlite3
import pandas as pd 

# %% Load CSVs
csv_customer = pd.read_csv("oth_data/customer.csv", sep= ";", encoding="latin-1")

csv_plant = pd.read_csv("oth_data/plant.csv", sep= ";", encoding="latin-1")

csv_shipment = pd.read_csv("oth_data/shipment.csv", sep= ";", encoding="latin-1")

csv_us_change = pd.read_csv("oth_data/us_change.csv", sep= ";", encoding="latin-1") 

# %% Write to SQLite
con = sqlite3.connect('oth_shpm.db')

csv_customer.to_sql("customer", con, if_exists="replace", index=False)

csv_plant.to_sql("plant", con, if_exists="replace", index=False)

csv_shipment.to_sql("shipment", con, if_exists="replace", index=False)

csv_us_change.to_sql("us_change", con, if_exists="replace", index=False)

print("Database created successfully")

# %% Read back
def get_data():
    con = sqlite3.connect('oth_shpm.db')

    customer =pd.read_sql_query("SELECT * FROM customer", con)
    plant =pd.read_sql_query("SELECT * FROM plant", con)
    shipment =pd.read_sql_query("SELECT * FROM shipment", con)

    con.close()

    return customer, plant, shipment

customer, plant, shipment = get_data()






# %%
