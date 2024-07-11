from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink
import time
import logging
import asyncio
from config import token_bot
from main import d, check_today, check_date, check_region, check_prikaz, check_post, check_ost, check_president, check_gov, check_mdrf,check_fed
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



bot = Bot(token = token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class Form(StatesGroup):
    region = State()
    date = State()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message_handler(commands = "start")
async def start_command(message: types.Message):

    start_keyboard = ["Список регионов", "Проверка", "Поиск", "Все документы", "Новости", "Федеральные округа"]
    keyboard = types.ReplyKeyboardMarkup(
         resize_keyboard = True, 
         input_field_placeholder = "Выберите нужную функцию"
         )
    keyboard.add(*start_keyboard)
    await message.reply("Добрый день, я выпускной проект Андрея Бондаренко!\n\nПеред началом работы ознакомьтесь с краткой инструкцией по команде /help", reply_markup = keyboard)




@dp.message_handler(Text(equals = "Новости"))
async def show_prikaz(message: types.Message):
    await message.answer("Функция в разработке...")

@dp.message_handler(Text(equals = "Федеральные округа"))
async def show_prikaz(message: types.Message):
    await message.answer("Функция в разработке...")



@dp.message_handler(Text(equals = "Назад"))
async def back_command(message: types.Message):

    start_keyboard = ["Список регионов", "Проверка", "Поиск", "Все документы", "Новости", "Федеральные округа"]
    keyboard = types.ReplyKeyboardMarkup(
         resize_keyboard = True, 
         input_field_placeholder = "Выберите нужную функцию"
         )
    keyboard.add(*start_keyboard)
    await message.answer("Выберите нужную функцию",reply_markup = keyboard)



@dp.message_handler(commands =  "help")
async def process_help_command(message: types.Message):
    await message.reply("<b>Краткая инструкция:</b>\n\n -С помощью этого бота можно получить и изучить всю законодательную базу по возобновляемым источникам энергии в РФ;\n\n -Для поиска по дате достаточно нажать соответствующую кнопку и ввести дату в предложенном формате;\n\n -Для отмены поиска введите команду \n/cancel;\n\n -По кнопке 'Проверка' производится отслеживание документов на сегодняшнюю дату.\n Автоматическая проверку проводится каждый день в 9 утра\n\n -Бот находится на этапе тестирования, поэтому некоторые функции могут работать не так, как надо.", parse_mode="HTML")

@dp.message_handler(commands =  "archive")
async def process_help_command(message: types.Message):
    await message.reply("Архивные документы об уже прошедших конкурсах можно найти в папке:\n (путь будет добавлен позже)")



@dp.message_handler(Text(equals = "Поиск"))
async def show_prikaz(message: types.Message):

    start_keyboard = ["Поиск по дате", "Поиск по региону", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard = True, 
            input_field_placeholder = "Выберите нужную функцию"
            )
    keyboard.add(*start_keyboard)
    await message.reply("Выберите нужный тип поиска", reply_markup = keyboard)




@dp.message_handler(Text(equals = "Все документы"))
async def show_rasporyazhenie(message: types.Message):

    start_keyboard = ["По типу документа", "Принявший орган", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard = True, 
            input_field_placeholder = "Выберите нужную функцию"
            )
    keyboard.add(*start_keyboard)
    await message.reply("Доступные типы документов:\n\n -Постановления(72 документа);\n -Приказы(41 документ);\n -Остальное(14 документов).\n\n Принявшие органы:\n\n -Правительство РФ(20 документов);\n -Федеральные органы исполнительной власти(11 документов);\n -Президент(1 документ;\n -Международные Договоры Российской Федерации(1 документ).", reply_markup = keyboard)




@dp.message_handler(Text(equals = "По типу документа"))
async def show_types(message: types.Message):
    start_keyboard = ["Приказы", "Постановления", "Остальное","Назад"]
    keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard = True, 
            input_field_placeholder = "Выберите нужную функцию"
            )
    keyboard.add(*start_keyboard)
    await message.reply("Выберите нужный тип, после этого бот выдаст несколько десятков сообщений.", reply_markup = keyboard)




