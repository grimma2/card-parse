from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import datetime


MONTH_KEYS = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Инюнь', 7: 'Июль',
              8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
month_now = MONTH_KEYS[int(str(datetime.datetime.now()).split('-')[1])]

markup_layer1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='За последние 30 дней',
                callback_data='layer1:last_30_days'),
            InlineKeyboardButton(text=f'За {month_now}', callback_data='layer1:last_month')
        ]
    ], resize_keyboard=True
)

most = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подробнее', callback_data='layer2:most')
        ]
    ]
)