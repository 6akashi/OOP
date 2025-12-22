from abc import ABC, abstractmethod

# Абстрактный класс


class AbstractAccount():
    user_id: str
    user_data: dict
    _balance: float = 0.0
    account_status: str

    def __init__(self, user_id, user_data, _balance, account_status):
        self.user_id = user_id
        self.user_data = user_data
        self._balance = max(0.0, _balance)
        self.account_status = account_status
        self.type_of_account = "Обычный"

    @property  # Геттер для баланса
    def balance(self):
        return self._balance

    @balance.setter  # Сеттер для баланса
    def balance(self, value):
        self._balance = value

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_account_info(self) -> dict:
        pass

    def __str__(self):
        info = self.get_account_info()
        return (f"Тип счета: {info.get('Тип счета', 'Неизвестно')}\n"
                f"Клиент: {info.get('Клиент', 'Неизвестно')}\n"
                f"Номер счета: {info.get('Номер счета', 'Неизвестно')}\n"
                f"Статус: {info.get('Статус', 'Неизвестно')}\n"
                f"Баланс: {info.get('Баланс', 'Неизвестно')}")


