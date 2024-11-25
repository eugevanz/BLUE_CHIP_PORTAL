import pandas as pd
import plotly.express as px
from dash import html, dcc
from shortnumbers import millify

from utils import Investment, fig_layout, custom_colours, format_currency


def investment_performance(investments: [Investment] = None, total: float = 0, prior: float = 0, order: str = None):
    lowest_price_investment, highest_price_investment, mid_price_investment = 0, 0, 0
    investment_fig = None

    if investments is None:
        investments = []
    else:
        lowest_price_investment = min(investments, key=lambda x: x.current_price, default=None).current_price
        highest_price_investment = max(investments, key=lambda x: x.current_price, default=None).current_price
        mid_price_investment = (highest_price_investment + lowest_price_investment) / 2

        investment_data = {
            'Investment': [investment.symbol for investment in investments],  # Use symbol as Investment name
            'Returns': [investment.current_price for investment in investments]  # Or another attribute you wish to plot
        }
        investments_df = pd.DataFrame(investment_data)
        investment_fig = px.bar(investments_df, x='Investment', y='Returns', color='Investment',
                                color_discrete_sequence=custom_colours)
        investment_fig.update_layout(**fig_layout)
    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Investments performance', className='uk-text-small'),
                format_currency(total),
                html.Div(['Compared to last month ', html.Span([
                    html.Span(['+' if total_difference > 0 else '']),
                    f'{total_difference:.2f}', '%'
                ], className=f'uk-text-{"success" if total_difference > 0 else "danger"}')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {millify(highest_price_investment)}']),
                            html.Div([f'R {millify(mid_price_investment)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_price_investment)}'])
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=investment_fig, style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle', style={
                                    'backgroundColor': custom_colours[i], 'width': '8px',
                                    'height': '8px'
                                }),
                                html.Div([item.investment_type], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(investments)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)