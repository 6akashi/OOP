import calendar
from datetime import date
from Day1.BankAccount import BankAccount
from Day1.Currency import Currency


class SavingsAccount(BankAccount):
    def __init__(self, balance, user_data, account_status, user_id=None, currency: str = 'RUB', user_percent: float = 0.05):
        super().__init__(balance, user_data, account_status, user_id=None)
        self.minimal_balance = balance
        self.user_percent = user_percent  # 5%
        self.type_of_account = "Сберегательный"

    # проверяем минимальный баланс
    def min_balance(self, balance, new_balance):
        self.new_balance = new_balance
        self.balance = balance
        if (self.new_balance < self.balance):
            self.minimal_balance = self.new_balance

    # Установка нового минимального баланса при снятии
    def withdraw(self, amount):
        current_balance = self.balance
        self.new_balance = super().withdraw(amount)
        self.min_balance(current_balance, self.new_balance)

    # Расчет месячных процентов
    def apply_monthly_interest(self):
        self._check_status()
        today = date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]

        # Рассчитываем проценты за день
        # Годовая ставка / 365 дней * количество дней в месяце
        daily_rate = self.user_percent / 365
        interest_in_money = self.minimal_balance * daily_rate * days_in_month

        print(
            f"За этот месяц вы заработали {interest_in_money:.2f} {self.currency}")
        print(
            f"Ваш минимальный баланс был {self.minimal_balance:.2f} {self.currency}")
        self.deposit(interest_in_money)
        self.minimal_balance = self.balance

    def get_account_info(self):
        info = super().get_account_info()
        if info is None:
            info = {}
        update_info = dict(info)

        update_info["Тип счета"] = 'Сберегательный'
        update_info["Минимальный баланс"] = f'{self.minimal_balance:.2f} {self.currency}'
        update_info["Ваш процент"] = f"{self.user_percent*100}%"

        return update_info

    def __str__(self):
        info = self.get_account_info()
        if info is None:
            return "Fuuuuuck"
        return (f"Тип счета: {info.get('Тип счета', 'Неизвестно')}\n"
                f"Клиент: {info.get('Клиент', 'Неизвестно')}\n"
                f"Номер счета: {info.get('Номер счета', 'Неизвестно')}\n"
                f"Статус: {info.get('Статус', 'Неизвестно')}\n"
                f"Баланс: {info.get('Баланс', 'Неизвестно')}\n"
                f"Минимальный баланс: {info.get('Минимальный баланс', 'Неизвестно')}\n"
                f"Ваш процент: {info.get('Ваш процент', 'Неизвестно')}\n")
