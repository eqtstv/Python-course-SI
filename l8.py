import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import keras
from datetime import datetime, timedelta
from pylab import rcParams
from matplotlib import rc
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error

sns.set(style='whitegrid', palette='muted', font_scale=1.5)
rcParams['figure.figsize'] = 16, 7

RANDOM_SEED = 44
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

def update_data(coin, date):
    d0 = datetime.today()
    d1 = datetime.strptime(date, "%Y-%m-%d")
    delta =  abs((d1 - d0).days)
    data = requests.get('https://min-api.cryptocompare.com/data/exchange/symbol/histoday?fsym={}&tsym=USD&limit={}'.format(coin, delta-1)).json()['Data']
    df =  pd.DataFrame()
    df['Volume'] = [day['volumetotal'] for day in data]
    df['Normalized_volume'] = (df['Volume']-df['Volume'].mean())/df['Volume'].std()
    df.drop('Volume', axis=1, inplace=True)
    return df

def split_data(df, split_percent=0.8):
    volume_data = df['Normalized_volume'].values
    volume_data = volume_data.reshape((-1,1))

    split_percent = split_percent
    split = int(split_percent*len(volume_data))

    volume_train = volume_data[:split]
    volume_test = volume_data[split:]
    
    return volume_train, volume_test

def create_model():
    model = Sequential()
    model.add(LSTM(128, input_shape=(look_back,1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.001))
    return model
    
def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

def plot_validation(y_train, y_test, y_pred):
    
    plt.plot(np.arange(0, len(y_train)), y_train, 'g', label="Data")
    plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_test, marker='.', label="True Volume")
    plt.plot(np.arange(len(y_train), len(y_train) + len(y_pred)), y_pred, 'r', marker='.', label="Predicted Volume", linewidth=2)
    plt.plot([], [], ' ', label="MSE: " + str(round(mean_squared_error(y_test[:-5], y_pred), 4)))
    plt.ylabel('Normalized Volume')
    plt.xlabel('Days from date entered')
    plt.legend()
    plt.show()


look_back = 5

# BTC, LTC, ETH
df = update_data('BTC', '2020-01-01')

volume_train, volume_test = split_data(df, 0.5)

train_generator = TimeseriesGenerator(volume_train, volume_train, length=look_back, batch_size=20)     
test_generator = TimeseriesGenerator(volume_test, volume_test, length=look_back, batch_size=1)

model = create_model()
model.fit_generator(train_generator, epochs=20, verbose=1, shuffle=False)

prediction = model.predict_generator(test_generator)

y_train, y_test, y_pred = volume_train.reshape((-1)), volume_test.reshape((-1)), prediction.reshape((-1))
plot_validation(y_train, y_test, y_pred)