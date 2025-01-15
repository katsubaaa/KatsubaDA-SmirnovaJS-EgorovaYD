import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, database_url):
        self.database_url = database_url

    def connect(self):
        """Создает подключение к базе данных."""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)

    def add_item(self, user_id, item_name, item_url, current_price):
        """Добавляет новый товар в таблицу."""
        if self.item_exists(user_id, item_url):
            return False  # Товар уже существует
        
        conn = self.connect()
        cursor = conn.cursor()
        try:
            price_history = json.dumps([{"date": datetime.now().isoformat(), "price": current_price}])
            cursor.execute("""
                INSERT INTO price_tracking (user_id, item_name, item_url, current_price, price_history)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, item_name, item_url, current_price, price_history))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_items(self, user_id):
        """Получает все товары пользователя."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, item_name, item_url, current_price, price_history, last_checked
                FROM price_tracking
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()
            
    def get_items_within_days(self, user_id, days):
        """Получает товары с историей изменений за последние N дней."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, item_name, current_price, price_history
                FROM price_tracking
                WHERE user_id = %s
            """, (user_id,))
            items = cursor.fetchall()

            # Фильтрация истории по количеству дней
            cutoff_date = datetime.now() - timedelta(days=days)
            for item in items:
                filtered_history = [
                    record for record in item["price_history"]
                    if datetime.fromisoformat(record["date"]) >= cutoff_date
                ]
                item["price_history"] = filtered_history
            return items
        finally:
            conn.close()
            
    def item_exists(self, user_id, item_url):
        """Проверяет, существует ли товар с таким URL для пользователя."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM price_tracking
                WHERE user_id = %s AND item_url = %s
            """, (user_id, item_url))
            return cursor.fetchone()["count"] > 0
        finally:
            conn.close()

    def delete_item(self, user_id, item_id):
        """Удаляет товар по ID, если он принадлежит пользователю."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM price_tracking
                WHERE user_id = %s AND id = %s
                RETURNING id
            """, (user_id, item_id))
            deleted_item = cursor.fetchone()
            conn.commit() 
            # Если `deleted_item` пустой, значит товар не найден или не принадлежит пользователю
            return bool(deleted_item)
        finally:
            conn.close()

    def update_price(self, item_id, new_price):
        """Обновляет текущую цену товара и добавляет запись в историю."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # Получаем текущую историю цен
            cursor.execute("""
                SELECT price_history 
                FROM price_tracking WHERE id = %s
            """, (item_id,))
            result = cursor.fetchone()
            if result:
                history = result["price_history"]
                history.append({"date": datetime.now().isoformat(), "price": new_price})

                # Обновляем текущую цену и историю
                cursor.execute("""
                    UPDATE price_tracking
                    SET current_price = %s, price_history = %s, last_checked = NOW()
                    WHERE id = %s
                """, (new_price, json.dumps(history), item_id))
                conn.commit()
        finally:
            conn.close()