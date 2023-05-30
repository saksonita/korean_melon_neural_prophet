
# Import libraries
import streamlit as st

import mysql.connector
import pandas as pd
# Read
import streamlit as st
from neuralprophet import save,load
import plotly.express as px

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

st.header('원시 데이터')
st.write(df)

st.header('성주참외 반입량')

# Plot!
fig = px.line(df, x='ds', y="y")
st.plotly_chart(fig, use_container_width=True)


print(validate)


# # Initialization
# if 'train' not in st.session_state:
#     st.session_state['train'] = train
# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = train


# # Initialization
# if 'df_resampled' not in st.session_state:
#     st.session_state['df_resampled'] = df