from Client import Client
from Day1.BankAccount import BankAccount
from Day1.Currency import Currency
from InvestmanAccount import InvestmentAccount
from PremiumAccount import PremiumAccount
from SavingsAccount import SavingsAccount
from Transaction import Transaction
from TransactionProccesor import TransactionProccessor
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

def create_closed(firstname, surname, phone, balance, status="Закрыт"):
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




def create_client(name, surname, client_id, client_login, client_password, client_status, accounts_list, contacts, age):
    client = Client(
        name = name, surname = surname, client_id = client_id, client_login = client_login, client_password=client_password, client_status=client_status,
    accounts_list = accounts_list, contacts=contacts, age = age
    )
    return client

# ============ ПОДГОТОВКА ДАННЫХ ============

# Создаем различные счета для тестирования
account_semyon_active_rub = create_active("Semyon", "Migal", "+79998885511", 10000, "Активный")
account_semyon_active_usd = create_active("Semyon", "Migal", "+79998885511", 5000, "Активный")
account_semyon_frozen = create_frozen("Semyon", "Migal", "+79998885511", 1000, "Заморожен")
account_semyon_closed = create_closed("Semyon", "Migal", "+79998885511", 1000, "Закрыт")
account_semyon_premium = create_premium_active("Semyon", "Migal", "+79998885511", 2000, "Активный")
account_semyon_savings = create_saving_active("Semyon", "Migal", "+79998885511", 3000, "Активный")

account_donald_active_rub = create_active("Donald", "Trump", "+79998885522", 8000, "Активный")
account_donald_active_usd = create_active("Donald", "Trump", "+79998885522", 4000, "Активный")
account_donald_low_balance = create_active("Donald", "Trump", "+79998885522", 100, "Активный")
account_donald_premium = create_premium_active("Donald", "Trump", "+79998885522", 10000, "Активный")

# Устанавливаем валюты
account_semyon_active_rub.currency = "RUB"
account_semyon_active_usd.currency = "USD"
account_donald_active_rub.currency = "RUB"
account_donald_active_usd.currency = "USD"

# Создаем клиентов
client_semyon = create_client(
    "Semyon", "Migal", None, "semyon", "pass123", "Active",
    accounts_list=[
        account_semyon_active_rub,
        account_semyon_active_usd,
        account_semyon_frozen,
        account_semyon_closed,
        account_semyon_premium,
        account_semyon_savings
    ],
    contacts="+79998885533",
    age=22
)

client_donald = create_client(
    "Donald", "Trump", None, "donald", "pass456", "Active",
    accounts_list=[
        account_donald_active_rub,
        account_donald_active_usd,
        account_donald_low_balance,
        account_donald_premium
    ],
    contacts="+79998885544",
    age=100
)



# Создаем процессинг и очередь
trans_procc = TransactionProccessor()
test_queue = TransactionQueue()

# ============ 10 ТЕСТОВЫХ ТРАНЗАКЦИЙ ============

# Транзакция 1: Нормальный перевод (должен пройти успешно)
# Сумма <= 5000, активные счета, достаточно денег
def create_transaction_1():
    sender_account_id = account_donald_active_rub.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=1000,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 1000
    return trans

# Транзакция 2: Перевод на замороженный счет (должна быть отклонена)
def create_transaction_2():
    sender_account_id = account_donald_active_rub.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_frozen.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=500,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 500
    return trans

# Транзакция 3: Перевод с закрытого счета (должна быть отклонена)
def create_transaction_3():
    sender_account_id = account_semyon_closed.get_account_info()['Номер счета']
    receiver_account_id = account_donald_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=300,
        sender=client_semyon,
        reciever=client_donald,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 300
    return trans

# Транзакция 4: Недостаточно средств (должна быть отклонена)
def create_transaction_4():
    sender_account_id = account_donald_low_balance.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=500,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 500  # На счету только 100, но с учетом овердрафта?
    return trans

# Транзакция 5: Премиум транзакция без комиссии
def create_transaction_5():
    sender_account_id = account_donald_premium.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=1000,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 1000
    trans.transaction_type = "Премиальный"
    return trans

# Транзакция 6: Конвертация валют RUB -> USD
def create_transaction_6():
    sender_account_id = account_donald_active_rub.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_usd.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=1000,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 1000
    return trans

# Транзакция 7: Конвертация валют USD -> RUB
def create_transaction_7():
    sender_account_id = account_donald_active_usd.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=500,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 500
    return trans

