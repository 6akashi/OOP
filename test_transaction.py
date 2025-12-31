from Client import Client
from Day1.BankAccount import BankAccount
from Day1.Currency import Currency
from InvestmanAccount import InvestmentAccount
from PremiumAccount import PremiumAccount
from SavingsAccount import SavingsAccount
from Transaction import Transaction
from TransactionQueue import TransactionQueue
#from Transaction import Transaction


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


def create_client(name, surname, client_id, client_login, client_password, client_status, accounts_list, contacts, age):
    client = Client(
        name = name, surname = surname, client_id = client_id, client_login = client_login, client_password=client_password, client_status=client_status,
    accounts_list = accounts_list, contacts=contacts, age = age
    )
    return client

client_semyon = create_client("Semyon", "Migal", None, "login", "Hardpass", "Active",
                              accounts_list=list((account_active,
                                             account_frozen,
                                             account_saving_active,
                                             account_premium_active,
                                             account_investment_active)), contacts="+79998885533", age = 22)

client_donald = create_client("Donald", "Trump", None, "login", "Hardpass", "Active",
                              accounts_list=list((account_active,
                                             account_frozen,
                                             account_saving_active,
                                             account_premium_active,
                                             account_investment_active)), contacts="+79998885533", age = 100)


reciever_account_index = client_semyon.accounts_list.index(account_active)
reciever_account_id = client_semyon.accounts_list[reciever_account_index].get_account_info()['Номер счета']

sender_account_index = client_donald.accounts_list.index(account_active)
sender_account_id = client_donald.accounts_list[sender_account_index].get_account_info()['Номер счета']

#print(reciever_account_id)
#sender_account_id = client_donald.accounts_list(account_active).get_account_info.get("Номер счета")

test_transaction = Transaction(transaction_sum=100, sender=client_donald, reciever=client_semyon, 
                               sender_account_id=sender_account_id, 
                               reciever_account_id=reciever_account_id)
test_transaction2 = Transaction(transaction_sum=50, sender=client_semyon, reciever=client_donald, 
                               sender_account_id=sender_account_id, 
                               reciever_account_id=reciever_account_id)

test_transaction_premium = Transaction(transaction_sum=50, sender=client_semyon, reciever=client_donald, 
                               sender_account_id=sender_account_id, 
                               reciever_account_id=reciever_account_id)
test_transaction_premium.transaction_type = "Премиальный"

test_transaction_deffered = Transaction(transaction_sum=50, sender=client_semyon, reciever=client_donald, 
                               sender_account_id=sender_account_id, 
                               reciever_account_id=reciever_account_id)
test_transaction_deffered.transaction_type = "Отложенная"

print(test_transaction_deffered.transaction_type)

#print(test_transaction)

test_queue = TransactionQueue()
test_queue_list = test_queue.add_to_queue(test_transaction)
print(test_queue_list)
test_queue_list = test_queue.add_to_queue(test_transaction2)
print(test_queue_list)
test_queue_list = test_queue.add_to_queue(test_transaction_premium)
print(test_queue_list)
test_queue_list = test_queue.add_to_queue(test_transaction)
print(test_queue_list)
test_queue_list = test_queue.add_to_queue(test_transaction_deffered)
print(test_queue_list)
test_queue_list = test_queue.add_to_queue(test_transaction)
print(test_queue_list)

for i in test_queue_list:
    print(i)

print("=================")
test_queue.cancel_transaction(test_transaction_deffered)

for i in test_queue_list:
    print(i)