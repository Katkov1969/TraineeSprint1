import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None, style="default"):
    """
    Создаёт график с отображением цены закрытия, скользящего среднего, RSI и MACD.

    :param data: DataFrame с данными об акциях.
    :param ticker: Тикер акции.
    :param period: Период данных.
    :param filename: Имя файла для сохранения графика.
    :param style: Стиль оформления графика (например, 'seaborn', 'ggplot', 'default').
    :return: None.
    """
    # Применяем стиль графика
    try:
        plt.style.use(style)
    except ValueError:
        print(f"Предупреждение: Стиль '{style}' не найден. Используется стиль по умолчанию.")
        plt.style.use("default")

    plt.figure(figsize=(12, 10))
    # График цен и скользящего среднего
    plt.subplot(4, 1, 1)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()
    plt.grid(True)

    # График RSI
    if 'RSI' in data:
        plt.subplot(4, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI', color='orange')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.title(f"{ticker} - RSI (Relative Strength Index)")
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()
        plt.grid(True)

    # График MACD
    if 'MACD' in data and 'Signal_Line' in data:
        plt.subplot(4, 1, 3)
        plt.plot(data.index, data['MACD'], label='MACD', color='blue')
        plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
        plt.title(f"{ticker} - MACD (Moving Average Convergence Divergence)")
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()
        plt.grid(True)

    # График ATR
    if 'ATR' in data:
        plt.subplot(4, 1, 4)
        plt.plot(data.index, data['ATR'], label='ATR', color='brown')
        plt.title(f"{ticker} - ATR (Average True Range)")
        plt.xlabel("Дата")
        plt.ylabel("ATR")
        plt.legend()
        plt.grid(True)

    #Сохранение    графика
    if filename is None:
        filename = f"{ticker}_{period}_indicators_chart.png"
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранён как {filename}")

