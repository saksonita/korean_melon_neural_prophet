# Read
import streamlit as st
from neuralprophet import save


train = st.session_state['train']

import numpy as np
import pandas as pd
from neuralprophet import NeuralProphet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# Define base Neural Prophet models with different configurations
models = [
NeuralProphet(
    growth='linear',
    n_lags=8, 
    n_forecasts=30*12,
    seasonality_mode='additive',
    n_changepoints=50,
    # num_hidden_layers=3,
    weekly_seasonality='auto',
    yearly_seasonality=True, 
    daily_seasonality=False, 
    normalize='minmax',
    # d_hidden=64, 
    learning_rate=0.03,
    batch_size=45,
    ),
    NeuralProphet(n_lags=10, learning_rate=0.001),
    NeuralProphet(n_lags=20, learning_rate=0.001),
    NeuralProphet(n_lags=10, learning_rate=0.01),
    NeuralProphet(n_lags=20, learning_rate=0.01),
]

# Create a progress bar
progress_bar = st.progress(0)

# Train the base models
for i, model in enumerate(models):
     # Update the progress bar with each iteration
    progress_bar.progress((i + 1) / len(models))
    model.fit(train, freq='D', epochs=200)
    save(model, "test_save_model.np")
    
# Complete the progress bar
progress_bar.progress(1)

