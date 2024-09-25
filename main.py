import json
import requests
from datetime import datetime

url = "http://publication.pravo.gov.ru/api/Documents?pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=0&SortDestination=1"

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/53736"
}

def check_today():
    
    date = datetime.now()
    today_date = datetime.strftime(date, "%d.%m.%Y")

    url = f"http://publication.pravo.gov.ru/api/Documents?=200&index=1&PublishDateFrom={today_date}&NumberSearchType=0&Name=возобновляемых&SortedBy=0&SortDestination=1"
    
    r = requests.get(url=url, headers = headers)

    today_laws = json.loads(r.text)
    return today_laws            

def check_date(date):
    
    url = f"http://publication.pravo.gov.ru/api/Documents?=200&index=1&PublishDateFrom={date}&PublishDateTo={date}&NumberSearchType=0&Name=возобновляемых&SortedBy=0&SortDestination=1"
    
    r = requests.get(url=url, headers = headers)

    date_laws = json.loads(r.text)
    print(date_laws)
    return date_laws

def check_this_week():

    url = f"http://publication.pravo.gov.ru/api/Documents?pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=0&SortDestination=1&PeriodType=weekly"

    r = requests.get(url=url, headers = headers)

    this_week_laws = json.loads(r.text)
    print(this_week_laws)
    return this_week_laws

def check_this_month():

    url = f"http://publication.pravo.gov.ru/api/Documents?pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=0&SortDestination=1&PeriodType=monthly"

    r = requests.get(url=url, headers = headers)

    this_month_laws = json.loads(r.text)
    print(this_month_laws)
    return this_month_laws

def check_region(i):
    
    with open ("regions_info.json", "r", encoding="utf-8") as file:
        regions = file.read()
    names = json.loads(regions)
    item = names[int(i)-1]
    region = item["code"]

    url = f"http://publication.pravo.gov.ru/api/Documents?pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=0&SortDestination=1&block={region}"

    r = requests.get(url=url, headers = headers)

    region_laws = json.loads(r.text)
    return region_laws

def check_laws():
     r = requests.get(url=url, headers=headers)
     all_lawssss = {}
     all_lawssss = json.loads(r.text)

     with open("laws_dict.json", "w", encoding = "utf-8") as file:
        json.dump(all_lawssss, file, indent=4, ensure_ascii=False)
    
     print("Функция успешно завершила работу")

def check_prikaz():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?pageSize=200&&pageSize=200&index=1&DocumentTypes=2dddb344-d3e2-4785-a899-7aa12bd47b6f&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=6&SortDestination=1"

    r = requests.get(url=url, headers = headers)

    prikaz_laws = json.loads(r.text)
    print(prikaz_laws)
    return prikaz_laws

def check_post():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&DocumentTypes=fd5a8766-f6fd-4ac2-8fd9-66f414d314ac&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=6&SortDestination=1"

    r = requests.get(url=url, headers = headers)

    post_laws = json.loads(r.text)
    print(post_laws)
    return post_laws

def check_ost():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&DocumentTypes=82a8bf1c-3bc7-47ed-827f-7affd43a7f27&DocumentTypes=0790e34b-784b-4372-884e-3282622a24bd&DocumentTypes=49a1ee72-097d-44e6-985d-f0cb7b036150&DocumentTypes=7ff5b3b5-3757-44f1-bb76-3766cabe3593&DocumentTypes=7732b2a0-c522-436f-8172-a251912e2fc9&DocumentTypes=7ccde0f1-39b0-49b9-9a61-2fee55402189&DocumentTypes=63c6ff4f-ed74-45b3-86e2-8a76b75d674d&DocumentTypes=e39a5fe7-2e9f-4023-a7af-f17b5f2dec56&DocumentTypes=4d76ef2a-6181-4e1c-bbd9-23ff836f8aca&DocumentTypes=d84850fc-c3f6-4595-a55c-bc8bcae02328&DocumentTypes=c0281bbe-6be1-45be-8acd-f319c99b85ad&DocumentTypes=8910e61f-371d-490c-a1b8-aa7b8a5a48be&DocumentTypes=49322bdb-8137-4b5f-bc94-792e88992fab&DocumentTypes=b1f44e8e-7699-4fe5-a9d1-7f6f62c7b89c&DocumentTypes=28b0f778-037b-456d-b510-2029cd6ed4ca&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=6&SortDestination=1"

    r = requests.get(url=url, headers = headers)

    ost_laws = json.loads(r.text)
    print(ost_laws)
    return ost_laws

def check_gov():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&SignatoryAuthorityId=8005d8c9-4b6d-48d3-861a-2a37e69fccb3&NumberSearchType=0&Name=возобновляемых&SortedBy=6&SortDestination=1"

    r = requests.get(url=url, headers = headers)

    gov_laws = json.loads(r.text)
    print(gov_laws)
    return gov_laws

def check_fed():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=6&SortDestination=1&block=federal_authorities"

    r = requests.get(url=url, headers = headers)

    fed_laws = json.loads(r.text)
    print(fed_laws)
    return fed_laws

def check_president():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&SignatoryAuthorityId=225698f1-cfbc-4e42-9caa-32f9f7403211&NumberSearchType=0&Name=возобновляемых&SortedBy=6&SortDestination=1"

    r = requests.get(url=url, headers = headers)

    president_laws = json.loads(r.text)
    print(president_laws)
    return president_laws

def check_mdrf():
        
    url = f"http://publication.pravo.gov.ru/api/Documents?&&pageSize=200&index=1&NumberSearchType=0&Name=%D0%B2%D0%BE%D0%B7%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D1%85&SortedBy=6&SortDestination=1&block=international"

    r = requests.get(url=url, headers = headers)

    mdrf_laws = json.loads(r.text)
    print(mdrf_laws)
    return mdrf_laws

def main():
    check_today()
    check_date()
    check_region()
    check_prikaz()
    check_post()
    check_ost()
    check_president()
    check_gov()
    check_mdrf()
    check_fed()
    # check_laws()   <--- Применялась только в первый раз для создания нового файла


with open ("laws_dict.json", "r", encoding="utf-8") as file:
    data = file.read()
    d = json.loads(data)


if __name__ == "__main__":
    main()