import streamlit as st
from bs4 import BeautifulSoup
import requests
import os
import json
import urllib.request
import time
# from streamlit_extras.switch_page_button import switch_page

st.title("Welcome to Disparse")
st.subheader("A Web Crawler for Posters found on displate.com")
link = st.text_input(label="Enter the Displate URL",placeholder="https://displate.com/displate/2897177")
my_bar = st.progress(0)
if link:
    my_bar.progress(20)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    scripts = soup.findAll("script", type="application/ld+json")
    script = scripts[1]
    script_string = str(script)
    st.info("Extracting link to image")
    my_bar.progress(50)
    img_url_start_index = script_string.find("image") + 9
    script_string = script_string[img_url_start_index:]
    img_url = script_string[:script_string.find('"')]
    st.info("Getting page")
    # with st.spinner("Getting page"):
    #     time.sleep(5)
    st.success('Done!')
    wall=st.image(img_url, width=250)
    my_bar.progress(100)
    if page.status_code != 200:
        st.error('Connection error', icon="🚨")
        quit()

with st.container():
        
    st.download_button(
        label="Download this image",
        data=img_url,
        file_name=f"{img_url}.jpg"
    )


    reverse = st.button(
        label="Reverse search this Image"
    )

if reverse:
    # with st.spinner("Searching Yandex Images"):
    #     time.sleep(5)
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
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    # st.write(response)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    st.write(img_search_url)