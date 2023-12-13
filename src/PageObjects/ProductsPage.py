from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.PageObjects.base.BasePage import BasePage
class ProductsPage(BasePage):
    def get_product_prices(self, product_type):
        produits = self.driver.find_elements(By.XPATH, f"//p[contains(text(),'{product_type}')]")
        prices = {}

        for product in produits:
            price_element = product.find_element(By.XPATH, "./following-sibling::p")
            product_price = self.extract_digits(price_element.text)
            prices[product] = product_price

        sorted_prices = sorted(prices.items(), key=lambda x: x[1])
        least_expensive_product = sorted_prices[0][0]

        return least_expensive_product

    def extract_digits(self, text):
        return int(''.join(filter(str.isdigit, text)))

    def click_buy_button(self, product_name):
        buy_button = self.driver.find_element(By.XPATH, f"//p[contains(text(),'{product_name}')]/following-sibling::button")
        buy_button.click()