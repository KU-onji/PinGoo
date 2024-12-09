from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service("/root/.local/bin/chromedriver")
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)
driver.get(
    "https://www.google.com/maps/place/%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E+%E4%BA%AC%E9%83%BD%E5%BA%97/@35.0438588,135.7849384,16z/data=!3m1!4b1!4m6!3m5!1s0x6001084ba7d50001:0xa2a8eb4a1f3a0460!8m2!3d35.0438588!4d135.7875133!16s%2Fg%2F11f3d26m20?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D"  # noqa
)
driver.implicitly_wait(3)
shop_name = driver.find_element(
    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'
)
print(shop_name.text)
driver.quit()
