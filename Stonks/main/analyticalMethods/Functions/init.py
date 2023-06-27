import os
from ..Prediction_methods.recurrent_n_n_method import train_stock_price_prediction_model
from .parser import generate_requests, change_url, list_of_columns, clear_nan, result, get_zero_indexes
from .shares import test_share_ids
from .tools import list_from_csv, is_deprecated, check_for_deprecation

current_directory = os.path.dirname(__file__)


def initialization():
    for share in test_share_ids:
        csv_path = os.path.join(current_directory, "..", "Shares", f"{share}.csv")
        h5_path = os.path.join(current_directory, "..", "Models", f"model_{share}.h5")
        # png_path = os.path.join(current_directory, "..", "Images", f"{share}.png")
        # csv
        if os.path.isfile(csv_path):
            if is_deprecated(check_for_deprecation(share, csv_path, "csv")):
                os.remove(csv_path)
        if not os.path.isfile(csv_path):
            dataframe = generate_requests(2000, change_url(share), result['history']['columns'], list_of_columns)
            prices_list_open = clear_nan(dataframe['OPEN'].values.tolist())
            zero_list = get_zero_indexes(prices_list_open)
            for column in range(len(zero_list)):
                dataframe = dataframe.drop(index=zero_list[column])
            dataframe.to_csv(csv_path)
        print(f"{share}.csv создан и актуален.")
        # png
        # if os.path.isfile(png_path):
        #     if is_deprecated(check_for_deprecation(share, png_path, "png")):
        #         os.remove(png_path)
        # if not os.path.isfile(png_path):
        #     save_image(list_from_csv(share, list_of_columns[0])[-10:],
        #                list_from_csv(share, list_of_columns[1])[-10:], png_path)
        # print(f"{share}.png уже создан и актуален.")
        # h5
        if os.path.isfile(h5_path):
            if is_deprecated(check_for_deprecation(share, h5_path, "h5")):
                os.remove(h5_path)
        if not os.path.isfile(h5_path):
            # list_from_csv(share_name, list_of_columns[1])
            train_stock_price_prediction_model(
                list_from_csv(share, list_of_columns[1]), share)
        print(f"model_{share}.h5 создан и актуален.")

    return "Инициализация необходимых файлов завершена. \n"
