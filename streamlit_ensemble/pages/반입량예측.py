# Read
import streamlit as st
from neuralprophet import save,load
import plotly.graph_objs as go
import numpy as np
from datetime import datetime
import pandas as pd



models = []  # An empty list to store the loaded models

for i in range(5):  # 'number_of_models' should be replaced with the number of models you have saved
    model = load(f"models/saved_model_{i}.np")  # Load the model from the file
    models.append(model)  # Add the loaded model to the list


validate = st.session_state.key
weights = [0.18077526, 0.18286206, 0.22576687, 0.18301374, 0.22758206]


future=models[1].make_future_dataframe(validate, periods=365, n_historic_predictions=200)





weights = np.array(weights)
ensemble_future = np.zeros(len(future))
for model, weight in zip(models, weights):
    forecast = model.predict(future)
    forecast_1= model.get_latest_forecast(forecast,include_history_data=True)
    forecast_1['origin-0'].fillna(0,inplace=True)

    ensemble_future += weight * forecast_1['origin-0'].values


st.header('성주참외 반입량 예측')
future['predicted'] = ensemble_future

# Create a date input widget with today's date selected by default
selected_date = st.date_input("Select a date:", value=datetime.today())

# You can access the selected date as a datetime object using `selected_date`
st.write(f"You selected {selected_date}")


future_2023 = future[future.ds.dt.year == 2023]
future_2023.reset_index(inplace=True, drop=True)

future_2023['predicted'] = future_2023['predicted'].apply(np.int64)

future_2023['predicted'] [future_2023['predicted'] <0]=0


# Filter the 'future' DataFrame to only include rows where 'ds' is greater than or equal to the selected date
future_filtered = future_2023[future_2023.ds >= pd.to_datetime(selected_date)]

trace_filtered = go.Scatter(x=future_filtered.ds, y=future_filtered['predicted'], mode='lines', name='Filtered Forecast')

# Create the figure
fig_filtered = go.Figure([trace_filtered])

# Add layout
fig_filtered.update_layout(
    title='Forecast Plot From Selected Date',
    xaxis=dict(title='Index'),
    yaxis=dict(title='Value'),
    width=1000,
    height=500,
)

# Display the plot
st.plotly_chart(fig_filtered, use_container_width=True)


st.write(future_filtered[['ds','predicted']])



# print(future.tail())




    

