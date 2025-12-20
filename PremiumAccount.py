from Day1.BankAccount import BankAccount


class PremiumAccount(BankAccount):
    def __init__(self,
                 balance,
                 user_data,
                 account_status,
                 user_id=None,
                 currency: str = 'RUB',
                 overdraft: bool = True,
                 overdraft_sum: float = -10000.0,
                 commision: float = 0.05,  # 5%
                 limits: float = 50000.0
                 ):
        super().__init__(balance,
                         user_data,
                         account_status,
                         user_id=None,
                         limits=limits,
                         overdraft=overdraft,
                         overdraft_sum=overdraft_sum)

        self.comision = commision
        self.type_of_account = "Премиальный"
        self.limits = limits

    def withdraw_comision(self):
        comision_sum = self.balance * self.comision
        self.withdraw(comision_sum)

    def get_account_info(self):
        info = super().get_account_info()
        info_update = dict(info)

        info_update['Сумма овердрафта'] = self.overdraft_sum
        info_update['Лимит на снятие'] = self.limits
        info_update['Коммисия на обслуживание'] = self.comision

        return info_update

    def __str__(self):
        info = self.get_account_info()
        if info is None:
            return "Fuuuuuck"
        return (f"Тип счета: {info.get('Тип счета', 'Неизвестно')}\n"
                f"Клиент: {info.get('Клиент', 'Неизвестно')}\n"
                f"Номер счета: {info.get('Номер счета', 'Неизвестно')}\n"
                f"Статус: {info.get('Статус', 'Неизвестно')}\n"
                f"Баланс: {info.get('Баланс', 'Неизвестно')}\n"
                f"Сумма овердрафта: {info.get('Сумма овердрафта', 'Неизвестно')}\n"
                f"Лимит на снятие: {info.get('Лимит на снятие', 'Неизвестно')}\n"
                f"Коммисия на обслуживание: {info.get('Коммисия на обслуживание', 'Неизвестно')}\n")
