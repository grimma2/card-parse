from info_db import DB
from botbuttons import markup_layer1, most, month_now
import my_settings

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import StatesGroup, State

cb = CallbackData('layer', 'text')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=my_settings.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
DB_connect = DB()
WARNING_TEXT = 'Устовленный лимит превышен'


class LayersState(StatesGroup):
    lay1 = State()
    lay2 = State()


class OgrState(StatesGroup):
    get_answer = State()


def support_handlers_layer1(for_):
    cursor = DB_connect.get_last_30_or_none('cost')
    req_on = DB_connect.get_ogr()
    default_sum = sum([data[0] for data in cursor])
    if not req_on == '':
        check = str(default_sum) + ' ' + WARNING_TEXT if default_sum > [
            x for x in DB_connect.get_ogr()
    ][0][0] else default_sum
    if for_ == 'layer1:last_30_days':
        if not cursor == '':
            return {'answer':
                        f'За последние 30 дней потрачено:, {check}',
                    'cursor': cursor
                    }
        else:
            return {'answer': 'Данные не найдены', 'cursor': cursor}
    elif for_ == 'layer1:last_month':
        if not cursor == '':
            return {'answer':
                        f'за {month_now} потрачено: {check}',
                    'cursor': cursor
                    }
        else:
            return {'answer': 'Данные не найдены', 'cursor': cursor}


def support_handlers_layer2(handler_obj, cursor_obj):
    CHECK_FIELDS = {0: 'Название', 1: 'Цена', 2: 'Дата'}

    return {'answer': {'chat_id': handler_obj.message.chat.id, 'text': ' '.join(
        [f'{CHECK_FIELDS[i]}: {data},' for i, data in enumerate(cursor_obj) if i < 3]
    )}}


@dp.message_handler(commands=['start', 'go'])
async def start_func(message: types.Message):
    await message.answer('Начало работы', reply_markup=markup_layer1)
    await LayersState.first()


@dp.callback_query_handler(text_contains='layer1', state=LayersState.lay1)
async def last_30_days(call: types.CallbackQuery, state: FSMContext):
    layer1_text = call.data
    await state.update_data(layer1_text=layer1_text)
    local_data = support_handlers_layer1(for_=layer1_text)
    await call.message.answer(local_data['answer'], reply_markup=most)
    await LayersState.next()


@dp.callback_query_handler(text_contains='layer2', state=LayersState.lay2)
async def most_info(call: types.CallbackQuery, state: FSMContext):
    fsm_data = await state.get_data()

    if fsm_data['layer1_text'] == 'layer1:last_30_days':
        local_data = DB_connect.get_last_30_or_none()
    elif fsm_data['layer1_text'] == 'layer1:last_month':
        local_data = DB_connect.get_last_month_or_none()

    for obj in local_data:
        query_data = support_handlers_layer2(handler_obj=call, cursor_obj=obj)['answer']
        await bot.send_message(chat_id=query_data['chat_id'], text=query_data['text'])

    await state.finish()


@dp.message_handler(commands=['dobavit_ogranicheniya'])
async def check_ogr(message: types.Message):
    await message.answer('Введи ограничение на траты')
    await OgrState.first()


@dp.message_handler(state=OgrState.get_answer)
async def answer_ogr(message: types.Message, state: FSMContext):
    try:
        DB_connect.add_ogr(int(message.text))
    except Exception:
        await message.answer('Ввести нужно число')
    else:
        await message.answer('Ограничение успешно установенно')

    await state.finish()


@dp.message_handler(commands=['del_ogr'])
async def del_ogr(message: types.Message):
    DB_connect.del_ogr()
    await message.answer('Ограничение успешно удаленно')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
