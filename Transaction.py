import datetime
import uuid
import logging
from Client import Client
from Day1.Errors import QueueIsFull
from CurrencyForConv import *

class Transaction:
    def __init__(self, transaction_sum: float, sender: Client, reciever: Client, 
                 sender_account_id, reciever_account_id):
        self.reciever_account_id = reciever_account_id
        self.sender_account_id = sender_account_id
        self.transaction_commission = 0.07
        self.reciever = reciever
        self.transaction_summ = transaction_sum
        self.sender = sender
        self.sender_currency = sender.get_my_account(sender_account_id).get_account_info().get("Валюта")
        self.reciever_currency = reciever.get_my_account(reciever_account_id).get_account_info().get("Валюта")
        self.transaction_status = "Выполняется"
        self.time_stamp = datetime.datetime
        self.transaction_type = "Usual"
        self.priority = False
        self.transaction_id = None
        self.number_of_retries = 0

        if self.transaction_id is None:
            self.transaction_id = str(uuid.uuid4())[:8].upper()

    #Заглушка для тестов транзакций
    def money_transfer(self):
        if self.transaction_summ <= 0:
            return "Неудача" 
        
        if self.transaction_summ <= 5000:
            return "Успешно"
        else: return "Неудача"

    def get_transaction_info(self) -> dict:
        info = {
            "Sender": self.sender.get_client_info(),
            "Reciever": self.reciever.get_client_info(),
            "Summ": self.transaction_summ,
            "Type": self.transaction_type
        }
        return info

    def __str__(self) -> str:
        info = self.get_transaction_info()
        return (
            #f"Sender: {info.get('Sender', 'Unknown')}\n"
            #f"Reciever: {info.get('Reciever', 'Unknown')}\n"
            #f"Summ: {info.get('Summ', 'Unknown')}"
            f"Type: {info.get('Type', 'Unknown')}"
        )