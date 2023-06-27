import matplotlib.pyplot as plt


def create_line_chart():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    plt.plot(x, y)
    plt.title("Пример линейного графика")
    plt.xlabel("Ось x")
    plt.ylabel("Ось y")
    plt.savefig('my_chart.png')  # сохраняем график в файл


create_line_chart()