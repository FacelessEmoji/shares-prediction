import math
import pandas as pd  # Для работы с таблицами данных (дата фреймы)
import requests  # Для запросов к серверу
import json  # Для обработки ответов сервера

empty_url = "http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities.json"
list_of_columns = ['OPEN', 'CLOSE', 'TRADEDATE']
result = json.loads(requests.get(empty_url).text)
data_shares = pd.DataFrame(columns=result['history']['columns'])


def change_url(share):
    assert share, f"Unfortunately, {share} is not a valid name for share."
    share_name = "/" + share.upper()
    return 'http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities' + share_name + '.json'


def check_for_amount(url):
    assert json.loads(requests.get(url).text)['history']['data'], "Input string is not a valid name for share."
    total_amount = 0
    strings = len(json.loads(requests.get(url).text)['history']['data'])
    total_amount += strings
    while strings == 100:
        updated_url = url + '?start=' + str(total_amount)
        strings = len(json.loads(requests.get(updated_url).text)['history']['data'])
        total_amount += strings
    return total_amount


def generate_requests(days, url, columns, column_names):
    flag = True
    # data = pd.DataFrame(columns=columns)
    share_life_span = check_for_amount(url)
    # print(check_for_amount(url))
    needed_amount = share_life_span - days
    assert share_life_span >= days, f"Share is trading only {share_life_span} days, but you choose {days} days. \n" \
                                    f"Please choose less than {share_life_span} days."
    assert days > 0, "Period of time must be greater than zero"
    if days <= 100:  # share_life_span % 100 != 0
        data = json.loads(requests.get(url + '?start=' + str(needed_amount)).text)['history']['data']
        return pd.DataFrame(data, columns=columns)[column_names]
    else:
        df = pd.DataFrame(columns=columns)
        while share_life_span > needed_amount:
            data = json.loads(requests.get(url + '?start=' + str(needed_amount)).text)['history']['data']
            if flag:
                df = pd.DataFrame(data, columns=columns)
                flag = False
            elif not flag:
                next_page = pd.DataFrame(data, columns=columns)
                df = pd.concat([df, next_page], ignore_index=True)
            needed_amount += 100
        return df[column_names]


def clear_nan(data: list):
    return [0 if math.isnan(x) else x for x in data]


def get_zero_indexes(data: list):
    return [index for index, value in enumerate(data) if value == 0]


def remove_elements_by_indexes(indexes: list, elements: list):
    return [element for index, element in enumerate(elements) if index not in indexes]

    # # Метод наименьших квадратов
    # print(calculate_prediction(40, prices_list))
    # # Реккуретные нейросети
    # print(share_price_prediction_deep_learning(prices_list))
    # # Метод скользящего среднего
    # print(share_price_prediction_ma(prices_list, 5))
    # # print(fact_result)
