import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, callback

from utils import custom_colours, fig_layout, cur


def transaction_performance(profile_id: str, order: str = None, dark: bool = True):
    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='transactions'),
        html.Div([
            html.Div([
                html.Div('Transactions performance', className='uk-text-small'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='legend', className='uk-flex uk-flex-column uk-height-small',
                                 style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='transact_fig', style={'height': '150px'}, config={'displayModeBar': False})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)


@callback(
    Output('transact_fig', 'figure'),
    Output('legend', 'children'),
    Input('profile_id', 'data')
)
def get_transact_fig(profile_id):
    transactions = cur.execute(
        'SELECT t.* FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE a.profile_id = ?',
        (profile_id,)
    ).fetchall()

    transact_df = pd.DataFrame({
        'Amount': [transaction.amount for transaction in transactions],
        'Type': [transaction.type for transaction in transactions],
    }).groupby('Type')['Amount'].sum().reset_index()
    transact_fig = px.pie(transact_df, values='Amount', names='Type', color='Type', color_discrete_sequence=[
        custom_colours[0], custom_colours[1]
    ])
    transact_fig.update_layout(**fig_layout)

    return transact_fig, [
        html.Div([
            html.Div(className='uk-border-circle', style={
                'backgroundColor': custom_colours[i], 'width': '8px',
                'height': '8px'
            }),
            html.Div([
                html.Div([item[0]], className='uk-text-uppercase'),
                html.Div([f'R {item[1]:,.2f}'], className='uk-text-bolder')
            ], className='uk-margin-small-left')
        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
        enumerate(list(transact_df.itertuples(index=False, name=None)))
    ]
