import pandas as pd

def calculate_indicators(data):
    """
    Рассчитывает дополнительные статистические индикаторы, такие как стандартное отклонение цены закрытия.

    :param data: DataFrame с данными об акциях.
    :return: DataFrame с добавленными индикаторами.
    """
    # Проверяем, есть ли колонка 'Close' в данных
    if 'Close' not in data:
        raise ValueError("В данных отсутствует колонка 'Close' для расчета индикаторов.")

    # Рассчитываем стандартное отклонение цены закрытия за скользящее окно (например, 20 дней)
    data['Std_Dev_Close'] = data['Close'].rolling(window=20).std()

    # Рассчитываем среднее (mean) цены закрытия за скользящее окно для сравнения
    data['Mean_Close'] = data['Close'].rolling(window=20).mean()

    return data