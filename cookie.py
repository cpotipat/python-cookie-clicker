from selenium import webdriver
from time import time

chrome_driver_path = MY_CHROME_DRIVER_PATH
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get cookie element to click on
cookie = driver.find_element_by_id("cookie")

# Get all upgrade item ids
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time() + 5
five_min = time() + (60 * 5)

while True:
    cookie.click()

    # Check every 5 seconds
    if time() > timeout:

        # Get all upgrade item tags
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        # Convert from tag to integer price
        for item in all_prices:
            item_text = item.text
            if item_text != "":
                price = int(item_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(price)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for i in range(len(item_prices)):
            cookie_upgrades[item_prices[i]] = item_ids[i]

        # Get current cookie count
        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Get all affordable items
        affordable_items = {}
        for price, item_id in cookie_upgrades.items():
            if cookie_count > price:
                affordable_items[price] = item_id

        # Buy the most expensive items
        max_price_item = max(affordable_items)
        to_buy_item_id = affordable_items[max_price_item]

        # Click the most expensive affordable item
        driver.find_element_by_id(to_buy_item_id).click()

        # Add another 5 seconds until the next check
        timeout = time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break
