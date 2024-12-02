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
from utils import engine, Account, profile_data

dash.register_page(__name__, path_template='/add-account/<profile_id>/', name='Add Account')


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
        dcc.Location(id='acc-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        navbar([
            ('Admin', f'/admin/{profile_id}/'), (f'Edit Profile ({profile.email})', f'/edit/{profile_id}/'),
            ('Add Account', '')
        ]),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Account']),
                            html.P(['Adding an account involves setting up a record to track financial data specific '
                                    'to a client’s finances. This includes creating a unique account name, '
                                    'like “Savings” or “Investment,” and specifying the type of account, '
                                    'such as “Checking,” “Loan,” or “Retirement.” '],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Account Type', className='uk-text-small'),
                                dcc.Dropdown([
                                    {'label': option, 'value': option} for option in [
                                        'Savings Account', 'Investment Account', 'Retirement Account',
                                        'Brokerage Account', 'Trust Account', 'Custodial Account',
                                        'Taxable Account', 'Tax-Deferred Account', 'Tax-Exempt Account',
                                        'Money Market Account', 'Certificate of Deposit (CD) Account',
                                        'Mutual Fund Account', 'Pension Account',
                                        'Self-Directed Investment Account', 'High-Yield Savings Account',
                                        'Fixed-Income Account', 'Annuity Account', 'Forex Trading Account',
                                        'Commodities Trading Account'
                                    ]], placeholder='Select account type', style={'color': '#172031'},
                                    className='uk-text-bolder uk-margin-remove-top', id='account_type')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Account Number', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: hashtag'}),
                                    dcc.Input(
                                        type='text',
                                        placeholder='Account Number',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='account_number'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Balance', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Balance',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='balance'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Button('Save', id='add-acc-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance,
                                        order='uk-flex-first@l', dark=False),
                    dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,
                                         prior=prior_payouts_balance, dark=False),
                    investment_performance(investments=investments, total=investments_balance,
                                           prior=prior_investments_balance, dark=False),
                    client_goal_performance(client_goals=client_goals, total=client_goals_balance,
                                            prior=prior_client_goals_balance, dark=False),
                    transaction_performance(transactions=transactions, total=transactions_balance,
                                            prior=prior_transactions_balance, dark=False),

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m'),
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer(is_light=False)
    ])


@callback(
    Output('acc-url', 'href'),
    State('profile-id-store', 'data'),
    State('account_type', 'value'),
    State('account_number', 'value'),
    State('balance', 'value'),
    Input('add-acc-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def add_account(profile_id, account_type, account_number, balance, n_clicks):
    with Session(engine) as session:
        if n_clicks and account_type and account_number and balance:
            session.add(Account(
                profile_id=profile_id, account_number=account_number, account_type=account_type, balance=balance
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('acc-nav', 'children'),
    Input('acc-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
