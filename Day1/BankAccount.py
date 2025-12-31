import uuid
from Day1.AbstractAccount import AbstractAccount
from Day1.Currency import Currency
from Day1.Errors import *


class BankAccount(AbstractAccount):
    def __init__(self, balance, user_data, account_status, user_id=None, currency: str = 'RUB', limits: float = 10000.0, overdraft: bool = False, overdraft_sum: float = 0.0):
        self.type_of_account = "Обычный"  # 2 дз
        self.limits = limits  # 2 дз
        self.overdraft = overdraft  # 2 дз

        # Проверка данных
        if not user_data['name'] or not isinstance(user_data['name'], str):
            raise InvalidOperationError(
                "Имя владельца обязательно должно быть строкой")
        if not isinstance(balance, (int, float)) or balance < 0:
            raise InvalidOperationError(
                "Баланс обязательно должен быть записан и быть положительным")

        # Создание 8-ми значного айди
        if user_id is None:
            user_id = str(uuid.uuid4())[:8].upper()

        # Вводимые валюты в верхний регистр
        currency_upper = currency.upper()

        # если есть овердрафт, присваеваем сумму
        if overdraft:
            self.overdraft_sum = overdraft_sum  # 2 дз

        # Пытаемся найти валюту у себя, если нет то ошибка
        try:
            self.currency = getattr(Currency, currency_upper)
        except (AttributeError, KeyError):
            raise InvalidOperationError(
                f'Неподдерживаемая валюта: {currency}. '
                f'Доступные валюты: RUB, USD, EUR, KZT, CNY'
            )

        super().__init__(user_id, user_data, balance, account_status)

    # Валидация суммы пополнения
    def _validate_amount(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError("Должно быть число")
        if amount <= 0:
            raise InvalidOperationError("Сумма должна быть положительной")

    # Проверка статусы
    def _check_status(self):
        if self.account_status == "Заморожен":
            raise AccountFrozenError("Счет заморожен")
        if self.account_status == "Закрыт":
            raise AccountClosedError("Счет закрыт")

    def get_account_id(self):
        return self.user_id

    # Провера баланса с учетом овердрафта
    def _check_balance(self, amount: float):
        if self.overdraft is False:
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"Недостаточно средств. Доступно: {self.balance:.2f}")
        else:
            if amount > (self.balance + abs(self.overdraft_sum)):
                raise InsufficientFundsError(
                    f'Недостаточно средства, ваш остаток с учетом овердрафта: {self.balance + abs(self.overdraft_sum)}')

    # Проверка на лимит, мб в валидацию можно сунуть
    def _check_amount(self, amount):
        if amount > self.limits:
            raise InsufficientFundsError(f'Лимит на снятие {self.limits}')

    # Пополнение
    def deposit(self, amount: float):
        self._validate_amount(amount)
        self._check_status()
        new_balance = self.balance + amount
        self.balance = new_balance
        print(f'Счет пополнен на {amount:.2f} {self.currency}')
        print(f'Ваш баланс: {new_balance}')

    # Снятие
    def withdraw(self, amount: float):
        self._validate_amount(amount)
        self._check_amount(amount)
        self._check_status()
        self._check_balance(amount)
        new_balance = self.balance - amount
        self.balance = new_balance
        print(f'Вы сняли со счета {amount:.2f} {self.currency}')
        print(f'Ваш баланс: {self.balance}')
        return new_balance

    # Получение данных
    def get_account_info(self):
        return {
            "Тип счета": self.type_of_account,
            "Клиент": self.user_data,
            "Номер счета": self.user_id,
            "Валюта": self.currency,
            "Статус": self.account_status,
            "Баланс": self.balance
        }

    def set_account_info(self, name_param, param):
        info = self.get_account_info()
        if name_param in info:
            if name_param == "Статус":
                self.account_status = param
            else: "Пока не сделали((("
        else:
            print(f"Параметра {name_param} не существует")
