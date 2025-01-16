import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db_manager import DatabaseManager
from parser import Parser

# Настройки
BOT_TOKEN = "7527184658:AAE1Ha6mDonhA7bPN4fPG_qSORBA_kQ8nYw"
DATABASE_URL = "postgresql://postgres:password@localhost:5432/db_emotions"

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db = DatabaseManager(DATABASE_URL)
parser = Parser()

# Команды
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("""Привет! Отправь ссылку на товар с Яндекс.Маркет, чтобы я отслеживал его цену. 
Если хочешь увидеть историю отслеживания цен на товары за последние n дней, напиши команду /history <кол-во дней>.
Если хочешь удалить товар из отслеживаемых, напиши команду /delete <id_предмета>""")

@dp.message_handler(commands=["history"])
async def history_command(message: types.Message):
    user_id = message.from_user.id
    command_parts = message.text.split()

    # Проверяем, указан ли параметр количества дней
    if len(command_parts) > 1:
        try:
            days = int(command_parts[1])
            if days <= 0:
                raise ValueError
        except ValueError:
            await message.reply("Укажите корректное количество дней (целое положительное число).")
            return
    else:
        days = None  # Если параметр не указан, выводим всю историю

    # Получаем данные из базы
    if days:
        items = db.get_items_within_days(user_id, days)
    else:
        items = db.get_items(user_id)

    if not items:
        await message.reply("У вас пока нет отслеживаемых товаров.")
        return

    # Формируем ответ
    response = f"История цен{' за последние {days} дней' if days else ''}:\n\n"
    for item in items:
        response += f"ID: {item['id']}\nНазвание: {item['item_name']}\nТекущая цена: {item['current_price']} ₽\n"
        if item["price_history"]:
            for record in item["price_history"]:
                response += f" - {record['date']}: {record['price']} ₽\n"
        else:
            response += " - Изменений за указанный период нет.\n"
        response += "\n"

    await message.reply(response)

@dp.message_handler(commands=["delete"])
async def delete_command(message: types.Message):
    user_id = message.from_user.id
    command_parts = message.text.split()
    if len(command_parts) != 2 or not command_parts[1].isdigit():
        await message.reply("Использование: /delete <id_предмета>")
        return

    item_id = int(command_parts[1])
    if not db.delete_item(user_id, item_id):
        await message.reply(f"Товар с ID {item_id} не найден или не принадлежит вам.")
        return

    await message.reply(f"Товар с ID {item_id} удален из отслеживания.")

@dp.message_handler()
async def add_item(message: types.Message):
    item_url = message.text.strip()
    if "market.yandex.ru" not in item_url:
        await message.reply("Это не ссылка на Яндекс.Маркет. Попробуй еще раз.")
        return

    price, title = parser.parse_item_details(item_url)
    if price is None or title is None:
        await message.reply("Не удалось получить информацию о товаре.")
        return

    if not db.add_item(message.from_user.id, title, item_url, price):
        await message.reply("Этот товар уже добавлен в отслеживание.")
        return

    await message.reply(f"Товар '{title}' добавлен! Цена: {price} ₽")

# Фоновая проверка цен
async def check_prices():
    while True:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_url, current_price, price_history, item_name FROM price_tracking")
        items = cursor.fetchall()

        for item in items:
            new_price, _ = parser.parse_item_details(item["item_url"])
            print(f"Проверка ID {item['id']} - новая цена: {new_price}, текущая: {item['current_price']}") #Отслеживание изменения цен
            if new_price and new_price != item["current_price"]:
                # Обновление цены в базе данных
                db.update_price(item["id"], new_price)
                print(f"Цена для ID {item['id']} обновлена.")
                conn.commit()

        conn.close()
        await asyncio.sleep(600)  # Проверять каждые 10 минут

# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_prices())  # Запуск фоновой задачи
    executor.start_polling(dp, skip_updates=True)

    