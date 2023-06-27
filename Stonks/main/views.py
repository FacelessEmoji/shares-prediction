from django.shortcuts import render
from .analyticalMethods.Functions.tools import *
from .analyticalMethods.Functions.init import *
from .analyticalMethods.Functions.shares import *

def info(request):
    return render(request, 'main/info.html', {"shares": test_share_ids})

def sharePage(request, share_name):
    x = list_from_csv(test_share_ids[test_share_ids.index(share_name)], list_of_columns[0])[-10:]
    y = list_from_csv(test_share_ids[test_share_ids.index(share_name)], list_of_columns[1])[-10:]
    z = list_from_csv(test_share_ids[test_share_ids.index(share_name)], list_of_columns[2])[-10:]
    data = [z.replace('2023-', '') for z in z]

    share_dict = get_graphic_data(x,y)


    stock_prices = list_from_csv(share_name, list_of_columns[1])

    fisher_test_result = (fisher_test(list_from_csv(share_name, list_of_columns[0])[-30:],
                                      list_from_csv(share_name, list_of_columns[1])[-30:], 0.05))
    student_test_result = (student_test(list_from_csv(share_name, list_of_columns[0])[-10:],
                                        list_from_csv(share_name, list_of_columns[1])[-10:], 0.05))
    LeastSquaresMethod = calculate_prediction_least_squares(stock_prices[-14:], period_list[0])
    MovAv = stock_prediction_ema(list_from_csv(share_name, list_of_columns[0])[-10:],
                                 list_from_csv(share_name, list_of_columns[1])[-10:])

    RecurrentNeuralNetworks = predict_stock_price(stock_prices, share_name)

    return render(request, 'main/shareInfoPage.html', {"share": share_name, "list1": x, "list2": y, "dd": data,
                                                       "fisher": fisher_test_result, "student": student_test_result,
                                                       "leastSq": LeastSquaresMethod, "MovAv": MovAv,
                                                       "RNN": RecurrentNeuralNetworks,
                                                       "shares": test_share_ids,
                                                       "share_info": test_share_descriptions[share_name],"ema":share_dict['EMA'],"x":share_dict['X']})


def faqPage(request):
    return render(request,'main/faq.html')

def aboutUsPage(requset):
    return render(requset,'main/aboutUs.html')



def init(request):
    initialization()

    return render(request,'main/init.html')




