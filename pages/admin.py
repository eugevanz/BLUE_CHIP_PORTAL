import dash
import plotly.express as px
from dash import dcc
from dash.html import Ul, A, Span, Img, H3, Label, Button, H2, Hr, Nav, Div, Li, P, Table, Tbody, Tr, Td
from sqlalchemy.orm import Session

from utils import calendar_view, Profile, engine, sign_out_button

dash.register_page(__name__, path='/admin/')


def menu_card():
    return Div(
        Ul([
            Li('Menu', className='uk-nav-header', style={'color': 'white'}),
            Li(A([
                Span(**{'data-uk-icon': 'icon: home'}, className='uk-margin-small-right'), 'Dashboard'
            ], className='uk-flex uk-flex-middle')),
            Li(A([
                Span(**{'data-uk-icon': 'icon: credit-card'}, className='uk-margin-small-right'), 'Transactions'
            ], className='uk-flex uk-flex-middle')),
            Li(A([
                Span(**{'data-uk-icon': 'icon: star'}, className='uk-margin-small-right'), 'My Goals'
            ], className='uk-flex uk-flex-middle')),
            Li(A([
                Span(**{'data-uk-icon': 'icon: nut'}, className='uk-margin-small-right'), 'Investment'
            ], className='uk-flex uk-flex-middle')),
            Li(A([
                Span(**{'data-uk-icon': 'icon: file-text'}, className='uk-margin-small-right'), 'Bills and Payment'
            ], className='uk-flex uk-flex-middle')),
            Li(A([
                Span(**{'data-uk-icon': 'icon: settings'}, className='uk-margin-small-right'), 'Analytics and Reports'
            ], className='uk-flex uk-flex-middle')),
            Li(className='uk-nav-divider uk-margin'),
            Li([
                Div(
                    Img(className='uk-border-circle', width='44', height='44',
                        src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                            '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp',
                        alt='profile-pic'),
                    className='uk-width-auto'
                ),
                Div([
                    H3('Title', className='uk-card-title uk-margin-remove-bottom', style={'color': 'white'}),
                    P('April 01, 2016', className='uk-text-meta uk-margin-remove-top')
                ], className='uk-width-expand')
            ], className='uk-grid-small uk-flex-middle uk-margin-left uk-margin-top', **{'data-uk-grid': 'true'}),
            Li(className='uk-nav-divider uk-margin'),
            Li('Support', className='uk-nav-header', style={'color': 'white'}),
            Li([
                A([
                    Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right'),
                    'Send an invite'
                ], className='uk-flex uk-flex-middle'),
                Div([
                    H3('Send an invite', className='uk-card-title uk-margin-remove-bottom'),
                    P('Please enter the recipient\'s email address so we know who you’re sending to.',
                      className='uk-text-small uk-margin-remove-top'),
                    Div([
                        Label('Email', className='uk-form-label'),
                        Div([
                            Span(**{'data-uk-icon': 'icon: mail'}, className='uk-form-icon'),
                            dcc.Input(className='uk-input uk-form-blank', type='email', name='form-invite-name')
                        ], className='uk-inline')
                    ], className='uk-margin', style={'color': '#88A9C3'}),
                    Div(
                        Button("Send Invite",
                               className='uk-button uk-button-large uk-width-1-1 uk-light',
                               style={'backgroundColor': '#091235'}),
                        className='uk-margin'
                    ),
                    P(id='invite-notifications', className='uk-margin')
                ], className='uk-card uk-card-body uk-card-default', **{'data-uk-drop': 'true'})
            ], className='uk-inline'),
            Li(A('Client Management')),
            Li(A('Audit Logs')),
            Li(A('Investment Reporting')),
            Li(A('Admin Support Hub')),
            sign_out_button()
        ], className='uk-nav uk-nav-default'),
        className='uk-card uk-card-body uk-card-default', style={'backgroundColor': '#2A3A58'}
    )


# , hx_post='/send-invite/',
#                                hx_target='#invite-notifications',
#                                hx_include="[name='form-invite-name']"

