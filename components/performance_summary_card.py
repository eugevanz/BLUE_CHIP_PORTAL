import pandas as pd
import plotly.express as px
from dash import html, dcc
from shortnumbers import millify

from utils import custom_colours, fig_layout, format_currency


def performance_summary(accounts_balance: float, payouts_balance: float, client_goals_balance: float,
                        transactions_balance: float, investments_balance: float, prior_accounts_balance: float,
                        prior_payouts_balance: float, prior_client_goals_balance: float,
                        prior_transactions_balance: float, prior_investments_balance: float,
                        width_class: str = None):
    total = sum([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    prior = sum([
        prior_accounts_balance, prior_payouts_balance, prior_client_goals_balance, prior_transactions_balance,
        prior_investments_balance
    ])

    lowest_ = min([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    highest_ = max([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    mid_ = (highest_ + lowest_) / 2

    # Check for special cases
    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    performance_df = pd.DataFrame({
        'Metric': ['Account Balance', 'Goal Progress', 'Investment Balance', 'Dividends', 'Total Transactions'],
        'Total Value': [accounts_balance, client_goals_balance, investments_balance, payouts_balance,
                        transactions_balance]
    })
    performance_fig = px.bar(
        performance_df, x='Metric', y='Total Value', color='Metric',
        color_discrete_sequence=custom_colours
    )
    performance_fig.update_layout(**fig_layout)

    return html.Div([
        html.Div([
            html.Div([
                html.Div(['Performance Summary'], className='uk-text-small'),
                format_currency(total),
                html.Div([
                    'Compared to last month ',
                    html.Span([
                        html.Span(['+' if total_difference > 0 else '']),
                        f'{total_difference:.2f}', '%'
                    ], className=f'uk-text-{"success" if total_difference > 0 else "danger"} uk-text-bolder')
                ], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {millify(highest_)}']),
                            html.Div([f'R {millify(mid_)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=performance_fig, className='uk-height-medium',
                                  config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(['Over the lifetime of the portfolio'], style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(className='uk-border-circle', style={
                            'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
                        }),
                        html.Div([
                            html.Div([item], className='uk-text-uppercase'),
                            html.Div([f'R {value:,.2f}'], className='uk-text-bolder')
                        ], className='uk-margin-small-left')
                    ], className='uk-flex uk-flex-middle uk-margin-right uk-margin-small-bottom') for i, item, value in
                    [(i, row[0], row[1]) for i, row in enumerate(performance_df.itertuples(index=False, name=None))]
                ], className='uk-flex uk-flex-wrap', style={'fontSize': '11px'})
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]})
    ], className=width_class, id='performance-summary')
