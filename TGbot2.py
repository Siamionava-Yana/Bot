
import sqlite3
import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

TOKEN = "6350885658:AAFSBg-l2tHccE7u3b9edrUMeYTLW13pq-s"

bot = telebot.TeleBot(TOKEN)

# Создание и подключение к базе данных
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton(text="Телевизоры")
    button2 = types.KeyboardButton(text="Смартфоны")
    button3 = types.KeyboardButton(text="Холодильники")
    button4 = types.KeyboardButton(text="Не сейчас")
    markup.add(button1, button2, button3, button4)
    bot.send_message(
        chat_id,
        f"Здравствуйте, {first_name}!\n"
        "Вас приветствует магазин ЭлектроСилушка. Рады Вам предложить продукцию компании SAMSUNG. "
        "Пожалуйста, укажите  раздел, который Вас интересует и мы Вам поможем! ",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if message.text == "Телевизоры":
            # Создание и подключение к базе данных
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            # Создание таблицы, если она не существует
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price_discounted TEXT
                )
            ''')
            connection.commit()

            base_url = "https://sila.by/catalog/televizory/SAMSUNG"
            response = requests.get(base_url).text
            soup = BeautifulSoup(response, "html.parser")

            # Находим элемент пагинации
            pagination = soup.find("div", class_="pages")
            if pagination:
                page_links = pagination.find_all("a")
                total_pages = len(page_links) - 2  # Исключаем первую и последнюю ссылки
            else:
                total_pages = 1

            for page in range(1, total_pages + 1):
                page_url = base_url + ("/page/" + str(page) if page > 1 else "")
                response = requests.get(page_url).text
                soup = BeautifulSoup(response, "html.parser")
                sections = soup.find_all("div", class_="tovars")
                for section in sections:
                    products = section.find_all("div", class_="tov_prew")
                    for item in products:
                        product_name = item.find("strong").get_text(strip=True)
                        product_image = item.find("a").find("img").get("src")
                        product_price = item.find("div", class_="price").get_text(strip=True)
                        product_link = item.find("a").get("href")
                        product_price_new = item.find("div", class_="price").find('b').get_text(strip=True)

                        all_products = f"{product_name}\n" \
                                       f"{product_image}\n" \
                                       f"Ссылка: {product_link}\n" \
                                       f"Цена (со скидкой,   без скидки): {product_price}"

                        bot.send_message(chat_id, all_products)

                        # Вставка данных в таблицу
                        cursor.execute('''
                            INSERT INTO products (name, price_discounted)
                            VALUES (?, ?)
                        ''', (product_name, product_price_new))
                        connection.commit()

            # Закрываем соединение с базой данных
            cursor.close()
            connection.close()

            bot.send_message(chat_id, "На этом всё. Можем ли мы Вам еще чем-то помочь?")


        if message.text == "Смартфоны":
            # Создание и подключение к базе данных
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            # Создание таблицы, если она не существует
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            price_discounted TEXT
                        )
                    ''')
            connection.commit()

            base_url = "https://sila.by/catalog/mobilnye_telefony/SAMSUNG"
            response = requests.get(base_url).text
            soup = BeautifulSoup(response, "html.parser")

            # Находим элемент пагинации
            pagination = soup.find("div", class_="pages")
            if pagination:
                page_links = pagination.find_all("a")
                total_pages = len(page_links) - 2  # Исключаем первую и последнюю ссылки
            else:
                total_pages = 1

            for page in range(1, total_pages + 1):
                page_url = base_url + ("/page/" + str(page) if page > 1 else "")
                response = requests.get(page_url).text
                soup = BeautifulSoup(response, "html.parser")
                sections = soup.find_all("div", class_="tovars")
                for section in sections:

                    products = section.find_all("div", class_="tov_prew")
                    for item in products:
                        product_name = item.find("strong").get_text(strip=True)
                        product_image = item.find("a").find("img").get("src")
                        product_price = item.find("div", class_="price").get_text(strip=True)
                        product_link = item.find("a").get("href")
                        product_price_new = item.find("div", class_="price").find('b').get_text(strip=True)

                        all_products = f"{product_name}\n" \
                                       f"{product_image}\n" \
                                       f"Ссылка: {product_link}\n" \
                                       f"Цена (со скидкой,   без скидки): {product_price}"

                        bot.send_message(chat_id, all_products)

                        # Вставка данных в таблицу
                        cursor.execute('''
                            INSERT INTO products (name, price_discounted)
                            VALUES (?, ?)
                        ''', (product_name, product_price_new))
                        connection.commit()

            # Закрываем соединение с базой данных
            cursor.close()
            connection.close()

            bot.send_message(chat_id, "На этом всё. Можем ли мы Вам еще чем-то помочь?")

        if message.text == "Холодильники":
            # Создание и подключение к базе данных
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            # Создание таблицы, если она не существует
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            price_discounted TEXT
                        )
                    ''')
            connection.commit()

            base_url = "https://sila.by/catalog/holodilniki/SAMSUNG"
            response = requests.get(base_url).text
            soup = BeautifulSoup(response, "html.parser")

            # Находим элемент пагинации
            pagination = soup.find("div", class_="pages")
            if pagination:
                page_links = pagination.find_all("a")
                total_pages = len(page_links) - 2  # Исключаем первую и последнюю ссылки
            else:
                total_pages = 1

            for page in range(1, total_pages + 1):
                page_url = base_url + ("/page/" + str(page) if page > 1 else "")
                response = requests.get(page_url).text
                soup = BeautifulSoup(response, "html.parser")
                sections = soup.find_all("div", class_="tovars")
                for section in sections:

                    products = section.find_all("div", class_="tov_prew")
                    for item in products:
                        product_name = item.find("strong").get_text(strip=True)
                        product_image = item.find("a").find("img").get("src")
                        product_price = item.find("div", class_="price").get_text(strip=True)
                        product_link = item.find("a").get("href")
                        product_price_new = item.find("div", class_="price").find('b').get_text(strip=True)

                        all_products = f"{product_name}\n" \
                                       f"{product_image}\n" \
                                       f"Ссылка: {product_link}\n" \
                                       f"Цена (со скидкой,   без скидки): {product_price}"

                        bot.send_message(chat_id, all_products)

                        # Вставка данных в таблицу
                        cursor.execute('''
                            INSERT INTO products (name, price_discounted)
                            VALUES (?, ?)
                        ''', (product_name, product_price_new))
                        connection.commit()

            # Закрываем соединение с базой данных
            cursor.close()
            connection.close()

            bot.send_message(chat_id, "На этом всё. Можем ли мы Вам еще чем-то помочь?")

        elif message.text == "Не сейчас":
            bot.send_message(chat_id, f"Всего хорошего! Ждем Вас в следующий раз! Ваша ЭлектроСилушка!")



bot.polling(none_stop=True)


