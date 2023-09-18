from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient


driver = webdriver.Chrome()

# Define cities and URLs
cities = ["Pune", "Delhi", "Mumbai", "Lucknow", "Agra", "Ahmedabad", "Kolkata", "Jaipur", "Chennai", "Bengaluru"]

# MongoDB connection
client = MongoClient('mongodb+srv://saranshtripathi27:DtEY9xoXl71fBxVZ@cluster0.s80qv5h.mongodb.net/')
db = client.project  
collection = db.property

def insertPropertyDetails(name, cost, p_type, locality, area, city, link):
    doc = {
        "name": name,
        "cost": cost,
        "property_type": p_type,
        "locality": locality,
        "area": area, 
        "city": city,
        "link": link,
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id 

for city in cities:
    url = f"https://www.99acres.com/search/property/buy/{city}?keyword={city}"
    driver.get(url)

    # Simulate scrolling down to load more content (adjust the number of scrolls as needed)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Get the HTML source after loading the dynamic content
    dynamic_html = driver.page_source

    # Parse the dynamic HTML content with BeautifulSoup
    soup = BeautifulSoup(dynamic_html, 'html.parser')

    # Extract and save specific elements from the dynamic page
    elements = soup.find_all('div', class_='projectTuple__descCont')

    for item in elements:
        name = item.find('a', class_='projectTuple__projectName projectTuple__pdWrap20 ellipsis').text.strip()
        cost = item.find('span', class_='list_header_bold configurationCards__srpPriceHeading configurationCards__configurationCardsHeading').text.strip()
        p_type = item.find('span', class_='list_header_semiBold configurationCards__configBandLabel').text.strip()
        locality = item.find('h2', class_='projectTuple__subHeadingWrap body_med ellipsis').text.strip()
        area = item.find('span', class_='caption_subdued_medium configurationCards__cardAreaSubHeadingOne').text.strip()
        link = item.find('a', class_='projectTuple__projectName projectTuple__pdWrap20 ellipsis')['href']

        # Save the scraped data to MongoDB
        print(property_data)
        insertPropertyDetails(name, cost, p_type, locality, area, city, link)

# Close the WebDriver
driver.quit()
