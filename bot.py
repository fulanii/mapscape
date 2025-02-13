"""Selenium imports"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

"""Other imports"""
import time
import os


class Bot:
    """A Selenium bot using Chrome to scrape Google Maps for business information."""
    def __init__(self, business_type:str, business_city:str, business_state_or_country:str):
        self.business_type = business_type
        self.business_city = business_city
        self.business_state_or_country = business_state_or_country
        self.url:str = f"https://www.google.com/maps/search/{self.business_type}+{self.business_city}+{self.business_state_or_country}"
        self.all_links_sett:set = set()

    def driver(self, is_detached:bool) -> webdriver.Chrome:
        """Set up the Selenium WebDriver."""
        options = Options()
        options.add_experimental_option("detach", is_detached)
        driver = webdriver.Chrome(options=options)

        return driver

    def scroll(self, driver:webdriver.Chrome) -> None:
        """Scroll through the page to load all business listings."""

        # div containing the scrollable content
        scrollable_div =  driver.find_elements(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_div[1])

            # Wait to load page
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div[1])

            if new_height == last_height:
                break

            last_height = new_height

    def get_all_links(self, driver:webdriver.Chrome) -> None:
        """Get all business links from the page."""

        # all bussiness a-tag links
        all_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.hfpxzc"))
        )

        for link in all_links:
            href = link.get_attribute('href')
            self.all_links_sett.add(href)

    def open_and_save_links(self, driver:webdriver.Chrome) -> None:
        """Open each business link in a new tab and scrape data. And save the data to a text file."""

        # Store the ID of the original window
        original_window = driver.current_window_handle

        for link in self.all_links_sett:
            # open new tab
            driver.execute_script("window.open('');") 

            # Switch to the new window and open new URL 
            driver.switch_to.window(driver.window_handles[1]) 

            # Open the link in the new tab
            driver.get(link) 

            try:

                # # Wait for modal to load and get business name
                business_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf.lfPIob"))
                ).text
                

                # find the business info elements **AFTER** clicking
                business_info_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "Io6YTe.fontBodyMedium.kR99db.fdkmkc "))
                )

                # create data folder is doesnt exists
                try:
                    os.mkdir("data")
                except FileExistsError:
                    pass

                with open(f"data/{self.business_type}_{self.business_city}_{self.business_state_or_country}.txt", "a") as f:
                    f.write(business_name + "\n")
                    for info in business_info_elements:
                        f.write(info.text + "\n")
                    f.write("----------------------------------------------------------------------" + "\n")

            except Exception as e:
                print(e)

            driver.close() 

            #Switch back to the old tab or window
            driver.switch_to.window(original_window)

            # wait 3 sec
            driver.implicitly_wait(3)


if __name__ == "__main__":
    business_type = "barbershop"
    business_city = "detroit"
    business_state_or_country = "Mi"

    test = Bot(business_type, business_city, business_state_or_country)

    driver = test.driver(is_detached=True)

    driver.get(test.url)

    test.scroll(driver)

    test.get_all_links(driver)

    test.open_and_save_links(driver)

    driver.quit()