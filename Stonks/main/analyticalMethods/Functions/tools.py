import os
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import f, ttest_ind


from ..Prediction_methods.least_squares_method import calculate_prediction_least_squares
from ..Prediction_methods.moving_average_method import stock_prediction_ema
from ..Prediction_methods.recurrent_n_n_method import predict_stock_price

from .parser import list_of_columns
from .shares import period_list

current_directory = os.path.dirname(__file__)


def is_deprecated(minutes: int):
    if minutes < 24 * 60:
        # print("Файл актуален.")
        return False
    elif minutes >= 24 * 60:
        # print("Файл не актуален.")
        return True
    # if minutes < 1:
    #     # print("Файл актуален.")
    #     return False
    # elif minutes >= 1:
    #     # print("Файл не актуален.")
    #     return True


def check_for_deprecation(share: str, path: str, file_type: str):
    # Получаем текущую дату и время
    current_date = datetime.now()
    # получаем информацию о файле
    file_info = os.stat(path)
    # извлекаем дату последнего изменения файла из информации о файле
    last_modified_timestamp = file_info.st_mtime
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)

    delta = int((current_date - last_modified_date).total_seconds() / 60)
    # конвертируем временную метку в человеко-читаемый формат
    # last_modified_time_csv = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_modified_timestamp_csv))
    # last_modified_time_h5 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_modified_timestamp_h5))
    # print(f"Дата последнего изменения файла {share}.csv: ", last_modified_time_csv)
    # print(f"Дата последнего изменения файла model_{share}.h5 ", last_modified_time_h5)
    if file_type == "csv":
        print(f"Количество минут c последнего изменения файла {share}.csv: ", delta)
    elif file_type == "h5":
        print(f"Количество минут c последнего изменения файла model_{share}.h5 ", delta)
    elif file_type == "png":
        print(f"Количество минут c последнего изменения файла {share}.png: ", delta)
    return delta


def list_from_csv(share_name: str, column_name: str):
    return pd.read_csv(os.path.join(current_directory, "..", "Shares", f"{share_name}.csv"))[column_name].tolist()


def fisher_test(open_prices: list, close_prices: list, alpha: float):
    n = len(open_prices)
    dfn, dfd = n - 1, n - 2  # степени свободы для числителя и знаменателя соответственно
    s1 = np.std(open_prices, ddof=1)
    s2 = np.std(close_prices, ddof=1)
    f_stat = (s1 ** 2) / (s2 ** 2)
    p_val = 1 - f.cdf(f_stat, dfn, dfd)  # p-value
    if p_val > alpha:
        return f"Метод Фишера: Дисперсии выборок не отличаются друг от друга. Акция стабильна.✅"
    else:
        return f"Метод Фишера: Дисперсии выборок отличаются друг от друга. Акция нестабильна.❌"


def student_test(open_prices: list, close_prices: list, alpha: float):
    # Вычисляем средние значения для двух выборок
    mean_start = np.mean(open_prices)
    mean_end = np.mean(close_prices)

    # Вычисляем стандартное отклонение для каждой выборки
    std_start = np.std(open_prices)
    std_end = np.std(close_prices)

    # Вычисляем t-статистику
    t_statistic = (mean_start - mean_end) / np.sqrt(
        (std_start ** 2 / len(open_prices)) + (std_end ** 2 / len(close_prices)))

    # Вычисляем количество степеней свободы
    degrees_of_freedom = len(open_prices) + len(close_prices) - 2

    # Определяем критическое значение для выбранного уровня значимости (например, 0.05)
    critical_value = ttest_ind(open_prices, close_prices, equal_var=False)[1] / 2

    # Сравниваем t-статистику с критическим значением
    if abs(t_statistic) > critical_value:
        return "Метод Стьюдента: Акция нестабильна❌\n"
    else:
        return "Метод Стьюдента: Акция стабильна✅\n"


def get_graphic_data(start_prices: list, end_prices: list):
    ema_array = pd.Series(end_prices).ewm(alpha=0.5, adjust=False).mean().to_numpy().tolist()
    x_array = [i for i in range(1, len(start_prices) + 1)]
    data_dict = {
        'EMA': ema_array,
        'X': x_array
    }
    return data_dict


# Пример
# print(get_graphic_data(stock_prices_open[-10:],
#                        stock_prices_close[-10:]))

#
# def save_image(start_prices: list, end_prices: list, path: str):
#     # Собираем датафрейм из массивов цен начала и конца торгов
#     df = pd.DataFrame({'Start Prices': start_prices, 'End Prices': end_prices})
#     # Вычисляем EMA
#     df['EMA'] = df['End Prices'].ewm(alpha=0.5, adjust=False).mean()
#     # Строим график цен акций и EMA
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['Start Prices'], label='Start Prices')
#     plt.plot(df['End Prices'], label='End Prices')
#     plt.plot(df['EMA'], label='EMA')
#     plt.legend()
#     plt.title('Stock Prices with EMA')
#     plt.savefig(path)


def get_prediction(share_name: str):
    # можно добавить альфу чтобы можно было менять и возможно колонки по которым считают нн и квадраты
    try:
        stock_prices = list_from_csv(share_name, list_of_columns[1])
        student_stability = student_test(list_from_csv(share_name, list_of_columns[0])[-10:],
                                         list_from_csv(share_name, list_of_columns[1])[-10:], 0.05)
        fisher_stability = fisher_test(list_from_csv(share_name, list_of_columns[0])[-30:],
                                       list_from_csv(share_name, list_of_columns[1])[-30:], 0.05)
        least_squares_method_prediction = calculate_prediction_least_squares(stock_prices, period_list[0])
        ema_method_prediction = stock_prediction_ema(list_from_csv(share_name, list_of_columns[0])[-10:],
                                                     list_from_csv(share_name, list_of_columns[1])[-10:])
        recurrent_nn_method_prediction = predict_stock_price(stock_prices, share_name)
    except Exception:
        return False
    else:
        return True

# примеры
# print(list_from_csv(test_share_ids[0], list_of_columns[1]))
#
# for column in list_of_columns:
#     print(list_from_csv(test_share_ids[0], column))
