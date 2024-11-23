from collections import defaultdict

from dash import html, dcc

from utils import Account, create_table_header, create_table_wrapper, table_item_decorator


@table_item_decorator
def clients_table(clients: list, accounts: [Account]):
    account_balances = defaultdict(float)
    for account in accounts:
        account_balances[account.profile_id] += account.balance

    header = create_table_header([
        html.Th(['Client'], className='uk-table-expand'),
        html.Th(['Account Balance'], className='uk-width-auto uk-visible@l'),
        html.Th([''], className='uk-table-shrink')
    ], style={'backgroundColor': '#2A3A58'})

    body = html.Tbody([
        html.Tr([
            html.Td([
                html.Div([
                    html.Div(
                        html.Img(
                            className='uk-border-circle', width='60', height='60',
                            src=client.profile_picture_url or '',
                            alt='profile-pic'
                        ) if client.profile_picture_url else html.Span(
                            **{'data-uk-icon': 'icon: user; ratio: 3;'}),
                        className='uk-width-auto'
                    ),
                    html.Div([
                        html.H3([
                            html.Span(client.first_name or 'First name', className='uk-text-bolder'),
                            html.Span(' '),
                            client.last_name or 'Last name'
                        ], className='uk-card-title uk-margin-remove-bottom', style={'color': 'white'}),
                        html.Div(client.email or 'No email provided', style={'fontSize': '11px'}),
                        html.P([
                            'Last active',
                            html.Span(client.created_at.strftime('%B %d, %Y'),
                                      className='uk-text-default uk-text-bolder uk-margin-small-left')
                        ], className='uk-text-meta uk-margin-remove-top')
                    ], className='uk-width-expand')
                ], className='uk-grid-small uk-flex-middle', **{'data-uk-grid': 'true'})
            ], className='uk-flex uk-flex-middle uk-flex-between'),
            html.Td([
                html.H3([f'R {account_balances[client.id]:,.2f}'.replace(',', ' ')],
                        className='uk-text-bolder uk-text-truncate')
            ], className='uk-visible@l'),
            html.Td([
                html.A(href=f'/edit/{str(client.id)}/', **{'data-uk-icon': 'icon: pencil'}, className='uk-icon-button')
            ])
        ], className='uk-animation-fade') for client in clients
    ]) if clients else None

    return create_table_wrapper(header, body, "No accounts found")


def client_insights(profiles_: list, accounts: [Account], prior_accounts_balance=0, accounts_balance=0):
    if prior_accounts_balance == 0:
        if accounts_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (accounts_balance - prior_accounts_balance) / prior_accounts_balance * 100

    return html.Div([
        dcc.Store(id='selected-profile-id'),
        html.Div([
            html.Div([
                html.Div(['Client Insights'], className='uk-text-small'),
                html.H2([f'R {accounts_balance:,.2f}'.replace(',', ' ')],
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span([
                    html.Span(['+' if total_difference > 0 else '']),
                    f'{total_difference:.2f}'.replace(',', ' '), '%'
                ], className=f'uk-text-{"success" if total_difference > 0 else "danger"}')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Hr(className='uk-margin-remove-bottom', style={'height': '2px', 'background': 'lightgray'}),
                clients_table(profiles_, accounts=accounts),
            ], className='uk-card-body')
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-1-1', id='client-insights')
