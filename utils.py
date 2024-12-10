import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By


def expand_shortened_url(shortened_url: str) -> str:
    response = requests.get(shortened_url)
    return response.url


def isGoogleMapsUrl(url: str) -> bool:
    return url.startswith("https://www.google.com/maps/place/")


def isShortenedUrl(url: str) -> bool:
    return url.startswith("https://maps.app.goo.gl/")


def get_shop_details(url: str) -> dict:
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    if isShortenedUrl(url):
        full_url = expand_shortened_url(url)
    else:
        full_url = url
    assert isGoogleMapsUrl(full_url), "URL is not a Google Maps URL"
    driver.get(full_url)
    driver.implicitly_wait(3)

    shop_name = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1',
    )
    shop_name = shop_name.text

    open_hours = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[4]/div[2]',
    )
    open_hours = open_hours.get_attribute("aria-label")
    open_hours = open_hours.split(".")[:-1][0]
    open_hours = open_hours.split("; ")
    open_hours = list(map(lambda x: x.split("、", 1), open_hours))
    open_hours = {day: hours for day, hours in open_hours}

    address = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[3]/button',
    )
    address = address.get_attribute("aria-label")
    address = address.split(" ")[2]

    review_button = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]',
    )
    review_button.click()
    driver.implicitly_wait(3)

    num_reviews = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]',
    )
    num_reviews = num_reviews.text

    driver.quit()
    return {
        "shop_name": shop_name,
        "open_hours": open_hours,
        "address": address,
        "num_reviews": num_reviews,
    }


def isOpen(open_hours: dict) -> bool:
    def format_open_hours(open_hours: dict) -> dict:
        formatted_open_hours = {}
        for day, hours in open_hours.items():
            if hours == "定休日":
                formatted_open_hours[day] = []
                continue
            li_hours = hours.split("、")
            li_hours = list(map(lambda x: x.replace("時", ":").replace("分", "").replace("～", "-"), li_hours))
            formatted_open_hours[day] = li_hours
        return formatted_open_hours

    now = time.localtime()
    dt_now = datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    weekday = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    day = weekday[now.tm_wday]

    formatted_open_hours = format_open_hours(open_hours)
    open_hours_today = formatted_open_hours.get(day, [])
    if open_hours_today == []:
        return False

    for hours in open_hours_today:
        start, end = hours.split("-")
        start = datetime.strptime(start, "%H:%M").time()
        end = datetime.strptime(end, "%H:%M").time()
        if start <= dt_now.time() <= end:
            return True
    return False


def search_shops_near_lab(keyword: str) -> list:
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    LAB_URL = "https://www.google.com/maps/place/%E4%BA%AC%E9%83%BD%E5%A4%A7%E5%AD%A6+%E7%B7%8F%E5%90%88%E7%A0%94%E7%A9%B67%E5%8F%B7%E9%A4%A8/@35.0275946,135.7812041,17z/data=!3m1!5s0x6001085626a00b8b:0xb743fb5198e28857!4m6!3m5!1s0x6001085626a411a3:0x70a2e13e53d9064!8m2!3d35.0275947!4d135.7837787!16s%2Fg%2F11b7jydgkl?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D"  # noqa
    driver.get(LAB_URL)
    driver.implicitly_wait(3)

    search_nearby_button = driver.find_element(
        By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/button',
    )
    search_nearby_button.click()
    driver.implicitly_wait(3)

    search_box = driver.find_element(By.XPATH, '//*[@id="XmI62e"]')
    search_box.send_keys(keyword)
    search_button = driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
    search_button.click()
    driver.implicitly_wait(3)

    pass
