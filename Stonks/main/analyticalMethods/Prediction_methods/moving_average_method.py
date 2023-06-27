import pandas as pd


def stock_prediction_ema(start_prices: list, end_prices: list, alpha=0.5, plot=False):
    # plot = True для показа графика
    last_price = end_prices[-1]
    # Собираем датафрейм из массивов цен начала и конца торгов
    df = pd.DataFrame({'Start Prices': start_prices, 'End Prices': end_prices})
    # Вычисляем изменение цены акций за каждый день
    df['Price Change'] = df['End Prices'] - df['Start Prices']
    # Вычисляем EMA
    df['EMA'] = df['End Prices'].ewm(alpha=alpha, adjust=False).mean()
    # Вычисляем среднее изменение цены акций
    mean_change = df['Price Change'].mean()
    # Вычисляем предсказание цены акций на следующий день
    prediction = df['EMA'].iloc[-1] + mean_change
    # if plot:
    #     # Строим график цен акций и EMA
    #     plt.figure(figsize=(10, 5))
    #     plt.plot(df['Start Prices'], label='Start Prices')
    #     plt.plot(df['End Prices'], label='End Prices')
    #     plt.plot(df['EMA'], label='EMA')
    #     plt.legend()
    #     plt.title('Stock Prices with EMA')
    #     plt.show()
    if round(prediction, 1) > round(last_price, 1):
        return f"Прогноз на завтра: {prediction:.2f}.\n" \
               f"Ожидается возрастание цены акции завтра.📈\n"
    elif round(prediction, 1) < round(last_price, 1):
        return f"Прогноз на завтра: {prediction:.2f}.\n" \
               f"Ожидается снижение цены акции завтра.📉\n"
    else:
        return f"Прогноз на завтра: {prediction:.2f}.\n" \
               f"Завтра цена акций, ожидаемо, сохранится на том же уровне.📊\n"

# выводить цену и итоговый прогноз


# def stock_price_prediction_ma(stock_prices: list, period: int):
#     # Вычисляем скользящее среднее за указанный период
#     ma = np.mean(stock_prices[-period:])
#
#     # Получаем последнюю известную цену
#     last_price = stock_prices[-1]
#
#     # Вычисляем прогноз на следующий день
#     next_day_forecast = ma
#
#     # Сравниваем прогноз и последнюю известную цену
#     if next_day_forecast > last_price:
#         return f"The stock price is expected to increase tomorrow.\n"
#     elif next_day_forecast < last_price:
#         return f"The stock price is expected to decrease tomorrow.\n"
#     else:
#         return f"The stock price is expected to stay the same tomorrow.\n"
#     # скользящее среднее по 7 и 14 дням и так выдавать прогноз,посмотреть как???
