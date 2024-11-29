from dash import html

from utils import Account, format_time, create_delete_item, format_currency


def accounts_table(accounts: [Account], profile_id: str, accounts_balance: float, prior_accounts_balance: float):
    if prior_accounts_balance == 0:
        if accounts_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (accounts_balance - prior_accounts_balance) / prior_accounts_balance * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Span(['Accounts'], className='uk-text-bolder'),
                format_currency(accounts_balance),
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-3-4@m')
