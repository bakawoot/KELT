from bs4 import BeautifulSoup
import requests
import re
import csv

website_link = 'https://timarszerszam.hu'
item_name_class = 'maintitle'
item_product_number = 'col-sm-9 col-xs-8 pb2_right product_no'
item_price = 'col-sm-9 col-xs-8 pb2_right price'
item_description = 'col-sm-9 col-xs-8 pb2_right lead'
item_long_description = 'product_tab act'
side_menu_id = 'left_menu_collapse'

def get_website(_weblink):
    _html_text = requests.get(_weblink).text
    _website = BeautifulSoup(_html_text, 'lxml')
    return _website

def replace_character(_string):
    _string = _string.replace('\xb2', 'SPECIALIS_KARAKTER').replace('\xd8', 'SPECIALIS_KARAKTER1').replace('\x84', 'SPECIALIS_KARAKTER2')
    _string = _string.replace('\xbc', 'SPECIALIS_KARAKTER3').replace('\x94', 'SPECIALIS_KARAKTER4').replace('\xbd', 'SPECIALIS_KARAKTER5')
    _string = _string.replace('\u25cf', 'SPECIALIS_KARAKTER6').replace('\u2009', 'SPECIALIS_KARAKTER7').replace('\xba', 'SPECIALIS_KARAKTER8')
    _string = _string.replace('\u2070', 'SPECIALIS_KARAKTER9').replace('\x81', 'SPECIALIS_KARAKTER10').replace('\xb9', 'SPECIALIS_KARAKTER11')
    _string = _string.replace('\u2300', 'SPECIALIS_KARAKTER12').replace('\x96', 'SPECIALIS_KARAKTER13').replace('\xb3', 'SPECIALIS_KARAKTER14')
    _string = _string.replace('\u2264', 'SPECIALIS_KARAKTER15').replace('\u2265', 'SPECIALIS_KARAKTER16').replace('\xf8', 'SPECIALIS_KARAKTER17')
    _string = _string.replace('\xf5', 'SPECIALIS_KARAKTER18').replace('\u2205', 'SPECIALIS_KARAKTER19').replace('\u2267', 'SPECIALIS_KARAKTER20')
    _string = _string.replace('\u200b', 'SPECIALIS_KARAKTER21').replace('\xfb', 'SPECIALIS_KARAKTER21').replace('\u2012', 'SPECIALIS_KARAKTER22')
    _string = _string.replace('\n', '').replace('\u2033', 'SPECIALIS_KARAKTER23').replace('\u2103', 'SPECIALIS_KARAKTER24').replace('\u03b1', 'SPECIALIS_KARAKTER25')
    _string = _string.replace('\u240d','SPECIALIS_KARAKTER26').replace('\u03bc','SPECIALIS_KARAKTER27').replace('\u0301','SPECIALIS_KARAKTER28').replace('\u0308','SPECIALIS_KARAKTER29')
    _string = _string.replace(';',',').replace('\u030b','SPECIALIS_KARAKTER30')
    return _string

def get_item (_item_link, _website, _item_name_class, _item_product_number, _item_price, _item_description, _item_long_description, _fam_link, _category_element, _subcategory):
    _row = []
    if _website.find(class_ = _item_name_class):
        _row.append(replace_character(website.find(class_ = _item_name_class).text))
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
        
    _row.append(_item_link)
    _row.append(_category_element.a.text)
    _row.append(_subcategory.a.text)
    return _row

website = get_website(website_link)
side_panel = website.find(id = side_menu_id)

with open('timarszerszam.csv', 'w', newline = '') as csv_file:
    write = csv.writer(csv_file, delimiter=';')
    for fam_link in side_panel.find_all('a'):
        website = get_website(fam_link.get('href'))

        #category depth 1
        if website.find(class_ = 'category_categories') != None:
            category_element = website.find(class_ = 'category_categories')
            for category in category_element.find_all(class_ = 'category_box_in'):
                website = get_website(website_link + category.a.get('href'))

                #category depth 2
                if website.find(class_ = 'category_categories') != None:
                    category_element = website.find(class_ = 'category_categories')
                    for subcategory in category_element.find_all(class_ = 'category_box_in'):
                        website = get_website(website_link + subcategory.a.get('href'))

                        #category depth 3
                        if website.find(class_ = 'category_categories') != None:
                            subcategory_element = website.find(class_ = 'category_categories')
                            for subcategory2 in subcategory_element.find_all(class_ = 'category_box_in'):
                                website = get_website(website_link + subcategory2.a.get('href'))

                                #category depth 4
                                if website.find(class_ = 'category_categories') != None:
                                    subcategory_element = website.find(class_ = 'category_categories')
                                    for subcategory3 in subcategory_element.find_all(class_ = 'category_box_in'):
                                        website = get_website(website_link + subcategory3.a.get('href'))

                                        #category depth 5
                                        if website.find(class_ = 'product_list2') != None:
                                            items = website.find(class_ = 'product_list2')
                                            for item in items.find_all(class_ = 'row product_box2'):
                                                a_tag = item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
                                                if hasattr(a_tag, 'href'):
                                                    item_link = website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                                                    website = get_website(website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href'))
                                                    write.writerow(get_item(item_link, website, item_name_class, item_product_number, item_price, item_description, item_long_description, fam_link, category_element, subcategory))
                                                #else:
                                                    #print('nincs')
                                                   # print (website_link)
                                else:
                                    if website.find(class_ = 'product_list2') != None:
                                        items = website.find(class_ = 'product_list2')
                                        for item in items.find_all(class_ = 'row product_box2'):
                                            a_tag = item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
                                            if hasattr(a_tag, 'href'):
                                                item_link = website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                                                website = get_website(website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href'))
                                                write.writerow(get_item(item_link, website, item_name_class, item_product_number, item_price, item_description, item_long_description, fam_link, category_element, subcategory))
                                            #else:
                                                #print('nincs')
                                                #print (website_link)
                        else:
                            if website.find(class_ = 'product_list2') != None:
                                items = website.find(class_ = 'product_list2')
                                for item in items.find_all(class_ = 'row product_box2'):
                                    a_tag = item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
                                    if hasattr(a_tag, 'href'):
                                        item_link = website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                                        website = get_website(website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href'))
                                        write.writerow(get_item(item_link, website, item_name_class, item_product_number, item_price, item_description, item_long_description, fam_link, category_element, subcategory))
                                    #else:
                                        #print('nincs')
                                        #print (website_link)
                else:
                    if website.find(class_ = 'product_list2') != None:
                        items = website.find(class_ = 'product_list2')
                        for item in items.find_all(class_ = 'row product_box2'):
                            a_tag = item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
                            if hasattr(a_tag, 'href'):
                                item_link = website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                                website = get_website(website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href'))
                            #else:
                                #print('nincs')
                                #print (website_link)
        else:
            if website.find(class_ = 'product_list2') != None:
                items = website.find(class_ = 'product_list2')
                for item in items.find_all(class_ = 'row product_box2'):
                    a_tag = item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a
                    if hasattr(a_tag, 'href'):
                        item_link = website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href')
                        website = get_website(website_link + item.find(class_ = 'col-sm-9 col-xs-8 pb2_right').a.get('href'))
                        write.writerow(get_item(item_link, website, item_name_class, item_product_number, item_price, item_description, item_long_description, fam_link, category_element, subcategory))
                    #else:
                        #print('nincs')
                        #print (website_link)
