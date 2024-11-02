import dash
from dash import dcc, callback, Output, State, Input
from dash.html import Div, Form, Span, Button
from sqlalchemy.orm import Session

from utils import engine, Account

dash.register_page(__name__, path_template='/add-account/<profile_id>/')


def layout(profile_id: str):
    return Div([
        dcc.Location(id='account-url'),
        Div(
            Form([
                Div([
                    Div('Account Type', className='uk-text-small'),
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

                Div([
                    Div('Account Number', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: hashtag'}),
                        dcc.Input(
                            type='text',
                            placeholder='Account Number',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='account_number'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Div([
                    Div('Balance', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                        dcc.Input(
                            type='number',
                            placeholder='Balance',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='balance'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Button('Save', id='add-acc-btn', className='uk-button uk-button-primary uk-margin')
            ]),
            className='uk-container'
        )
    ], className='uk-section')


@callback(
    Output('account-url', 'href'),
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
