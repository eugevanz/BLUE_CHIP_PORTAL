from collections import defaultdict

import dash
from dash import dcc, html, callback, Output, Input

from admin_graphs import market_performance, portfolio_performance, asset_performance, performance_summary
from utils import sign_out_button, navbar, create_table_wrapper, table_item_decorator, create_table_header, \
    all_profile_data

dash.register_page(__name__, path='/admin/', name='Admin')

data = all_profile_data()
profiles = data['profiles']
accounts = data['accounts']
accounts_balance = data['accounts_balance']
prior_accounts_balance = data['prior_accounts_balance']
dividends_and_payouts = data['dividends_and_payouts']
payouts_balance = data['payouts_balance']
prior_payouts_balance = data['prior_payouts_balance']
client_goals = data['client_goals']
client_goals_balance = data['client_goals_balance']
prior_client_goals_balance = data['prior_client_goals_balance']
transactions = data['transactions']
transactions_balance = data['transactions_balance']
prior_transactions_balance = data['prior_transactions_balance']
investments = data['investments']
investments_balance = data['investments_balance']
prior_investments_balance = data['prior_investments_balance']


def menu_card():
    return html.Div([
        html.Div([
            html.Div([
                html.Img(className='uk-border-circle uk-margin', width='44', height='44',
                         src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                             '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp',
                         alt='profile-pic'),
                html.Div(['Administrator'], className='uk-text-small'),
                html.H3([html.Span('First name', className='uk-text-bolder'), ' Last name'],
                        className='uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['username@email.com'], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Ul([
                    # html.Li('Menu', className='uk-nav-header', style={'color': 'white'}),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: home'}, className='uk-margin-small-right'), 'Dashboard'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: credit-card'}, className='uk-margin-small-right'), 'Transactions'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: star'}, className='uk-margin-small-right'), 'My Goals'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: nut'}, className='uk-margin-small-right'), 'Investment'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: file-text'}, className='uk-margin-small-right'), 'Bills and Payment'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(html.A([
                    #     html.Span(**{'data-uk-icon': 'icon: settings'}, className='uk-margin-small-right'),
                    #     'Analytics and Reports'
                    # ], className='uk-flex uk-flex-middle')),
                    # html.Li(className='uk-nav-divider uk-margin'),

                    html.Li('Support', className='uk-nav-header'),
                    html.Li([
                        html.A([
                            html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right'),
                            'Send an invite'
                        ], className='uk-flex uk-flex-middle'),
                        html.Div([
                            html.H3('Send an invite', className='uk-card-title uk-margin-remove-bottom'),
                            html.P('Please enter the recipient\'s email address so we know who you’re sending to.',
                                   className='uk-text-small uk-margin-remove-top'),
                            html.Div([
                                html.Label('Email', className='uk-form-label'),
                                html.Div([
                                    html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-form-icon'),
                                    dcc.Input(className='uk-input uk-form-blank', type='email', name='form-invite-name')
                                ], className='uk-inline')
                            ], className='uk-margin', style={'color': '#88A9C3'}),
                            html.Div(
                                html.Button("Send Invite",
                                            className='uk-button uk-button-large uk-width-1-1 uk-light',
                                            style={'backgroundColor': '#091235'}),
                                className='uk-margin'
                            ),
                            html.P(id='invite-notifications', className='uk-margin')
                        ], className='uk-card uk-card-body uk-card-default', **{'data-uk-drop': 'true'})
                    ], className='uk-inline'),
                    html.Li(html.A('Client Management')),
                    html.Li(html.A('Audit Logs')),
                    html.Li(html.A('Investment Reporting')),
                    html.Li(html.A('Admin Support Hub')),
                    sign_out_button()
                ], className='uk-nav uk-nav-default')
            ], className='uk-card-body'),
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ])


@table_item_decorator
def clients_table(clients: list):
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


def client_insights_card(profiles_: list):
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
                clients_table(profiles_),
            ], className='uk-card-body')
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-1-1')


# @callback(
#     Output('selected-profile-id', 'data'),
#     State({'type': 'client-insights-id', 'index': MATCH}, 'id'),
#     Input({'type': 'client-insights-id', 'index': MATCH}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def get_profile_id(profile_id, n_clicks):
#     if n_clicks: return profile_id
#
#
# @callback(
#     Output('url', 'pathname', allow_duplicate=True),
#     Input('selected-profile-id', 'data'),
#     prevent_initial_call=True
# )
# def goto_edit(profile_id):
#     # print(dash.page_registry['pages.edit_client']['path'])
#     if profile_id: return f'/edit/{profile_id}/'


def layout():
    return html.Div([
        html.Div(id='admin-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        dcc.Location(id='admin-url'),
        html.Div([
            html.Div(id='adm-nav',
                     **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
            dcc.Location(id='edit-url'),
            html.Div([
                html.Div(menu_card()),
                market_performance(),
                # html.Div(overview_card()),
                portfolio_performance(),
                asset_performance(),
                performance_summary(accounts_balance, payouts_balance, client_goals_balance, transactions_balance,
                                    investments_balance, prior_accounts_balance, prior_payouts_balance,
                                    prior_client_goals_balance, prior_transactions_balance, prior_investments_balance),
                client_insights_card(profiles_=profiles)
            ], **{'data-uk-grid': 'true'},
                className='uk-padding uk-child-width-1-4@m uk-grid-small uk-grid-match')
        ], style={'backgroundColor': '#88A9C3'})
    ])


@callback(
    Output('admin-nav', 'children'),
    Input('admin-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
