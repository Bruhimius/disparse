import streamlit as st
from bs4 import BeautifulSoup
import requests
import os
import json
import urllib.request
def yandex():
    p = requests.get(img_url)
    index = img_url.rindex("/")
    save_name = img_url[index:]
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
    st.write(response)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    urllib.request.urlopen(img_search_url)
    return img_search_url
def ups():
    y=yandex()
    img_search_url=y.img_search_url
    r = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        data={
            'image': img_search_url,
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )
    print(r.json())


st.title("Welcome to Disparse")
st.subheader("A Web Crawler for Posters found on displate.com")
link = st.text_input(label="Enter the Displate URL",)
page = requests.get(link)

if page.status_code != 200:
    st.error('Connection error', icon="🚨")
    quit()

st.write("Getting page")

soup = BeautifulSoup(page.text, "html.parser")

scripts = soup.findAll("script", type="application/ld+json")

script = scripts[1]
# print(script)
script_string = str(script)

st.write("Extracting link to img")

img_url_start_index = script_string.find("image") + 9
# print(img_url_start_index)
script_string = script_string[img_url_start_index:]

img_url = script_string[:script_string.find('"')]

st.write("IMG URL:")
# st.write("img_url")
st.image(img_url,use_column_width=.25)
st.download_button(
    label="Download this image",
    data=img_url,
    file_name=f"{img_url}.jpg"
    )
st.button(
    label="Reverse search this Image",
    on_click=yandex()
    )
st.button(
    label="Upscale this image",
    on_click=ups()
)

