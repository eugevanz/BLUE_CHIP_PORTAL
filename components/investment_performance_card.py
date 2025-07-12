import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input, callback

from utils import fig_layout, custom_colours, cur


def investment_performance(profile_id: str, order: str = None, dark: bool = True):
    return html.Div([
        dcc.Store('name', data='investments'),
        dcc.Store('column', data='current_price'),
        dcc.Store('profile_id', data=profile_id),
        html.Div([
            html.Div([
                html.Div('Investments performance', className='uk-text-small'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div(id='highest_'),
                            html.Div(id='mid_', className='uk-margin-auto-vertical'),
                            html.Div(id='lowest_')
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='investment_fig', style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(id='legend', className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)


@callback(
    Output('investment_fig', 'figure'),
    Output('legend', 'children'),
    Input('profile_id', 'data')
)
def get_investment_fig(profile_id):
    investments = cur.execute(
        'SELECT i.* FROM investments i JOIN accounts a ON i.account_id = a.id WHERE a.profile_id = ?',
        (profile_id,)
    ).fetchall()

    investment_data = {
        'Investment': [investment.symbol for investment in investments],  # Use symbol as Investment name
        'Returns': [investment.current_price for investment in investments]  # Or another attribute you wish to plot
    }
    investments_df = pd.DataFrame(investment_data)
    investment_fig = px.bar(investments_df, x='Investment', y='Returns', color='Investment',
                            color_discrete_sequence=custom_colours)
    investment_fig.update_layout(**fig_layout)

    return investment_fig, [
        html.Div([
            html.Div(className='uk-border-circle', style={
                'backgroundColor': custom_colours[i], 'width': '8px',
                'height': '8px'
            }),
            html.Div([item.investment_type], className='uk-margin-small-left uk-text-small')
        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in enumerate(investments)
    ]
