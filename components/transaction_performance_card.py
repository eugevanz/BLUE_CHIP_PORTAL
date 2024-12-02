import pandas as pd
import plotly.express as px
from dash import html, dcc

from utils import Transaction, custom_colours, fig_layout, format_currency


def transaction_performance(transactions: [Transaction] = None, total: float = 0, prior: float = 0, order: str =
None, dark: bool = True):
    transact_fig, transact_df = None, None

    if transactions:
        transact_df = pd.DataFrame({
            'Amount': [transaction.amount for transaction in transactions],
            'Type': [transaction.type for transaction in transactions],
        }).groupby('Type')['Amount'].sum().reset_index()
        transact_fig = px.pie(transact_df, values='Amount', names='Type', color='Type', color_discrete_sequence=[
            custom_colours[0], custom_colours[1]
        ])
        transact_fig.update_layout(**fig_layout)

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
                html.Div('Transactions performance', className='uk-text-small'),
                format_currency(total),
                html.Div(['Compared to last month ', html.Span([
                    html.Span(['+' if total_difference > 0 else '']),
                    f'{total_difference:.2f}', '%'
                ], className=f'uk-text-{"success" if total_difference > 0 else "danger"} uk-text-bolder')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
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
                        ], className='uk-flex uk-flex-column uk-height-small', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=transact_fig, style={'height': '150px'}, config={'displayModeBar': False})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)
