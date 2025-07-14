import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout for the front page
app.layout = dbc.Container(
    [
        # Title
        html.H1(
            "Volatility Monitor and Trading Indicators",
            className="text-center my-5",
            style={"fontWeight": "bold", "color": "#2c3e50"},
        ),
        # Button group for navigation
        dbc.Row(
            [
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 1",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page1",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 2",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page2",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 3",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page3",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 4",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page4",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
            ],
            justify="center",
        ),
    ],
    fluid=True,
    className="py-5",
)

# Placeholder routes (to be updated later)
app.clientside_callback(
    """
    function(href) {
        return href;
    }
    """,
    dash.dependencies.Output("page-content", "children"),
    dash.dependencies.Input("url", "pathname"),
)

if __name__ == "__main__":
    app.run(debug=True)