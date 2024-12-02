import base64
from typing import Dict, Type

import dash
from dash import dcc, Output, callback, Input, State, html, ALL
from dash.exceptions import PreventUpdate
from sqlalchemy.orm import Session

from components.accounts_table_card import accounts_table
from components.client_goals_table_card import client_goals_table
from components.client_profile_card import client_profile
from components.footer_section import footer
from components.investments_table_card import investments_table
from components.navbar import navbar
from components.payouts_table_card import payouts_table
from components.transactions_table_card import transactions_table
from utils import (
    Profile, Account, Investment, Transaction, ClientGoal,
    engine, DividendOrPayout, supabase_admin, profile_data
)

dash.register_page(__name__, path_template='/edit/<profile_id>/', name='Edit Profile')


def layout(profile_id: str):
    """Creates the layout for a client's profile page."""
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
        dcc.Location(id='edit-url'),
        dcc.Store('profile-id-store', data=profile_id),
        navbar([('Admin', f'/admin/{profile_id}/'), (f'Edit Profile ({profile.email})', '')]),
        html.Div([
            html.Div([
                html.Div([
                    client_profile(profile),
                    accounts_table(accounts, profile_id, accounts_balance, prior_accounts_balance),
                    investments_table(investments, profile_id, investments_balance, prior_investments_balance),
                    transactions_table(transactions, profile_id, transactions_balance, prior_transactions_balance),
                    client_goals_table(client_goals, profile_id, client_goals_balance, prior_client_goals_balance),
                    payouts_table(dividends_and_payouts, profile_id, payouts_balance, prior_payouts_balance)
                ], className='uk-child-width-1-2@m uk-padding-small uk-grid-small', **{'data-uk-grid': 'true'})
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer()
    ], className='uk-background-secondary')


@callback(
    Output('profile_pic', 'src'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('profile-id-store', 'data'),
    State('profile-pic-store', 'data'),
    prevent_initial_callback=True
)
def update_profile_pic(contents, filename, profile_id, profile_pic):
    if not contents: return profile_pic

    # MAX_FILE_SIZE = 5 * 1024 * 1024
    content_type, content_string = contents.split(',')
    if not content_type.startswith('data:image/'): return profile_pic

    try:
        data = base64.b64decode(content_string)
        response = supabase_admin.storage.from_('profile_pics').upload(
            filename,
            data,
            file_options={'content-type': content_type, 'upsert': 'true'}
        )

        if response:
            public_url = supabase_admin.storage.from_('profile_pics').get_public_url(filename)
            with Session(engine) as session:
                profile = session.query(Profile).filter_by(id=profile_id).first()
                if profile:
                    profile.profile_picture_url = public_url
                    session.commit()
                    return public_url
    except Exception as e:
        print(f"Error updating profile picture: {e}")

    return profile_pic


@callback(
    State('profile-id-store', 'data'),
    Input('first_name', 'value'),
    Input('last_name', 'value')
)
def update_name(profile_id, first_name, last_name):
    if not any([first_name, last_name]):
        raise PreventUpdate

    with Session(engine) as session:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if first_name is not None:
            profile.first_name = first_name
        if last_name is not None:
            profile.last_name = last_name
        session.commit()


@callback(
    Output('edit-nav', 'children'),
    Input('edit-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)


# Model mapping dictionary
MODEL_MAPPING: Dict[str, Type[Account | Investment | Transaction | ClientGoal | DividendOrPayout]] = {
    'delete_account': Account,
    'delete_investment': Investment,
    'delete_transaction': Transaction,
    'delete_goal': ClientGoal,
    'delete_payout': DividendOrPayout
}


def create_delete_callback(delete_type: str):
    """
    Factory function to create delete callbacks for different models.

    Args:
        delete_type (str): The type of delete operation (e.g., 'delete_account')
    """
    model = MODEL_MAPPING[delete_type]

    @callback(
        Output('edit-url', 'href', allow_duplicate=True),
        Input({'type': delete_type, 'index': ALL}, 'n_clicks'),
        State({'type': delete_type, 'index': ALL}, 'id'),
        State('profile-id-store', 'data'),
        prevent_initial_call=True
    )
    def delete_handler(n_clicks, ids, profile_id):
        if not n_clicks or not any(n_clicks):
            raise PreventUpdate

        clicked_index = next((i for i, clicks in enumerate(n_clicks) if clicks), None)
        if clicked_index is None:
            raise PreventUpdate

        item_id = ids[clicked_index]['index']
        with Session(engine) as session:
            session.delete(session.query(model).filter_by(id=item_id).first())
            session.commit()
            return f'/edit/{profile_id}/'

    return delete_handler


# Create all delete callbacks
delete_account = create_delete_callback('delete_account')
delete_investment = create_delete_callback('delete_investment')
delete_transaction = create_delete_callback('delete_transaction')
delete_goal = create_delete_callback('delete_goal')
delete_payout = create_delete_callback('delete_payout')
