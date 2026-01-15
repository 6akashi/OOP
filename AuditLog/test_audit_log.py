#!/usr/bin/env python3
"""
Минимальный тест AuditLog
"""
from datetime import datetime

from AuditLog import AuditLog



# Простые тесты
print("="*50)
print("МИНИМАЛЬНЫЕ ТЕСТЫ AUDITLOG")
print("="*50)

# Тест 1: Singleton
print("\n1. Тест Singleton:")
log1 = AuditLog.AuditLog()
log2 = AuditLog.AuditLog()
print(f"log1 is log2: {log1 is log2} ✅" if log1 is log2 else "❌")

# Тест 2: Логирование
print("\n2. Тест логирования:")
log1.log("CRITICAL", "Первое сообщение", "TEST")
log1.log("WARNING", "Второе сообщение", "TEST")
print(f"Логов в буфере: {len(log1.buffer)} ✅" if len(log1.buffer) == 2 else "❌")

# Тест 3: Получение последних логов
print("\n3. Тест get_recent_logs:")
recent = log1.get_recent_logs(1)
print(f"Последний лог: {recent[0].id if recent else 'Нет'} ✅" if recent and recent[0].id == "test2" else "❌")

# Тест 4: Фильтрация
print("\n4. Тест filter_logs:")
info_logs = log1.filter_logs({"Level": "INFO"})
print(f"INFO логов: {len(info_logs)} ✅" if len(info_logs) == 1 else "❌")

# Тест 5: Очистка
print("\n5. Тест clear_buffer:")
log1.clear_buffer()
print(f"Буфер пуст: {len(log1.buffer) == 0} ✅" if len(log1.buffer) == 0 else "❌")

print("\n" + "="*50)
print("ТЕСТЫ ЗАВЕРШЕНЫ")
print("="*50)