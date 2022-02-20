
from selenium import webdriver
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time

#MongoDB
cluster = MongoClient("mongodb+srv://Will:zRWcpj4gaew9bd3@cluster0.eawjg.mongodb.net/AirBnB-Scraper?retryWrites=true&w=majority")
db = cluster["AirBnB-Scraper"]
collection = db["Listing"]
collection.delete_many({})


#Set up webDriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("/home/will/chromedriver")

driver.get("https://www.airbnb.com/s/Knoxville--Tennessee--United-States/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&tab_id=home_tab&checkin=2022-02-18&checkout=2022-02-19&source=structured_search_input_header&search_type=autocomplete_click")
time.sleep(2)
html = driver.page_source

soup = BeautifulSoup(html, features="html.parser")
listings = []

#get the listings
listings_list = soup.find_all('div', class_='cm4lcvy')
num = len(listings_list)
for x in range(num):
    box = listings_list[x]

#get the listing name
    listings_Name = box.find('span', class_='ts5gl90').get_text()
#get listing info
    listing_Link = box.find('a', class_='l8au1ct')['href']
    listing_Bedrooms = box.find_all('span', class_='mp2hv9t')[1].get_text()
    listing_Bathrooms = box.find_all('span', class_='mp2hv9t')[3].get_text()
    listing_Features = box.find_all('div', class_='i1wgresd')[1].get_text()
    listing_Type = box.find('div', class_='mj1p6c8').get_text()
    listing_Thumb = box.find('img', class_='_6tbg2q')['src']
    capacity = listing_Bedrooms, listing_Bathrooms

#outputsrc
    print(
        'Name:',listings_Name,
        '\n Type:',listing_Type,
        '\n Capacity:', listing_Bedrooms,listing_Bathrooms,
        '\n Features:', listing_Features,
        '\n URL:','www.airbnb.com'+listing_Link,
        '\n img:', listing_Thumb,

    )
    post = {"_id": x,
            'Name': listings_Name,
            'Type': listing_Type,
            'Capacity': capacity,
            'Features': listing_Features,
            'URL': listing_Link,
            'img': listing_Thumb
            }
    collection.insert_one(post)
driver.close()