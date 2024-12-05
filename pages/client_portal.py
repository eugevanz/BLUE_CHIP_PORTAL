import dash
from dash import html

from components.account_performance_card import account_performance
from components.client_goal_performance_card import client_goal_performance
from components.client_menu_card import client_menu
from components.dividend_performance_card import dividend_performance
from components.footer_section import footer
from components.investment_performance_card import investment_performance
from components.market_performance_card import market_performance
from components.navbar import navbar
from components.performance_summary_card import performance_summary
from components.transaction_performance_card import transaction_performance
from utils import profile_data


def name(profile_id=None):
    profile_email = profile_data(profile_id)['profile'].email
    return profile_email


dash.register_page(__name__, name=name)


def layout():
    return html.Div([
        navbar([('My Profile', '')]),
        html.Div([
            html.Div([
                html.Div([
                    client_menu(),
                    market_performance(),
                    performance_summary(is_client=True),
                    account_performance(),
                    dividend_performance(),
                    client_goal_performance(),
                    investment_performance(),
                    transaction_performance()
                ], **{'data-uk-grid': 'true'},
                    className='uk-child-width-1-3@m uk-grid-small uk-padding-small uk-grid-match')
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer()
    ], className='uk-background-secondary uk-light')
