from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import database


# Обработчик команды start
def start(update, context):
    update.message.reply_text('Привет! Я бот для учета продаж. Для просмотра всех команд введите /help_command. '
                              'Рекомендуем начать работу с ботом с заполнения таблиц при помощи команд '
                              '/add_goods и /add_in_stock.')


# Определите константы для состояний диалога
ADD_GOODS_NAME, ADD_GOODS_PRICE, ADD_GOODS_EXPECTED_PRICE = range(3)


# Определите функции для каждого состояния диалога
def add_goods_start(update, context):
    update.message.reply_text('Введите название товара:')
    return ADD_GOODS_NAME


def add_goods_name(update, context):
    context.user_data['add_goods'] = {'product_name': update.message.text}
    update.message.reply_text('Введите цену закупки:')
    return ADD_GOODS_PRICE


def add_goods_price(update, context):
    try:
        context.user_data['add_goods']['purchase_price'] = float(update.message.text)
        update.message.reply_text('Введите ожидаемую цену продажи:')
        return ADD_GOODS_EXPECTED_PRICE
    except ValueError:
        update.message.reply_text('Неправильный формат цены. Введите число с плавающей точкой (например, 10.99):')
        return ADD_GOODS_PRICE


def add_goods_expected_price(update, context):
    try:
        context.user_data['add_goods']['expected_price'] = float(update.message.text)
        # Добавляем товар в таблицу
        database.add_goods(
            context.user_data['add_goods']['product_name'],
            context.user_data['add_goods']['purchase_price'],
            context.user_data['add_goods']['expected_price']
        )

        # Отправляем сообщение
        update.message.reply_text('Товар успешно добавлен!')

        # Очищаем контекст
        context.user_data['add_goods'].clear()

        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Неправильный формат цены. Введите число с плавающей точкой (например, 10.99):')
        return ADD_GOODS_EXPECTED_PRICE


def add_goods_cancel(update, context):
    context.user_data['add_goods'].clear()
    update.message.reply_text('Добавление товара отменено.')
    return ConversationHandler.END


def add_goods_error(update, context):
    update.message.reply_text('Что-то пошло не так. Попробуйте еще раз позже.')
    return ConversationHandler.END


def goods(update, context):
    # Получаем данные из таблицы goods
    goods_data = database.get_goods()

    if len(goods_data) == 0:
        message = "Артикулы еще не записаны. " \
                  "Используйте /add_goods для добавления новых артикулов. "
        # Отправляем сообщение
        update.message.reply_text(message)

    else:
        message = "{:<10} {:<10} {:<14} {:<10}".\
            format("Артикул |", "Название |", "Цена закупки |", "Ожид. цена")
        message += "\n" + "-" * 70
        for item in goods_data:
            message += "\n{:<10} {:<20} {:<10.2f} {:<10.2f}".format(item[0], item[1], item[2], item[3])
        # Отправляем сообщение
        update.message.reply_text(message)


# Определите константы для состояний диалога
ADD_IN_STOCK_PRODUCT_CODE, ADD_IN_STOCK_QUANTITY = range(2)


# Определите функции для каждого состояния диалога
def add_in_stock_start(update, context):
    update.message.reply_text('Введите артикул товара:')
    return ADD_IN_STOCK_PRODUCT_CODE


def add_in_stock_product_code(update, context):
    # Получаем аргументы команды
    product_code = update.message.text

    # Получаем данные о товаре из таблицы goods
    product_data = database.get_product_data(product_code)
    if product_data is None:
        update.message.reply_text(f"Товар с артикулом {product_code} не найден. Введите артикул товара:")
        return ADD_IN_STOCK_PRODUCT_CODE

    # Сохраняем данные о товаре в контексте
    context.user_data['add_in_stock'] = {
        'product_code': product_code,
        'product_name': product_data[0],
        'purchase_price': product_data[1],
        'expected_price': product_data[2]
    }

    update.message.reply_text('Введите количество товара:')
    return ADD_IN_STOCK_QUANTITY


def add_in_stock_quantity(update, context):
    try:
        # Парсим аргументы команды
        quantity = int(update.message.text)

        product_code = context.user_data['add_in_stock']['product_code']
        purchase_price = context.user_data['add_in_stock']['purchase_price']
        expected_price = context.user_data['add_in_stock']['expected_price']

        # Вычисляем purchase_sum и expected_sum
        purchase_sum = purchase_price * quantity
        expected_sum = expected_price * quantity

        # Добавляем товар на склад
        status = "В продаже"
        database.add_in_stock(product_code, quantity, purchase_sum, status, expected_sum)

        # Отправляем сообщение
        update.message.reply_text('Товары успешно добавлены в продажу!')

        # Очищаем контекст
        context.user_data['add_in_stock'].clear()

        return ConversationHandler.END

    except ValueError:
        update.message.reply_text('Ошибка при добавлении товара на склад. Введите количество товара:')
        return ADD_IN_STOCK_QUANTITY


