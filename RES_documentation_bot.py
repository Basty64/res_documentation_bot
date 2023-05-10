import datetime
from config import token_bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import json
import requests
import time

bot = Bot(token = token_bot)
dp = Dispatcher(bot)

with open ("all_laws.json", "r", encoding="utf-8") as file:
    data = file.read()

d = json.loads(data)

@dp.message_handler(commands = "start")
async def start_command(message: types.Message):
    start_command = ["Все приказы", "Все постановления", "Остальные документы", "Проверить наличие новых документов"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(*start_command)
    await message.answer("Добрый день, я выпускной проект Андрея Бондаренко!", reply_markup = keyboard)

@dp.message_handler(Text(equals = "Все приказы"))
async def show_prikaz(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] == "Приказ":
            prikaz = f"{count}. {items['SignatoryAuthorityName']}\n\n"\
            f"{items['Name']}\n\n"\
            f"Ссылка для просмотра: http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}\n"\
            f"Ссылка на скачивание pdf: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf\n"\
            f"Первая страница в jpg: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1\n"
            count += 1
            print(prikaz)
            time.sleep(0.5) 
            await message.answer(prikaz)

@dp.message_handler(Text(equals = "Остальные документы"))
async def show_rasporyazhenie(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] != "Приказ" and items["DocumentTypeName"] != "Постановление":
            doc = f"{items['DocumentTypeName']}\n\n"\
            f"{count}. {items['SignatoryAuthorityName']}\n\n"\
            f"{items['Name']}\n\n"\
            f"Ссылка для просмотра: http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}\n"\
            f"Ссылка на скачивание pdf: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf\n"\
            f"Первая страница в jpg: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1\n"
            count += 1
            print(doc)
            await message.answer(doc)

@dp.message_handler(Text(equals = "Все постановления"))
async def show_postanovlenie(message: types.Message):
    count = 1
    for items in d["Documents"]:
        if items["DocumentTypeName"] == "Постановление":
            prikaz = f"{count}. {items['SignatoryAuthorityName']}\n\n"\
            f"{items['Name']}\n\n"\
            f"Ссылка для просмотра: http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}\n"\
            f"Ссылка на скачивание pdf: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf\n"\
            f"Первая страница в jpg: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']}&pngIndex=1\n"
            count += 1
            print(prikaz)
            time.sleep(0.2) 
            await message.answer(prikaz)

@dp.message_handler(Text(equals = "Проверить наличие новых документов"))
async def show_rasporyazhenie(message: types.Message):

    count = 1
    # with open ("test.json", encoding="utf-8") as file:
    #         data = file.read()
    # url = "http://publication.pravo.gov.ru/api/Document/Get?DocumentTypes=%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&RangeSize=200"

    # headers = {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    #         }

    # r = requests.get(url=url, headers=headers)
        
    # new_data = json.loads(r.text)

    # for items in new_data["Documents"]:

    #     document_id = items["Id"]

    #     if document_id in data:
    #             continue
    #     else:
    #             count = 1
    #             for items in new_data["Documents"]:
    #                     doc = f"{items['DocumentTypeName']}\n\n"\
    #                     f"{count}. {items['SignatoryAuthorityName']}\n\n"\
    #                     f"{items['Name']}\n\n"\
    #                     f"Ссылка для просмотра: http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}\n"\
    #                     f"Ссылка на скачивание pdf: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf\n"\
    #                     f"Первая страница в jpg: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']};pngIndex=1\n"
    #                     count += 1
    #                     print(doc)
    if count == 1:
                    str = "Новые документы отсутствуют"
    else:
                    str = "Найдены новые документы!"
    await message.answer(str)

@dp.message_handler(Text)
async def message_answer(message: types.Message):
    await bot.send_message(message.from_user.id, "Я могу показать немного документов \U0001F449\U0001F448")

if __name__ == "__main__":
    executor.start_polling(dp)