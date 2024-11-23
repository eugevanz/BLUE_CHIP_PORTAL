from datetime import date

import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy.orm import Session

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.dividend_performance_card import dividend_performance
from components.investment_performance_card import investment_performance
from components.navbar import navbar
from components.transaction_performance_card import transaction_performance
from utils import engine, DividendOrPayout, profile_data

dash.register_page(__name__, path_template='/add-payout/<profile_id>/', name='Add Dividend/Payout')


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
        html.Div([
            html.Div([
                html.Div([
                    html.Img(
                        src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                            '/Blue%20Chip%20Invest%20Logo.001.png',
                        width='60', height='60'),
                    html.Div(['BLUE CHIP INVESTMENTS'],
                             style={'fontFamily': '"Noto Sans", sans-serif', 'fontOpticalSizing': 'auto',
                                    'fontWeight': '400', 'fontStyle': 'normal', 'lineHeight': '22px',
                                    'color': '#091235', 'width': '164px'})
                ], className='uk-logo uk-flex'),
                html.Div([f'Add Dividend/Payout / {profile.email}'])
            ], className='uk-grid-large uk-flex-bottom uk-padding-small', **{'data-uk-grid': 'true'})
        ], className='uk-card uk-card-body'),
        html.Div([
            dcc.Location(id='pay-url'),
            dcc.Store(id='profile-id-store', data=profile_id),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Dividend/Payout']),
                            html.P(['Adding a dividend or payout typically involves recording a financial transaction '
                                    'associated with an investment account to document income received from holdings, '
                                    'like stocks or funds, that distribute earnings to account holders.'],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Payout Date', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': 'icon: calendar'}),
                                    dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                         id='payment_date', date=date.today())
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Account', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': account.account_number, 'value': str(account.id)} for account in
                                        accounts
                                    ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Amount', className='uk-text-small'),
                                dcc.Input(
                                    type='number',
                                    placeholder='Amount',
                                    className='uk-input uk-text-bolder uk-width-1-1',
                                    id='amount'
                                )
                            ], className='uk-margin'),

                            html.Button('Save', id='add-pay-btn', n_clicks=0,
                                        className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,
                                         prior=prior_payouts_balance,
                                         order='uk-flex-first@l'),
                    account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance),
                    investment_performance(investments=investments, total=investments_balance,
                                           prior=prior_investments_balance),
                    client_goal_performance(client_goals=client_goals, total=client_goals_balance,
                                            prior=prior_client_goals_balance),
                    transaction_performance(transactions=transactions, total=transactions_balance,
                                            prior=prior_transactions_balance)

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')
            ], className='uk-container')
        ], className='uk-section')
    ])


@callback(
    Output('pay-url', 'href'),
    State('profile-id-store', 'data'),
    State('account_id', 'value'),
    Input('payment_date', 'date'),
    State('amount', 'value'),
    Input('add-pay-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def post(profile_id, account_id, payment_date, amount, n_clicks):
    with Session(engine) as session:
        if n_clicks and account_id and payment_date and amount:
            session.add(DividendOrPayout(
                account_id=account_id, amount=amount, payment_date=payment_date
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('pay-nav', 'children'),
    Input('pay-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