@dp.message_handler(Text(equals = "Приказы"))
async def show_prikaz(message: types.Message):

    prikaz = check_prikaz()
    count = 1
    for items in prikaz["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
    # await message.answer("Назад")




@dp.message_handler(Text(equals = "Постановления"))
async def show_prikaz(message: types.Message):

    post = check_post()
    count = 1
    for items in post["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(post, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)



@dp.message_handler(Text(equals = "Остальное"))
async def show_prikaz(message: types.Message):

    ost = check_ost()
    count = 1
    for items in ost["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            ost = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(ost, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
            time.sleep(0.1)

@dp.message_handler(Text(equals = "Принявший орган"))
async def show_types(message: types.Message):
    start_keyboard = ["ФОИВ", "МДРФ", "Президент","Правительство РФ","Назад"]
    keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard = True, 
            input_field_placeholder = "Выберите нужную функцию"
            )
    keyboard.add(*start_keyboard)
    await message.reply("Выберите нужный тип, после этого бот выдаст несколько десятков сообщений.", reply_markup = keyboard)


@dp.message_handler(Text(equals = "Правительство РФ"))
async def show_gov(message: types.Message):

    gov = check_gov()
    count = 1
    for items in gov["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            gov = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(gov, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
            time.sleep(0.1)


@dp.message_handler(Text(equals = "ФОИВ"))
async def show_fed(message: types.Message):

    fed = check_fed()
    count = 1
    for items in fed["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            fed = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(fed, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
            time.sleep(0.1)


@dp.message_handler(Text(equals = "Президент"))
async def show_president(message: types.Message):

    president = check_president()
    count = 1
    for items in president["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            president = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(president, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
            time.sleep(0.1)


@dp.message_handler(Text(equals = "МДРФ"))
async def show_mdrf(message: types.Message):

    mdrf = check_mdrf()
    count = 1
    for items in mdrf["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            mdrf = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(mdrf, parse_mode="HTML", disable_web_page_preview=True, disable_notification=True)
            time.sleep(0.1)


# Функция проверки новых документов по сегодняшней дате.
@dp.message_handler(Text(equals = "Проверка"))
async def new_documents(message: types.Message):

    today_laws = check_today()
    count = 1
    await message.answer("Проверяю...")
    count = 1

    time.sleep(1.5)

    if today_laws['itemsTotalCount'] == 0:

        await message.answer("Сегодня новых документов не обнаружено")
    
    elif today_laws['itemsTotalCount'] == 1:

        await message.answer("Обнаружен новый документ!")
    
        for items in today_laws["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)

    else:

        await message.answer("Обнаружены новые документы!")

        for items in today_laws["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)
#  Конец функции


@dp.message_handler(Text(equals = "Список регионов"))
async def show_pregionlist(message: types.Message):
    with open("regions.txt", "r", encoding="utf-8") as file:
        data = file.read()
    data = data.split("\n")

    ultradata = '\n'.join(data)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = "Поиск по региону", callback_data = "Поиск по региону"))
    await message.answer(f"<b>Список регионов по алфавиту</b>\n\n{ultradata}\n Всего: 94 документа", parse_mode="HTML", reply_markup = keyboard)



@dp.callback_query_handler(text = "Поиск по региону")
async def region_documents_finder(call: types.CallbackQuery):
    await Form.region.set()
    await call.message.answer("Введите номер региона", parse_mode="HTML")
    await call.answer()

@dp.message_handler(state=Form.region)
async def process_name(message: types.Message, state: FSMContext):

    info_region = check_region(message.text)
    await state.finish()

    if info_region['itemsTotalCount'] == 0:
       
        await message.reply("Документов по данному региону не обнаружено")

    else:

        await message.reply("Обнаружены документы, загружаю...")

        time.sleep(2) 
        count = 1
        for items in info_region["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)


@dp.message_handler(Text(equals ="Поиск по региону"))
async def region_documents_finder(message: types.message):


    with open("regions.txt", "r", encoding="utf-8") as file:
        data = file.read()
    data = data.split("\n")

    ultradata = '\n'.join(data)
    await message.answer(f"<b>Список регионов по алфавиту</b>\n\n{ultradata}", parse_mode="HTML")

    time.sleep(0.1)
    await Form.region.set()
    await message.answer("Введите номер региона", parse_mode="HTML")
    await Form.region.set()

@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Поиск отменён.')

@dp.message_handler(state=Form.region)
async def process_name(message: types.Message, state: FSMContext):

    info_region = check_region(message.text)
    await state.finish()

    if info_region['itemsTotalCount'] == 0:
       
        await message.reply("Документов по данному региону не обнаружено")

    else:

        await message.reply("Обнаружены документы, загружаю...")

        time.sleep(2) 
        count = 1
        for items in info_region["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            prikaz = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)



@dp.message_handler(Text(equals = "Поиск по дате"))
async def region_documents_finder(message: types.message):

    # Set state
    await Form.date.set()
    await message.reply("Введите дату в формате дд.мм.гг (Пример - 06.04.2023)")
    await Form.date.set()


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
    await message.reply('Поиск отменён.')


@dp.message_handler(state=Form.date)
async def process_name(message: types.Message, state: FSMContext):

    await message.reply(f"Вы ввели {message.text}") 
    await state.finish()
    date_laws = check_date(message.text)
    count = 1
    if date_laws['itemsTotalCount'] == 0:

        await message.answer("По данной дате документов не обнаружено")
        
    elif date_laws['itemsTotalCount'] > 29:

        await message.answer("Дата введена неправильно, повторите попытку")

    else:

        await message.answer("Обнаружены документы, загружаю...")

        time.sleep(2) 

        for items in date_laws["items"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
            linked = hlink(items['complexName'], link1)

            link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
            link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

            document = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
            f"{hlink('Ссылка для скачивания первой страницы', link3)}"
            count += 1
            await message.answer(document, parse_mode="HTML", disable_web_page_preview=True)


# async def laws_every_day():
#     while True:
#         today_laws = check_today()
#         count = 1

#         if today_laws['itemsTotalCount'] == 0:
            
#             await bot.send_message(user_id, "[Ежедневное оповещение]", disable_notification=True)
#             await bot.send_message(user_id, "Сегодня новых документов не обнаружено", disable_notification=True)
    
#         else:

#             await bot.send_message(user_id, "Обнаружены новые документы!", disable_notification=True)

#             for items in today_laws["items"]:
#                 link1 = f"http://publication.pravo.gov.ru/Document/View/{items['eoNumber']}"
#                 linked = hlink(items['complexName'], link1)

#                 link2 = f"http://publication.pravo.gov.ru/file/pdf?eoNumber={items['eoNumber']}"
#                 link3 = f"http://publication.pravo.gov.ru/GetImage?documentId={items['id']}&pageNumber=1"

#                 document = f"{count}. {linked} \n\n Опубликован {items['viewDate']}\n\n"\
#                 f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\
#                 f"{hlink('Ссылка для скачивания первой страницы', link3)}"
#                 count += 1
#                 await bot.send_message(document, parse_mode="HTML", disable_web_page_preview=True)

#         await asyncio.sleep(1)
        

@dp.message_handler(Text)
async def message_answer(message: types.Message):
    await bot.send_message(message.from_user.id, "Я могу показать немного документов \U0001F449\U0001F448")

if __name__ == '__main__':

    # loop = asyncio.get_event_loop()
    # loop.create_task(laws_every_day())
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

