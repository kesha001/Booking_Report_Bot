# Class responsible for interactions with filters
# once results from search are reached
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


# TODO: add more filtration options
class BookingFiltration():
    
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def select_property_ratings(self, *ratings):
        rating_elements = self.driver.find_elements(
            By.XPATH, "//div[@id='filter_group_class_:R14q:']//*"
        )
        filtered_elements = []
        for rating in ratings:
            for element in rating_elements:
                if element.get_attribute('data-filters-item') == f'class:class={rating}':
                    filtered_elements.append(element)

        for element in filtered_elements:
            element.click()

        # Can also be done with specifying XPATH "//div[@id='filter_group_class_:R14q:']//div[@data-filters-item='class:class=4']"
    
    def sort_results(self):
        # TODO: add more sorting parameters
        sorting_panel_element = self.driver.find_element(
            By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']"
        )
        sorting_panel_element.click()
        
        price_sort_element = self.driver.find_element(
            By.XPATH, "//div[@data-testid='sorters-dropdown']//button[@data-id='price']"
        )
        price_sort_element.click()
