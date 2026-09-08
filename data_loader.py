import pandas as pd
from sqlalchemy import create_engine

# CSV load karein
df = pd.read_csv('sales_data.csv')

# Missing values hatayein
df = df.dropna()

# SQLite Database banayein (bina kisi installation ke)
engine = create_engine('sqlite:///database.db')

# Data ko table mein save karein
df.to_sql('sales', con=engine, if_exists='replace', index=False)
print("Database ready!")