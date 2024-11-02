from datetime import date

import dash
from dash import dcc, callback, Output, State, Input
from dash.html import Div, Span, Button
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, DividendOrPayout

dash.register_page(__name__, path_template='/add-payout/<profile_id>/')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()

    return Div([
        dcc.Location(id='payout-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        Div([
            Div([
                Div('Account', className='uk-text-small'),
                Div([
                    dcc.Dropdown([
                        {'label': account.account_number, 'value': str(account.id)} for account in accounts
                    ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                ], className='uk-text-bolder uk-margin-remove-top')
            ], className='uk-margin'),

            Div([
                Div('Payout Date', className='uk-text-small'),
                Div([
                    Span(className='uk-form-icon', **{'data-uk-icon': 'icon: calendar'}),
                    dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                         id='payment_date', date=date.today())
                ], className='uk-margin-remove-top uk-inline')
            ], className='uk-margin'),

            Div([
                Div('Amount', className='uk-text-small'),
                dcc.Input(
                    type='number',
                    placeholder='Amount',
                    className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                    id='amount'
                )
            ], className='uk-margin'),

            Button('Save', id='add-pay-btn', className='uk-button uk-button-primary uk-margin')

        ], className='uk-container')
    ], className='uk-section')


@callback(
    Output('payout-url', 'href'),
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
