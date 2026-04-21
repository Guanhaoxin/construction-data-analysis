import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('projects.csv')
engine = create_engine('mysql+pymysql://root:Ghx2005101.@localhost/construction_db')
df.to_sql('projects', engine, if_exists='replace', index=False)
print("导入成功，共", len(df), "条")
