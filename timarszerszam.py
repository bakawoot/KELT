from bs4 import BeautifulSoup
import requests
import re
import csv

def fetch_website(_weblink):
    _html_text = requests.get(_weblink).text
    _website = BeautifulSoup(_html_text, 'lxml')
    return _website

#fetch website
website_link = 'https://www.timarszerszam.hu/'
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
        for category in category_element.find_all(class_ = 'category_box_in'):
            categories.append(category.a.get('href'))

for i in range(len(categories)):
    website = fetch_website(website_link + categories[i])
    #check if we have more categories or not
    if website.find(class_ = 'category_categories') == None:
        if website.find(class_ = 'product_list2') != None:
            items_list = website.find(class_ = 'product_list2')
            for item in items_list.find_all(class_ = 'row product_box2'):
                item_links.append(website_link + item.a.get('href'))
                
items = []
rows = []
for i in range(len(item_links)):
    website = fetch_website(item_links[i])
    #gyártói cikkszám
    rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right product_no').text)
    #megnevezés
    rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right').text)
    #ár
    rows.append(website.find(class_ = 'col-sm-9 col-xs-8 pb2_right price').text)
    #készletinfó
    if website.find(class_ = "stock outstock"):
        rows.append(website.find(class_ = "stock outstock").text)
    if website.find(class_ = "stock instock"):
        rows.append(website.find(class_ = "stock instock").text)
    #hivatkozás
    rows.append(item_links[i].replace('\n' , ' '))
    
    items.append(rows)
    rows = []

with open('timarszerszam.csv', 'w', newline = '') as csv_file:
    write = csv.writer(csv_file, delimiter=';')
    for i in range(len(items)):
        write.writerow(items[i])

