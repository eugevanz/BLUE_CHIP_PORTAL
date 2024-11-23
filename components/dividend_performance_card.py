import pandas as pd
from dash import html, dcc
from shortnumbers import millify
import plotly.express as px

from utils import format_time, custom_colours, fig_layout, DividendOrPayout


def dividend_performance(dividends_and_payouts: [DividendOrPayout] = None, total: float = 0, prior: float = 0,
                         order: str = None):
    lowest_payout, highest_payout, mid_payout = 0, 0, 0
    oldest_date, latest_date, mid_date = None, None, None
    payouts_fig = None

    if dividends_and_payouts:
        # Calculate payouts
        lowest_payout = min(dividends_and_payouts, key=lambda x: x.amount, default=None).amount
        highest_payout = max(dividends_and_payouts, key=lambda x: x.amount, default=None).amount
        mid_payout = (highest_payout + lowest_payout) / 2

        # Sort by payment_date to find the relevant dates
        sorted_payouts = sorted(dividends_and_payouts, key=lambda x: x.payment_date)
        if sorted_payouts:
            oldest_date = sorted_payouts[0].payment_date
            latest_date = sorted_payouts[-1].payment_date
            mid_date = sorted_payouts[len(sorted_payouts) // 2].payment_date

        payouts_df = pd.DataFrame({
            'Date': [payout.payment_date for payout in dividends_and_payouts],
            'Amount': [payout.amount for payout in dividends_and_payouts]
        })
        payouts_df['Date'] = pd.to_datetime(payouts_df['Date'])
        payouts_fig = px.line(payouts_df, x='Date', y='Amount', markers=True, line_shape='spline')
        payouts_fig.update_traces(line=dict(width=8), marker=dict(size=12), line_color=custom_colours[0])
        payouts_fig.update_layout(**fig_layout)

    # Calculate the percentage difference
    if prior == 0:
        total_difference = float('inf') if total != 0 else 0
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Dividend/Payout performance', className='uk-text-small'),
                html.H2([f'R {total:,.2f}'.replace(',', ' ')],
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
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
                            html.Div([f'R {millify(highest_payout)}']),
                            html.Div([f'R {millify(mid_payout)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_payout)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=payouts_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([format_time(date)]) for date in [oldest_date, mid_date, latest_date] if date
                        ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)