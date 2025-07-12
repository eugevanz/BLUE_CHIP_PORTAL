import dash
from dash import html

from components.admin_menu_card import admin_menu
from components.asset_performance_card import asset_performance
from components.client_insights_card import client_insights
from components.footer_section import footer
from components.market_performance_card import market_performance
from components.navbar import navbar
from components.performance_summary_card import performance_summary
from components.portfolio_performance_card import portfolio_performance

dash.register_page(__name__, name='Admin -- Blue Chip Investments')


def layout():
    return html.Div([
        navbar([('Admin', '')]),

        html.Div([
            html.Div([
                html.Div([
                    admin_menu(),
                    market_performance(),
                    performance_summary(width_class='uk-width-1-2@m'),
                    portfolio_performance(width_class='uk-width-1-2@m'),
                    asset_performance(width_class='uk-width-2-3@m'),
                    client_insights(width_class='uk-width-1-3@m')
                ], **{'data-uk-grid': 'true'}, className='uk-child-width-1-4@m uk-grid-small uk-grid-match')
            ], className='uk-container')
        ], className='uk-section uk-section-small'),
        footer()
    ], className='uk-background-secondary uk-light')
