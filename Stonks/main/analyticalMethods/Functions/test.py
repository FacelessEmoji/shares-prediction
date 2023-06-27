from ..Prediction_methods.least_squares_method import calculate_prediction_least_squares
from ..Prediction_methods.moving_average_method import stock_prediction_ema
from ..Prediction_methods.recurrent_n_n_method import predict_stock_price

from .init import initialization
from .parser import list_of_columns
from .shares import test_share_ids
from .tools import list_from_csv, fisher_test, student_test

print(initialization())
for share_name in test_share_ids:
    stock_prices_open = list_from_csv(share_name, list_of_columns[0])
    stock_prices_close = list_from_csv(share_name, list_of_columns[1])
    alpha = 0.05
    print(fisher_test(stock_prices_open[-30:],
                      stock_prices_close[-30:], alpha))
    print(student_test(stock_prices_open[-10:],
                       stock_prices_close[-10:], alpha))
    print("Least Squares Method:")
    print(calculate_prediction_least_squares(stock_prices_close[-14:], 14))
    print("Exponential Moving Average: ")
    # print(share_price_prediction_ma(stock_prices, period_list[1]))
    print(stock_prediction_ema(stock_prices_open[-10:],
                               stock_prices_close[-10:]))
    print("Recurrent Neural Networks:")
    print(predict_stock_price(stock_prices_close, share_name))
