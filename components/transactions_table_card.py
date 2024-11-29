from dash import html

from utils import Transaction, create_delete_item, format_time, format_currency


def transactions_table(transactions: [Transaction], profile_id: str, transactions_balance: float,
                       prior_transactions_balance: float):
    if prior_transactions_balance == 0:
        if transactions_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (transactions_balance - prior_transactions_balance) / prior_transactions_balance * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Span(['Transactions'], className='uk-text-bolder'),
                format_currency(transactions_balance),
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
                        ])
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ])
