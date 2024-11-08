import dash
import plotly.express as px
from dash import dcc, html, callback, Output, Input
from sqlalchemy.orm import Session

from utils import calendar_view, Profile, engine, sign_out_button, navbar, create_table_wrapper, create_table_header, \
    table_item_decorator, market_performance

dash.register_page(__name__, path='/admin/', name='Admin')


def menu_card():
    return html.Div(
        html.Ul([
            html.Li('Menu', className='uk-nav-header', style={'color': 'white'}),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: home'}, className='uk-margin-small-right'), 'Dashboard'
            ], className='uk-flex uk-flex-middle')),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: credit-card'}, className='uk-margin-small-right'), 'Transactions'
            ], className='uk-flex uk-flex-middle')),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: star'}, className='uk-margin-small-right'), 'My Goals'
            ], className='uk-flex uk-flex-middle')),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: nut'}, className='uk-margin-small-right'), 'Investment'
            ], className='uk-flex uk-flex-middle')),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: file-text'}, className='uk-margin-small-right'), 'Bills and Payment'
            ], className='uk-flex uk-flex-middle')),
            html.Li(html.A([
                html.Span(**{'data-uk-icon': 'icon: settings'}, className='uk-margin-small-right'),
                'Analytics and Reports'
            ], className='uk-flex uk-flex-middle')),
            html.Li(className='uk-nav-divider uk-margin'),
            html.Li([
                html.Div(
                    html.Img(className='uk-border-circle', width='44', height='44',
                             src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                                 '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp',
                             alt='profile-pic'),
                    className='uk-width-auto'
                ),
                html.Div([
                    html.H3('Title', className='uk-card-title uk-margin-remove-bottom', style={'color': 'white'}),
                    html.P('April 01, 2016', className='uk-text-meta uk-margin-remove-top')
                ], className='uk-width-expand')
            ], className='uk-grid-small uk-flex-middle uk-margin-left uk-margin-top', **{'data-uk-grid': 'true'}),
            html.Li(className='uk-nav-divider uk-margin'),
            html.Li('Support', className='uk-nav-header', style={'color': 'white'}),
            html.Li([
                html.A([
                    html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right'),
                    'Send an invite'
                ], className='uk-flex uk-flex-middle'),
                html.Div([
                    html.H3('Send an invite', className='uk-card-title uk-margin-remove-bottom'),
                    html.P('Please enter the recipient\'s email address so we know who you’re sending to.',
                           className='uk-text-small uk-margin-remove-top'),
                    html.Div([
                        html.Label('Email', className='uk-form-label'),
                        html.Div([
                            html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-form-icon'),
                            dcc.Input(className='uk-input uk-form-blank', type='email', name='form-invite-name')
                        ], className='uk-inline')
                    ], className='uk-margin', style={'color': '#88A9C3'}),
                    html.Div(
                        html.Button("Send Invite",
                                    className='uk-button uk-button-large uk-width-1-1 uk-light',
                                    style={'backgroundColor': '#091235'}),
                        className='uk-margin'
                    ),
                    html.P(id='invite-notifications', className='uk-margin')
                ], className='uk-card uk-card-body uk-card-default', **{'data-uk-drop': 'true'})
            ], className='uk-inline'),
            html.Li(html.A('Client Management')),
            html.Li(html.A('Audit Logs')),
            html.Li(html.A('Investment Reporting')),
            html.Li(html.A('Admin Support Hub')),
            sign_out_button()
        ], className='uk-nav uk-nav-default'),
        className='uk-card uk-card-body uk-card-default', style={'backgroundColor': '#2A3A58'}
    )


