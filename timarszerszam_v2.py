from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen

import concurrent.futures
import csv

WEBSITE_LINK = 'https://timarszerszam.hu'
ITEM_NAME_CLASS = 'maintitle'
ITEM_PRODUCT_NUMBER = 'col-sm-9 col-xs-8 pb2_right product_no'
ITEM_PRICE = 'col-sm-9 col-xs-8 pb2_right price'
ITEM_DESCRIPTION = 'col-sm-9 col-xs-8 pb2_right lead'
ITEM_LONG_DESCRIPTION = 'product_tab act'
SIDE_MENU_ID = 'left_menu_collapse'


def get_website(_weblink):
    _response = urlopen(_weblink)
    if _response.code == 200:  # 200: OK
        _website_data = BeautifulSoup(_response.read().decode("UTF-8"), 'lxml')
        return _website_data


def get_every_family_link(_side_panel):
    _family_links = []
    for _fam_link in _side_panel.find_all('a'):
        _family_links.append(_fam_link.get('href'))
    print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every main category.')
    return _family_links


def get_last_category_depth(_family_link):
    _last_categories = []
    _categories = []
    _categories.append(_family_link)    
    while _categories:
        _website = get_website(_categories[0])
        if _website.find(class_ = 'category_categories') is not None:
            _website = get_website(_categories[0])
            for _category_box_in in _website.find_all(class_ = 'category_box_in'):
                _categories.append(WEBSITE_LINK + _category_box_in.a.get('href'))
        else:
            _last_categories.append(_categories[0])
        if _categories:
            _categories.pop(0)
    return _last_categories
        

def get_item_links(_category_link):
    _item_links = []
    _website = get_website(_category_link)
    if _website.find(class_ = 'product_list2') is not None:
        _items = _website.find(class_ = 'product_list2')
        for _item in _items.find_all(class_ = 'row product_box2'):
            _a_tag = _item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
            if hasattr(_a_tag, 'href'):
                _item_link = WEBSITE_LINK + _item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                _item_links.append(_item_link)
    # else:
        # le kell kezelni
    return _item_links


def replace_character(_string):
    _string = _string.replace('\xb2', 'SPECIALIS_KARAKTER').replace('\xd8', 'SPECIALIS_KARAKTER1').replace('\x84', 'SPECIALIS_KARAKTER2')
    _string = _string.replace('\xbc', 'SPECIALIS_KARAKTER3').replace('\x94', 'SPECIALIS_KARAKTER4').replace('\xbd', 'SPECIALIS_KARAKTER5')
    _string = _string.replace('\u25cf', 'SPECIALIS_KARAKTER6').replace('\u2009', 'SPECIALIS_KARAKTER7').replace('\xba', 'SPECIALIS_KARAKTER8')
    _string = _string.replace('\u2070', 'SPECIALIS_KARAKTER9').replace('\x81', 'SPECIALIS_KARAKTER10').replace('\xb9', 'SPECIALIS_KARAKTER11')
    _string = _string.replace('\u2300', 'SPECIALIS_KARAKTER12').replace('\x96', 'SPECIALIS_KARAKTER13').replace('\xb3', 'SPECIALIS_KARAKTER14')
    _string = _string.replace('\u2264', 'SPECIALIS_KARAKTER15').replace('\u2265', 'SPECIALIS_KARAKTER16').replace('\xf8', 'SPECIALIS_KARAKTER17')
    _string = _string.replace('\xf5', 'SPECIALIS_KARAKTER18').replace('\u2205', 'SPECIALIS_KARAKTER19').replace('\u2267', 'SPECIALIS_KARAKTER20')
    _string = _string.replace('\u200b', 'SPECIALIS_KARAKTER21').replace('\xfb', 'SPECIALIS_KARAKTER21').replace('\u2012', 'SPECIALIS_KARAKTER22')
    _string = _string.replace('\n', '').replace('\u2033', 'SPECIALIS_KARAKTER23').replace('\u2103', 'SPECIALIS_KARAKTER24')
    _string = _string.replace('\u03b1', 'SPECIALIS_KARAKTER25').replace('\u240d','SPECIALIS_KARAKTER26').replace('\u03bc','SPECIALIS_KARAKTER27')
    _string = _string.replace('\u0301','SPECIALIS_KARAKTER28').replace('\u0308','SPECIALIS_KARAKTER29').replace(';',',')
    _string = _string.replace('\u030b','SPECIALIS_KARAKTER30')
    return _string


