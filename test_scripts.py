from selenium import webdriver
import time
import datetime
from src.PageObjects.weather import Weather
from src.PageObjects.ProductsPage import ProductsPage
from src.PageObjects.CartPage import CartPage

def test_weather_shopper():
    driver = webdriver.Chrome()
    driver.maximize_window()

    home_page = Weather(driver)
    home_page.open()

    x = datetime.datetime.now()
    driver.save_screenshot(f'screenshots/screenshot-{x.year}-{x.month}-{x.day}_{x.hour}_{x.minute}_{x.second}.png')

    if home_page.get_current_temperature() < 19:
        home_page.click_moisturizers()
        products_page = ProductsPage(driver)
        aloe_product = products_page.get_product_prices('Aloe')
        almond_product = products_page.get_product_prices('Almond')
        products_page.click_buy_button(aloe_product.text)
        products_page.click_buy_button(almond_product.text)

    elif home_page.get_current_temperature() > 34:
        home_page.click_sunscreen()
        products_page = ProductsPage(driver)
        spf_50_product = products_page.get_product_prices('SPF-50')
        spf_30_product = products_page.get_product_prices('SPF-30')
        products_page.click_buy_button(spf_50_product.text)
        products_page.click_buy_button(spf_30_product.text)

    cart_page = CartPage(driver)
    cart_page.click_cart()
    cart_page.proceed_to_checkout()
    cart_page.fill_payment_details("n.danouni@mundiapolis.ma", "4242424242424242", "1224", "333", "24")

    time.sleep(5)
    driver.quit()

test_weather_shopper()
