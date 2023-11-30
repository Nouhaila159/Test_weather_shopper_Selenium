from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import re

x = datetime.datetime.now()

def extract_digits(text):
    return int(''.join(filter(str.isdigit, text)))

def test_google_search():
    # Instancier l'objet driver
    driver = webdriver.Edge()
    driver.maximize_window()
    # Accéder à weathershopper.pythonanywhere.com
    driver.get("https://weathershopper.pythonanywhere.com/")
    # Vérifier l'URL de la page
    assert driver.current_url == "https://weathershopper.pythonanywhere.com/", "Ce n'est pas la bonne URL"
    # Prendre une capture d'écran de la page
    driver.save_screenshot(f'screenshots/screenshot-{x.year}-{x.month}-{x.day}{x.hour}{x.minute}_{x.second}.png')
    # Mettre à jour l'assertion pour le titre
    assert driver.title == "Current Temperature", "Mauvais titre de la page"

    moisture = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[1]/a/button")
    sunscreen = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/a/button")
    time.sleep(5)

    temperature_str = driver.find_element(By.ID, "temperature").text.replace(' ℃', '')
    # Extrait uniquement les chiffres de la chaîne
    temperature = int(''.join(filter(str.isdigit, temperature_str)))

    # Moisture
    if temperature <= 19:
        moisture.click()
        # Almond
        Almond_products = driver.find_elements(By.XPATH, "//p[contains(text(),'Almond')]")
        min_price_Almond = 9999
        for product in Almond_products:
            price_element = product.find_element(By.XPATH, "./following-sibling::p")
            product_price = extract_digits(price_element.text)
            min_price_Almond = min(min_price_Almond, product_price)
        print(f"Minimum Price for Almond: {min_price_Almond}")
        # Aloe
        Aloe_products = driver.find_elements(By.XPATH, "//p[contains(text(),'Aloe')]")
        min_price_Aloe = 9999
        for product in Aloe_products:
            price_element = product.find_element(By.XPATH, "following-sibling::p")
            product_price = extract_digits(price_element.text)
            min_price_Aloe = min(min_price_Aloe, product_price)
        print(f"Minimum Price for Aloe: {min_price_Aloe}")
        time.sleep(10)
        driver.find_element(By.XPATH, f"//p[contains(text(), '{str(min_price_Aloe)}')]//following-sibling::button").click()
        driver.find_element(By.XPATH, f"//p[contains(text(), '{str(min_price_Almond)}')]//following-sibling::button").click()
        fill_payment_form(driver)
    # Sunscreen
    elif temperature >= 34:
        sunscreen.click()
        # SPF-50
        spf50_products = driver.find_elements(By.XPATH, "//p[contains(text(),'SPF-50')]")
        min_price_spf50 = 999
        for product in spf50_products:
            price_element = product.find_element(By.XPATH, "./following-sibling::p")
            price_text = price_element.text.replace("Price: Rs. ", "")
            price_digits = ''.join(filter(lambda x: x.isdigit() or x == '.', price_text))
            price = int(price_digits)
            min_price_spf50 = min(min_price_spf50, price)
        print(f"Minimum Price for SPF-50: Rs. {min_price_spf50}")
        # SPF-30
        spf30_products = driver.find_elements(By.XPATH, "//p[contains(text(),'SPF-30')]")
        min_price_spf30 = 999
        for product in spf30_products:
            price_element = product.find_element(By.XPATH, "following-sibling::p")
            price_text = price_element.text.replace("Price: Rs. ", "")
            price_digits = ''.join(filter(lambda x: x.isdigit() or x == '.', price_text))
            price = int(price_digits)
            min_price_spf30 = min(min_price_spf30, price)
        print(f"Minimum Price for SPF-30: Rs. {min_price_spf30}")

        driver.find_element(By.XPATH, f"//p[contains(text(), '{str(min_price_spf30)}')]//following-sibling::button").click()
        driver.find_element(By.XPATH, f"//p[contains(text(), '{str(min_price_spf50)}')]//following-sibling::button").click()
        fill_payment_form(driver)

def fill_payment_form(driver):
    # Click on the cart
    cart = driver.find_element(By.XPATH, "/html/body/nav/ul/button")
    cart.click()

    # Click on the checkout button
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/button").click()

    # Switch to the iframe
    driver.switch_to.frame(0)

    # Fill in the payment form
    form_elements = [
        driver.find_element(By.ID, "email"),
        driver.find_element(By.ID, "card_number"),
        driver.find_element(By.ID, "cc-exp"),
        driver.find_element(By.ID, "cc-csc")
    ]

    credit_card_info = ["n.danouni@mundiapolis.ma", "4242424242424242", "1130", "123"]

    for element, info in zip(form_elements, credit_card_info):
        typeslowly(element, info)

    # Fill in the zip code separately (outside the loop)
    zip_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'billing-zip'))
    )
    zip_element.send_keys("26100")

    # Click the submit button
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]'))
    )
    submit_button.click()

    time.sleep(5)
    driver.quit()

# Define the typeslowly function
def typeslowly(loc, text):
    for i in text:
        loc.send_keys(i)
        time.sleep(0.5)

test_google_search()
