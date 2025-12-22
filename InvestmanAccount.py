from Day1.BankAccount import BankAccount


class InvestmentAccount(BankAccount):
    def __init__(self,
                 balance,
                 user_data,
                 account_status,
                 user_id=None,
                 currency='RUB',
                 limits=10000,
                 overdraft=False,
                 overdraft_sum=None,
                 investment_packs: dict = {
                     'Apple': 0.03,
                     'Samsung': 0.06,
                     'LG': 0.04
                 },  # Акции: сколько приносят в процентах
                 actives: dict = {
                     'stocks': 0.1,
                     'bonds': 0.13,
                     'etf': 0.11
                 }):
        super().__init__(balance, user_data, account_status,
                         user_id, currency, limits, overdraft, overdraft_sum = 0.0)

        self.investment_packs = investment_packs
        self.actives = actives
        self.type_of_account = 'Инвестиционный'

    # расчет суммы процентов всех инвестиций
    def index_from_investment(self):
        return sum(self.investment_packs.values())

    # расчет суммы процентов всех активов
    def index_from_actives(self):
        return sum(self.actives.values())

    # Расчет годового заработка с активов
    def project_yearly_growth(self):
        index = self.index_from_actives() + self.index_from_investment()
        amount = self.balance * index
        print(f'Ваша выручка за год: {amount}')
        self.deposit(amount)

    def get_account_info(self):
        info = super().get_account_info()

        # перечисление всех акций пользователя
        def dict_to_string(d):
            return ", ".join(d.keys())

        info['Портфель инвестиций'] = dict_to_string(self.investment_packs)
        info['Активы'] = dict_to_string(self.actives)

        return info


    def __str__(self):
        info = self.get_account_info()
        if info is None:
            return "Fuuuuuck"
        return (f"Тип счета: {info.get('Тип счета', 'Неизвестно')}\n"
                f"Клиент: {info.get('Клиент', 'Неизвестно')}\n"
                f"Номер счета: {info.get('Номер счета', 'Неизвестно')}\n"
                f"Статус: {info.get('Статус', 'Неизвестно')}\n"
                f"Баланс: {info.get('Баланс', 'Неизвестно')}\n"
                f"Портфель инвестиций: {info.get('Портфель инвестиций', 'Неизвестно')}\n"
                f"Активы: {info.get('Активы', 'Неизвестно')}\n"
                )
