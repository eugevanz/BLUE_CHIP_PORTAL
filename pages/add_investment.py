from datetime import date

import dash
from dash import dcc, callback, Output, Input, State, html
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, Investment, navbar, investment_performance, account_performance, \
    dividend_performance, client_goal_performance, \
    transaction_performance

dash.register_page(__name__, path_template='/add-investment/<profile_id>/', name='Add Investment')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()

    return html.Div([
        html.Div(id='inv-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
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
                            html.Div([
                                html.Div('Investment Start Date', className='uk-text-small'),
                                dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                     id='purchase_date', date=date.today())
                            ], className='uk-margin'),

                            html.Button('Save', id='add-inv-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    investment_performance('uk-flex-first@l'),
                    account_performance(),
                    dividend_performance(),
                    client_goal_performance(),
                    transaction_performance()

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
