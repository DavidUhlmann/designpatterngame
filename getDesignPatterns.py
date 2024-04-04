# Contents of getDesignPatterns.py
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AzureArchitecturePatternsScraper:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(self.url)
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table[aria-label='Table 2']"))
            )
            data = []
            for row in table.find_elements(By.TAG_NAME, "tr"):
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 0:
                    name = cells[0].text
                    hyperlink = cells[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                    if hyperlink.startswith("/"):
                        hyperlink = "https://learn.microsoft.com" + hyperlink
                    data.append({"Name": name, "Hyperlink": hyperlink})
            return data

class DesignPatternDetailsScraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_details(self):
        details = {
            "DesignPattern": "",
            "Description": "",
            "Link": ""  # This will be populated in the main function
        }

        title_element = self.soup.find('h1', class_='title is-1')
        if title_element:
            details["DesignPattern"] = title_element.text.strip()

        content_element = self.soup.find('div', class_='content')
        if content_element:
            first_paragraph = content_element.find('p')
            if first_paragraph:
                details["Description"] = first_paragraph.text.strip()

        return details