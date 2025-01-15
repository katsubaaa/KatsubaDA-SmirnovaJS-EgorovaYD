from bs4 import BeautifulSoup
import requests
import re

# Парсинг цены и названия товара с Яндекс.Маркет
class Parser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def parse_item_details(self, item_url):
        try:
            response = requests.get(item_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Попытка получить основную цену
            price_element = soup.find("span", {"data-auto": "price-value"})
            if price_element:
                price = float(price_element.get_text(strip=True).replace(" ", "").replace("₽", "").strip())
            else:
                # Если основной цены нет, ищем альтернативный элемент
                price = self._parse_alternative_price(soup)

            # Получение названия товара
            title_element = soup.find("h1", {"data-auto": "productCardTitle"})
            title = title_element.get_text(strip=True) if title_element else "Без названия"

            return price, title
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            return None, None

    def _parse_alternative_price(self, soup):
        """
        Извлекает альтернативную цену из элементов со старыми ценами.
        """
        try:
            # Ищем элемент с альтернативной ценой
            alt_price_element = soup.find("span", {"data-auto": "snippet-price-old"})
            if not alt_price_element:
                return None

            # Извлекаем текст цены с использованием регулярного выражения
            price_text = alt_price_element.get_text(strip=True)
            match = re.search(r"(\d[\d\s]*\d)", price_text)  # Ищем первое числовое значение
            if match:
                return float(match.group(1).replace(" ", "").replace(" ", ""))
            return None
        except Exception as e:
            print(f"Ошибка парсинга альтернативной цены: {e}")
            return None