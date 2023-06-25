# Methods for parsing data from hotel deal boxes
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class BookingReport:
    
    def __init__(self, search_result_elements: WebElement):
        self.search_result_elements = search_result_elements
        self.deal_boxes = self.pull_deal_boxes()

    
    def pull_deal_boxes(self):
        return self.search_result_elements.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]'
        )
    

    def pull_deal_data(self):
        collection = []
        for deal_box in self.deal_boxes:
            # pull hotel name
            hotel_name = deal_box.find_element(
                            By.CSS_SELECTOR, 'div[data-testid="title"]'
                        ).get_attribute('innerHTML').strip() 
            
            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]'
            ).get_attribute('innerHTML').strip().replace("&nbsp", "")

            hotel_score_element = deal_box.find_element(
                By.CSS_SELECTOR, 'div[data-testid="review-score"]'
            )
            hotel_score = hotel_score_element.find_element(
                By.XPATH, 'div[1]'
            ).get_attribute('innerHTML')

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        
        return collection



