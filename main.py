import streamlit as st

import plots_monitor

st.plotly_chart(plots_monitor.plots())