def overview_card():
    return Div([
        Div(
            Div(
                Div('Overview', className='uk-text-default uk-text-bolder'),
                className='uk-flex uk-flex-between'
            ),
            className='uk-card-header'
        ),
        Div([
            Div([
                Div([
                    Div('40', className='uk-text-large uk-text-bolder'),
                    Div('Transactions', className='uk-text-truncate', style={'fontSize': '11px'})
                ]),
                Div([
                    Div('24', className='uk-text-large uk-text-bolder'),
                    Div('Income', style={'fontSize': '11px'})
                ]),
                Div([
                    Div('16', className='uk-text-large uk-text-bolder'),
                    Div('Outcome', style={'fontSize': '11px'})
                ])
            ], **{'data-uk-grid': 'true'}, className='uk-child-width-expand uk-text-center')
        ], className='uk-card-body'),
        Div(calendar_view(), className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def portfolio_value_card():
    df = px.data.gapminder()
    fig = px.scatter(df.query('year==2007'), x='gdpPercap', y='lifeExp', size='pop', color='continent',
                     hover_name='country', log_x=True, size_max=60)
    return Div([
        Div(
            Div([
                Div('Portfolio Value', className='uk-text-default uk-text-bolder'),
                A(['US Dollar', Span(**{'data-uk-drop-parent-icon': 'true'})], className='uk-link-muted uk-text-small'),
                Div(
                    Ul(
                        [
                            Li(A('US Dollar', className='uk-link-muted uk-text-small')),
                            Li(A('ZA Rand', className='uk-link-muted uk-text-small')),
                            Li(A('EURO', className='uk-link-muted uk-text-small')),
                            Li(A('British Pound', className='uk-link-muted uk-text-small'))
                        ],
                        className='uk-list uk-list-divider'
                    ),
                    className='uk-card uk-card-body', style={'backgroundColor': '#2A3A58'},
                    **{'data-uk-dropdown': 'true'}
                )
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        Div([
            Div('Balance', className='uk-text-small'),
            H2('R8,167,514.57',
               className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
            Div(['Compared to last month ', Span('+24.17%', className='uk-text-success')],
                className='uk-text-small uk-margin-remove-top')
        ], className='uk-card-body'),
        Div([
            dcc.Graph(id='portfolio-value-graph', figure=fig)
        ], className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def assets_card():
    return Div([
        Div(
            Div([
                Div('Asset Allocation', className='uk-text-default uk-text-bolder'),
                Div([
                    Span(**{'data-uk-icon': 'icon: table'}),
                    Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        Div([
            Div('Quarterly Growth Rate', className='uk-text-small'),
            H2('+24.17%', className='uk-text-bolder uk-margin-remove-top uk-text-success'),
            Div([Div('0M'), Div('71M'), Div('142M')],
                className='uk-flex uk-flex-between uk-text-bolder', style={'fontSize': '8px'}),
            Hr(),
            # Table(
            #     Caption('Asset Allocation'),
            #     Thead(
            #         Tr(
            #             *[Th(title, scope='col') for title in ['Asset', 'Value']]
            #         ),
            #     ),
            #     Tbody(
            #         Tr([
            #             Td(style={'--size': value}) for value in [0.7, 0.5, 0.4, 0.3, 0.2]
            #         ])
            #     ),
            #     className='charts-css bar multiple stacked'
            # ),
            # Ul([
            #     Li(Div([title, Br(), Span(value, className='uk-text-bolder')], className='uk-text-small'))
            #     for title, value in [
            #         ('Stocks (Equities)', '4,083,757.29 USD'),
            #         ('Bonds (Fixed Income Securities)', '1,633,502.91 USD'),
            #         ('Real Estate', '1,225,127.19 USD'),
            #         ('Commodities', '816,751.46 USD'),
            #         ('Cash and Cash Equivalents', '408,375.73 USD')
            #     ]
            # ], className='charts-css legend legend-square uk-margin', style={'border': '0'})
        ], className='uk-card-body')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def performance_summary_card():
    return Div([
        Div(
            Div([
                Div('Performance Summary', className='uk-text-default uk-text-bolder'),
                Div([
                    Span(**{'data-uk-icon': 'icon: table'}),
                    Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        Div([
            Div([
                Div([
                    Div('Top Performer: Stocks (Equities)', className='uk-text-small'),
                    H2('R8,167,514.57',
                       className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                    Div(['Compared to last month ', Span('+24.17%', className='uk-text-success')],
                        className='uk-text-small uk-margin-remove-top')
                ]),
                Button('View All', style={'backgroundColor': '#88A9C3', 'color': '#091235'},
                       className='uk-button uk-button-small')
            ], className='uk-flex uk-flex-between uk-flex-middle'),
            # Ul([
            #     Li(title) for title in [
            #         'Stocks (Equities)', 'Bonds (Fixed Income Securities)', 'Real Estate', 'Commodities',
            #         'Cash and Cash Equivalents'
            #     ]
            # ], className='charts-css legend legend-inline legend-square uk-margin', style={'border': '0'}),
            Div(
                Div(
                    Div([
                        Div('142M'),
                        Div('71M', className='uk-margin-auto-vertical'),
                        Div('0M')
                    ], className='uk-flex uk-flex-column uk-flex-between uk-text-bolder', style={'fontSize': '8px'}),
                    className='uk-width-auto'
                ),
                **{'data-uk-grid': 'true'},
                className='uk-grid-divider uk-child-width-expand uk-grid-match uk-grid-small'
            ),
            Div([
                Div('Jul'),
                Div('Aug'),
                Div('Sep'),
                Div('Oct')
            ], className='uk-flex uk-flex-between uk-text-bolder uk-text-small uk-margin',
                style={'paddingLeft': '54px'})
        ], className='uk-card-body')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def client_insights_card(clients: list):
    if not clients:  # Early return if no clients
        return Div('No clients available', className='uk-text-danger')

    client_items = [
        Tr([
            Td(
                Div([
                    Div(
                        Img(
                            className='uk-border-circle', width='60', height='60',
                            src=client.profile_picture_url or '',
                            alt='profile-pic'
                        ) if client.profile_picture_url else Span(
                            **{'data-uk-icon': 'icon: user; ratio: 3;'}),
                        className='uk-width-auto'
                    ),
                    Div([
                        H3([
                            Span(client.first_name or 'First name', className='uk-text-bolder'),
                            Span(' '),
                            client.last_name or 'Last name'
                        ], className='uk-card-title uk-margin-remove-bottom', style={'color': 'white'}),
                        Div(client.email or 'No email provided', style={'fontSize': '11px'}),
                        P([
                            'Last active',
                            Span(client.created_at.strftime('%B %d, %Y'),
                                 className='uk-text-default uk-text-bolder uk-margin-small-left')
                        ], className='uk-text-meta uk-margin-remove-top')
                    ], className='uk-width-expand')
                ], className='uk-grid-small uk-flex-middle', **{'data-uk-grid': 'true'}),
                className='uk-flex uk-flex-between'
            ),
            Td(A(href=f'/edit/{str(client.id)}/', **{'data-uk-icon': 'icon: pencil'}))
        ]) for client in clients
    ]

    return Div([
        Div([
            dcc.Store(id='selected-profile-id'),
            Div([
                Div('Client Insights', className='uk-text-default uk-text-bolder'),
                Div([
                    Span(**{'data-uk-icon': 'icon: table'}),
                    Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between')
        ], className='uk-card-header'),
        Div(
            Table([
                Tbody([*client_items])
            ], className='uk-table uk-table-hover'),
            className='uk-card-body'
        ),
        Div(
            Nav(
                Ul([
                    Li(
                        A([
                            Span(**{'data-uk-pagination-previous': 'true'}, className='uk-margin-small-right'),
                            'Previous'
                        ], href='#')
                    ),
                    Li(
                        A([
                            'Next',
                            Span(**{'data-uk-pagination-next': 'true'}, className='uk-margin-small-left')
                        ], href='#'),
                        className='uk-margin-auto-left'
                    )
                ], className='uk-pagination', **{'data-uk-margin': 'true'})
            ),
            className='uk-card-footer'
        )
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


# @callback(
#     Output('selected-profile-id', 'data'),
#     State({'type': 'client-insights-id', 'index': MATCH}, 'id'),
#     Input({'type': 'client-insights-id', 'index': MATCH}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def get_profile_id(profile_id, n_clicks):
#     if n_clicks: return profile_id
#
#
# @callback(
#     Output('url', 'pathname', allow_duplicate=True),
#     Input('selected-profile-id', 'data'),
#     prevent_initial_call=True
# )
# def goto_edit(profile_id):
#     # print(dash.page_registry['pages.edit_client']['path'])
#     if profile_id: return f'/edit/{profile_id}/'


def layout():
    with Session(engine) as session:
        clients = session.query(Profile).all()
        session.commit()
        return Div([
            Div([
                # Div(menu_card()),
                # Div(overview_card()),
                Div(portfolio_value_card()),
                Div(assets_card()),
                Div(performance_summary_card(), className='uk-width-1-2@m'),
                Div(client_insights_card(clients=clients), className='uk-width-1-2@m')
            ], **{'data-uk-grid': 'true'},
                className='uk-padding uk-child-width-1-4@m uk-grid-small uk-grid-match uk-flex-right')
        ], style={'backgroundColor': '#091235'})
