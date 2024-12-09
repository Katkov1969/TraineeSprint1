import yfinance as yf
import pandas as pd


# def fetch_stock_data(ticker, period='1mo'):
#     """
#         Загружает данные об акциях для указанного тикера и периода.
#
#         :param ticker: Тикер акции.
#         :param period: Период данных (например, '1mo', '6mo', '1y').
#         :return: DataFrame с историческими данными акций.
#     """
#     stock = yf.Ticker(ticker)
#     data = stock.history(period=period)
#     return data

def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    """
    Загружает данные об акциях для указанного тикера, периода или диапазона дат.

    :param ticker: Тикер акции.
    :param period: Период данных (например, '1mo', '6mo', '1y'). Используется, если start_date и end_date не указаны.
    :param start_date: Дата начала анализа (в формате YYYY-MM-DD).
    :param end_date: Дата окончания анализа (в формате YYYY-MM-DD).
    :return: DataFrame с историческими данными акций.
    """
    stock = yf.Ticker(ticker)

    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        data = stock.history(period=period)

    return data


def add_moving_average(data, window_size=5):
    """
        Добавляет скользящее среднее в DataFrame.

        :param data: DataFrame с данными об акциях.
        :param window_size: Окно для скользящего среднего.
        :return: DataFrame с добавленным скользящим средним.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Рассчитывает RSI (Relative Strength Index) и добавляет его в DataFrame.

    :param data: DataFrame с данными об акциях.
    :param window: Окно для расчёта RSI.
    :return: DataFrame с добавленным RSI.
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


def calculate_macd(data: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> pd.DataFrame:
    """
    Рассчитывает MACD (Moving Average Convergence Divergence) и добавляет его в DataFrame.

    :param data: DataFrame с данными об акциях.
    :param short_window: Короткий период для EMA.
    :param long_window: Длинный период для EMA.
    :param signal_window: Период для сигнальной линии.
    :return: DataFrame с добавленным MACD и сигнальной линией.
    """
    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()

    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

    return data

def calculate_atr(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Рассчитывает ATR (Average True Range) и добавляет его в DataFrame.

    :param data: DataFrame с данными об акциях.
    :param window: Окно для расчёта ATR.
    :return: DataFrame с добавленным ATR.
    """
    # Создаём сдвинутый столбец Close для предыдущего дня
    data['Close_prev'] = data['Close'].shift(1)

    # Истинный диапазон (True Range)
    data['TR'] = data.apply(
        lambda row: max(
            row['High'] - row['Low'],  # Диапазон текущего дня
            abs(row['High'] - row['Close_prev']),  # Разрыв вверх
            abs(row['Low'] - row['Close_prev'])    # Разрыв вниз
        ), axis=1
    )

    # ATR как скользящее среднее истинного диапазона
    data['ATR'] = data['TR'].rolling(window=window).mean()

    # Удаляем временный столбец Close_prev (необязательно)
    data.drop(columns=['Close_prev'], inplace=True)

    return data
