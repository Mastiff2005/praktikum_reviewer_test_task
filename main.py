import datetime as dt


# Хорошо бы добавить docstrings для всех классов и методов классов. https://peps.python.org/pep-0257/
# Также не помешают аннотации типов при объявлении методов. https://peps.python.org/pep-0484/
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Можно получить текущую дату проще: dt.date.today()
        self.date = (
            dt.datetime.now().date() if
            # лучше написать условие на одной строке: if not date - это улучшит читаемость
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
        # всё выражение можно написать в одну строку, используя sum и list comprehension
        # https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        for Record in self.records:
            # 1. Текущую дату можно получить проще (см. выше)
            # 2. Лучше вычислить дату заранее, чтобы улучшить читаемость кода
            if Record.date == dt.datetime.now().date():
                # можно так: today_stats += record.amount (если вычисление не через sum)
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # текущую дату можно получить проще (см. выше)
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # 1. Можно упростить условие, используя in range(7) https://docs.python.org/3/library/stdtypes.html?highlight=range#range
                # 2. тогда не придется выражение (today - record.date) вычислять 2 раза.
                # 3. Здесь также напрашивается sum и list comprehension.
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Следует избегать однобуквенных обозначений переменных - лучше называть их в соответствии
        # с их назначением
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Такие переносы давно уже не в моде :) Следует использовать скобки.
            # Если в строке не подставляются переменные, f-строку использовать не нужно
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                # 1. Если используются именованные аргументы, то они должны быть с маленькой буквы
                                # 2. Но лучше не "хардкодить" название валют в методе, а вынести названия и курсы в словарь на уровне класса,
                                # который затем перебирать в цикле. Вообще, нужно по возможности избегать "захардкоженных" значений и использовать
                                # переменные.
                                # 3. Переносы лучше выдержать в едином стиле (например как на стр. 11)
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # а если в метод будет передано значение не "usd", "eur" или "rub"? Нужно сделать проверку в самом начале,
        # поддерживается ли переданная валюта, если нет - return
        # (подход "Guard Block" https://medium.com/lemon-code/guard-clauses-3bc0cd96a2d3)
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
                   # лучше использовать abs https://pythonz.net/references/named/abs/
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    
    # Если в дочернем классе метод родительского класса никак не изменяется, переопределять его не нужно,
    # соответственно использовать super() не требуется.
    def get_week_stats(self):
        super().get_week_stats()
