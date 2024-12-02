from datetime import date

import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy.orm import Session

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.dividend_performance_card import dividend_performance
from components.footer_section import footer
from components.investment_performance_card import investment_performance
from components.navbar import navbar
from components.transaction_performance_card import transaction_performance
from utils import ClientGoal, engine, profile_data

dash.register_page(__name__, path_template='/add-client-goal/<profile_id>/', name='Add Client Goal')


def layout(profile_id: str):
    data = profile_data(profile_id)
    profile = data['profile']
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

    return html.Div([
        dcc.Location(id='goal-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        navbar([
            ('Admin', f'/admin/{profile_id}/'), (f'Edit Profile ({profile.email})', f'/edit/{profile_id}/'),
            ('Add Client Goal', '')
        ]),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Client Goal']),
                            html.P(['Adding client goals involves setting up specific, measurable objectives tailored '
                                    'to each client’s financial plan. This process typically includes defining the '
                                    'goal (e.g., saving a certain amount by a target date), establishing milestones, '
                                    'and tracking progress over time. Visual representations, such as progress bars '
                                    'or gauge charts, are often used to display these goals within a dashboard, '
                                    'making it easy for both the client and advisor to monitor achievement levels. '],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Target Date', className='uk-text-small'),
                                dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                     id='target_date', date=date.today())
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Goal', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': option, 'value': option} for option in [
                                            'Retirement Savings', 'Emergency Fund', 'Education Fund', 'Home Purchase',
                                            'Debt Reduction', 'Vacation Fund', 'Investment Growth', 'Business Start-Up',
                                            'Charitable Giving', 'Wealth Accumulation', 'Major Purchase',
                                            'Health and Wellness', 'Estate Planning', 'Early Retirement',
                                            'Legacy Planning'
                                        ]
                                    ], placeholder='Select account type', style={'color': '#172031'}, id='goal_type')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),  # Field for goal type

                            html.Div([
                                html.Div('Current Savings', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Current Savings',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='current_savings'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Target Amount', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Target Amount',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='target_amount'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Button('Save', id='add-goa-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    client_goal_performance(client_goals=client_goals, total=client_goals_balance,
                                            prior=prior_client_goals_balance, order='uk-flex-first@l', dark=False),
                    account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance,
                                        dark=False),
                    dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,
                                         prior=prior_payouts_balance, dark=False),
                    investment_performance(investments=investments, total=investments_balance,
                                           prior=prior_investments_balance, dark=False),
                    transaction_performance(transactions=transactions, total=transactions_balance,
                                            prior=prior_transactions_balance, dark=False)

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer(is_light=False)
    ])


@callback(
    Output('goal-url', 'href'),
    State('profile-id-store', 'data'),
    State('goal_type', 'value'),
    State('current_savings', 'value'),
    State('target_amount', 'value'),
    Input('target_date', 'date'),
    Input('add-goa-btn', 'n_clicks')
)
def add_client_goal(profile_id, goal_type, current_savings, target_amount, target_date, n_clicks):
    with Session(engine) as session:
        if n_clicks and goal_type and current_savings and target_amount and target_date:
            session.add(ClientGoal(
                current_savings=current_savings, goal_type=goal_type, profile_id=profile_id,
                target_amount=target_amount, target_date=target_date
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('goal-nav', 'children'),
    Input('goal-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
