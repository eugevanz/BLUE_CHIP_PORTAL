import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input, callback

from utils import format_time, custom_colours, fig_layout, cur


def dividend_performance(order: str = None, dark: bool = True):
    return html.Div([
        dcc.Store('name', data='dividends_payouts'),
        dcc.Store('profile_id'),
        html.Div([
            html.Div([
                html.Div('Dividend/Payout performance', className='uk-text-small'),
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
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='payouts_fig', style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(id='legend', className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)


@callback(
    Output('payouts_fig', 'figure'),
    Output('legend', 'children'),
    Input('profile_id', 'data')
)
def get_payouts_fig(profile_id):
    dividends_payouts = cur.execute(
        'SELECT dp.* FROM dividends_and_payouts dp JOIN accounts a ON dp.account_id = a.id WHERE a.profile_id = ? '
        'ORDER BY dp.payment_date ASC', (profile_id,)
    ).fetchall()

    if dividends_payouts:
        payment_dates = [row['payment_date'] for row in dividends_payouts]  # Extract payment_date from rows
        oldest_date = payment_dates[0]
        latest_date = payment_dates[-1]
        mid_date = payment_dates[len(payment_dates) // 2]

        payouts_df = pd.DataFrame({
            'Date': [payout.payment_date for payout in dividends_payouts],
            'Amount': [payout.amount for payout in dividends_payouts]
        })
        payouts_df['Date'] = pd.to_datetime(payouts_df['Date'])
        payouts_fig = px.line(payouts_df, x='Date', y='Amount', markers=True, line_shape='spline')
        payouts_fig.update_traces(line=dict(width=8), marker=dict(size=12), line_color=custom_colours[0])
        payouts_fig.update_layout(**fig_layout)

        return payouts_fig, [
            html.Div([format_time(date)]) for date in [oldest_date, mid_date, latest_date] if date
        ]
    else:
        raise dash.exceptions.PreventUpdate
