import pandas as pd
from sqlalchemy import create_engine

password = input("请输入 MySQL root 密码: ")
df = pd.read_csv('projects.csv')
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/construction_db')
df.to_sql('projects', engine, if_exists='replace', index=False)
print("导入成功，共", len(df), "条记录")
