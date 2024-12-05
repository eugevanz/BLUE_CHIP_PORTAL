from dash import html, dcc

from utils import format_time, \
    sign_out_button, cur


def admin_menu():
    recent_account = cur.execute(
        "SELECT * FROM accounts ORDER BY COALESCE(updated_at, '0001-01-01T00:00:00') DESC LIMIT 1;"
    ).fetchone()
    recent_goal = cur.execute(
        "SELECT * FROM client_goals ORDER BY COALESCE(updated_at, '0001-01-01T00:00:00') DESC LIMIT 1;"
    ).fetchone()
    recent_payout = cur.execute(
        "SELECT * FROM dividends_payouts ORDER BY COALESCE(payment_date, '0001-01-01T00:00:00') DESC LIMIT 1;"
    ).fetchone()
    recent_invest = cur.execute(
        "SELECT * FROM investments ORDER BY COALESCE(updated_at, '0001-01-01T00:00:00') DESC LIMIT 1;"
    ).fetchone()
    recent_trans = cur.execute(
        "SELECT * FROM transactions ORDER BY COALESCE(created_at, '0001-01-01T00:00:00') DESC LIMIT 1;"
    ).fetchone()

    return html.Div([
        dcc.Store(id='profile-store'),
        html.Div([
            html.Div([
                html.Img(className='uk-border-circle uk-margin', width='44', height='44',
                         id='profile-picture-url', alt='profile-pic'),
                html.Div(['Administrator'], className='uk-text-small'),
                html.H3([
                    html.Span(id='first-name', className='uk-text-bolder'),
                    html.Br(), html.Span(id='last-name')
                ], className='uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(id='email', className='uk-text-small uk-margin-remove-top')
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
                                            ]) if recent_account else None,
                                            html.Tr([
                                                html.Td(['Goal: ', recent_goal.goal_type]),
                                                html.Td([format_time(recent_goal.updated_at)]),
                                            ]) if recent_goal else None,
                                            html.Tr([
                                                html.Td(['Recent payout']),
                                                html.Td([format_time(recent_payout.payment_date)]),
                                            ]) if recent_payout else None,
                                            html.Tr([
                                                html.Td([recent_invest.investment_type, ' investment']),
                                                html.Td([format_time(recent_invest.updated_at)]),
                                            ]) if recent_invest else None,
                                            html.Tr([
                                                html.Td([recent_trans.type], className='uk-text-uppercase'),
                                                html.Td([format_time(recent_trans.created_at)]),
                                            ]) if recent_trans else None
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
