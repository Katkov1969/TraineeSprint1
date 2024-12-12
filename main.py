import data_download as dd
import data_plotting as dplt
import pandas as pd
import data_processing as dp



def calculate_and_display_average_price(data: 'pd.DataFrame') -> None:
    """
    Вычисляет и выводит среднюю цену закрытия акций за заданный период.

    :param data: DataFrame с данными об акциях, который должен содержать колонку 'Close'.
    :return: None. Результат выводится в консоль.
    """
    if 'Close' not in data:
        print("Ошибка: В переданном DataFrame отсутствует колонка 'Close'.")
        return

    # Вычисляем среднюю цену закрытия
    average_price = data['Close'].mean()

    # Выводим результат в консоль
    print(f"Средняя цена закрытия за заданный период: {average_price:.2f}")

def notify_if_strong_fluctuations(data: pd.DataFrame, threshold: float) -> None:
    """
    Анализирует данные и уведомляет пользователя, если разница между максимальной и минимальной
    ценой закрытия превышает заданный порог.

    :param data: DataFrame с данными об акциях, который должен содержать колонку 'Close'.
    :param threshold: Процентный порог, при превышении которого выводится уведомление.
    :return: None. Уведомление выводится в консоль.
    """
    if 'Close' not in data:
        print("Ошибка: В переданном DataFrame отсутствует колонка 'Close'.")
        return

    # Вычисляем максимальную и минимальную цену закрытия
    max_close = data['Close'].max()
    min_close = data['Close'].min()

    # Вычисляем разницу в процентах
    fluctuation = ((max_close - min_close) / min_close) * 100

    # Выводим разницу на консоль
    print(f"Разница между максимальной и минимальной ценой закрытия: {fluctuation:.2f}%")

    # Проверяем, превышает ли разница порог
    if fluctuation > threshold:
        print("Превышен порог колебаний цены акций!")
    else:
        print("Порог колебаний цены НЕ превышен!")


def export_data_to_csv(data: pd.DataFrame, filename: str) -> None:
    """
    Сохраняет данные об акциях в файл в формате CSV.

    :param data: DataFrame с данными об акциях.
    :param filename: Имя файла, куда будут сохранены данные.
    :return: None. Данные сохраняются в указанный файл.
    """
    try:
        # Сохраняем DataFrame в CSV файл
        data.to_csv(filename, index=True)
        print(f"Данные успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")


def main():
    """
        Основная функция программы. Запрашивает ввод от пользователя, загружает данные,
        обрабатывает их и выводит результаты, включая график и среднюю цену закрытия.
        """
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc)»: ")

    # Запрос периода или дат начала и окончания
    use_dates = input("Вы хотите указать даты начала и окончания? (да/нет): ").strip().lower()
    if use_dates in ['да', 'yes', 'y']:
        start_date = input("Введите дату начала анализа (в формате YYYY-MM-DD): ")
        end_date = input("Введите дату окончания анализа (в формате YYYY-MM-DD): ")
        period = None           # Период будет игнорироваться
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        start_date = None
        end_date = None

    # Запрашиваем порог колебаний
    try:
        threshold = float(input("Введите порог колебаний цен в процентах (например, 7 для 7%): "))
    except ValueError:
        print("Ошибка: Порог колебаний должен быть числом.")
        return

    # Загружаем данные об акциях
    stock_data = dd.fetch_stock_data(ticker, period=period, start_date=start_date, end_date=end_date)

    # Проверяем, получили ли мы данные
    if stock_data.empty:
        print("Не удалось загрузить данные для указанного тикера и периода. Проверьте ввод.")
        return

    # Добавляем скользящее среднее, RSI и MACD
    stock_data = dd.add_moving_average(stock_data)
    stock_data = dd.calculate_rsi(stock_data)
    stock_data = dd.calculate_macd(stock_data)
    stock_data = dd.calculate_atr(stock_data)

    # Вычисляем и выводим среднюю цену закрытия
    calculate_and_display_average_price(stock_data)

    # Проверяем колебания цен
    notify_if_strong_fluctuations(stock_data, threshold)

    # Расчет индикаторов
    stock_data = dp.calculate_indicators(stock_data)  # Добавлен расчет индикаторов



    # Строим график с индикаторами

    # Запрос стиля оформления графика
    style = input("Введите стиль оформления графика (например, 'seaborn', 'ggplot', 'default'): ").strip() # Изменение

    # Создание и сохранение графика
    dplt.create_and_save_plot(stock_data, ticker, period or f"{start_date}_to_{end_date}", style=style)  # Изменение


    # Расчет среднего значения цены закрытия
    dp.calculate_average_close(stock_data)

    # Построение интерактивного графика
    dplt.create_interactive_plot(stock_data, ticker)

    # Спрашиваем пользователя, хочет ли он экспортировать данные в CSV
    export_choice = input("Хотите ли вы экспортировать данные в CSV? (да/нет): ").strip().lower()
    if export_choice in ['да', 'yes', 'y']:
        # Указываем имя файла
        filename = f"{ticker}_{period or (f'{start_date}_to_{end_date}')}_stock_data.csv"
        export_data_to_csv(stock_data, filename)

if __name__ == "__main__":
    main()
