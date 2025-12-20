from Client import Client
from Day1.BankAccount import BankAccount
from Day1.Currency import Currency
from InvestmanAccount import InvestmentAccount
from PremiumAccount import PremiumAccount
from SavingsAccount import SavingsAccount


def create_active(firstname, surname, phone, balance, status="Активный"):
    account = BankAccount(
        user_data={
            'name': firstname,
            'surname': surname,
            'phone': phone
        },
        balance=balance,
        account_status=status,
        currency='USD'
    )

    return account


def create_frozen(firstname, surname, phone, balance, status="Заморожен"):
    account = BankAccount(
        user_data={
            'name': firstname,
            'surname': surname,
            'phone': phone
        },
        balance=balance,
        account_status=status,
        currency='USD'
    )

    return account


def create_saving_active(firstname, surname, phone, balance, status="Активный"):
    account = SavingsAccount(
        user_data={
            'name': firstname,
            'surname': surname,
            'phone': phone
        },
        balance=balance,
        account_status=status,
        currency='USD',
    )
    return account


def create_premium_active(firstname, surname, phone, balance, status="Активный"):
    account = PremiumAccount(
        user_data={
            'name': firstname,
            'surname': surname,
            'phone': phone
        },
        balance=balance,
        account_status=status,
        currency='USD')

    return account


def create_investment_active(firstname, surname, phone, balance, status="Активный"):
    account = InvestmentAccount(
        user_data={
            'name': firstname,
            'surname': surname,
            'phone': phone
        },
        balance=balance,
        account_status=status,
        currency='USD')

    return account


account_active = create_active(
    "Semyon", "Migal", "+79998885511", 999, "Активный")
account_frozen = create_frozen(
    "Donald", "Trump", "+79998885511", 999, "Заморожен")

account_saving_active = create_saving_active(
    "Semyon", "Migal", "+79998885511", 999, "Активный")

account_premium_active = create_premium_active(
    "Semyon", "Migal", "+79998885511", 100, "Активный")

account_investment_active = create_investment_active(
    "Semyon", "Migal", "+79998885511", 100, "Активный")

# проверка первого дз

# print(account_active)
# print(account_frozen)

# account_active.deposit(10000)
# account_active.withdraw(100)

# account_frozen.deposit(10000000)


# Проверка второго дз

# print(account_saving_active)

# account_saving_active.withdraw(100)

# print(account_saving_active)

# account_saving_active.apply_monthly_interest()

# print(account_saving_active)

# print(account_premium_active)

# account_premium_active.withdraw(1000)
# print(account_premium_active)

#print(account_investment_active)
#account_investment_active.project_yearly_growth()


"""
РАБОТА КЛАССА КЛИЕНТ
"""

def create_client(name, surname, client_id, client_login, client_password, client_status, accounts_list, contacts, age):
    client = Client(
        name = name, surname = surname, client_id = client_id, client_login = client_login, client_password=client_password, client_status=client_status,
    accounts_list = accounts_list, contacts=contacts, age = age
    )
    return client

client_semyon = create_client("Semyon", "Migal", None, "login", "Hardpass", "Active",
                              accounts_list=(account_active,
                                             account_frozen,
                                             account_saving_active,
                                             account_premium_active,
                                             account_investment_active), contacts="+79998885533", age = 22)



client_semyon.add_client()
print(client_semyon)
client_semyon.print_account(account_active.get_account_info()['Номер счета'])
client_semyon.get_total_balance()
