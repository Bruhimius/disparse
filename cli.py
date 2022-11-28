from bs4 import BeautifulSoup
import requests
import os
import json

url = ""
print("ENTER YOUR URL FROM displate.com")
url = str(input(""))

page = requests.get(url)

if page.status_code != 200:
    print("Connection error")
    quit()

print("Getting page")

soup = BeautifulSoup(page.text, "html.parser")

scripts = soup.findAll("script", type="application/ld+json")

script = scripts[1]
# print(script)
script_string = str(script)

print("Extracting link to img")

img_url_start_index = script_string.find("image") + 9
# print(img_url_start_index)
script_string = script_string[img_url_start_index:]

img_url = script_string[:script_string.find('"')]

print("IMG URL:")

print(img_url)

print("Saving")

p = requests.get(img_url)

index = img_url.rindex("/")

save_name = img_url[index:]

print("Save as "+save_name)

if not os.path.isdir("out_imgs"):
     os.mkdir("out_imgs")


out = open("out_imgs"+save_name, "wb")

out.write(p.content)

out.close()

file_path = f"out_imgs\\{save_name}"
search_url = 'https://yandex.ru/images/search'
files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
response = requests.post(search_url, params=params, files=files)
print(response)
query_string = json.loads(response.content)['blocks'][0]['params']['url']
img_search_url = search_url + '?' + query_string
print(img_search_url)