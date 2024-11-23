import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# --------------------------------connecting to the website-------------------------------------------------------------
response = requests.get(url="https://appbrewery.github.io/Zillow-Clone/")
zillow_sf_listing = response.text

# ------------------------------------------Web Scraping----------------------------------------------------------------
soup = BeautifulSoup(zillow_sf_listing, "html.parser")

# listing address
listing_address = soup.find_all("address")
listing_address_list = [listing.text.strip() for listing in listing_address]

# listing price
listing_price = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
listing_price_list = [listing.text.split("+")[0].split("/")[0] for listing in listing_price]

# listing link
listing_link = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
listing_link_list = [listing["href"] for listing in listing_link]


# --------------------------------------Google form auto filling--------------------------------------------------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for i in range(len(listing_address_list)):
    # Your own google form path
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfHJSecErN0VnfrlsxO-CiOp9_xlzOWqlfWQVTlu2z61pVu2Q/viewform?usp=sf_link")
    time.sleep(2)

    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(listing_address_list[i])

    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(listing_price_list[i])

    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(listing_link_list[i])

    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()