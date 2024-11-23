from dash import html, dcc

from utils import profile_data, Account, ClientGoal, DividendOrPayout, Investment, Transaction, format_time, \
    sign_out_button


def admin_menu(accounts: [Account], client_goals: [ClientGoal], dividends_and_payouts: [DividendOrPayout],
               investments: [Investment], transactions: [Transaction], profile_id=None):
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
                         src=profile['profile'].profile_picture_url, alt='profile-pic'),
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
                        html.A(['Send an invite'], className='uk-link-reset',
                               **{'data-uk-toggle': 'target: #offcanvas-invite'}),
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
                        html.A(['Audit Logs'], **{'data-uk-toggle': 'target: #offcanvas-audit'},
                               className='uk-link-reset'),
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
