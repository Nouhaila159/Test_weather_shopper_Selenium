from src.PageObjects.base.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Weather(BasePage):
    URL = "https://weathershopper.pythonanywhere.com/"
    MOISTURIZERS_BUTTON = (By.XPATH, "/html/body/div/div[3]/div[1]/a/button")
    SUNSCREEN_BUTTON = (By.XPATH, "/html/body/div/div[3]/div[2]/a/button")

    def open(self):
        self.driver.get(self.URL)

    def click_moisturizers(self):
        self.driver.find_element(*self.MOISTURIZERS_BUTTON).click()

    def click_sunscreen(self):
        self.driver.find_element(*self.SUNSCREEN_BUTTON).click()
    def get_current_temperature(self):
        temperature_element = self.driver.find_element(By.ID, "temperature")
        temperature_text = temperature_element.text
        current_temperature = int(''.join(filter(str.isdigit, temperature_text)))
        return current_temperature
    