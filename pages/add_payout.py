from datetime import date

import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, DividendOrPayout, navbar, dividend_performance, account_performance, \
    investment_performance, \
    client_goal_performance, transaction_performance

dash.register_page(__name__, path_template='/add-payout/<profile_id>/', name='Add Dividend/Payout')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()

    return html.Div([
        html.Div(id='pay-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
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
                                html.Div('Account', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': account.account_number, 'value': str(account.id)} for account in
                                        accounts
                                    ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Payout Date', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': 'icon: calendar'}),
                                    dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                         id='payment_date', date=date.today())
                                ], className='uk-margin-remove-top uk-inline')
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

                    dividend_performance('uk-flex-first@l'),
                    account_performance(),
                    investment_performance(),
                    client_goal_performance(),
                    transaction_performance()

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
