from Day1.Errors import QueueIsFull
from Transaction import Transaction


class TransactionQueue:
    def __init__(self):
        
        self.transaction_queue: list = []
        self.max_queue_len = 10

    def add_to_queue(self, transaction: Transaction):
        self._check_queue()
        premium_transactions = 0
        if self._check_priority(transaction) == True:
            for trans in self.transaction_queue:
                if trans.transaction_type == "Премиальный":
                    premium_transactions += 1

            self.transaction_queue.insert(premium_transactions, transaction)
        elif self._check_deffered_transaction(transaction) == True:
                self.transaction_queue.append(transaction)
        else: 
            if len(self.transaction_queue) == 0:
                self.transaction_queue.append(transaction)
            else:
                self.before_deffered_transaction(transaction)
        #print(self.transaction_queue)
        return self.transaction_queue


    def _check_queue(self):
        if len(self.transaction_queue)== self.max_queue_len:
            raise QueueIsFull("Очередь полная, попробуйте позже")

    def transaction_refuse(self, transaction: Transaction):
        self.transaction_queue.pop(self.transaction_queue.index(transaction))
        return self.transaction_queue

    def _check_deffered_transaction(self, transaction: Transaction):
        transaction_type = transaction.get_transaction_info()["Type"]
        if transaction_type == "Отложенная":
            return True
        else: return False

    def _check_priority(self, transaction: Transaction):
        transaction_type = transaction.get_transaction_info()["Type"]
        if transaction_type == "Премиальный":
            return True
        else: return False
    
    def before_deffered_transaction(self, transaction: Transaction):
        non_deffered_operation = len(self.transaction_queue)-1
        if self.transaction_queue[len(self.transaction_queue)-1].get_transaction_info()["Type"] == "Отложенная":
            reversed_queue: list = reversed(self.transaction_queue)
            for trans in reversed_queue:
                if trans.transaction_type == "Отложенная":
                    non_deffered_operation -= 1
                else: continue
            self.transaction_queue.insert(non_deffered_operation-1, transaction)
        else:
            self.transaction_queue.append(transaction)
        return self.transaction_queue

    def cancel_transaction(self, transaction: Transaction):
        self.transaction_queue.pop(self.transaction_queue.index(transaction))
        return self.transaction_queue


    def print_queue(self):
        info = []
        for i in self.transaction_queue:
            info.append(i.get_transaction_info())
        return info


    def __str__(self):
        info = self.print_queue
        for i in info:
            transaction += i 

        return transaction