def add_in_stock_cancel(update, context):
    context.user_data['add_in_stock'].clear()
    update.message.reply_text('Добавление товара на склад отменено.')
    return ConversationHandler.END


def add_in_stock_error(update, context):
    update.message.reply_text('Что-то пошло не так. Попробуйте еще раз позже.')
    return ConversationHandler.END


def in_stock(update, context):
    # Получаем данные из таблицы in_stock
    stock_data = database.get_in_stock()

    if len(stock_data) == 0:
        message = "Товаров в продаже нет. Используйте /add_in_stock для добавления товаров в продажу."
        # Отправляем сообщение
        update.message.reply_text(message)

    else:
        # Выводим данные в табличном виде
        message = "{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format("№ записи", "Артикул", "Количество",
                                                                     "Закуп", "Статус", "Ожид. сумма")
        message += "\n" + "-" * 70
        for item in stock_data:
            message += "\n{:<16} {:<16} {:<16} {:<16} {:<16} {:<16}".format(item[0], item[1], item[2], item[3],
                                                                            item[4], item[5])
        # Отправляем сообщение
        update.message.reply_text(message)


def in_stock_statistics(update, context):
    # Получаем данные из таблицы in_stock
    stock_data = database.get_in_stock()

    # Вычисляем суммы цен закупки и ожидаемых цен продаж
    purchase_sum = sum(item[3] for item in stock_data)
    expected_sum = sum(item[5] for item in stock_data)

    # Вычисляем разницу между ожидаемой суммой продаж и суммой закупки
    difference = expected_sum - purchase_sum

    # Выводим статистику
    message = f"Сумма закупки: {purchase_sum:.2f}\nСумма ожидаемых продаж: {expected_sum:.2f}\n" \
              f"Разница: {difference:.2f}"
    update.message.reply_text(message)


# Определяем стадии разговора
IN_STOCK_ID, QUANTITY, SALES_SUM = range(3)


def start_goods_sold(update, context):
    update.message.reply_text("Введите ID записи в таблице in_stock:")
    return IN_STOCK_ID


def get_quantity(update, context):
    in_stock_id = update.message.text
    if not in_stock_id.isdigit():
        update.message.reply_text("Неправильный формат ID записи. Введите целое число.")
        return IN_STOCK_ID

    in_stock_id = int(in_stock_id)
    in_stock_data = database.get_in_stock_by_id(in_stock_id)
    if in_stock_data is None:
        update.message.reply_text(f"Товар с ID {in_stock_id} не найден.")
        return ConversationHandler.END

    context.user_data['in_stock_id'] = in_stock_id
    update.message.reply_text("Введите количество проданных товаров:")
    return QUANTITY


def get_sales_sum(update, context):
    quantity = update.message.text
    if not quantity.isdigit():
        update.message.reply_text("Неправильный формат количества проданных товаров. Введите целое число.")
        return QUANTITY

    quantity = int(quantity)
    context.user_data['quantity'] = quantity
    update.message.reply_text("Введите сумму продаж:")
    return SALES_SUM


def process_goods_sold(update, context):
    sales_sum = update.message.text
    in_stock_id = context.user_data.get('in_stock_id')
    quantity = context.user_data.get('quantity')

    sales_sum = float(sales_sum)

    in_stock_data = database.get_in_stock_by_id(in_stock_id)

    product_code, quantity_in_stock, purchase_sum, status, expected_sum = in_stock_data

    if quantity > quantity_in_stock:
        update.message.reply_text(f"Количество проданных товаров ({quantity}) превышает "
                                  f"количество товаров в наличии ({quantity_in_stock}).")
        return ConversationHandler.END

    if quantity_in_stock == quantity or quantity_in_stock == 0:
        new_purchase_sum = 0
        new_expected_sum = 0
    else:
        new_purchase_sum = purchase_sum / quantity_in_stock * (quantity_in_stock - quantity)
        new_expected_sum = expected_sum / quantity_in_stock * (quantity_in_stock - quantity)

    sold_status = "Продано"

    quantity_in_stock -= quantity
    if quantity_in_stock == 0:
        status = "Продано"
    database.update_in_stock(in_stock_id, quantity_in_stock, new_purchase_sum, status, new_expected_sum)

    database.add_sold(in_stock_id, quantity, sold_status, sales_sum)

    update.message.reply_text('Товар успешно продан!')
    return ConversationHandler.END


