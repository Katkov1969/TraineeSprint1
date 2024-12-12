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


def calculate_average_close(data):
    """
    Вычисляет среднее значение цены закрытия и выводит результат в консоль.

    :param data: DataFrame с данными об акциях.
    :return: None
    """
    if 'Close' not in data:
        raise ValueError("В данных отсутствует колонка 'Close' для расчета среднего значения.")

    average_close = data['Close'].mean()
    print(f"Среднее значение цены закрытия: {average_close:.2f}")
    return average_close