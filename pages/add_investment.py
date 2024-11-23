from datetime import date

import dash
from dash import dcc, callback, Output, Input, State, html
from sqlalchemy.orm import Session

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.dividend_performance_card import dividend_performance
from components.investment_performance_card import investment_performance
from components.navbar import navbar
from components.transaction_performance_card import transaction_performance
from utils import engine, Investment, profile_data

dash.register_page(__name__, path_template='/add-investment/<profile_id>/', name='Add Investment')


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
                html.Div([f'Add Investment / {profile.email}'])
            ], className='uk-grid-large uk-flex-bottom uk-padding-small', **{'data-uk-grid': 'true'})
        ], className='uk-card uk-card-body'),
        html.Div([
            dcc.Location(id='inv-url'),
            dcc.Store(id='profile-id-store', data=profile_id),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Investment']),
                            html.P(['Adding an investment involves recording a financial asset or contribution '
                                    'intended for growth, typically with specific goals or performance expectations.'],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Investment Start Date', className='uk-text-small'),
                                dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                     id='purchase_date', date=date.today())
                            ], className='uk-margin'),
                            html.Div([
                                html.Div('Select Account', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': account.account_number, 'value': str(account.id)} for account in
                                        accounts
                                    ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin') if accounts else None,
                            html.Div([
                                html.Div('Investment Type', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': option, 'value': option} for option in [
                                            'Stocks (Equities)', 'Bonds (Fixed Income)', 'Mutual Funds',
                                            'Exchange-Traded Funds (ETFs)',
                                            'Real Estate', 'Commodities', 'Cryptocurrency', 'Private Equity',
                                            'Hedge Funds',
                                            'Savings Accounts & Certificates of Deposit (CDs)', 'Annuities', 'Options'
                                        ]
                                    ], placeholder='Select account type', style={'color': '#172031'},
                                        id='investment_type')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),
                            html.Div([
                                # Symbol (Required)
                                html.Div('Symbol', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: symbol'}),
                                    dcc.Input(
                                        type='text',
                                        placeholder='Symbol',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='symbol'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),
                            html.Div([
                                # Investment Amount (Quantity) (Required)
                                html.Div('Investment Amount (Quantity)', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: cart'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Investment Amount',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='quantity'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),
                            html.Div([
                                # Investment Purchase Price (Required)
                                html.Div('Investment Purchase Price', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Investment Purchase Price',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='purchase_price'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),
                            html.Div([
                                # Current Price (Required)
                                html.Div('Current Price', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Current Price',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='current_price'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Button('Save', id='add-inv-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    investment_performance(investments=investments, total=investments_balance,
                                           prior=prior_investments_balance,
                                           order='uk-flex-first@l'),
                    account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance),
                    dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,
                                         prior=prior_payouts_balance),
                    client_goal_performance(client_goals=client_goals, total=client_goals_balance,
                                            prior=prior_client_goals_balance),
                    transaction_performance(transactions=transactions, total=transactions_balance,
                                            prior=prior_transactions_balance)

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')

            ], className='uk-container')
        ], className='uk-section')
    ])


@callback(
    Output('inv-url', 'href'),
    State('profile-id-store', 'data'),
    State('account_id', 'value'),
    State('investment_type', 'value'),
    State('symbol', 'value'),
    State('quantity', 'value'),
    State('purchase_price', 'value'),
    State('current_price', 'value'),
    Input('purchase_date', 'date'),
    Input('add-inv-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def add_investment(profile_id, account_id, investment_type, symbol, quantity, purchase_price, current_price,
                   purchase_date, n_clicks):
    with Session(engine) as session:
        if (n_clicks and account_id and investment_type and symbol and quantity and purchase_price and current_price
                and purchase_date):
            session.add(Investment(
                account_id=account_id, investment_type=investment_type, symbol=symbol, quantity=quantity,
                purchase_price=purchase_price, current_price=current_price, purchase_date=purchase_date
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('inv-nav', 'children'),
    Input('inv-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
