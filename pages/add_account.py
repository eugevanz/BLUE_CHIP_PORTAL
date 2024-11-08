import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy.orm import Session

from utils import engine, Account, navbar, dividend_performance, account_performance, investment_performance, \
    transaction_performance, \
    client_goal_performance

dash.register_page(__name__, path_template='/add-account/<profile_id>/', name='Add Account')


def layout(profile_id: str):
    return html.Div([
        html.Div(id='acc-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        dcc.Location(id='acc-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
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

                    account_performance('uk-flex-first@l'),
                    dividend_performance(),
                    investment_performance(),
                    client_goal_performance(),
                    transaction_performance()

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m'),
            ], className='uk-container')
        ], className='uk-section')
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
