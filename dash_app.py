# dash_app.py
import wbdata as wb
import pandas as pd
import datetime as dt

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("World Bank Data Explorer (wbdata + Dash)"),
    html.Div([
        html.Label("Countries (ISO3, comma-separated)"),
        dcc.Input(id="countries", value="USA,GBR,IND", type="text", style={"width":"100%"}),
    ], style={"marginBottom":"8px"}),
    html.Div([
        html.Label("Indicator code"),
        dcc.Input(id="indicator", value="NY.GDP.PCAP.CD", type="text", style={"width":"100%"}),
    ], style={"marginBottom":"8px"}),
    dcc.RangeSlider(min=1990, max=dt.datetime.today().year, value=[2000, dt.datetime.today().year],
                    id="year_range", marks=None, tooltip={"placement":"bottom","always_visible":True}),
    html.Button("Load data", id="load", n_clicks=0, style={"marginTop":"8px"}),
    dcc.Loading(dcc.Graph(id="graph"), type="cube")
], style={"maxWidth":"900px", "margin":"40px auto", "padding":"12px"})

@app.callback(
    Output("graph", "figure"),
    Input("load", "n_clicks"),
    Input("countries", "value"),
    Input("indicator", "value"),
    Input("year_range", "value"),
    prevent_initial_call=True
)
def update_graph(n, countries, indicator, year_range):
    country_list = [c.strip().upper() for c in countries.split(",") if c.strip()]
    indicator_map = {indicator: "value"}
    start_year, end_year = year_range
    df_raw = wb.get_dataframe(indicator_map, country=country_list, data_date=(dt.datetime(start_year,1,1), dt.datetime(end_year,12,31)), convert_date=True)
    df = df_raw.reset_index().rename(columns={"country":"country","date":"date"}).sort_values(["country","date"])
    if df.empty:
        return px.scatter(title="No data returned — check your inputs.")
    fig = px.line(df, x="date", y="value", color="country", title=f"{indicator}")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
