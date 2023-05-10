import requests 
import json

url = "http://publication.pravo.gov.ru/api/Document/Get?DocumentTypes=%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&RangeSize=200"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

r = requests.get(url=url, headers=headers)

data = json.loads(r.text)

with open("test.json", "w", encoding="utf-8") as file:
    file.write(r.text)

def check_news_update():
        with open ("test.json", encoding="utf-8") as file:
            data = file.read()

        url = "http://publication.pravo.gov.ru/api/Document/Get?DocumentTypes=%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&RangeSize=200"

        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            }

        r = requests.get(url=url, headers=headers)
        
        new_data = json.loads(r.text)

        for items in new_data["Documents"]:

            document_id = items["Id"]

            if document_id in data:
                continue
            else:
                count = 1
                for items in new_data["Documents"]:
                        doc = f"{items['DocumentTypeName']}\n\n"\
                        f"{count}. {items['SignatoryAuthorityName']}\n\n"\
                        f"{items['Name']}\n\n"\
                        f"Ссылка для просмотра: http://publication.pravo.gov.ru/Document/View/{items['EoNumber']}\n"\
                        f"Ссылка на скачивание pdf: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf\n"\
                        f"Первая страница в jpg: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']};pngIndex=1\n"
                        count += 1
                        print(doc)

def get_all_prikaz():
    count = 1
    for items in data["Documents"]:
        if items["DocumentTypeName"] == "Приказ":
            print(f"{count}. {items['Name']}")
            print(f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf")
            print(f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']};pngIndex=1","\n")
            count += 1

def get_all_rasporyazhenie():
    count = 1
    for items in data["Documents"]:
        if items["DocumentTypeName"] == "Распоряжение":
            print(f"{count}. {items['Name']}")
            print(f"Ссылка для скачивания документа: http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf")
            print(f"Картинка с первой страницей документа: http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']};pngIndex=1","\n")
            count += 1

def get_all_postanovlenie():
    count = 1
    for items in data["Documents"]:
        if items["DocumentTypeName"] == "Постановление":
            print(f"{count}. {items['Name']}")
            print(f"http://publication.pravo.gov.ru/File/GetFile/{items['EoNumber']}?type=pdf")
            print(f"http://publication.pravo.gov.ru/File/GetImage?DocumentId={items['Id']};pngIndex=1","\n")
            count += 1

# def main():
#     check_news_update()

# if __name__ == '__main__':
#     main()

# SignDateSingle – точная дата подписания НПА в формате ДД.ММ.ГГГГ