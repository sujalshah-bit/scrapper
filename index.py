from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_projects(browser, url):
    browser.get(url)

    element = WebDriverWait(browser,120).until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))
    # all the project divs containing project infomation scrapped.
    page_content = browser.find_elements(By.CLASS_NAME, 'content')
    print(len(page_content))
    for project in page_content:
        #contributor name
        contributor = project.find_element(By.CLASS_NAME,"contributor__content").text

        #organization name
        org_container = project.find_element(By.CLASS_NAME,"organization")
        org = org_container.find_element(By.CLASS_NAME,"mentor__content").text

        #project title
        title = project.find_element(By.CLASS_NAME,"title").text

        #project description
        description = project.find_element(By.CLASS_NAME,"description").text

        view_code = project.find_element(By.CLASS_NAME,"mat-focus-indicator").click()

        # Switch to the new tab or window (assuming it opens in a new tab or window)
        browser.switch_to.window(browser.window_handles[-1])

        print(f"Contributor: {contributor}")
        print(f"Organization: {org}")
        print(f"title: {title}")
        print(f"description: {description}")
        print("\n")




if __name__ == "__main__":
    browser = webdriver.Firefox()
    url = "https://summerofcode.withgoogle.com/programs/2023/projects"
    scrape_projects(browser, url)