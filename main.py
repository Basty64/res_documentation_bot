import json
import requests
from datetime import datetime


url = "http://publication.pravo.gov.ru/api/Document/Get?DocumentTypes=%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&RangeSize=200"

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/53736"
}

def check_today():
    
    date = datetime.now()
    today_date = datetime.strftime(date, "%d.%m.%Y")
    

    url = f"http://publication.pravo.gov.ru/api/Document/Get?PubDateType=single&PubDateSingle={today_date}&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85"
    
    r = requests.get(url=url, headers = headers)

    today_laws = json.loads(r.text)
    return today_laws
                

def check_date(date):
    
    url = f"http://publication.pravo.gov.ru/api/Document/Get?PubDateType=single&PubDateSingle={date}&DocumentName=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85"
    
    r = requests.get(url=url, headers = headers)

    date_laws = json.loads(r.text)
    print(date_laws)
    return date_laws

def check_laws():
     r = requests.get(url=url, headers=headers)
     all_lawssss = {}
     all_lawssss = json.loads(r.text)

     with open("laws_dict.json", "w", encoding = "utf-8") as file:
        json.dump(all_lawssss, file, indent=4, ensure_ascii=False)
    
     print("Функция успешно завершила работу")


                              
def main():
    check_today()
    check_date()
    # check_laws()   <--- Применялась только в первый раз для создания нового файла


with open ("all_laws.json", "r", encoding="utf-8") as file:
    data = file.read()
    d = json.loads(data)


if __name__ == "__main__":
    main()