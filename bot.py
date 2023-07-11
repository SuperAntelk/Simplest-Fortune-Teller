from datetime import date


import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from services.predictor import PredictorService

#ФИО,дата,повторяющиеся каждый под каждым,вычеркивается четные столбцы,
#УТРО ДЕНЬ ВЕЧЕР вычеркиваются в буквы в каждом последовательности
#ДНУВРО
#подсчёт количества букв в каждом из времен
#Д-дорога
# по остатку считалочкой от Днувро:
# Н-неожиданность
# У-удача
# В-встреча
# р-радость
# о-обида

bot=Bot(token=TOKEN)

storage = MemoryStorage()
dp=Dispatcher(bot=bot,storage=storage)
predict=PredictorService().predict

class Form(StatesGroup):
    name=State()
    predict=State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_name=message.from_user.first_name
    logging.info(f'{user_id=} {user_full_name=} ')

    await Form.name.set()
    ans_text=md.text('/help')
    await message.answer(f"Привет! Для прогноза, напиши своё ФИО")


# You can use state='*' if you want to handle all states
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Cancelled.')

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """Process user name"""

    # Finish our conversation
    async with state.proxy() as data:
        data['name'] = message.text
        #btn
        button_predict_today = InlineKeyboardButton('Прогноз на сегодня',callback_data='btn_predict_today')
        predict_kb=InlineKeyboardMarkup()
        predict_kb.add(button_predict_today)


        await message.reply(md.text(f"Отлично, {data['name']}!\nТеперь ты можешь получить получить прогноз на сегодня "),reply_markup=predict_kb)
    await Form.next()


#print('OUTPUUUT\n',predict(name,today))


@dp.message_handler(commands=['прогноз'],state=Form.predict)
async def predict_handler(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        prediction=predict(data['name'],date.today())
        data['predict']=prediction
        await message.answer(
           md.text(prediction.name,
                   prediction.date,
                   prediction.code,
                   *[f'\n{k.capitalize()}\n{v.key}\n{v.key_len}\n{v.predict}'for k,v in prediction.predictions.items()],
                   sep='\n')
        )

@dp.callback_query_handler(lambda c: c.data == 'btn_predict_today',state=Form.predict)
async def process_callback_predict(callback_query: types.CallbackQuery,state: FSMContext):
    async with state.proxy() as data:
        prediction=predict(data['name'],date.today())
        data['predict']=prediction
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
           md.text(prediction.name,
                   prediction.date,
                   prediction.code,
                   *[f'\n{k.capitalize()}\n{v.key}\n{v.key_len}\n{v.predict}'for k,v in prediction.predictions.items()],
                   sep='\n')
        )


if __name__ == '__main__':
    executor.start_polling(dp)