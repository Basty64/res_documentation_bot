import json
import requests
from bs4 import BeautifulSoup as bs4

# url = "http://www.gov.ru/main/regions/regioni-44.html"

# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
#     }

# r = requests.get(url=url, headers=headers)

# r.encoding = "windows-1251"
# with open("all_sites.html", "w", encoding="windows 1251") as file:
#     file.write(r.text)


with open ("ttt.html", encoding = "utf-8") as file:
    data = file.read()

soup = bs4(data, "lxml")

for soups in soup.find_all("b"):
    soups.name = "a"
    soups["name"] = soups.text
    soups.clear()

regions = soup.find_all("a")

regions_sites = {}



# for region in regions:
#     region_name = region.get("name")
#     region_link = region.get("href")
#     region_site_name = region.text
#     if type(region_name) == str:
#         print(region_name,"\n")
#         good_name = region_name
    # else:
    #     print(f"Название сайта - {region_site_name} || Ссылка - {region_link} \n")
    

    # regions_sites[good_name] = {
    #     region_site_name: region_link
    # }

# with open("testing.json", "w", encoding="utf-8") as file:
#     json.dump(regions_sites, file, indent = 4, ensure_ascii = False)