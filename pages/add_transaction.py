import dash
from dash import dcc, callback, Output, State, Input
from dash.html import Div, Button, P, Span
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, Transaction

dash.register_page(__name__, path_template='/add-transaction/<profile_id>/')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()
    return Div([
        dcc.Location(id='transaction-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        Div([
            Div([
                Div([
                    Div('Select Account', className='uk-text-small'),
                    Div([
                        P([
                            dcc.Dropdown([
                                {'label': account.account_number, 'value': str(account.id)} for account in accounts
                            ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                        ], className='uk-text-bolder uk-margin-remove-top')
                    ])
                ], className='uk-margin'),

                Div([
                    Div('Transaction Type', className='uk-text-small'),
                    Div([
                        dcc.Dropdown([
                            {'label': option, 'value': option} for option in ['debit', 'credit']
                        ], placeholder='Select account type', style={'color': '#172031'}, id='trans_type')
                    ], className='uk-text-bolder uk-margin-remove-top')
                ], className='uk-margin'),

                Div([
                    Div('Description', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: info'}),
                        dcc.Input(
                            type='text',
                            placeholder='Transaction Description',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='description'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Div([
                    Div('Transaction Amount', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                        dcc.Input(
                            type='number',
                            placeholder='Transaction Amount',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='amount'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Button('Save', id='add-tra-btn', className='uk-button uk-button-primary uk-margin')
            ])
        ], className='uk-container')
    ], className='uk-section')


@callback(
    Output('transaction-url', 'href'),
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
