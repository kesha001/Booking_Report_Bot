import os
import types
from typing import List
import time
import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    
    def __init__(self, driver_path="D:/SeleniumDrivers/Chrome", \
                    binary_path="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe", \
                    detach=False, disable_logging=True):     
        self.driver_path = driver_path
        self.binary_path = binary_path
        self.detach = detach

        # os.environ['PATH'] += self.driver_path   

        self.option = webdriver.ChromeOptions()
        self.option.binary_location = self.binary_path
        
        # Detach to left window opened
        if self.detach:
            self.option.add_experimental_option("detach", True)
        if disable_logging:
            self.option.add_experimental_option('excludeSwitches', ['enable-logging'])

        super(Booking, self).__init__(options=self.option)

        self.implicitly_wait(15)
        self.maximize_window()


    def land_first_page(self):
        self.get(const.BASE_URL)
        

    def close_popup(self):
        """
        Removes popup that is shown in the beggining to sign in
        """
        try:
            close_button = self.find_element(
                By.XPATH, '//div[@class="e284d5707f"]//button[@type="button"]'
            )
            close_button.click()
            print("popup found")
        except:
            print('did not find popup')
            pass


    def change_currency(self, currency="EUR"):
        # open currency picker
        currency_picker_element = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'
        )
        currency_picker_element.click()

        # select currency from input
        try:
            picked_currency_element = self.find_element(
                By.XPATH, f'//div[@class="a448481077"]//div[text()="{currency}"]' # '//div[@class="a448481077"]//div[@class=" ea1163d21f"]'
            )
            picked_currency_element.click()
        except:
            print("Wrong language selected")


    def select_place_to_go(self, place="Ukraine"):
        search_field = self.find_element(By.ID, ":Ra9:")
        search_field.clear()
        search_field.send_keys(place)

        # time to show autocomplete resuts
        time.sleep(1)

        # select the first result
        autocomplete_result = self.find_element(By.XPATH, '//ul[@data-testid="autocomplete-results"]//li[1]')
        autocomplete_result.click()
    
    # TODO: add support for different months
    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
                By.CSS_SELECTOR, f"span[data-date='{check_in_date}']"
            )
        check_in_element.click()

        check_out_element = self.find_element(
                By.CSS_SELECTOR, f"span[data-date='{check_out_date}']"
            )
        check_out_element.click()


    def select_adults(self, adult_num=3):
        # TODO: make for children and rooms
        group_element = self.find_element(
                By.CSS_SELECTOR, "button[data-testid='occupancy-config']"
            )
        group_element.click()

        minus_adults_button_element = self.find_element(
            By.XPATH, "//input[@id='group_adults']/..//button[contains(@class, 'cd7aa7c891')]"
        )
        # minus_adults_button_element.click()
        
        plus_adults_button_element = self.find_element(
            By.XPATH, "//input[@id='group_adults']/..//button[contains(@class, 'd64a4ea64d')]"
        )

        default_adults_number_element = self.find_element(
            By.XPATH, "//input[@id='group_adults']/..//span[@class='e615eb5e43']"
        )
        # reduce count of adults to 1 (min value)
        default_adults_number = int(default_adults_number_element.text)
        for _ in range(default_adults_number-1):
            minus_adults_button_element.click()
        
        for _ in range(adult_num-1):
            plus_adults_button_element.click()

    def do_search(self):
        search_element = self.find_element(
            By.XPATH, "//button[@type='submit']"
        )

        search_element.click()
    

    # TODO: add more interactivity via arguments
    def apply_filters(self):
        filtration_obj = BookingFiltration(self)
        filtration_obj.select_property_ratings(0, 4)
        # to give time list to reload
        time.sleep(1)
        filtration_obj.sort_results()


    def report_results(self):
        search_result_elements = self.find_element(
                By.ID, 'search_results_table'
            )
        
        booking_report = BookingReport(search_result_elements)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"],
        )
        table.add_rows(booking_report.pull_deal_data())

        print(table)