import math
import statistics


def calculate_prediction_least_squares(list_of_prices: list, period: int):
    assert period > 9, f"You choose {period} days for your period of prediction.\n" \
                       "Please choose 10 days or more for your period of prediction, otherwise it will be incorrect!"
    assert len(list_of_prices) > 9, f"You choose {len(list_of_prices)} days for your period of prediction.\n" \
                                    "Please choose 10 days or more for your period of prediction," \
                                    " otherwise it will be incorrect!"
    assert period == len(list_of_prices), f"Period of prediction is {period} days, but there are {len(list_of_prices)}" \
                                          f" prices in list. \n They must be equal!"
    x_values = [x for x in range(1, period + 1)]
    y_values = list_of_prices
    x_mean = statistics.mean(x_values)
    x_minus_x_mean = [x_values[i] - x_mean for i in range(len(x_values))]
    y_mean = statistics.mean(y_values)
    y_minus_y_mean = [y_values[i] - y_mean for i in range(len(y_values))]
    xmxm_multiply_ymym = [x_minus_x_mean[i] * y_minus_y_mean[i] for i in range(period)]
    x_minus_x_mean_squared = [x_minus_x_mean[i] ** 2 for i in range(period)]
    y_minus_y_mean_squared = [y_minus_y_mean[i] ** 2 for i in range(period)]
    list_of_sums = [sum(xmxm_multiply_ymym), sum(x_minus_x_mean_squared),
                    sum(y_minus_y_mean_squared)]
    s_x_squared = list_of_sums[1] / period
    s_y_squared = list_of_sums[2] / period
    k_x_y = list_of_sums[0] / period
    r_x_y = k_x_y / (math.sqrt(s_x_squared * s_y_squared))
    k = r_x_y * (math.sqrt(s_y_squared / s_x_squared))
    b = y_mean - (k * x_mean)
    if k > 0:
        trend_signal = "Ожидается возрастание цены акции завтра.📈\n"
    elif k < 0:
        trend_signal = "Ожидается снижение цены акции завтра.📉\n"
    else:
        trend_signal = "Завтра цена акций, ожидаемо, сохранится на том же уровне.📊\n"
    # print(trend_signal)
    if r_x_y < -0.7:
        confidence_signal = "Ожидается снижение цены акции завтра.📉\n"
    elif r_x_y > 0.7:
        confidence_signal = "Ожидается возрастание цены акции завтра.📈\n"
    else:
        confidence_signal = "Завтра цена акций, ожидаемо, сохранится на том же уровне.📊\n"
    # print(confidence_signal)
    if trend_signal == confidence_signal:
        result_signal = trend_signal
    else:
        result_signal = "Завтра цена акций, ожидаемо, сохранится на том же уровне.📊\n"
    # print(result_signal)
    return result_signal
