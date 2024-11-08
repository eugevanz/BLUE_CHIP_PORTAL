import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, Transaction, navbar, transaction_performance, account_performance, \
    dividend_performance, investment_performance, \
    client_goal_performance

dash.register_page(__name__, path_template='/add-transaction/<profile_id>/', name='Add Transaction')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()

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

                    transaction_performance('uk-flex-first@l'),
                    account_performance(),
                    dividend_performance(),
                    investment_performance(),
                    client_goal_performance(),

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
