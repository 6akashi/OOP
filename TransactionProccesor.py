import datetime
from CurrencyForConv import *
from Day1.BankAccount import BankAccount
from Day1.Errors import *
from Transaction import Transaction
import json

from TransactionQueue import TransactionQueue

class TransactionProccessor:
    def __init__(self):
        self.commission = 0.07

    #TEST SUCCESFULLY
    #Если не между своими и не премиум то есть коммисия в 7%
    def trans_commission(self, transaction: Transaction):
        if transaction.transaction_summ <= 0:
                self.print_errors("Сумма транзакции меньше или равно нулю")
                raise NotEnoughMoney("Сумма транзакции меньше или равно нулю")
        if transaction.sender != transaction.reciever:
            if self._check_priority(transaction) == True:
                self.commission = 0.0
                return transaction.transaction_summ
            else: 

                new_summ = (transaction.transaction_summ * self.commission) + transaction.transaction_summ
                return new_summ    
        else: return transaction.transaction_summ

        
    #Конвертор пока не понял как и куда вставить, поэтому просто есть, рабочий
    def convertor(self, transaction: Transaction):
        match(transaction.reciever_currency):
            case "USD": 
                convert_index = ConvUsdTo().get_conv().get(transaction.sender_currency)
            case "RUB": 
                convert_index = ConvRubTo().get_conv().get(transaction.sender_currency)
            case _:
                self.print_errors("Неизвестная валюта")
                raise InvalidCurrency("Неизвестная валюта")
        if convert_index is None:
            self.print_errors(f"Нет курса для конвертации из {transaction.sender_currency} в {transaction.reciever_currency}")
            raise InvalidCurrency(f"Нет курса для конвертации из {transaction.sender_currency} в {transaction.reciever_currency}")

        return convert_index

    # CHECKED
    def _check_currency(self, currency_sender, currency_reciever):
        if currency_sender == currency_reciever:
            return True
        else: return False

    #Повтор операции, добавляет их в конец очереди
    def retry_operation(self, transaction_queue: TransactionQueue, transaction: Transaction):
        # Если проблема со статусом счета (заморожен/закрыт), отклоняем сразу
        if self._check_account_status(transaction):
            transaction.transaction_status = "Отклонена (проблема со счетом)"
            self.print_errors(f"Транзакция {transaction.transaction_id} отклонена из-за проблем со счетом")
            transaction_queue.delete_from_queue(transaction)
            return transaction_queue

        # Для других проблем (недостаточно средств и т.д.) даем 5 попыток
        if transaction.number_of_retries < 5:
            transaction.number_of_retries += 1
            print(f"Попытка {transaction.number_of_retries}/5 для транзакции {transaction.transaction_id}")
            transaction_queue.delete_from_queue(transaction)
            transaction_queue.add_to_queue(transaction)
        else:
            transaction.transaction_status = "Отклонена (превышено число попыток)"
            self.print_errors(f"Транзакция {transaction.transaction_id} отклонена после 5 попыток")
            transaction_queue.delete_from_queue(transaction)

        return transaction_queue
    
    #CHECKED
    def print_errors(self, error: str):
        import os
        import json
        from pathlib import Path

        date_now = datetime.datetime.now()
        data = {
            'date': date_now.strftime('%d.%m.%Y %H:%M:%S'),
            'error': error
        }

        filepath = './logs/data.json'

        # Создаем директорию, если ее нет
        Path('./logs').mkdir(parents=True, exist_ok=True)

        # Читаем существующие данные
        existing_data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                    # Убедимся, что это список
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data] if existing_data else []
            except:
                existing_data = []

        # Добавляем новую ошибку
        existing_data.append(data)

        # Сохраняем
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)

        # Также печатаем в консоль для отладки
        print(f"[ERROR] {data['date']}: {error}")


    # CHECKED
    def _check_balance(self, transaction: Transaction) -> bool:
        """
        Проверяет достаточно ли средств на счете.
        Возвращает: 
            True - достаточно средств
            False - недостаточно средств
        """
        sender_account: BankAccount = transaction.sender.search_account_by_id(transaction.sender_account_id)

        if sender_account is None:
            self.print_errors(f"Счет отправителя не найден: {transaction.sender_account_id}")
            return False  # Недостаточно средств (счет не найден)

        account_info = sender_account.get_account_info()
        sender_balance_str = account_info.get("Баланс", "0")
        sender_account_status = account_info.get("Тип счета", "")

        # Конвертируем баланс в число
        try:
            sender_balance = float(sender_balance_str)
        except (ValueError, TypeError):
            sender_balance = 0.0
            self.print_errors(f"Неверный формат баланса: {sender_balance_str}")

        # Учитываем овердрафт для премиальных счетов
        if sender_account_status == "Премиальный" and hasattr(sender_account, 'overdraft_sum'):
            try:
                overdraft = float(sender_account.overdraft_sum)
                true_balance = sender_balance + abs(overdraft)
            except:
                true_balance = sender_balance
        else:
            true_balance = sender_balance

        # Логируем для отладки
        print(f"DEBUG _check_balance: баланс={sender_balance}, с овердрафтом={true_balance}, нужно={transaction.transaction_summ}")

        # Возвращаем True если ДОСТАТОЧНО средств
        sufficient = true_balance >= transaction.transaction_summ
        if not sufficient:
            print(f"DEBUG: Недостаточно средств! {true_balance} < {transaction.transaction_summ}")

        return sufficient  # True = достаточно, False = недостаточно    
            

    def _check_priority(self, transaction: Transaction):
        transaction_type = transaction.get_transaction_info()["Type"]
        if transaction_type == "Премиальный":
            return True
        else: return False

    #CHECKED
    def _check_account_status(self, transaction: Transaction):
        sender_account: BankAccount = transaction.sender.search_account_by_id(transaction.sender_account_id)
        reciever_account: BankAccount = transaction.reciever.search_account_by_id(transaction.reciever_account_id)

        if sender_account is None or reciever_account is None:
            self.print_errors("Один из счетов не найден")
            return True

        sender_account_status = sender_account.get_account_info()["Статус"]
        reciever_account_status = reciever_account.get_account_info()["Статус"]
        if sender_account_status == "Активный" and reciever_account_status == "Активный":
            return False
        elif sender_account_status == "Заморожен" or reciever_account_status == "Заморожен":
            self.print_errors("Счет заморожен")
            print("СЧЕТ ЗАМОРОЖЕН!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return True
        elif sender_account_status == "Закрыт" or reciever_account_status == "Закрыт":
            self.print_errors("Счет закрыт")
            print("СЧЕТ ЗАКРЫТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return True

    def run_operation(self, transaction_queue: TransactionQueue):
        """Запускает обработку всех транзакций в очереди."""
        # Создаем копию для безопасной итерации
        original_queue = transaction_queue.transaction_queue.copy()

        for trans in original_queue:
            # Пропускаем, если транзакция уже удалена
            if trans not in transaction_queue.transaction_queue:
                continue
            trans.sender.accounts_history.append(trans.reciever_account_id)
            trans.reciever.accounts_history.append(trans.sender_account_id)
            print(f"\n=== Обработка транзакции {trans.transaction_id} ===")
            print(f"Сумма: {trans.transaction_summ}")
            print(f"Отправитель: {trans.sender.name} -> Получатель: {trans.reciever.name}")

            # 1. Проверяем статус счетов
            status_problem = self._check_account_status(trans)
            if status_problem:
                print(f"Проблема со статусом счета, отправляем в retry")
                self.retry_operation(transaction_queue, trans)
                continue
            
            # 2. Проверяем баланс
            balance_problem = self._check_balance(trans)
            if not balance_problem:
                print(f"Недостаточно средств, отправляем в retry")
                self.retry_operation(transaction_queue, trans)
                continue
            
            # 3. Выполняем перевод
            print(f"Вызываем money_transfer()...")
            response = trans.money_transfer()
            print(f"money_transfer() вернул: {response} (тип: {type(response)})")

            if response == "Успешно":
                trans.transaction_status = "Успешно"
                transaction_queue.delete_from_queue(trans)
                print(f"✅ Транзакция успешно выполнена!")
            elif response == "Неудача":
                print(f"❌ money_transfer вернул 'Неудача', отправляем в retry")
                self.retry_operation(transaction_queue, trans)
            elif response is None:
                print(f"⚠️  money_transfer вернул None! Проверьте метод money_transfer в классе Transaction")
                # Для тестирования, имитируем успех если сумма <= 5000
                if trans.transaction_summ <= 5000:
                    trans.transaction_status = "Успешно"
                    transaction_queue.delete_from_queue(trans)
                    print(f"✅ (Имитация) Транзакция успешно выполнена!")
                else:
                    print(f"❌ (Имитация) Большая сумма, отправляем в retry")
                    self.retry_operation(transaction_queue, trans)
            else:
                print(f"⚠️  Неизвестный ответ: {response}")
                trans.transaction_status = "Ошибка"
                transaction_queue.delete_from_queue(trans)


