import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:12345@localhost/eq_project")

try:
  connection = pymysql.connect(
      host = "localhost",
      user = "root",
      password = "12345",
      database = "eq_project",
      cursorclass = pymysql.cursors.DictCursor
  )

  print ("connected to MySQl successfully!")

except Exception as e:
  print("connection failed:", e)


import pandas as pd
df = pd.read_csv('C:/Users/Legion/Desktop/New folder/earthquake_data.csv')

df.to_sql(
    name = "earthquakes",
    con = engine,
    if_exists = "append",
    index = False
)





