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
        self.transaction_commission = self.commision_for_transfer
        self.reciever = reciever
        self.transaction_summ = transaction_sum
        self.sender = sender
        self.sender_currency = sender.get_my_account(sender_account_id).get_account_info().get("Валюта")
        self.reciever_currency = reciever.get_my_account(reciever_account_id).get_account_info().get("Валюта")
        self.transaction_status = "Выполняется"
        self.refuse_reason = ""
        self.time_stamp = datetime.datetime
        self.transaction_type = "Usual"
        self.transaction_queue: list = []
        self.max_queue_len = 10
        self.priority = False
        self.transaction_id = None

        if self.transaction_id is None:
            self.transaction_id = str(uuid.uuid4())[:8].upper()

    #Сначада смотрим приоритет, если есть, то ставим последним из приоритетов
    #Если нет, смотрим есть ли в очереди отложенные операции, если есть, то ставим перед ними
    #def add_to_queue(self):
    #    premium_transactions = 0
    #    if self.priority == True:
    #        for transaction in self.transaction_queue:
    #            if transaction.transaction_type == "Премиальный":
    #                premium_transactions += 1
#        self.transaction_queue.insert(premium_transactions - 1, self)
    #    else:
    #        if self._check_deffered_transaction:
    #            self.deffered_transaction
    #        else: self.transaction_queue.append(self)
#    return self.transaction_queue

    #def _check_queue(self):
    #    if max(self.transaction_queue) == self.max_queue_len:
    #        raise QueueIsFull("Очередь полная, попробуйте позже")

    #def transaction_refuse(self):
    #    self.transaction_queue.pop(self.transaction_queue.index(self))
    #    return self.transaction_queue

    def _check_deffered_transaction(self):
        deffered_transaction = False
        last_transaction = self.transaction_queue[-1]
        if last_transaction.transaction_type == "Отложен":
            deffered_transaction = True
        return deffered_transaction
            

    #def deffered_transaction(self):
    #    deffered_operation = max(self.transaction_queue)
    #    if self.transaction_queue[max(self.transaction_queue)-1] != "Отложенная":
    #        reversed_queue: list = self.transaction_queue.reverse()
    #        for transaction in reversed_queue:
    #            if transaction.transaction_type == "Отложенная":
    #                deffered_operation -= 1
    #        non_deffered_transaction = self.transaction_queue.pop()
    #        self.transaction_queue.insert(deffered_operation, non_deffered_transaction)
    #    return self.transaction_queue

    
    def commision_for_transfer(self):
        if self.sender == self.reciever or self.sender.get_my_account(self.sender_account_id).get_account_info()["Тип счета"] == "Премиальный":
            self.transaction_commission = 0
        else: self.transaction_commission = 0.05

    def _check_currency(self, currency_sender, currency_reciever):
        if currency_sender == currency_reciever:
            return True
        else: return False

    def convert_currency(self):
        match(self.reciever_currency):
            case "USD": 
                convert_index = ConvUsdTo.get_conv.get(self.sender_currency)
            case "RUB": 
                convert_index = ConvRubTo.get_conv.get(self.sender_currency)
                
        
        #self.transaction_summ *= convert_index
        return convert_index
        

    def run_operation(self):
        for transaction in self.transaction_queue:
            transaction.transaction_status = "В процессе"
            try_counts = 0
            while transaction.transaction_status == "В процессе":
                response = self.money_transfer()
                if response == "Успешно":
                    transaction.transaction_status = response
                    break
                try_counts += 1
                if try_counts == 5:
                    transaction.transaction_status = "Неудачно"
                    transaction.delete_from_queue()

    def delete_from_queue(self):
        self.transaction_queue.pop(self.transaction_queue.index(self))

    def money_transfer(self):
        pass

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