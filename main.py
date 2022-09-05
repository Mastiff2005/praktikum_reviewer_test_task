import datetime as dt


# Хорошо бы добавить docstrings для всех классов и методов классов. https://peps.python.org/pep-0257/
# Также не помешают аннотации типов при объявлении методов. https://peps.python.org/pep-0484/
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # 1. Можно получить текущую дату проще: dt.date.today()
        # 2. Получение текущей даты следует вынести в те методы, где она используется
        self.date = (
            dt.datetime.now().date() if
            # лучше написать условие на одной строке: if not date - это улучшит читаемость (можно лучше)
            not
            # 1. Ипользование тернарного оператора - это хорошо
            # 2. При подобном методе переноса последнюю скобку лучше также перенести
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # переменные принято называть с маленькой буквы. Тем более что тут это не название класса,
        # а временная переменная, которая используется только в этом цикле
        # весь цикл можно написать в одну строку, используя sum и list comprehension https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        for Record in self.records:
            # текущую дату можно получить проще (см. выше)
            if Record.date == dt.datetime.now().date():
                # можно так: today_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # текущую дату можно получить проще (см. выше)
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # можно упростить условие, используя in range(7) https://docs.python.org/3/library/stdtypes.html?highlight=range#range
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Такие переносы давно уже не в моде :) Следует использовать скобки (ссылку, PEP8).
            # Если в строке не подставляются переменные, f-строку использовать не нужно
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                # 1. Если использовать именованные аргументы, то они должны быть с маленькой буквы
                                # 2. Переносы лучше выдержать в едином стиле (например как на стр. 11)
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # лучше не "хардкодить" название валют в методе, а вынести названия и курсы в словарь на уровне класса,
        # который затем перебирать в цикле. Вообще, нужно по возможности избегать "захардкоженных" значений и использовать переменные
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # а если в метод будет передано значение не "usd", "eur" или "rub"? Нужно сделать проверку в самом начале,
        # поддерживает ли метод переданную в него валюту, если нет - return
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # здесь для округления до двух знаков после запятой используется round, ниже - format. Лучше придерживаться одного стиля.
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # см. выше про переносы
            return 'Денег нет, держись:' \
                   # можно использовать abs
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
