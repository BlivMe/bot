import sqlite3


# Создание базы данных и таблиц
def create_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    # Создание таблицы goods
    c.execute('''CREATE TABLE IF NOT EXISTS goods
                 (product_code INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_name TEXT NOT NULL,
                  purchase_price REAL NOT NULL,
                  expected_price REAL NOT NULL);''')

    # Создание таблицы in_stock
    c.execute('''CREATE TABLE IF NOT EXISTS in_stock
                 (in_stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_code INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  purchase_sum REAL NOT NULL,
                  status TEXT NOT NULL,
                  expected_sum REAL NOT NULL,
                  FOREIGN KEY (product_code) REFERENCES goods (product_code));''')

    # Создание таблицы sold
    c.execute('''CREATE TABLE IF NOT EXISTS sold
                 (sold_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  in_stock_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  status TEXT NOT NULL,
                  sales_sum REAL NOT NULL,
                  FOREIGN KEY (in_stock_id) REFERENCES in_stock (in_stock_id));''')

    conn.commit()
    conn.close()


# Функция добавления товара в таблицу goods
def add_goods(product_name, purchase_price, expected_price):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("INSERT INTO goods (product_name, purchase_price, expected_price) "
              "VALUES (?, ?, ?)",
              (product_name, purchase_price, expected_price))
    conn.commit()
    conn.close()


# Функция добавления запаса товара в таблицу in_stock
def add_in_stock(product_code, quantity, purchase_sum, status, expected_sum):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("INSERT INTO in_stock (product_code, quantity, purchase_sum, status, expected_sum) "
              "VALUES (?, ?, ?, ?, ?)",
              (product_code, quantity, purchase_sum, status, expected_sum))
    conn.commit()
    conn.close()


# Функция добавления продажи товара в таблицу sold
def add_sold(in_stock_id, quantity, status, sales_sum):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("INSERT INTO sold (in_stock_id, quantity, status, sales_sum) "
              "VALUES (?, ?, ?, ?)",
              (in_stock_id, quantity, status, sales_sum))
    conn.commit()
    conn.close()


# Функция получения списка товаров
def get_goods():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT * FROM goods")
    rows = c.fetchall()
    conn.close()
    return rows


# Функция получения списка запасов товаров
def get_in_stock():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT * FROM in_stock where status = 'В продаже'")
    rows = c.fetchall()
    conn.close()
    return rows


def get_in_stock_by_id(in_stock_id):
    """
    Получает данные о товаре из таблицы in_stock по его идентификатору.

    :param in_stock_id: Идентификатор товара в таблице in_stock.
    :return: Кортеж с данными о товаре
    (product_code, product_name, quantity, purchase_sum, status, expected_sum) или None, если запись не найдена.
    """
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT product_code, quantity, purchase_sum, status, expected_sum FROM in_stock WHERE in_stock_id=?",
              [in_stock_id])
    result = c.fetchone()
    conn.close()
    return result if result is not None else None


# Функция получения списка продаж товаров
def get_sold():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sold where status = 'Продано'")
    rows = c.fetchall()
    conn.close()
    return rows


def get_product_data(product_code):
    # Получаем данные о товаре из таблицы goods
    connection = sqlite3.connect('sales.db')
    cursor = connection.cursor()
    cursor.execute("SELECT product_name, purchase_price, expected_price FROM goods WHERE product_code = ?",
                   [product_code])
    result = cursor.fetchone()
    connection.close()
    return result


# Функция обновления товара в таблице goods
def update_good(product_code, new_product_name=None, new_purchase_price=None, new_expected_price=None):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    # Формируем запрос для обновления данных
    update_query = "UPDATE goods SET "
    update_params = []

    if new_product_name is not None:
        update_query += "product_name=?, "
        update_params.append(new_product_name)

    if new_purchase_price is not None:
        update_query += "purchase_price=?, "
        update_params.append(new_purchase_price)

    if new_expected_price is not None:
        update_query += "expected_price=?, "
        update_params.append(new_expected_price)

    # Убираем лишнюю запятую в конце запроса
    update_query = update_query[:-2]

    # Добавляем условие для поиска нужного товара
    update_query += " WHERE product_code=?"
    update_params.append(product_code)

    # Выполняем запрос на обновление данных
    c.execute(update_query, tuple(update_params))
    conn.commit()
    conn.close()


# Функция обновления запаса товара в таблице in_stock
def update_in_stock(in_stock_id, new_quantity=None, new_purchase_sum=None, new_status=None, new_expected_sum=None):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    # Формируем запрос для обновления данных
    update_query = "UPDATE in_stock SET "
    update_params = []

    if new_quantity is not None:
        update_query += "quantity=?, "
        update_params.append(new_quantity)

    if new_purchase_sum is not None:
        update_query += "purchase_sum=?, "
        update_params.append(new_purchase_sum)

    if new_status is not None:
        update_query += "status=?, "
        update_params.append(new_status)

    if new_expected_sum is not None:
        update_query += "expected_sum=?, "
        update_params.append(new_expected_sum)

    # Убираем лишнюю запятую в конце запроса
    update_query = update_query[:-2]

    # Добавляем условие для поиска нужного запаса товара
    update_query += " WHERE in_stock_id=?"
    update_params.append(in_stock_id)

    # Выполняем запрос на обновление данных
    c.execute(update_query, tuple(update_params))
    conn.commit()
    conn.close()


# Функция обновления продажи товара в таблице sold
def update_sold(sold_id, new_quantity=None, new_status=None, new_sum=None):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    # Формируем запрос для обновления данных
    update_query = "UPDATE sold SET "
    update_params = []

    if new_quantity is not None:
        update_query += "quantity=?, "
        update_params.append(new_quantity)

    if new_status is not None:
        update_query += "status=?, "
        update_params.append(new_status)

    if new_sum is not None:
        update_query += "sum=?, "
        update_params.append(new_sum)

    # Убираем лишнюю запятую в конце запроса
    update_query = update_query[:-2]

    # Добавляем условие для поиска нужной продажи товара
    update_query += " WHERE sold_id=?"
    update_params.append(sold_id)

    # Выполняем запрос на обновление данных
    c.execute(update_query, tuple(update_params))
    conn.commit()
    conn.close()


def calculate_total_sales_sum():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT SUM(sales_sum) FROM sold WHERE status = 'Продано'")
    total_sales_sum = c.fetchone()[0]
    conn.close()
    return total_sales_sum


def update_sold_status():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("UPDATE sold SET status = 'Деньги выданы' WHERE status = 'Продано'")
    conn.commit()
    conn.close()
