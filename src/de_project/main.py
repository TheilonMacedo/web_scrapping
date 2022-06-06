import os
from datetime import date

import pandas as pd
import streamlit as st

import plots_monitor as plots_monitor

st.plotly_chart(plots_monitor.plots())

data_usd_brl = pd.read_sql("SELECT * FROM usd_brl", "sqlite:///usd_brl.db")
data_pmi = pd.read_sql("SELECT * FROM pmi", "sqlite:///pmi.db")


def get_msg(text: str):
    import dotenv
    import requests

    dotenv.load_dotenv()

    token = os.getenv("token")
    userID = "2078337734"
    message = text

    # Create url
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Create json link with message
    data = {"chat_id": userID, "text": message}

    # POST the message
    requests.post(url, data)


dolar_actual = float(data_usd_brl["Ultimo"][0].replace(",", "."))

if dolar_actual < 4.5:
    get_msg(
        f"""{date.today()}: Investment notification:
Dolar lower than 4,5: this month value U${dolar_actual}"""
    )
if data_pmi["actual"][1] < 50:
    get_msg(
        f"""{date.today()}: Investment notification:
PMI lower than 50%: this month value {data_pmi["actual"][1]}%"""
    )
