
# Import libraries
import streamlit as st

import mysql.connector
import pandas as pd

# Setup MySQL connection
db = mysql.connector.connect(
    host="192.168.0.120",
    user="root",
    passwd="Dbnis3258!@#$",
    database="nita"
)

# Create a cursor (an instance of MySQLCursor class)
cursor = db.cursor()

# Execute SQL query
cursor.execute("SELECT * FROM Seongju_반입량_processed")

# Fetch all the rows
data = cursor.fetchall()

# Create dataframe from data
df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])

cursor.close()
db.close()




#train test split
cutoff = "2023-01-01" #데이터 분할 기준
train = df[df['ds']<cutoff]
validate = df[df['ds']>=cutoff]

st.header('Raw Data')
st.write(train)

# Initialization
if 'train' not in st.session_state:
    st.session_state['train'] = train
# Initialization
if 'df_resampled' not in st.session_state:
    st.session_state['df_resampled'] = df