def get_category( _website):
    _category = []
    if(_website.find(class_ = 'breadcrumb')):
        _category_element = _website.find(class_ = 'breadcrumb')
        for _a in _category_element.find_all('a'):
            _category.append(_a.text)
    _category.pop(0)
    return _category



def get_item_data(_item_link):
    _row = []
    _website = get_website(_item_link)
    if _item_link.endswith('/t'):
        get_category(_website)
        if _website.find(class_ = ITEM_NAME_CLASS):
            _row.append(replace_character(_website.find(class_ = ITEM_NAME_CLASS).text))
        else:
            _row.append('NINCS_NEV')

        if _website.find(class_ = ITEM_PRODUCT_NUMBER):
            _row.append(replace_character(_website.find(class_ = ITEM_PRODUCT_NUMBER).text))
        else:
            _row.append('NINCS_SOROZATSZAM')
                
        if _website.find(class_ = ITEM_DESCRIPTION):   
            _row.append(replace_character(_website.find(class_ =  ITEM_DESCRIPTION).text))
        else:
            _row.append('NINCS_LEIRAS')

        if _website.find(class_ = ITEM_PRICE):
            _row.append(replace_character(_website.find(class_ =  ITEM_PRICE).text))
        else:
            _row.append('NINCS_AR')
            
        if _website.find(class_ = ITEM_LONG_DESCRIPTION):
            _row.append(replace_character(_website.find(class_ = ITEM_LONG_DESCRIPTION).text))
        else:
            _row.append('')

        if _website.find(class_ = "stock outstock") or _website.find(class_ = "stock instock"):
            if _website.find(class_ = "stock outstock"):
                _row.append(_website.find(class_ = "stock outstock").text)

            if _website.find(class_ = "stock instock"):
                _row.append(_website.find(class_ = "stock instock").text)
        else:
            _row.append('Nincs_raktarinfo')
        _row.append('van_linkje')
            
        _row.append(_item_link)
            
    else:
        for _item in _website.find_all(class_ = 'row product_box2'):
            _row.append(replace_character(_website.find_all(class_ = 'row')[0].text))  # Megnevezés
            print (_website.find_all(class_ = 'row')[0].text)
            print(_item_link)
            _row.append(replace_character(_website.find_all(class_ = 'row')[1].text))  # Gyártói cikkszám
            _row.append(replace_character(_website.find_all(class_ = 'row')[3].text))  # Leírás
            _row.append(replace_character(_website.find_all(class_ = 'row')[4].text))  # Ár
                                          
            _row.append('')                                                            # Hosszú leírás

            if _website.find(class_ = 'pli_loc_item green') is not  None:
                _row.append('Raktáron')
            else:
                _row.append('Nincs raktáron')
            _row.append('nem_volt_linkje')
            _row.append(_item_link)
    _row.append(get_category(_website))    
    return _row


print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Start.')

website = get_website(WEBSITE_LINK)
side_panel = website.find(id = SIDE_MENU_ID)

family_links = get_every_family_link(side_panel)

family_links.pop()  # We don't care about the last family

last_category_depth_links = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_last_category_depth, family_links)
    for result in results:
        last_category_depth_links.append(result)
        
i = 0
for row in last_category_depth_links:
    for category in row:
        i += 1
print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every last category depth.', i)


item_links = []
for row in last_category_depth_links:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_item_links, row)
        for result in results:
            item_links.append(result)

i = 0
for row in item_links:
    for item in row:
        i += 1
print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every item link.', i)

item_links2 = []
for row in item_links:
    for item in row:
        item_links2.append(item)

item_data = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_item_data, item_links2)
    for result in results:
        item_data.append(result)

print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Got every item data.', i)

with open('timarszerszam.csv', 'w', newline = '') as csv_file:
    write = csv.writer(csv_file, delimiter=';')
    for item in item_data:
        write.writerow(item)

print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Done.')
