def plots():
    import datetime

    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    import load_data

    data_pmi = load_data.get_pmi()
    data_usd_brl = load_data.get_currency()

    data_pmi["fluctuation"] = data_pmi["previous"] - data_pmi["actual"]
    data_pmi.drop_duplicates(subset=["date"], inplace=True)

    # _______________________________________________________________________
    data_usd_brl = data_usd_brl.apply(lambda x: x.str.replace(",", "."))

    list_1 = [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
    ]
    list_2 = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    for i, _ in enumerate(list_1):
        data_usd_brl["Data"] = data_usd_brl["Data"].str.replace(list_1[i], list_2[i])

    data_usd_brl["fluctuation"] = data_usd_brl["Ultimo"].astype(float).diff(1)

    data_usd_brl.drop_duplicates(subset=["Data"], inplace=True)

    for i, _ in enumerate(data_usd_brl["Data"]):
        data_usd_brl["Data"][i] = datetime.datetime.strptime(
            data_usd_brl["Data"][i], "%b %y"
        ).strftime("%Y-%m-%d")

    fig = make_subplots(rows=1, cols=2, subplot_titles=("BCI", "Dólar - Real"))

    fig.add_trace(
        go.Waterfall(
            name="20",
            orientation="v",
            measure=["relative"],
            x=data_pmi["date"],
            textposition="outside",
            y=data_pmi["fluctuation"],
            base=data_pmi["actual"].iloc[1],
            increasing={"marker": {"color": "rgb(217, 17, 57)"}},
            decreasing={"marker": {"color": "rgb(7, 181, 117)"}},
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Waterfall(
            name="20",
            orientation="v",
            measure=["relative"],
            x=data_usd_brl["Data"],
            textposition="outside",
            y=data_usd_brl["fluctuation"],
            base=data_usd_brl["Ultimo"].astype(float).iloc[0],
            decreasing={"marker": {"color": "rgb(217, 17, 57)"}},
            increasing={"marker": {"color": "rgb(7, 181, 117)"}},
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        title="Índices Monitorados - PMI e cotação USD",
        title_font_family="Droid Sans Mono",
        title_font_size=20,
        showlegend=False,
    )

    fig.update_xaxes(title_text="Data")
    fig.update_yaxes(
        title_text="Índice de Gerentes de Compras (PMI) da Caixin", col=1, row=1
    )
    fig.update_yaxes(
        title_text="USD/BRL - Dólar Americano - Real Brasileiro", col=2, row=1
    )

    return fig

    # # fig.show()
    # import streamlit as st

    # st.plotly_chart(fig)