def sold(update, context):
    # Получаем список продаж товаров
    sold_data = database.get_sold()

    # Если список пуст, выводим сообщение об этом
    if len(sold_data) == 0:
        message = "Список продаж пуст."
        # Отправляем сообщение
        update.message.reply_text(message)

    else:
        # Выводим данные в табличном виде
        message = "{:<8} {:<10} {:<10} {:<10} {:<10}".format("Sold ID", "№ in_stock", "Количество",
                                                             "Статус", "Сумма продажи")
        message += "\n" + "-" * 70
        for item in sold_data:
            message += "\n{:<20} {:<18} {:<13} {:<13} {:<10.2f}".format(item[0], item[1], item[2], item[3], item[4])
        # Отправляем сообщение
        update.message.reply_text(message)


def money_to_be_issued(update, context):
    # Рассчитываем общую сумму продаж со статусом "Продано"
    total_sales_sum = database.calculate_total_sales_sum()

    # Если сумма продаж не равна None, отправляем ее пользователю в Telegram
    if total_sales_sum is not None:
        message = "Общая сумма продаж: {:.2f}".format(total_sales_sum)
        update.message.reply_text(message)
    else:
        message = "Нет записей со статусом 'Продано'."
        update.message.reply_text(message)


def get_money(update, context):
    # Рассчитываем общую сумму продаж со статусом "Продано"
    total_sales = database.calculate_total_sales_sum()

    # Обновляем статусы продаж в таблице sold на "Деньги выданы"
    database.update_sold_status()

    # Выводим сообщение, что статусы изменены
    text = "Статусы продаж изменены на 'Деньги выданы'."
    update.message.reply_text(text)

    # Если сумма продаж не равна None, отправляем ее пользователю в Telegram
    if total_sales is not None:
        # Инициализируем бота и отправляем сообщение
        message = "Общая полученная сумма: {:.2f}".format(total_sales)
        update.message.reply_text(message)
    else:
        # Если в таблице sold нет записей со статусом "Продано",
        # отправляем соответствующее сообщение пользователю в Telegram
        message = "Нет записей со статусом 'Продано'."
        update.message.reply_text(message)


# Обработчик неизвестных команд
def unknown(update, context):
    update.message.reply_text("Извините, я не понимаю эту команду.")


# Обработчик сообщений
def echo(update, context):
    update.message.reply_text(update.message.text)


def help_command(update, context):
    help_text = '''
    Список команд:
    /start - Запуск бота
    /help_command - Получение справки по командам
    /add_goods - Добавление нового товара в базу
    /goods - Вывод всех артикулов товаров
    /add_in_stock - Добавление новых товаров в продажу
    /in_stock - Вывод всех товаров в продаже
    /in_stock_statistics - Вывод статистики по товарам в продаже
    /goods_sold - Продажа товаров
    /sold - Вывод всех проданных товаров
    /money_to_be_issued - Рассчитываем общую сумму продаж со статусом "Продано"
    /get_money - Получить деньги
    '''
    update.message.reply_text(help_text)


# Основная функция
def main():
    # создание бота
    updater = Updater("6209453965:AAEeVf502zmYV8LhZk2g3N44V9nUSuSsO-Y", use_context=True)

    # получение диспетчера команд
    dp = updater.dispatcher

    # добавление обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help_command", help_command))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add_goods', add_goods_start)],
        states={ADD_GOODS_NAME: [MessageHandler(Filters.text, add_goods_name)],
                ADD_GOODS_PRICE: [MessageHandler(Filters.text, add_goods_price)],
                ADD_GOODS_EXPECTED_PRICE: [MessageHandler(Filters.text, add_goods_expected_price)]},
        fallbacks=[CommandHandler('cancel', add_goods_cancel)],
        allow_reentry=True))
    dp.add_handler(CommandHandler("goods", goods))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add_in_stock', add_in_stock_start)],
        states={
            ADD_IN_STOCK_PRODUCT_CODE: [MessageHandler(Filters.text, add_in_stock_product_code)],
            ADD_IN_STOCK_QUANTITY: [MessageHandler(Filters.text, add_in_stock_quantity)]
        },
        fallbacks=[CommandHandler('cancel', add_in_stock_cancel)],
        allow_reentry=True))
    dp.add_handler(CommandHandler("in_stock", in_stock))
    dp.add_handler(CommandHandler("in_stock_statistics", in_stock_statistics))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('goods_sold', start_goods_sold)],
        states={
            IN_STOCK_ID: [MessageHandler(Filters.text, get_quantity)],
            QUANTITY: [MessageHandler(Filters.text, get_sales_sum)],
            SALES_SUM: [MessageHandler(Filters.text, process_goods_sold)]
        },
        fallbacks=[],
        allow_reentry=True))
    dp.add_handler(CommandHandler("sold", sold))
    dp.add_handler(CommandHandler("money_to_be_issued", money_to_be_issued))
    dp.add_handler(CommandHandler("get_money", get_money))

    # добавление обработчика неизвестных команд
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # запуск бота
    updater.start_polling()

    # остановка бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    database.create_db()
    main()
