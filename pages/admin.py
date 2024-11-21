from collections import defaultdict

import dash
from dash import dcc, html, callback, Output, Input, State

from admin_graphs import market_performance, portfolio_performance, asset_performance, performance_summary
from utils import sign_out_button, navbar, create_table_wrapper, table_item_decorator, create_table_header, \
    all_profile_data, format_time, supabase_admin, profile_data

dash.register_page(__name__, path_template='/admin/<profile_id>/', name='Admin')

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


def menu_card(profile_id=None):
    recent_account = max(accounts, key=lambda account: account.updated_at)
    recent_goal = max(client_goals, key=lambda goal: goal.updated_at)
    recent_payout = max(dividends_and_payouts, key=lambda payout: payout.payment_date)
    recent_invest = max(investments, key=lambda invest: invest.updated_at)
    recent_trans = max(transactions, key=lambda trans: trans.created_at)
    profile = profile_data(profile_id)

    return html.Div([
        html.Div([
            html.Div([
                html.Img(className='uk-border-circle uk-margin', width='44', height='44',
                         src=profile['profile'].profile_picture_url,
                         # src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                         # '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp',
                         alt='profile-pic'),
                html.Div(['Administrator'], className='uk-text-small'),
                html.H3([
                    html.Span(profile['profile'].first_name, className='uk-text-bolder'),
                    html.Br(), html.Span([profile['profile'].last_name])
                ], className='uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div([profile['profile'].email or 'email address'], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Ul([
                    html.Li('Support', className='uk-nav-header'),
                    html.Li([
                        html.A([
                            'Send an invite'
                        ], className='uk-link-reset', **{'data-uk-toggle': 'target: #offcanvas-invite'}),
                        html.Div([
                            html.Div([
                                html.H3(['Send an invite'], className='uk-heading-bullet'),
                                html.P('Please enter the recipient\'s email address so we know who you’re sending to.',
                                       className='uk-text-small uk-margin-remove-top'),
                                html.Div('Email', className='uk-text-meta'),
                                html.Div([
                                    html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-form-icon'),
                                    dcc.Input(className='uk-input', type='email', id='form-invite-email')
                                ], className='uk-inline uk-width-1-1'),
                                html.Div([
                                    html.Button([
                                        'Send Invite'
                                    ], style={'backgroundColor': '#88A9C3'},
                                        className='uk-button uk-button-large uk-width-1-1 uk-light',
                                        id='form-invite-button', n_clicks=0),
                                ], className='uk-margin'),
                                html.P(id='invite-notifications', className='uk-margin')
                            ], className='uk-offcanvas-bar')
                        ], id='offcanvas-invite', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    html.Li(html.A([
                        'Client Management'
                    ], href='#client-insights', **{'data-uk-scroll': 'true'}, className='uk-link-reset')),
                    html.Li([
                        html.A([
                            'Audit Logs'
                        ], **{'data-uk-toggle': 'target: #offcanvas-audit'}, className='uk-link-reset'),
                        html.Div([
                            html.Div([
                                html.H3(['Audit Logs'], className='uk-heading-bullet'),
                                html.P(
                                    'Review and analyze system-generated records to monitor user actions, '
                                    'ensure security and compliance, diagnose issues, and maintain operational insights.',
                                    className='uk-text-small uk-margin-remove-top'),
                                html.Div([
                                    html.Table([
                                        html.Caption(['Recent Updates'], className='uk-text-bolder'),
                                        html.Tbody([
                                            html.Tr([
                                                html.Td([recent_account.account_type]),
                                                html.Td([format_time(recent_account.updated_at)]),
                                            ]),
                                            html.Tr([
                                                html.Td(['Goal: ', recent_goal.goal_type]),
                                                html.Td([format_time(recent_goal.updated_at)]),
                                            ]),
                                            html.Tr([
                                                html.Td(['Recent payout']),
                                                html.Td([format_time(recent_payout.payment_date)]),
                                            ]),
                                            html.Tr([
                                                html.Td([recent_invest.investment_type, ' investment']),
                                                html.Td([format_time(recent_invest.updated_at)]),
                                            ]),
                                            html.Tr([
                                                html.Td([recent_trans.type], className='uk-text-uppercase'),
                                                html.Td([format_time(recent_trans.created_at)]),
                                            ])
                                        ]),
                                    ], className='uk-table uk-table-divider')
                                ], className='uk-margin')
                            ], className='uk-offcanvas-bar')
                        ], id='offcanvas-audit', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    sign_out_button()
                ], className='uk-nav uk-nav-default')
            ], className='uk-card-body'),
        ], className='uk-card')
    ], className='uk-width-1-5@m')


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
    ], className='uk-width-1-1', id='client-insights')


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


def layout(profile_id: str):
    return html.Div([
        dcc.Store(id='admin-url'),
        dcc.Store(id='access_token', storage_type='session'),
        html.Div(id='admin-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        dcc.Location(id='admin-url'),
        html.Div([
            html.Div(id='adm-nav',
                     **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
            dcc.Location(id='edit-url'),
            html.Div([
                menu_card(profile_id),
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


@callback(
    Output('invite-notifications', 'children'),
    State('form-invite-email', 'value'),
    Input('form-invite-button', 'n_clicks')
)
def send_invite(email, n_clicks):
    if n_clicks and email:
        try:
            response = supabase_admin.auth.admin.invite_user_by_email(email)
            print(response)
            if response and response.user:
                return html.Span(f'Invite sent to {response.user.email}', className='uk-text-success uk-text-bolder')
            else:
                return html.Span(f'Error sending invite: {response["error"]["message"]}',
                                 className='uk-text-danger uk-text-bolder')
        except Exception as e:
            return html.Span(f'Invitation error: {e}', className='uk-text-danger uk-text-bolder')


@callback(
    Output('admin-url', 'href'),
    Output('access_token', 'data', allow_duplicate=True),
    Input('sign_out', 'n_clicks'),
    prevent_initial_call=True
)
def sign_out(n_clicks):
    if n_clicks:
        return '/', None
