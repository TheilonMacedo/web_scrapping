def get_data_pmi():
    import logging
    import os
    import re
    import time

    import arrow
    import numpy as np
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from sqlalchemy import create_engine
    from webdriver_manager.chrome import ChromeDriverManager

    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)

    logging.info("Starting to perform data collection...")

    INVESTING_PAGE_URL = (
        "https://www.investing.com/economic-calendar/chinese-caixin-services-pmi-596"
    )

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    print("Teste")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options,
    )
    driver.get(INVESTING_PAGE_URL)
    time.sleep(10)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            )
        ).click()
        time.sleep(2)
    except:
        print("Erro ao chegar ao site.")

    logging.info("Getting PMI values...")

    for i in range(20):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="showMoreHistory596"]/a'))
        ).click()
        time.sleep(2)

    body = driver.find_elements(By.CSS_SELECTOR, "#eventHistoryTable596 > tbody")
    for i in body:
        get = pd.Series(i.text)

    driver.close()
    driver.quit()

    logging.info("Starting data storing process...")

    def split_in_date(text):
        return re.split(r"((?:0?[1-9][0-2]):[0-5][0-9])", text)

    values_list = [split_in_date(i) for i in list(get[0].split("\n"))]

    month_list = [
        "(Jan)",
        "(Feb)",
        "(Mar)",
        "(Apr)",
        "(May)",
        "(Jun)",
        "(Jul)",
        "(Aug)",
        "(Sep)",
        "(Oct)",
        "(Nov)",
        "(Dec)",
    ]

    month_replacement = {i: "" for i in month_list}

    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
            string_1 = text.strip()
            string_2 = arrow.get(string_1, "MMM DD, YYYY").format("YYYY-MM-DD")
        return string_2

    date = [replace_all(i[0], month_replacement) for i in values_list]
    close = [i[1] for i in values_list]
    time_data = pd.DataFrame({"date": date, "close": close})

    logging.info("Time data acquired...")

    def get_pmi_values(record_list, col_names):
        pmi_values = [
            i[2].replace("   ", " NaN ").strip().split(" ") for i in record_list
        ]
        df = pd.DataFrame()
        for i, k in enumerate(col_names):
            vals = [j[i] for j in pmi_values]
            df[k] = vals
        return df

    numeric_cols = ["actual", "forecast", "previous"]

    price_data = get_pmi_values(values_list, numeric_cols)

    logging.info("PMI values acquired. Storing data...")

    final_data = pd.concat([time_data, price_data], axis=1)

    final_data[numeric_cols] = (
        final_data[numeric_cols].replace("NaN", np.NaN).apply(pd.to_numeric)
    )

    disk_engine = create_engine("sqlite:///pmi.db")

    def write_to_disk(df):
        df.to_sql("pmi", disk_engine, if_exists="append", index=False)

    write_to_disk(final_data)

    logging.info("Data stored successfully.")


if __name__ == "__main__":
    get_data_pmi()
