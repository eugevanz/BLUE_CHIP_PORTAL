import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input, callback

from utils import custom_colours, fig_layout, cur


def account_performance(profile_id: str, order: str = None, dark: bool = True):
    return html.Div([
        dcc.Store('name', data='accounts'),
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('column', data='balance'),
        html.Div([
            html.Div([
                html.Div('Accounts performance', className='uk-text-small'),
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
                        ], className='uk-flex uk-flex-column uk-height-medium',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='account_fig', style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(['Over the lifetime of the portfolio'], style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div(id='card-footer', className='uk-card-footer')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)


@callback(
    Output('account_fig', 'figure'),
    Output('card-footer', 'children'),
    Input('profile_id', 'data')
)
def get_account_fig(profile_id):
    accounts = cur.execute('SELECT * FROM accounts WHERE profile_id = ?', (profile_id,)).fetchall()

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

    return account_fig, html.Div([
        html.Div([
            html.Div(className='uk-border-circle', style={
                'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
            }),
            html.Div([
                html.Div([account.account_type], className='uk-text-uppercase'),
                html.Div([f'R {account.balance:,.2f}'], className='uk-text-bolder')
            ], className='uk-margin-small-left')
        ], className='uk-flex uk-flex-middle uk-margin-right') for i, account in
        enumerate(accounts)
    ], className='uk-flex uk-flex-wrap', style={'fontSize': '11px'})
