import os
from datetime import date

import pandas as pd
import streamlit as st

import plots_monitor as plots_monitor

plots = plots_monitor.plots()

data_usd_brl = pd.read_sql("SELECT * FROM usd_brl", "sqlite:///usd_brl.db")
data_pmi = pd.read_sql("SELECT * FROM pmi", "sqlite:///pmi.db")


def get_msg(text: str):
    import dotenv
    import requests

    dotenv.load_dotenv()

    token = os.environ.get("token")
    userID = "2078337734"
    message = text

    # Create url
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Create json link with message
    data = {"chat_id": userID, "text": message, "document": "attach://file"}
    file = {"file": open("plots.html", "rb")}

    # POST the message
    requests.post(url, data, files=file)


dolar_actual = float(data_usd_brl["Ultimo"][0].replace(",", "."))

if dolar_actual < 4.5:
    get_msg(
        f"""{date.today()}: Notificação de índices:
Dólar menor que 4,5: valor atual U${dolar_actual}"""
    )
if data_pmi["actual"][1] < 50:
    get_msg(
        f"""{date.today()}: Notificação de índices:
PMI menor que 50%: valor atual {data_pmi["actual"][1]}%"""
    )


st.plotly_chart(plots)
