from dash import html, dcc

from utils import format_time, create_delete_item, custom_colours, cur


def accounts_table(profile_id: str):
    accounts = cur.execute('SELECT * FROM accounts WHERE profile_id = ?', (profile_id,)).fetchall() or []

    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='accounts'),
        html.Div([
            html.Div([
                html.Span(['Accounts'], className='uk-text-bolder'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('', className=f'uk-table-shrink'),
                                html.Th('Balance', className=f'uk-table-expand'),
                                html.Th('Account Type', className=f'uk-table-expand'),
                                html.Th('Account', className=f'uk-table-expand'),
                                html.Th('Last Update', className=f'uk-table-expand')
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                create_delete_item(type_id='delete_account', item_id=str(account.id)),
                                html.Td(f'R {account.balance:,.2f}'),
                                html.Td(account.account_type, className='uk-text-bolder uk-text-uppercase'),
                                html.Td(account.account_number),
                                html.Td(format_time(account.updated_at), className='uk-text-muted')
                            ]) for account in accounts
                        ]) if accounts else None
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], className='uk-overflow-auto uk-height-large')
            ], className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{
                        'data-uk-icon': 'icon: plus; ratio: 0.6'
                    }, className='uk-margin-small-right'),
                    'Add Account'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'/add-account/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[-1]})
    ], className='uk-width-3-4@m')
