import pandas as pd
import plotly.express as px
from dash import html, dcc
from shortnumbers import millify

from utils import custom_colours, fig_layout, Account


def account_performance(accounts: [Account] = None, total: float = 0, prior: float = 0,
                        order: str = None):
    lowest_account, highest_account, mid_account = 0, 0, 0
    account_fig = None

    if accounts is None:
        accounts = []
    else:
        lowest_account = min(accounts, key=lambda x: x.balance, default=None).balance
        highest_account = max(accounts, key=lambda x: x.balance, default=None).balance
        mid_account = (highest_account + lowest_account) / 2

        accounts_df = pd.DataFrame({
            'Date': [account.created_at for account in accounts],
            'Balance': [account.balance for account in accounts],
            'Type': [account.account_type for account in accounts]
        })
        accounts_df['Date'] = pd.to_datetime(accounts_df['Date'])
        account_fig = px.scatter(
            accounts_df, x="Date", y="Balance", size="Balance", color="Date",
            hover_data={'Date': True, 'Balance': True, 'Type': True}, size_max=60,
            color_discrete_sequence=custom_colours
        )
        account_fig.update_layout(**fig_layout)

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
                html.Div('Accounts performance', className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_account)}']),
                            html.Div([f'R {millify(mid_account)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_account)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=account_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle', style={
                                    'backgroundColor': custom_colours[i], 'width': '8px',
                                    'height': '8px'
                                }),
                                html.Div([account.account_type], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, account in
                            enumerate(accounts)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)