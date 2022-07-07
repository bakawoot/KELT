from bs4 import BeautifulSoup
import requests
import re
import csv

def fetch_website(_weblink):
    _html_text = requests.get(_weblink).text
    _website = BeautifulSoup(_html_text, 'lxml')
    return _website

#fetch website
website_link = 'https://www.timarvasker.hu/'
website = fetch_website(website_link)

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
    website = fetch_website(family_links[i])
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
                if 'http://timarszerszam.hu/' not in item.a.get('href'):
                    item_links.append(website_link + item.a.get('href'))

for i in range(len(categories)):
    website = fetch_website(website_link + categories[i])
    #check if we have more categories or not
    if website.find(class_ = 'category_categories') != None:
        #if category element exists
        category_element = website.find(class_ = 'category_categories')
        for category in category_element.find_all(class_ = 'pic'):
            categories.append(category.a.get('href'))
            
for i in range(len(categories)):
    website = fetch_website(website_link + categories[i])
    #check if we have more categories or not
    if website.find(class_ = 'category_categories') == None:
        if website.find(class_ = 'product_list2 table-responsive') != None:
            items_list = website.find(class_ = 'product_list2 table-responsive')
            for item in items_list.find_all(class_ = 'odd'):
                if 'http://timarszerszam.hu/' not in item.a.get('href'):
                    item_links.append(website_link + item.a.get('href'))
            for item in items_list.find_all(class_ = 'even'):
                if 'http://timarszerszam.hu/' not in item.a.get('href'):
                    item_links.append(website_link + item.a.get('href'))
                    
items = []
rows = []
for i in range(len(item_links)):
    website = fetch_website(item_links[i])
    if 'http://www.timarvasker.hu/' in item_links[i] or 'https://www.timarvasker.hu/' in item_links[i]:
        #cikkszám
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right product_no').text.replace('\n' , ' '))
        #megnevezés
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right print_hide').text.replace('\n' , ' ').replace('\xf5', 'ő'))
        #ár
        rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right price').text.replace('\n' , ' '))
        #Termékleírás
        if website.find(class_ = 'product_tab act') != None:
            rows.append(website.find(class_ = 'product_tab act').text.replace('\n' , ' ').replace('\xf5', 'ő'))
        else:
            rows.append('')
        #hivatkozás
        rows.append(item_links[i])

        for stock in website.find_all(class_ = 'product_stock_span'):
            if stock.find(class_ = "glyphicon glyphicon-ok"):
                rows.append(stock.text + "OK")
            else:
                rows.append(stock.text + "NEM OK")
            
        items.append(rows)
        rows = []

with open('timarvasker.csv', 'w', newline = '') as csv_file:
    write = csv.writer(csv_file)
    for i in range(len(items)):
        write.writerow(items[i])
