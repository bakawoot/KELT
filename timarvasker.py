#megvannak azok a termékek linkjei, amelyek nincsenek kategóriába sorolva, csak családba!
#megvannak azon kategóriák linkjei, amelyek közvetlenül családhoz vannak sorolva

#todo: kategória kezelés


from bs4 import BeautifulSoup
import requests
import re
import csv

#fetch website
website_link = 'https://www.timarvasker.hu/'
html_text = requests.get(website_link).text
website = BeautifulSoup(html_text, 'lxml')

#declare element for the family list
side_panel = website.find(id = 'left_menu_collapse')

#get every family link 
family_links = []
for link in side_panel.find_all('a'):
    family_links.append(link.get('href'))
    #print(link.get('href'))

categories = []
items =[]
#fetch website & get categories element
for i in range(len(family_links)):
    #get website
    html_text = requests.get(family_links[i]).text
    website = BeautifulSoup(html_text, 'lxml')

    #check if we have categories or not
    if website.find(class_ = 'category_categories') != None:

        #if category element exists
        category_element = website.find(class_ = 'category_categories')
        for category in category_element.find_all(class_ = 'pic'):
            #print(category.a.get('href'))
            categories.append(category.a.get('href'))
            
        #for category in website.find_all(class_ = 'category_box_in'):
        #    categories.append(category.a.get('href'))
        
    else:
        
        #if category element doesn't exist:
        if website.find(class_ = 'product_list') != None:
            items_list = website.find(class_ = 'product_list')
            for item in items_list.find_all(class_ = 'col-sm-9 col-xs-8 pb2_right'):
                items.append(item.a.get('href'))
    #print(items)

for i in range(len(categories)):
    html_text = requests.get(website_link + categories[i]).text
    website = BeautifulSoup(html_text, 'lxml')

    #check if we have more categories or not
    if website.find(class_ = 'category_categories') != None:

        #if category element exists
        category_element = website.find(class_ = 'category_categories')
        for category in category_element.find_all(class_ = 'pic'):
            #print(category.a.get('href'))
            categories.append(category.a.get('href'))

for i in range(len(categories)):
    html_text = requests.get(website_link + categories[i]).text
    website = BeautifulSoup(html_text, 'lxml')

    #check if we have more categories or not
    if website.find(class_ = 'category_categories') == None:
        print('újabb kategória')
        if website.find(class_ = 'product_list2 table-responsive') != None:
            items_list = website.find(class_ = 'product_list2 table-responsive')
            for item in items_list.find_all(class_ = 'cpcol_1'):
                print(item.a)
