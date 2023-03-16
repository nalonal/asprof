import mysql.connector
conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="2wsx@WSX1qazZAQ!",
                port=13306
        )
curr = conn.cursor()
curr.execute("CREATE DATABASE IF NOT EXISTS asprof_db")
conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2wsx@WSX1qazZAQ!",
        port=13306,
        database = "asprof_db"
)
curr = conn.cursor()
curr.execute('''CREATE TABLE IF NOT EXISTS scimago_tb(
   Rank                INTEGER  NOT NULL PRIMARY KEY 
  ,Sourceid            TEXT
  ,Title               TEXT
  ,Type                TEXT
  ,Issn                TEXT
  ,SJR                 TEXT
  ,SJR_Best_Quartile   TEXT
  ,H_index             INTEGER
  ,Total_Docs_3years   INTEGER
  ,Total_Docs_2021     INTEGER
  ,Total_Refs          INTEGER
  ,Total_Cites_3years  INTEGER
  ,Citable_Docs_3years INTEGER
  ,Cites_Doc_2years    TEXT
  ,Ref_Doc             TEXT
  ,Country             TEXT
  ,Region              TEXT
  ,Publisher           TEXT
  ,Coverage            TEXT
  ,Categories          TEXT
  ,Areas               TEXT
);''')

import pandas as pd
data = pd.read_csv("scimagojr_tb.csv", delimiter= ';')
data = data.fillna("-")

for index, row in data.iterrows():
    curr.execute('INSERT INTO scimago_tb(Rank,Sourceid,Title,Type,Issn,SJR,SJR_Best_Quartile,H_index,Total_Docs_2021,Total_Docs_3years,Total_Refs,Total_Cites_3years,Citable_Docs_3years,Cites_Doc_2years,Ref_Doc,Country,Region,Publisher,Coverage,Categories,Areas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',(row['Rank'],row['Sourceid'],row['Title'],row['Type'],row['Issn'],row['SJR'],row['SJR Best Quartile'],row['H index'],row['Total Docs. (2021)'],row['Total Docs. (3years)'],row['Total Refs.'],row['Total Cites (3years)'],row['Citable Docs. (3years)'],row['Cites / Doc. (2years)'],row['Ref. / Doc.'],row['Country'],row['Region'],row['Publisher'],row['Coverage'],row['Categories'],row['Areas']))
    conn.commit()
