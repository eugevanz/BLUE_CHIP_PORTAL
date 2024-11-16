import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy.orm import Session

from edit_graphs import transaction_performance, account_performance, dividend_performance, investment_performance, \
    client_goal_performance
from utils import engine, Transaction, navbar, profile_data

dash.register_page(__name__, path_template='/add-transaction/<profile_id>/', name='Add Transaction')


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
        html.Div(id='tra-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        html.Div([
            dcc.Location(id='tra-url'),
            dcc.Store(id='profile-id-store', data=profile_id),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Transaction']),
                            html.P(['Adding a transaction involves recording a financial event, typically either a '
                                    'debit (expense) or a credit (income), associated with a client’s account. '],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Select Account', className='uk-text-small'),
                                html.Div([
                                    html.P([
                                        dcc.Dropdown([
                                            {'label': account.account_number, 'value': str(account.id)} for account in
                                            accounts
                                        ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                                    ], className='uk-text-bolder uk-margin-remove-top')
                                ])
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Transaction Type', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': option, 'value': option} for option in ['debit', 'credit']
                                    ], placeholder='Select account type', style={'color': '#172031'}, id='trans_type')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Description', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: info'}),
                                    dcc.Input(
                                        type='text',
                                        placeholder='Transaction Description',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='description'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Transaction Amount', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Transaction Amount',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='amount'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Button('Save', id='add-tra-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    transaction_performance(transactions=transactions, total=transactions_balance,prior=prior_transactions_balance,
                                            order='uk-flex-first@l'),
                    account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance),
                    dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,prior=prior_payouts_balance),
                    investment_performance(investments=investments, total=investments_balance,prior=prior_investments_balance),
                    client_goal_performance(client_goals=client_goals, total=client_goals_balance,prior=prior_client_goals_balance)

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')
            ], className='uk-container')
        ], className='uk-section')
    ])


@callback(
    Output('tra-url', 'href'),
    State('profile-id-store', 'data'),
    State('account_id', 'value'),
    State('trans_type', 'value'),
    State('amount', 'value'),
    State('description', 'value'),
    Input('add-tra-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def add_transaction(profile_id, account_id, trans_type, amount, description, n_clicks):
    with Session(engine) as session:
        if n_clicks and profile_id and account_id and trans_type and amount and description:
            session.add(Transaction(
                account_id=account_id, type=trans_type, amount=amount, description=description
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('tra-nav', 'children'),
    Input('tra-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
