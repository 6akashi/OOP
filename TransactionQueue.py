from Day1.Errors import QueueIsFull
from Transaction import Transaction


class TransactionQueue:
    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.transaction_queue: list = []
        self.max_queue_len = 10
        self.priority = False

    def add_to_queue(self):
        premium_transactions = 0
        if self.priority == True:
            for transaction in self.transaction_queue:
                if transaction.transaction_type == "Премиальный":
                    premium_transactions += 1

            self.transaction_queue.insert(premium_transactions - 1, self.transaction)
        else:
            self.transaction_queue.append(self.transaction)
        self._check_deffered_transaction()
        return self.transaction_queue

    def _check_queue(self):
        if max(self.transaction_queue) == self.max_queue_len:
            raise QueueIsFull("Очередь полная, попробуйте позже")

    def transaction_refuse(self):
        self.transaction_queue.pop(self.transaction_queue.index(self.transaction))
        return self.transaction_queue

    def _check_deffered_transaction(self):
        deffered_operation = max(self.transaction_queue)
        if self.transaction_queue[max(self.transaction_queue)-1] != "Отложенная":
            reversed_queue = self.transaction_queue.reverse()
            for transaction in reversed_queue:
                if transaction.transaction_type == "Отложенная":
                    deffered_operation -= 1
            non_deffered_transaction = self.transaction_queue.pop()
            self.transaction_queue.insert(deffered_operation, non_deffered_transaction)
        return self.transaction_queue
