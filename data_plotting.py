import matplotlib.pyplot as plt
import plotly.graph_objects as go


def create_and_save_plot(data, ticker, period, filename=None, style="default"):
    """
    Создаёт график с отображением цены закрытия, скользящего среднего, RSI, MACD и стандартного отклонения.

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

    plt.figure(figsize=(12, 12))

    # График цен и скользящего среднего
    plt.subplot(5, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price')
    if 'Moving_Average' in data:
        plt.plot(data.index, data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()
    plt.grid(True)

    # График RSI
    if 'RSI' in data:
        plt.subplot(5, 1, 2)
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
        plt.subplot(5, 1, 3)
        plt.plot(data.index, data['MACD'], label='MACD', color='blue')
        plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
        plt.title(f"{ticker} - MACD (Moving Average Convergence Divergence)")
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()
        plt.grid(True)

    # График стандартного отклонения
    if 'Std_Dev_Close' in data:
        plt.subplot(5, 1, 4)
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.plot(data.index, data['Mean_Close'], label='Mean Close (20)', color='green')
        plt.fill_between(data.index,
                         data['Mean_Close'] - data['Std_Dev_Close'],
                         data['Mean_Close'] + data['Std_Dev_Close'],
                         color='gray', alpha=0.3, label='Std Dev (20)')
        plt.title(f"{ticker} - Стандартное отклонение цены закрытия (20 дней)")
        plt.xlabel("Дата")
        plt.ylabel("Цена")
        plt.legend()
        plt.grid(True)

    # График ATR (если он есть)
    if 'ATR' in data:
        plt.subplot(5, 1, 5)
        plt.plot(data.index, data['ATR'], label='ATR', color='brown')
        plt.title(f"{ticker} - ATR (Average True Range)")
        plt.xlabel("Дата")
        plt.ylabel("ATR")
        plt.legend()
        plt.grid(True)

    # Сохранение графика
    if filename is None:
        filename = f"{ticker}_{period}_indicators_chart.png"
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранён как {filename}")

def create_interactive_plot(data, ticker):
    """
    Создаёт интерактивный график с использованием Plotly.

    :param data: DataFrame с данными об акциях.
    :param ticker: Тикер акции.
    :return: None (открывает интерактивный график в браузере).
    """
    if 'Close' not in data:
        raise ValueError("В данных отсутствует колонка 'Close' для построения графика.")

    fig = go.Figure()

    # Добавляем линию цены закрытия
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price'
    ))

    # Добавляем скользящее среднее, если оно есть
    if 'Mean_Close' in data:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Mean_Close'],
            mode='lines',
            name='Moving Average (20 days)',
            line=dict(dash='dash', color='orange')
        ))

    # Настройка графика
    fig.update_layout(
        title=f"Интерактивный график акций {ticker}",
        xaxis_title="Дата",
        yaxis_title="Цена",
        template="plotly_white"
    )

    # Отображаем график
    fig.show()
