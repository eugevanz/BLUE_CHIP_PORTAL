import dash
from dash import html, callback, Output, Input, State

from components.admin_menu_card import admin_menu
from components.asset_performance_card import asset_performance
from components.client_insights_card import client_insights
from components.market_performance_card import market_performance
from components.navbar import navbar
from components.performance_summary_card import performance_summary
from components.portfolio_performance_card import portfolio_performance
from utils import all_profile_data, supabase_admin

dash.register_page(__name__, path_template='/admin/<profile_id>/', name='Admin')

data = all_profile_data()
profiles = data['profiles']
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


def layout(profile_id: str):
    return html.Div([
        navbar([('Admin', f'/admin/{profile_id}/')]),

        html.Div([
            html.Div([
                html.Div([
                    admin_menu(profile_id=profile_id, accounts=accounts, client_goals=client_goals,
                               dividends_and_payouts=dividends_and_payouts, investments=investments,
                               transactions=transactions),
                    market_performance(),
                    performance_summary(accounts_balance, payouts_balance, client_goals_balance, transactions_balance,
                                        investments_balance, prior_accounts_balance, prior_payouts_balance,
                                        prior_client_goals_balance, prior_transactions_balance,
                                        prior_investments_balance, width_class='uk-width-1-2@m'),
                    portfolio_performance(width_class='uk-width-1-2@m'),
                    asset_performance(width_class='uk-width-2-3@m'),
                    client_insights(profiles_=profiles, prior_accounts_balance=prior_accounts_balance,
                                    accounts_balance=accounts_balance, accounts=accounts, width_class='uk-width-1-3@m')
                ], **{'data-uk-grid': 'true'}, className='uk-child-width-1-4@m uk-grid-small uk-grid-match')
            ], className='uk-container')
        ], className='uk-section')
    ], style={'backgroundColor': '#88A9C3'})


@callback(
    Output('invite-notifications', 'children'),
    State('form-invite-email', 'value'),
    Input('form-invite-button', 'n_clicks')
)
def send_invite(email, n_clicks):
    if n_clicks and email:
        try:
            response = supabase_admin.auth.admin.invite_user_by_email(email)
            print(response)
            if response and response.user:
                return html.Span(f'Invite sent to {response.user.email}', className='uk-text-success uk-text-bolder')
            else:
                return html.Span(f'Error sending invite: {response["error"]["message"]}',
                                 className='uk-text-danger uk-text-bolder')
        except Exception as e:
            return html.Span(f'Invitation error: {e}', className='uk-text-danger uk-text-bolder')
