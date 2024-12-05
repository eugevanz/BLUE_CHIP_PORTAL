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
    Account, Investment, Transaction, ClientGoal,
    engine, DividendOrPayout, supabase, cur
)

dash.register_page(__name__, path_template='/edit/<profile_id>/', name='Edit Profile')


def layout(profile_id: str):
    profile_response = supabase.table('profiles').select('*').eq('id', profile_id).limit(1).single().execute()
    profile = profile_response.data

    return html.Div([
        dcc.Location(id='edit-url'),
        dcc.Store('profile-id-store', data=profile_id),
        navbar([('Admin', '/admin/'), (f'Edit Profile ({profile.email})', '')]),
        html.Div([
            html.Div([
                html.Div([
                    client_profile(profile),
                    accounts_table(profile_id),
                    investments_table(profile_id),
                    transactions_table(profile_id),
                    client_goals_table(profile_id),
                    payouts_table(profile_id)
                ], className='uk-child-width-1-2@m uk-padding-small uk-grid-small', **{'data-uk-grid': 'true'})
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer()
    ], className='uk-background-secondary')


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
        cur.execute(f'DELETE FROM {model} WHERE id = ?',(item_id,))
        return f'/edit/{profile_id}/'

    return delete_handler


# Create all delete callbacks
delete_account = create_delete_callback('delete_account')
delete_investment = create_delete_callback('delete_investment')
delete_transaction = create_delete_callback('delete_transaction')
delete_goal = create_delete_callback('delete_goal')
delete_payout = create_delete_callback('delete_payout')