# Транзакция 8: Большая сумма (>5000) - money_transfer вернет "Неудача"
def create_transaction_8():
    sender_account_id = account_donald_premium.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=6000,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 6000  # > 5000, money_transfer вернет "Неудача"
    return trans

# Транзакция 9: Отрицательная сумма - должна вызвать исключение
def create_transaction_9():
    sender_account_id = account_donald_active_rub.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=100,
        sender=client_donald,
        reciever=client_semyon,
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = -100  # Отрицательная сумма
    return trans

# Транзакция 10: Перевод на тот же счет (самому себе)
def create_transaction_10():
    sender_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    receiver_account_id = account_semyon_active_rub.get_account_info()['Номер счета']
    
    trans = Transaction(
        transaction_sum=500,
        sender=client_semyon,
        reciever=client_semyon,  # Сам себе!
        sender_account_id=sender_account_id,
        reciever_account_id=receiver_account_id
    )
    trans.transaction_summ = 500
    return trans

# ============ ФУНКЦИЯ ДЛЯ ТЕСТИРОВАНИЯ ============

def test_all_transactions():
    """Тестирует все 10 транзакций"""
    
    # Создаем все транзакции
    transactions = [
        create_transaction_1(),
        create_transaction_2(),
        create_transaction_3(),
        create_transaction_4(),
        create_transaction_5(),
        create_transaction_6(),
        create_transaction_7(),
        create_transaction_8(),
        create_transaction_9(),
        create_transaction_10()
    ]
    
    # Добавляем все в очередь
    print("=" * 60)
    print("ДОБАВЛЕНИЕ ТРАНЗАКЦИЙ В ОЧЕРЕДЬ")
    print("=" * 60)
    
    for i, trans in enumerate(transactions, 1):
        try:
            test_queue.add_to_queue(trans)
            print(f"Транзакция {i}: Добавлена в очередь (ID: {trans.transaction_id})")
        except Exception as e:
            print(f"Транзакция {i}: Ошибка при добавлении - {e}")
    
    print(f"\nВсего в очереди: {len(test_queue.transaction_queue)} транзакций\n")
    
    # Тестируем различные методы процессинга
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ МЕТОДОВ ПРОЦЕССИНГА")
    print("=" * 60)
    
    for i, trans in enumerate(test_queue.transaction_queue, 1):
        print(f"\n--- Транзакция {i} (ID: {trans.transaction_id}) ---")
        
        # Проверка статуса счетов
        try:
            status_check = trans_procc._check_account_status(trans)
            print(f"Проверка статуса счетов: {'ПРОБЛЕМА' if status_check else 'OK'}")
        except Exception as e:
            print(f"Проверка статуса счетов: ОШИБКА - {e}")
        
        # Проверка баланса
        try:
            balance_check = trans_procc._check_balance(trans)
            print(f"Проверка баланса: {'НЕДОСТАТОЧНО СРЕДСТВ' if not balance_check else 'OK'}")
        except Exception as e:
            print(f"Проверка баланса: ОШИБКА - {e}")
        
        # Проверка валюты
        try:
            currency_check = trans_procc._check_currency(
                trans.sender_currency,
                trans.reciever_currency
            )
            print(f"Проверка валюты: {'СОВПАДАЮТ' if currency_check else 'РАЗНЫЕ'}")
        except Exception as e:
            print(f"Проверка валюты: ОШИБКА - {e}")
        
        # Проверка приоритета
        try:
            priority_check = trans_procc._check_priority(trans)
            print(f"Проверка приоритета: {'ПРЕМИУМ' if priority_check else 'ОБЫЧНАЯ'}")
        except Exception as e:
            print(f"Проверка приоритета: ОШИБКА - {e}")
        
        # Расчет комиссии
        try:
            commission_result = trans_procc.trans_commission(trans)
            print(f"Комиссия: {commission_result} (исходная: {trans.transaction_summ})")
        except Exception as e:
            print(f"Комиссия: ОШИБКА - {e}")
        
        # Конвертация валют (если нужно)
        if trans.sender_currency != trans.reciever_currency:
            try:
                conversion_rate = trans_procc.convertor(trans)
                print(f"Курс конвертации {trans.sender_currency}->{trans.reciever_currency}: {conversion_rate}")
            except Exception as e:
                print(f"Конвертация: ОШИБКА - {e}")
    
    # Запуск обработки очереди
    print("\n" + "=" * 60)
    print("ЗАПУСК ОБРАБОТКИ ОЧЕРЕДИ")
    print("=" * 60)
    
    try:
        print(f"Начало обработки. В очереди: {len(test_queue.transaction_queue)} транзакций")
        trans_procc.run_operation(test_queue)
        print(f"Обработка завершена. В очереди осталось: {len(test_queue.transaction_queue)} транзакций")
        
        # Выводим статусы всех транзакций
        print("\nСтатусы транзакций после обработки:")
        for i, trans in enumerate(test_queue.transaction_queue, 1):
            print(f"  {i}. ID: {trans.transaction_id}, Статус: {trans.transaction_status}, "
                  f"Попыток: {trans.number_of_retries}")
        
        # Проверяем логи ошибок
        print("\n" + "=" * 60)
        print("ПРОВЕРКА ЛОГОВ ОШИБОК")
        print("=" * 60)
        
        try:
            import json
            with open('./logs/data.json', 'r', encoding='utf-8') as f:
                logs = json.load(f)
                print(f"Всего записей в логе: {len(logs)}")
                for log in logs[-5:]:  # Последние 5 ошибок
                    print(f"  [{log['date']}] {log['error']}")
        except FileNotFoundError:
            print("Файл логов не найден")
        except Exception as e:
            print(f"Ошибка при чтении логов: {e}")
            
    except Exception as e:
        print(f"Ошибка при обработке очереди: {e}")
        import traceback
        traceback.print_exc()

