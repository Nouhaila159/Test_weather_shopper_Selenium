from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.PageObjects.base.BasePage import BasePage

class CartPage(BasePage):
    CART_BUTTON = (By.XPATH, "/html/body/nav/ul/button")
    CHECKOUT_BUTTON = (By.XPATH, "/html/body/div[1]/div[3]/form/button")
    EMAIL_FIELD = (By.ID, "email")
    CARD_NUMBER_FIELD = (By.ID, "card_number")
    EXP_DATE_FIELD = (By.ID, "cc-exp")
    CSC_FIELD = (By.ID, "cc-csc")
    BILLING_ZIP_FIELD = (By.ID, "billing-zip")
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="submitButton"]')

    def click_cart(self):
        self.driver.find_element(*self.CART_BUTTON).click()

    def proceed_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

    def fill_payment_details(self, email, card_number, exp_date, csc, zip_code):
        self.driver.switch_to.frame(0)
        formulaire = [
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))),
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "card_number"))),
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cc-exp"))),
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cc-csc")))
        ]

        credit_card_info = [email, card_number, exp_date, csc]

        def typeslowly(loc, text):
            for i in text:
                loc.send_keys(i)

        for i in range(4):
            typeslowly(formulaire[i], credit_card_info[i])

        zip_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'billing-zip'))
        )
        zip_element.send_keys(zip_code)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]'))
        )
        submit_button.click()