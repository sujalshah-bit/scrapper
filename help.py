from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def write_json(product):
    # Open the file in append mode ('a+')
    with open("data.json", "a+") as file:
        # Check if the file is empty (no data or empty JSON)
        file.seek(0)
        data = file.read()
        if data:
            # If the file is not empty, load existing JSON data
            existing_data = json.loads(data)
        else:
            # If the file is empty, initialize with an empty list
            existing_data = []
        
        # Append the new product to the existing data
        existing_data.append(product)
        
        # Move the file cursor to the beginning and truncate the file
        file.seek(0)
        file.truncate()
        
        # Write the combined data (existing + new) as JSON to the file
        json.dump(existing_data, file, indent=2)

def scrape_amazon_page(browser, url):
    browser.get(url)
    count = 0

    while True:
        elem_lists = browser.find_elements(By.CLASS_NAME, 's-card-container')
        
        for item in elem_lists:
            count += 1
            title = item.find_element(By.TAG_NAME, 'h2').text[:30]
            try:
                price = item.find_element(By.CLASS_NAME, 'a-price').text
            except Exception as e:
                print("err")
            img_url = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            product_url = item.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute("href")

            data = {
                "id": count,
                "title": title,
                "price": price,
                "image URL": img_url,
                "product URL": product_url
            }
            write_json(data)
            print(f"Scraped data for item {count}")

        element = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME, 's-pagination-next')))
        try:
            next_button = browser.find_element(By.CLASS_NAME, 's-pagination-next')
            is_disabled = next_button.get_attribute("aria-disabled")
        except:
            is_disabled = True

        if is_disabled == "true":
            break
        else:
            next_button.click()
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 's-card-container')))

if __name__ == "__main__":
    browser = webdriver.Firefox()
    url = "https://www.amazon.in/s?k=mobile%20cover&i=aps&ref=nb_sb_ss_inft-rank-pairwise-override-in-t3_2_12&crid=12VYIZ9SG671J&sprefix=mobile%20cover%2Caps%2C798"
    scrape_amazon_page(browser, url)
