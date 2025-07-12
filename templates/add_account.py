import dash
from dash import dcc, callback, Output, State, Input, html

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.dividend_performance_card import dividend_performance
from components.footer_section import footer
from components.investment_performance_card import investment_performance
from components.navbar import navbar
from components.transaction_performance_card import transaction_performance
from utils import supabase, cur, conn

dash.register_page(__name__, path_template='/add-account/<profile_id>/', name='Add Account')


def layout(profile_id: str):
    profile_response = supabase.table('profiles').select('*').eq('id', profile_id).limit(1).single().execute()
    profile = profile_response.data

    return html.Div([
        dcc.Location(id='acc-url'),
        dcc.Store(id='profile_id'),
        navbar([
            ('Admin', f'/admin/{profile_id}/'), (f'Edit Profile ({profile.email})', f'/edit/{profile.id}/'),
            ('Add Account', '')
        ]),
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

                    account_performance(profile_id=profile_id, order='uk-flex-first@l', dark=False),
                    dividend_performance(profile_id=profile_id, dark=False),
                    investment_performance(profile_id=profile_id, dark=False),
                    client_goal_performance(profile_id=profile_id, dark=False),
                    transaction_performance(profile_id=profile_id, dark=False),

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m'),
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer(is_light=False)
    ])


@callback(
    Output('acc-url', 'href'),
    State('profile-id', 'data'),
    State('account_type', 'value'),
    State('account_number', 'value'),
    State('balance', 'value'),
    Input('add-acc-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def add_account(profile_id, account_type, account_number, balance, n_clicks):
    if n_clicks and account_type and account_number and balance:
        cur.execute(
            'INSERT INTO accounts (profile_id, account_number, account_type, balance) VALUES (?, ?, ?)',
            (profile_id, account_number, account_type, balance)
        )
        conn.commit()
        return f'/edit/{profile_id}/'
    else:
        raise dash.exceptions.PreventUpdate
