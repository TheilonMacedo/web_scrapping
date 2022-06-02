import logging
import os

import pandas as pd

import get_table_pmi
import usd_brl

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)

try:
    os.remove("pmi.db")
    os.remove("usd_brl.db")
except FileNotFoundError:
    pass


def get_pmi():
    get_table_pmi.get_data_pmi()
    data_pmi = pd.read_sql("SELECT * FROM pmi", "sqlite:///pmi.db")
    logging.info("BSI created and loaded successfully.")
    print(data_pmi)
    return data_pmi


def get_currency():
    usd_brl.get_data_usd_brl()
    data_usd_brl = pd.read_sql("SELECT * FROM usd_brl", "sqlite:///usd_brl.db")
    logging.info("USD-BRL created and loaded successfully.")
    print(data_usd_brl)
    return data_usd_brl


if __name__ == "__main__":
    get_currency()
    get_pmi()