# ============ ОТДЕЛЬНЫЕ ТЕСТЫ ДЛЯ ОСНОВНЫХ СЦЕНАРИЕВ ============

def test_specific_scenarios():
    """Тестирует конкретные сценарии по отдельности"""
    
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ОСНОВНЫХ СЦЕНАРИЕВ")
    print("=" * 60)
    
    # Сценарий 1: Успешная транзакция
    print("\n1. Успешная транзакция (< 5000):")
    trans1 = create_transaction_1()
    test_queue1 = TransactionQueue()
    test_queue1.add_to_queue(trans1)
    trans_procc.run_operation(test_queue1)
    print(f"   Результат: {trans1.transaction_status}")
    
    # Сценарий 2: Замороженный счет
    print("\n2. Перевод на замороженный счет:")
    trans2 = create_transaction_2()
    test_queue2 = TransactionQueue()
    test_queue2.add_to_queue(trans2)
    trans_procc.run_operation(test_queue2)
    print(f"   Результат: {trans2.transaction_status}")
    
    # Сценарий 3: Большая сумма (> 5000)
    print("\n3. Большая сумма (> 5000):")
    trans3 = create_transaction_8()
    test_queue3 = TransactionQueue()
    test_queue3.add_to_queue(trans3)
    trans_procc.run_operation(test_queue3)
    print(f"   Результат: {trans3.transaction_status}, Попыток: {trans3.number_of_retries}")
    
    # Сценарий 4: Отрицательная сумма
    print("\n4. Отрицательная сумма:")
    trans4 = create_transaction_9()
    try:
        commission = trans_procc.trans_commission(trans4)
        print(f"   Результат: Комиссия рассчитана ({commission})")
    except Exception as e:
        print(f"   Результат: Ошибка (как и ожидалось) - {e}")
    
    # Сценарий 5: Конвертация валют
    print("\n5. Конвертация валют (RUB -> USD):")
    trans5 = create_transaction_6()
    try:
        rate = trans_procc.convertor(trans5)
        print(f"   Результат: Курс {rate}")
        print(f"   Сумма {trans5.transaction_summ} RUB = {trans5.transaction_summ * rate} USD")
    except Exception as e:
        print(f"   Результат: Ошибка - {e}")

# ============ ЗАПУСК ТЕСТОВ ============

if __name__ == "__main__":
    # Тест всех транзакций
    test_all_transactions()
    
    # Дополнительные тесты сценариев
    test_specific_scenarios()
    
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)


# Проверка работы money_transfer
print("\n=== ТЕСТ МЕТОДА MONEY_TRANSFER ===")
test_trans = create_transaction_1()
print(f"Тестовая транзакция: сумма={test_trans.transaction_summ}")

# Проверяем напрямую
result = test_trans.money_transfer()
print(f"money_transfer() вернул: '{result}'")

# Проверяем для большой суммы
test_trans.transaction_summ = 6000
result2 = test_trans.money_transfer()
print(f"Для суммы 6000 money_transfer() вернул: '{result2}'")

# Проверяем для малой суммы
test_trans.transaction_summ = 1000
result3 = test_trans.money_transfer()
print(f"Для суммы 1000 money_transfer() вернул: '{result3}'")