import os

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

current_directory = os.path.dirname(__file__)


def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i:(i + time_steps)].values)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


def train_stock_price_prediction_model(data: list, share_name: str):
    # Load data
    df = pd.DataFrame(data, columns=['Price'])

    # Normalize data
    scaler = MinMaxScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

    # Split data into training and testing sets
    train_size = int(len(df) * 0.8)
    train_df = df[:train_size]
    test_df = df[train_size:]

    time_steps = 10
    X_train, y_train = create_dataset(train_df, train_df, time_steps)
    X_test, y_test = create_dataset(test_df, test_df, time_steps)

    model = Sequential([
        LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
        Dropout(0.2),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    # Train model
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=16,
        validation_split=0.1,
        shuffle=False
    )

    # Save model
    model.save(os.path.join(current_directory, "..", "Models", f"model_{share_name}.h5"))


def predict_stock_price(data: list, share_name: str):
    last_price = data[-1]
    # Load model
    model = load_model(os.path.join(current_directory, "..", "Models", f"model_{share_name}.h5"))

    # Load data
    df = pd.DataFrame(data, columns=['Price'])

    # Normalize data
    scaler = MinMaxScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

    time_steps = 10
    last_day = df['Price'].values[-time_steps:]
    last_day = np.reshape(last_day, (1, time_steps, 1))

    # Make predictions
    forecast = model.predict(last_day, verbose=0)

    # Rescale predictions and test data
    forecast = scaler.inverse_transform(forecast)[0][0]

    if round(forecast, 1) > round(last_price, 1):
        return f"Прогноз на завтра: {forecast:.2f}.\n" \
               f"Ожидается возрастание цены акции завтра.📈\n"
    elif round(forecast, 1) < round(last_price, 1):
        return f"Прогноз на завтра: {forecast:.2f}.\n" \
               f"Ожидается снижение цены акции завтра.📉\n"
    else:
        return f"Прогноз на завтра: {forecast:.2f}.\n" \
               f"Завтра цена акций, ожидаемо, сохранится на том же уровне.📊\n"
