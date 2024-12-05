from dash import html, dcc

from utils import create_delete_item, format_time, custom_colours, cur


def transactions_table(profile_id: str):
    transactions = cur.execute(
        'SELECT t.* FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE a.profile_id = ?', (profile_id,)
    ).fetchall() or []

    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='transactions'),
        html.Div([
            html.Div([
                html.Span(['Transactions'], className='uk-text-bolder'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('', className=f'uk-table-shrink'),
                                html.Th('Description', className=f'uk-table-expand'),
                                html.Th('Transaction Type', className=f'uk-table-expand'),
                                html.Th('Amount', className=f'uk-table-expand'),
                                html.Th('Last Updated', className=f'uk-table-expand')
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                create_delete_item(type_id='delete_transaction', item_id=str(transaction.id)),
                                html.Td(transaction.description),
                                html.Td(transaction.type,
                                        className=f'uk-text-{"success" if transaction.type == "debit" else "danger"}'),
                                html.Td(f'R {transaction.amount:,.2f}'),
                                html.Td(format_time(transaction.created_at))
                            ]) for transaction in transactions
                        ]) if transactions else None
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], className='uk-overflow-auto uk-height-large')
            ], className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{'data-uk-icon': 'icon: plus; ratio: 0.6'}, className='uk-margin-small-right'),
                    'Add transaction'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'/add-transaction/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[-1]})
    ])
