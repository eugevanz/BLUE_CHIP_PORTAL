import dash
from dash import html

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.client_menu_card import client_menu
from components.dividend_performance_card import dividend_performance
from components.footer_section import footer
from components.investment_performance_card import investment_performance
from components.market_performance_card import market_performance
from components.performance_summary_card import performance_summary
from components.transaction_performance_card import transaction_performance
from utils import profile_data


def name(profile_id=None):
    profile_email = profile_data(profile_id)['profile'].email
    return profile_email


dash.register_page(__name__, path_template='/client_portal/<profile_id>/', name=name)


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
        html.Div([
            html.Div([
                html.Img(
                    src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                        '/Blue%20Chip%20Invest%20Logo.001.png',
                    width='60', height='60'),
                html.Div(['BLUE CHIP INVESTMENTS'],
                         style={'fontFamily': '"Noto Sans", sans-serif', 'fontOpticalSizing': 'auto',
                                'fontWeight': '400', 'fontStyle': 'normal', 'lineHeight': '22px',
                                'color': '#091235', 'width': '164px'})
            ], className='uk-logo uk-flex uk-padding-small')
        ], className='uk-card uk-card-body'),
        html.Div([
            client_menu(profile),
            market_performance(),
            performance_summary(accounts_balance, payouts_balance, client_goals_balance, transactions_balance,
                                investments_balance, prior_accounts_balance, prior_payouts_balance,
                                prior_client_goals_balance, prior_transactions_balance, prior_investments_balance),
            account_performance(accounts=accounts, total=accounts_balance, prior=prior_accounts_balance),
            dividend_performance(dividends_and_payouts=dividends_and_payouts, total=payouts_balance,
                                 prior=prior_payouts_balance),
            client_goal_performance(client_goals=client_goals, total=client_goals_balance,
                                    prior=prior_client_goals_balance),
            investment_performance(investments=investments, total=investments_balance,
                                   prior=prior_investments_balance),
            transaction_performance(transactions=transactions, total=transactions_balance,
                                    prior=prior_transactions_balance)
        ], **{'data-uk-grid': 'true'}, className='uk-child-width-1-3@m uk-grid-small uk-padding-small uk-grid-match'),
        footer()
    ], style={'backgroundColor': '#88A9C3'})
