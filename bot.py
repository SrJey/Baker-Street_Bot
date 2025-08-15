import asyncio
import os
import pandas as pd
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile

# Здесь остальные импорты из предыдущей версии бота (sqlite3, datetime, qrcode, APScheduler и т.д.)
# ...

BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
ADMIN_CHAT_IDS = [int(x) for x in os.getenv("ADMIN_CHAT_IDS", "").split(",") if x.strip().isdigit()]
EMPLOYEE_CSV = os.getenv("EMPLOYEE_CSV", "table-3c7afa33-d834-4feb-85a1-5d90237a9fd8-5.csv")

# Функция проверки прав админа
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_CHAT_IDS

# Загрузка сотрудников
def load_employees():
    df = pd.read_csv(EMPLOYEE_CSV)
    return {str(row[0]).strip(): str(row[1]).strip() for _, row in df.iterrows()}

employees = load_employees()

# Команда для добавления нового сотрудника
async def cmd_add_employee(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("Доступ запрещён.")
        return
    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        await message.reply("Использование: /add_employee КОД ФИО")
        return
    code, name = parts[1], parts[2]
    if code in employees:
        await message.reply("Сотрудник с таким кодом уже существует.")
        return
    # Добавляем в словарь и CSV
    employees[code] = name
    df = pd.DataFrame(list(employees.items()), columns=["code", "name"])
    df.to_csv(EMPLOYEE_CSV, index=False)
    await message.reply(f"Сотрудник {name} добавлен с кодом {code}.")

# Команды отчётов с авторизацией
async def cmd_report_today(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("Доступ запрещён.")
        return
    # ... код формирования отчёта за сегодня ...

async def cmd_report_month(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("Доступ запрещён.")
        return
    # ... код формирования отчёта за месяц ...

async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.message.register(cmd_add_employee, Command("add_employee"))
    dp.message.register(cmd_report_today, Command("report_today"))
    dp.message.register(cmd_report_month, Command("report_month"))
    # Остальные хендлеры из исходной версии бота
    # ...
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
