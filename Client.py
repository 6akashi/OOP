import uuid
from datetime import time, datetime
from re import search

from pyexpat.errors import messages

from Day1.Errors import *
from Day1.BankAccount import BankAccount
from PremiumAccount import PremiumAccount
from SavingsAccount import SavingsAccount
from InvestmanAccount import InvestmentAccount


class Client():
    def __init__(self, name: str, surname: str, client_id: str, client_login: str, client_password: str,  client_status,
                 accounts_list: list, contacts: str, age: int):
        self.name = name
        self.surname = surname
        self.client_id = client_id
        self.client_login = client_login
        self.client_password = client_password
        self.client_status = client_status
        self. accounts_list = accounts_list
        self.contacts = contacts
        self.age = age
        self.authenticate = False
        self.client_rank:int = 1
        if self.age <= 18 and age is isinstance(age, int):
            raise AgeError('Ваш возраст должен быть больше 18-ти лет и целым числом')


    def add_client(self):
        if self.client_id is None:
            self.client_id = str(uuid.uuid4())[:8].upper()
        else:
            raise AccountAllreadyExist('У вас уже есть аккаунт')
        print('Ваш аккаунт создан!')
        print(f"Имя: {self.name}"
              f'Фамилия: {self.surname}'
              f"Номер телефона: {self.contacts}"
              f"Возраст: {self.age}")

    def open_account(self, type_of_account, balance, percent_for_saving, overdraft_sum, commision, limits, investment_packs: dict, actives: dict):
        if type_of_account == "Обычный":
            account = BankAccount(balance=balance, user_data={
                "Имя: ": self.name,
                "Фамилия": self.surname,
                "Номер телефона": self.contacts
            })

        if type_of_account == "Сберегательный":
            account = SavingsAccount(balance=balance, user_data={
                "Имя: ": self.name,
                "Фамилия": self.surname,
                "Номер телефона": self.contacts
            }, user_percent = percent_for_saving)

        if type_of_account == "Премиум":
            account = PremiumAccount(balance=balance, user_data={
                "Имя: ": self.name,
                "Фамилия": self.surname,
                "Номер телефона": self.contacts
            }, overdraft_sum=overdraft_sum, commision=commision, limits=limits)

        if type_of_account == "Инвестиционный":
            account = InvestmentAccount(balance=balance, user_data={
                "Имя: ": self.name,
                "Фамилия": self.surname,
                "Номер телефона": self.contacts
            }, investment_packs=investment_packs, actives=actives)

        else:
            print("Такого типа счета не существует")

        self.accounts_list.append(account.get_account_info())



    def _check_authenticate(self):
        if self.authenticate != True:
            print("Войдите в аккаунт")
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            self.authenticate_client(login, password)
        else: pass

    def send_message_to_clien(self, message):
        pass

    def _suspected_operation(self):
        message = "ПОДОЗРИТЕЛЬЯ ОПЕРАЦИЯ"
        self.send_message_to_clien(message)
        print(message)

    def _check_time(self):
        startime = time(0, 0, 0)
        endtime = time(5,0,0)
        time_now = datetime.now().time()
        if time_now in range(startime, endtime):
            raise TimeError('В это время невозможно совершить данную операцию')


    def search_account_by_id(self, id):
        self._check_time()
        #self._check_authenticate()
        for account in self.accounts_list:
            if account["Номер счета"] == id:
                id_account = self.accounts_list.index(account)
        account = self.accounts_list[id_account]
        return account

    def close_account(self, id):
        self._check_time()
        #self._check_authenticate()
        account = self.search_account_by_id(id)
        account.set_account_info(name_param="Статус", param="Закрыт")
        print(f"Вы закрыли счет с номером {account.account_id}")

    def freeze_account(self, id):
        self._check_time()
        #self._check_authenticate()
        account = self.search_account_by_id(id)
        account.set_account_info(name_param="Статус", param="Заморожен")
        print(f"Вы заморозили счет с номером {account.account_id}")


    def authenticate_client(self, login, password):
        for i in range(3):
            if self.client_login == login and self.client_password == password:
                self.authenticate = True
                return self.authenticate
            else:
                if i != 3:
                    print("Вы ввели неправлиьно логин и пароль"
                        f"У вас осталость {3-i} попытки")
                else:
                    print("Вак аккаунт заблокирован")
                    self.client_status = "Заблокирован"

    def get_total_balance(self):
        #self._check_authenticate()
        total_balance = 0.0
        for account_dict in self.accounts_list:
            balance_value = account_dict.get_account_info()['Баланс']
            total_balance += balance_value

        print(f'Общий баланс {total_balance}')
        return total_balance

    def get_client_rank(self):
        return self.client_rank


    def get_client_info(self):
        return {
            "Имя": self.name,
            "Фамилия": self.surname,
            "Айди": self.client_id,
            "Логин": self.client_login,
            "Пароль": self.client_password,
            "Статус": self.client_status,
            "Список аккаунтов": self.accounts_list,
            "Контакты": self.contacts,
            "Возраст": self.age,
            "Авторизован": self.authenticate,
            "Ранг клиента": self.client_rank
        }

    def print_account(self, id):
        account = self.search_account_by_id(id)
        account_info = account.get_account_info()
        print(account_info)

    def __str__(self):
        info = self.get_client_info()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Айди: {self.client_id}\n"
            f"Логин: {self.client_login}\n"
            f"Пароль: {self.client_password}\n"
            f"Статус: {self.client_status}\n"
            f"Список аккаунтов: {self.accounts_list}\n"
            f"Контакты: {self.contacts}\n"
            f"Возраст: {self.age}\n"
            f"Авторизован: {self.authenticate}\n"
            f"Ранг клиента: {self.client_rank}\n"
        )





