#megvannak azok a termékek linkjei, amelyek nincsenek kategóriába sorolva, csak családba!
#megvannak azon kategóriák linkjei, amelyek közvetlenül családhoz vannak sorolva

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

categories = []
item_links =[]
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
            categories.append(category.a.get('href'))       
    else:
        
        #if category element doesn't exist:
        if website.find(class_ = 'product_list') != None:
            items_list = website.find(class_ = 'product_list')
            for item in items_list.find_all(class_ = 'col-sm-9 col-xs-8 pb2_right'):
                if 'http://timarszerszam.hu/' in item.a.get('href'):
                    item_links.append(item.a.get('href'))
                else:
                    item_links.append(website_link + item.a.get('href'))

for i in range(len(categories)):
    html_text = requests.get(website_link + categories[i]).text
    website = BeautifulSoup(html_text, 'lxml')

    #check if we have more categories or not
    if website.find(class_ = 'category_categories') != None:

        #if category element exists
        category_element = website.find(class_ = 'category_categories')
        for category in category_element.find_all(class_ = 'pic'):
            categories.append(category.a.get('href'))

for i in range(len(categories)):
    html_text = requests.get(website_link + categories[i]).text
    website = BeautifulSoup(html_text, 'lxml')

    #check if we have more categories or not
    if website.find(class_ = 'category_categories') == None:
        if website.find(class_ = 'product_list2 table-responsive') != None:
            items_list = website.find(class_ = 'product_list2 table-responsive')
            for item in items_list.find_all(class_ = 'odd'):
                if 'http://timarszerszam.hu/' in item.a.get('href'):
                    item_links.append(item.a.get('href'))
                else:
                    item_links.append(website_link + item.a.get('href'))
                    
            for item in items_list.find_all(class_ = 'even'):
                if 'http://timarszerszam.hu/' in item.a.get('href'):
                    item_links.append(item.a.get('href'))
                else:
                    item_links.append(website_link + item.a.get('href'))

print(item_links)

items = []
rows = []
for i in range(len(item_links)):
    print(item_links[i])
    html_text = requests.get(item_links[i]).text
    website = BeautifulSoup(html_text, 'lxml')
    if 'https://www.timarvasker.hu/' in item_links[i]:
        print('jó oldalt vizsgálunk')
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right product_no').text.replace('\n' , '').replace('\xf5', 'HIBÁSKARAKTER'))
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right print_hide').text.replace('\n' , '').replace('\xf5', 'HIBÁSKARAKTER'))
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right price').text.replace('\n' , '').replace('\xf5', 'HIBÁSKARAKTER'))
        #rows.append(website.find(class_ = 'count2'))
        if website.find(class_ = 'product_tab act') != None:
            rows.append(website.find(class_ = 'product_tab act').text.replace('\n' , '').replace('\xf5', 'ő'))
            
        items.append(rows)
        rows = []

        print(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right product_no').text.replace('\n' , ''))
        print(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right print_hide').text.replace('\n' , ''))
        print(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right price').text.replace('\n' , ''))
        #print(website.find(class_ = 'count2'))
        if website.find(class_ = 'product_tab act') != None:
            print(website.find(class_ = 'product_tab act').text.replace('\n' , ''))

print(items)

with open('timarvasker.csv', 'w', newline = '') as csv_file:
    write = csv.writer(csv_file)
    for i in range(len(items)):
        write.writerow(items[i])