def overview_card():
    return html.Div([
        html.Div(
            html.Div(
                html.Div('Overview', className='uk-text-default uk-text-bolder'),
                className='uk-flex uk-flex-between'
            ),
            className='uk-card-header'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Div('40', className='uk-text-large uk-text-bolder'),
                    html.Div('Transactions', className='uk-text-truncate', style={'fontSize': '11px'})
                ]),
                html.Div([
                    html.Div('24', className='uk-text-large uk-text-bolder'),
                    html.Div('Income', style={'fontSize': '11px'})
                ]),
                html.Div([
                    html.Div('16', className='uk-text-large uk-text-bolder'),
                    html.Div('Outcome', style={'fontSize': '11px'})
                ])
            ], **{'data-uk-grid': 'true'}, className='uk-child-width-expand uk-text-center')
        ], className='uk-card-body'),
        html.Div(calendar_view(), className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def portfolio_value_card():
    df = px.data.gapminder()
    fig = px.scatter(df.query('year==2007'), x='gdpPercap', y='lifeExp', size='pop', color='continent',
                     hover_name='country', log_x=True, size_max=60)
    return html.Div([
        html.Div(
            html.Div([
                html.Div('Portfolio Value', className='uk-text-default uk-text-bolder'),
                html.A(['US Dollar', html.Span(**{'data-uk-drop-parent-icon': 'true'})],
                       className='uk-link-muted uk-text-small'),
                html.Div(
                    html.Ul(
                        [
                            html.Li(html.A('US Dollar', className='uk-link-muted uk-text-small')),
                            html.Li(html.A('ZA Rand', className='uk-link-muted uk-text-small')),
                            html.Li(html.A('EURO', className='uk-link-muted uk-text-small')),
                            html.Li(html.A('British Pound', className='uk-link-muted uk-text-small'))
                        ],
                        className='uk-list uk-list-divider'
                    ),
                    className='uk-card uk-card-body', style={'backgroundColor': '#2A3A58'},
                    **{'data-uk-dropdown': 'true'}
                )
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        html.Div([
            html.Div('Balance', className='uk-text-small'),
            html.H2('R8,167,514.57',
                    className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
            html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                     className='uk-text-small uk-margin-remove-top')
        ], className='uk-card-body'),
        html.Div([
            dcc.Graph(figure=fig)
        ], className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


def assets_card():
    return html.Div([
        html.Div(
            html.Div([
                html.Div('Asset Allocation', className='uk-text-default uk-text-bolder'),
                html.Div([
                    html.Span(**{'data-uk-icon': 'icon: table'}),
                    html.Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        html.Div([
            html.Div('Quarterly Growth Rate', className='uk-text-small'),
            html.H2('+24.17%', className='uk-text-bolder uk-margin-remove-top uk-text-success'),
            html.Div([html.Div('0M'), html.Div('71M'), html.Div('142M')],
                     className='uk-flex uk-flex-between uk-text-bolder', style={'fontSize': '8px'}),
            html.Hr(),
            # html.Table(
            #     Caption('Asset Allocation'),
            #     Thead(
            #         html.Tr(
            #             *[Th(title, scope='col') for title in ['Asset', 'Value']]
            #         ),
            #     ),
            #     html.Tbody(
            #         html.Tr([
            #             html.Td(style={'--size': value}) for value in [0.7, 0.5, 0.4, 0.3, 0.2]
            #         ])
            #     ),
            #     className='charts-css bar multiple stacked'
            # ),
            # html.Ul([
            #     html.Li(Div([title, Br(),html.Span(value, className='uk-text-bolder')], className='uk-text-small'))
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
    return html.Div([
        html.Div(
            html.Div([
                html.Div('Performance Summary', className='uk-text-default uk-text-bolder'),
                html.Div([
                    html.Span(**{'data-uk-icon': 'icon: table'}),
                    html.Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between'),
            className='uk-card-header'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Div('Top Performer: Stocks (Equities)', className='uk-text-small'),
                    html.H2('R8,167,514.57',
                            className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                    html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                             className='uk-text-small uk-margin-remove-top')
                ]),
                html.Button('View All', style={'backgroundColor': '#88A9C3', 'color': '#091235'},
                            className='uk-button uk-button-small')
            ], className='uk-flex uk-flex-between uk-flex-middle'),
            # html.Ul([
            #     html.Li(title) for title in [
            #         'Stocks (Equities)', 'Bonds (Fixed Income Securities)', 'Real Estate', 'Commodities',
            #         'Cash and Cash Equivalents'
            #     ]
            # ], className='charts-css legend legend-inline legend-square uk-margin', style={'border': '0'}),
            html.Div(
                html.Div(
                    html.Div([
                        html.Div('142M'),
                        html.Div('71M', className='uk-margin-auto-vertical'),
                        html.Div('0M')
                    ], className='uk-flex uk-flex-column uk-flex-between uk-text-bolder', style={'fontSize': '8px'}),
                    className='uk-width-auto'
                ),
                **{'data-uk-grid': 'true'},
                className='uk-grid-divider uk-child-width-expand uk-grid-match uk-grid-small'
            ),
            html.Div([
                html.Div('Jul'),
                html.Div('Aug'),
                html.Div('Sep'),
                html.Div('Oct')
            ], className='uk-flex uk-flex-between uk-text-bolder uk-text-small uk-margin',
                style={'paddingLeft': '54px'})
        ], className='uk-card-body')
    ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#172031'})


@table_item_decorator
def clients_table(clients: list):
    header = create_table_header(['', 'Client'])
    body = html.Tbody([
        html.Tr([
            html.Td([
                html.A(href=f'/edit/{str(client.id)}/', **{'data-uk-icon': 'icon: pencil'},
                       className='uk-icon-button')
            ]),
            html.Td(
                html.Div([
                    html.Div(
                        html.Img(
                            className='uk-border-circle', width='60', height='60',
                            src=client.profile_picture_url or '',
                            alt='profile-pic'
                        ) if client.profile_picture_url else html.Span(
                            **{'data-uk-icon': 'icon: user; ratio: 3;'}),
                        className='uk-width-auto'
                    ),
                    html.Div([
                        html.H3([
                            html.Span(client.first_name or 'First name', className='uk-text-bolder'),
                            html.Span(' '),
                            client.last_name or 'Last name'
                        ], className='uk-card-title uk-margin-remove-bottom', style={'color': 'white'}),
                        html.Div(client.email or 'No email provided', style={'fontSize': '11px'}),
                        html.P([
                            'Last active',
                            html.Span(client.created_at.strftime('%B %d, %Y'),
                                      className='uk-text-default uk-text-bolder uk-margin-small-left')
                        ], className='uk-text-meta uk-margin-remove-top')
                    ], className='uk-width-expand')
                ], className='uk-grid-small uk-flex-middle', **{'data-uk-grid': 'true'}),
                className='uk-flex uk-flex-between'
            )
        ], className='uk-animation-fade') for client in clients
    ]) if clients else None

    return create_table_wrapper(header, body, "No accounts found")


def client_insights_card(clients: list):
    if not clients:  # Early return if no clients
        return html.Div('No clients available', className='uk-text-danger')

    return html.Div([
        html.Div([
            dcc.Store(id='selected-profile-id'),
            html.Div([
                html.Div('Client Insights', className='uk-text-default uk-text-bolder'),
                html.Div([
                    html.Span(**{'data-uk-icon': 'icon: table'}),
                    html.Span('Filter', className='uk-margin-small-left')
                ], className='uk-text-small uk-flex uk-flex-middle')
            ], className='uk-flex uk-flex-between')
        ], className='uk-card-header'),
        html.Div(
            clients_table(clients),
            className='uk-card-body'
        )
    ], className='uk-card uk-card-secondary')


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
        return html.Div([
            html.Div(id='admin-nav',
                     **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
            dcc.Location(id='admin-url'),
            html.Div([
                html.Div(id='adm-nav',
                         **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
                dcc.Location(id='edit-url'),
                html.Div([
                    html.Div(menu_card()),
                    market_performance(),
                    # html.Div(overview_card()),
                    html.Div(portfolio_value_card()),
                    html.Div(assets_card()),
                    html.Div(performance_summary_card(), className='uk-width-1-2@m'),
                    html.Div(client_insights_card(clients=clients), className='uk-width-1-2@m')
                ], **{'data-uk-grid': 'true'},
                    className='uk-padding uk-child-width-1-4@m uk-grid-small uk-grid-match')
            ], style={'backgroundColor': '#88A9C3'})
        ])


@callback(
    Output('admin-nav', 'children'),
    Input('admin-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
