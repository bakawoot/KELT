from bs4 import BeautifulSoup
from datetime import datetime

import concurrent.futures
import requests
import re
import csv

WEBSITE_LINK = 'https://timarszerszam.hu'
ITEM_NAME_CLASS = 'maintitle'
ITEM_PRODUCT_NUMBER = 'col-sm-9 col-xs-8 pb2_right product_no'
ITEM_PRICE = 'col-sm-9 col-xs-8 pb2_right price'
ITEM_DESCRIPTION = 'col-sm-9 col-xs-8 pb2_right lead'
ITEM_LONG_DESCRIPTION = 'product_tab act'
SIDE_MENU_ID = 'left_menu_collapse'

def get_website(_weblink):
    _html_text = requests.get(_weblink).text
    _website = BeautifulSoup(_html_text, 'lxml')
    
    return _website


def get_every_family_link(_side_panel):
    _family_links = []
    for _fam_link in _side_panel.find_all('a'):
        _family_links.append(_fam_link.get('href'))
    print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every main category.')
    return _family_links


def get_every_category_link(_family_link, _WEBSITE_LINK):
    _categories = []
    _categories.append(_family_link)
    _website = get_website(_categories[0])
    _last_categories = []
    
    while _categories:
        #print(_categories)
        if _website.find(class_ = 'category_categories') is not None:
            _website = get_website(_categories[0])
            for _category_box_in in _website.find_all(class_ = 'category_box_in'):
                _categories.append(WEBSITE_LINK + _category_box_in.a.get('href'))
        else:
            _last_categories.append(_categories[0])
        if _categories:
            del _categories[0]
    return _last_categories
        
def find_last_category_depth(_category_links):
    print(_category_links)
    _last_category = []
    for _category in _category_links:
        _website = get_website(_category)
        if _website.find(class_ = 'category_categories') is None:
            return _category


def get_item_links(_category_link, _WEBSITE_LINK):
    print(_category_link)
    _item_links = []
    _no_item_link_category = []
    _website = get_website(_category_link)
    if _website.find(class_ = 'product_list2') is not None:
        _items = _website.find(class_ = 'product_list2')
        for _item in _items.find_all(class_ = 'row product_box2'):
            _a_tag = _item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
            if hasattr(_a_tag, 'href'):
                _item_link = _WEBSITE_LINK + _item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                _item_links.append(_item_link)
    else:
        _item_links.append(_category)
    
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


def get_item_data (_item_link, _website, _item_name_class, _item_product_number, _item_price, _item_description, _item_long_description):
    _row = []
    if _item_link.endswith('/t'):
        if _website.find(class_ = _item_name_class):
            _row.append(replace_character(_website.find(class_ = _item_name_class).text))
        else:
            _row.append('NINCS_NEV')

        if _website.find(class_ = _item_product_number):
            _row.append(replace_character(_website.find(class_ = _item_product_number).text))
        else:
            _row.append('NINCS_SOROZATSZAM')
                
        if _website.find(class_ = _item_description):   
            _row.append(replace_character(_website.find(class_ =  _item_description).text))
        else:
            _row.append('NINCS_LEIRAS')

        if _website.find(class_ = _item_price):
            _row.append(replace_character(_website.find(class_ =  _item_price).text))
        else:
            _row.append('NINCS_AR')
            
        if _website.find(class_ = _item_long_description):
            _row.append(replace_character(_website.find(class_ = _item_long_description).text))
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
    
    return _row


print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Start.')

website = get_website(WEBSITE_LINK)
side_panel = website.find(id = SIDE_MENU_ID)

family_links = get_every_family_link(side_panel)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_every_category_link, family_links, WEBSITE_LINK)

    for result in results:
        print(result)
        
print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every category.')



    
#with concurrent.futures.ThreadPoolExecutor() as executor:
#    results = executor.map(find_last_category_depth, categories)
#print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every last category depth.')
#last_categories = []
#for result in results:
#    last_categories.append(result)


#with concurrent.futures.ThreadPoolExecutor() as executor:
#    results = executor.map(get_item_links, last_categories, WEBSITE_LINK)
#print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Found every item link.')
#item_links = []
#for result in results:
#    item_links.append(result)

#print(item_links)
#item_links = get_item_links(last_categories, WEBSITE_LINK)

#with open('timarszerszam.csv', 'w', newline = '') as csv_file:
#    write = csv.writer(csv_file, delimiter=';')
#    for item_link in item_links:
#        website = get_website(item_link)
#        write.writerow(get_item_data(item_link, website, ITEM_NAME_CLASS, ITEM_PRODUCT_NUMBER, ITEM_PRICE, ITEM_DESCRIPTION, ITEM_LONG_DESCRIPTION))

print('[' + datetime.now().strftime("%H:%M:%S") + ']' , 'Done.')

#with open('timarszerszam.csv', 'w', newline = '') as csv_file:
#        write = csv.writer(csv_file, delimiter=';')
#        write.writerow(get_item(item_link, website, ITEM_NAME_CLASS, ITEM_PRODUCT_NUMBER, ITEM_PRICE, ITEM_DESCRIPTION, ITEM_LONG_DESCRIPTION))
