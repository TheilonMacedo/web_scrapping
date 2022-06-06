def get_data_usd_brl():
    import logging
    import os
    import time
    from datetime import date
    from typing import List

    import pandas as pd
    import unidecode
    from dotenv import load_dotenv
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from sqlalchemy import create_engine
    from webdriver_manager.chrome import ChromeDriverManager

    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)

    logging.info("Starting to perform data collection...")

    load_dotenv()
    SENHA = os.getenv("Senha")
    EMAIL = os.getenv("Email")
    INVESTING_PAGE_URL = "https://br.investing.com/currencies/usd-brl-historical-data"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get(INVESTING_PAGE_URL)
    time.sleep(10)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()
    time.sleep(5)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="userAccount"]/div/a[1]'))
    ).click()
    time.sleep(5)

    input_element = driver.find_element_by_xpath('//*[@id="loginFormUser_email"]')
    input_element.send_keys(EMAIL)
    input_element = driver.find_element_by_xpath('//*[@id="loginForm_password"]')
    input_element.send_keys(SENHA)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="signup"]/a'))
    ).click()
    time.sleep(20)

    select = Select(driver.find_element_by_xpath('//*[@id="data_interval"]'))
    select.select_by_visible_text("Mensal")

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="widgetFieldDateRange"]'))
    ).click()
    time.sleep(5)

    input_element = driver.find_element_by_xpath('//*[@id="startDate"]')
    input_element.clear()
    input_element.send_keys("31/12/1994")

    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    input_element = driver.find_element_by_xpath('//*[@id="endDate"]')
    input_element.clear()
    input_element.send_keys(d1)

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="applyBtn"]'))
    ).click()
    time.sleep(5)

    body = driver.find_elements(By.CSS_SELECTOR, "#curr_table")
    for i in body:
        get = pd.Series(i.text)

    driver.close()
    driver.quit()

    logging.info("Starting data storing process...")

    names = get[0].split("\n")[0].split(" ")
    headers = [unidecode.unidecode(i) for i in names]

    def join_str(pd_series: pd.Series) -> List[List[str]]:
        entries = pd_series[0].split("\n")[1:]
        entries_list = [i.split(" ") for i in entries]
        for i, _ in enumerate(entries_list):
            entries_list[i][0:2] = [" ".join(entries_list[i][0:2])]

        return entries_list

    logging.info("Data collection finished.")

    final_data = pd.DataFrame(join_str(get), columns=headers)
    disk_engine = create_engine("sqlite:///usd_brl.db")

    def write_to_disk(df):
        df.to_sql("usd_brl", disk_engine, if_exists="append", index=False)

    write_to_disk(final_data)

    logging.info("Data stored successfully.")


if __name__ == "__main__":
    get_data_usd_brl()
