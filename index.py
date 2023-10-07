from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def write_json(data, stop):
    # Open the file in append mode
    with open("data.json", "a") as file:
        # Check if the file is empty (i.e., doesn't contain an array yet)
        file.seek(0, 2)  # Move to the end of the file
        if file.tell() == 0:
            # If the file is empty, write an opening square bracket
            file.write("[\n")

        if stop:
            # Serialize and write the new JSON object
            json_str = json.dumps(data, indent=4)
            file.write(json_str)
            file.write("\n")
            file.write("]")
        else:
            # Serialize and write the new JSON object
            json_str = json.dumps(data, indent=4)
            file.write(json_str)
            file.write(",\n")


       




def scrape_projects(browser, url):
    browser.get(url)


    count = 0
    while True:
        element = WebDriverWait(browser,120).until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))
        # all the project divs containing project infomation scrapped.
        page_content = browser.find_elements(By.CLASS_NAME, 'content')
        print(len(page_content))
        next_button = browser.find_element(By.XPATH, "//button[@aria-label='Next page']")
        for index, project in enumerate(page_content):
            
            count +=1
            #contributor name
            contributor = project.find_element(By.CLASS_NAME,"contributor__content").text

            #organization name
            org_container = project.find_element(By.CLASS_NAME,"organization")
            org = org_container.find_element(By.CLASS_NAME,"mentor__content").text

            #project title
            title = project.find_element(By.CLASS_NAME,"title").text

            #project description
            description = project.find_element(By.CLASS_NAME,"description").text

            #link 
            link = project.find_element(By.TAG_NAME,"a").get_attribute('href')

            data = {
                "contributor":contributor,
                "org":org,
                "title":title,
                "description":description,
                "link":link,
            }
            if next_button.get_attribute("disabled"):
                print(len(page_content) -1)
                print(index)
                if (len(page_content)- 1 ) == index:
                    write_json(data,True)
                else:
                    write_json(data, False)
        
            else:
                write_json(data, False)

            print(f'done {count}')
        
        if next_button.get_attribute("disabled"):
            break
        browser.execute_script("arguments[0].click();", next_button)
def scrape_info(link, browser, data):
    browser.get(link)

    element = WebDriverWait(browser,120).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    contributor_name = browser.find_element(By.CLASS_NAME,"contributor__name").text
    dd = browser.find_elements(By.XPATH, "//dd[@class='text--weight-medium']")
    technologies = dd[2].text
    topic = dd[3].text
    
    data2 = {
        "technologies":technologies,
        "topic":topic
    }

    # Search for contributor_name in data.json and append data2 to the matching object
    for item in data:
        if item["contributor"] == contributor_name:
            item.update(data2)
    
    # Write the updated data back to data.json
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    browser = webdriver.Firefox()
    url = "https://summerofcode.withgoogle.com/programs/2023/projects"
    scrape_projects(browser, url)

    try:
    # Load the JSON data from data.json
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)  # Load data from data.json

        for object in data:  # Iterate through the objects in the loaded JSON data
            link = object['link']
            scrape_info(link, browser, data)

    except Exception as e:
        print(f'error {e}')
    
        
