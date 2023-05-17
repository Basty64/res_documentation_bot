from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink
import time
import logging
import asyncio
from config import token_bot
from main import d, check_today, check_date
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

    start_command = ["Все приказы", "Все постановления", "Остальные документы", "Поиск по дате", "Список регионов", "Проверить наличие новых документов"]
    keyboard = types.ReplyKeyboardMarkup(
         resize_keyboard = True, 
         input_field_placeholder = "Выберите нужную функцию"
         )
    keyboard.add(*start_command)
    await message.reply("Добрый день, я выпускной проект Андрея Бондаренко!", reply_markup = keyboard)

@dp.message_handler(commands =  "help")
async def process_help_command(message: types.Message):
    await message.reply("<b>Краткая инструкция:</b>\n\n -Первые три кнопки можно использовать только один раз, они выдают все доступные документы;\n\n -Для поиска по регионам достаточно написать начало требуемого региона или скопировать название из списка (функция в разработке);\n\n -Проверка производится каждый день в 9 утра.", parse_mode="HTML")

@dp.message_handler(commands =  "archive")
async def process_help_command(message: types.Message):
    await message.reply("Архивные документы об уже прошедших конкурсах можно найти в папке:\n (путь будет добавлен позже)")

@dp.message_handler(Text(equals = "Все приказы"))
async def show_prikaz(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] == "Приказ":

            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}"
            linked = hlink(items['DocumentTypeName'], link1)

            link2 = f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf"
            link3 = f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1"

            
            prikaz = f"{count}. {linked} от {items['DocumentDate']}\n\n"\
            f"<b>{items['SignatoryAuthorityName']}.</b>\n\n"\
            f"{items['Name']}. \n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\

            count += 1
            time.sleep(0.3) 
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)

@dp.message_handler(Text(equals = "Все постановления"))
async def show_postanovlenie(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] == "Постановление":
            
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}"
            linked = hlink(items['DocumentTypeName'], link1)

            link2 = f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf"
            link3 = f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1"

            
            prikaz = f"{count}. {linked} от {items['DocumentDate']}\n\n"\
            f"<b>{items['SignatoryAuthorityName']}.</b>\n\n"\
            f"{items['Name']}. \n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"\

            count += 1
            time.sleep(0.3) 
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)



@dp.message_handler(Text(equals = "Остальные документы"))
async def show_rasporyazhenie(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] != "Приказ" and items["DocumentTypeName"] != "Постановление":
            
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}"
            linked = hlink(items['DocumentTypeName'], link1)

            link2 = f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf"
            link3 = f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1"

            prikaz = f"{count}. {linked} от {items['DocumentDate']}\n\n"\
            f"<b>{items['SignatoryAuthorityName']}.</b>\n\n"\
            f"{items['Name']}. \n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"

            count += 1
            time.sleep(0.3) 
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)


@dp.message_handler(Text(equals = "Проверить наличие новых документов"))
async def show_rasporyazhenie(message: types.Message):

    today_laws = check_today()
    count = 1
    await message.answer("Проверяю...")
    if today_laws['TotalDocumentsCount'] == 0:

        await message.answer("Сегодня новых документов не обнаружено")
    
    else:

        await message.answer("Обнаружены новые документы!")

        for items in today_laws["Documents"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}"
            linked = hlink(items['DocumentTypeName'], link1)

            link2 = f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf"
            link3 = f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1"

            prikaz = f"{count}. {linked} от {items['DocumentDate']}\n\n"\
            f"<b>{items['SignatoryAuthorityName']}.</b>\n\n"\
            f"{items['Name']}. \n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)



@dp.message_handler(Text(equals = "Список регионов"))
async def show_pregionlist(message: types.Message):
    with open("regions.txt", "r", encoding="utf-8") as file:
        data = file.read()
    data = data.split("\n")
    data.sort()
    ultradata = '\n'.join(data)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = "Поиск по региону", callback_data = "Поиск по региону"))
    await message.reply(f"<b>Список регионов по алфавиту</b>\n\n{ultradata}", parse_mode="HTML", reply_markup = keyboard)


@dp.callback_query_handler(text = "Поиск по региону")
async def region_documents_finder(call: types.CallbackQuery):
    await Form.region.set()
    await call.message.answer("Введите название региона", parse_mode="HTML")
    await call.answer()


@dp.message_handler(Text(equals = "Поиск по дате"))
async def region_documents_finder(message: types.message):

    # Set state
    await Form.date.set()
    await message.reply("Введите дату в формате дд.мм.гг (Пример - 06.04.2023)")
    await Form.date.set()

def import_date(state=Form.date):
    personal_date = Form.date
    return personal_date


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


@dp.message_handler(state=Form.region)
async def process_name(message: types.Message, state: FSMContext):

    # list()
    # for items in d["Documents"]:
    #     if message.text in items["SignatoryAuthorityName"]:
    #      list.append(items)    

    await state.finish()
    await message.reply("Функция в разработке, поиск по региону будет добавлен позже" )  
    # await message.reply(list)

@dp.message_handler(state=Form.date)
async def process_name(message: types.Message, state: FSMContext):

    # list()
    # for items in d["Documents"]:
    #     if message.text in items["SignatoryAuthorityName"]:
    #      list.append(items)   

    
    
    await message.reply(f"Вы ввели дату {message.text}") 
    await state.finish()

    date_laws = check_date(message.text)
    count = 1
    if date_laws['TotalDocumentsCount'] == 0:

        await message.answer("По данной дате документов не обнаружено")
    
    else:

        await message.answer("Обнаружены документы, загружаю...")

        time.sleep(2) 

        for items in date_laws["Documents"]:
            link1 = f"http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}"
            linked = hlink(items['DocumentTypeName'], link1)

            link2 = f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf"
            link3 = f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1"

            prikaz = f"{count}. {linked} от {items['DocumentDate']}\n\n"\
            f"<b>{items['SignatoryAuthorityName']}.</b>\n\n"\
            f"{items['Name']}. \n\n"\
            f"{hlink('Ссылка для скачивания документа в pdf', link2)}\n"
            count += 1
            await message.answer(prikaz, parse_mode="HTML", disable_web_page_preview=True)

@dp.message_handler(Text)
async def message_answer(message: types.Message):
    await bot.send_message(message.from_user.id, "Я могу показать немного документов \U0001F449\U0001F448")

if __name__ == '__main__':

    # loop = asyncio.get_event_loop()
    # loop.create_task(news_every_minute())

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())