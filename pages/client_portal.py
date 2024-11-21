from datetime import datetime

import dash
from dash import html

from components.client_menu_card import client_menu_card
from utils import calendar_view, sign_out_button, profile_data

dash.register_page(__name__, path_template='/client_portal/<profile_id>/', name='Client Portal')


def nav_offcanvas(header: str):
    return Div(
        [H3(header, className='uk-width-small uk-margin-remove')],  # Wrap in a list
        className='uk-margin-medium-bottom uk-margin-small-top uk-padding',
        style={'background-color': '#88A9C3'}
    )


def articles_offcanvas(articles: list, icon: str):
    return Div(
        [
            Article(
                Div(**{'data-uk-icon': f'icon: {icon}'}),
                P(header, className='uk-text-bolder'),
                P(article),
                className='uk-article',
                id=element
            ) for header, article, element in articles
        ],
        className='uk-flex uk-flex-wrap'
    )








def overview_card():
    return Div([
        Div(
            Div(
                [
                    Div('Overview', className='uk-text-default uk-text-bolder'),
                    Div(datetime.now().strftime('%B %Y'), className='uk-text-small')
                ],
                className='uk-flex uk-flex-between'
            ),
            className='uk-card-header'
        ),
        Div([
            Div([
                Div([
                    Div('40', className='uk-text-large uk-text-bolder'),
                    Div('Transactions', className='uk-text-truncate', style={'font-size': '11px'})
                ]),
                Div([
                    Div('24', className='uk-text-large uk-text-bolder'),
                    Div('Income', style={'font-size': '11px'})
                ]),
                Div([
                    Div('16', className='uk-text-large uk-text-bolder'),
                    Div('Outcome', style={'font-size': '11px'})
                ])
            ], **{'data-uk-grid': 'true'}, className='uk-child-width-expand uk-text-center')
        ], className='uk-card-body'),
        Div([
            calendar_view(),
            Nav(
                Ul([
                    Li(
                        A(
                            [Span(**{'data-uk-pagination-previous': 'true'}, className='uk-margin-small-right'),
                             'September'],
                            href='#'
                        )
                    ),
                    Li(
                        A(
                            ['November', Span(**{'data-uk-pagination-next': 'true'}, className='uk-margin-small-left')],
                            href='#'
                        ),
                        className='uk-margin-auto-left'
                    )
                ], className='uk-pagination', **{'data-uk-margin': 'true'}),
                className='uk-margin-medium-top'
            ),
            A([
                Div(
                    Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right',
                         style={'color': '#89CFF0'}),
                    className='uk-width-auto'
                ),
                Div(
                    Div('Top 5 Portfolio Holdings: Tech Giants Lead with Apple, Tesla, and Amazon Driving Strong '
                        'Returns'[:80] + '...', style={'color': '#89CFF0'}, className='uk-text-bolder')
                )
            ], **{'data-uk-grid': 'true'}, **{'data-uk-toggle': 'true'}, href='#messages',
                className='uk-child-width-expand uk-grid-small uk-margin-medium-top uk-text-muted')
        ], className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'background-color': '#172031'})


def portfolio_value_card():
    return Div(
        [
            Div(
                Div(
                    [
                        Div('Portfolio Value', className='uk-text-default uk-text-bolder'),
                        A(['US Dollar', Span(**{'data-uk-drop-parent-icon': True})],
                          className='uk-link-muted uk-text-small'),
                        Div(
                            [
                                Ul(
                                    [
                                        Li(A('US Dollar', className='uk-link-muted uk-text-small')),
                                        Li(A('ZA Rand', className='uk-link-muted uk-text-small')),
                                        Li(A('EURO', className='uk-link-muted uk-text-small')),
                                        Li(A('British Pound', className='uk-link-muted uk-text-small'))
                                    ],
                                    className='uk-list uk-list-divider'
                                )
                            ],
                            className='uk-card uk-card-body',
                            style={'background-color': '#2A3A58'},
                            **{'data-uk-dropdown': 'true'}
                        )
                    ],
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            Div(
                [
                    Div('Balance', className='uk-text-small'),
                    H2('R8,167,514.57',
                       className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                    Div(
                        ['Compared to last month ', Span('+24.17%', className='uk-text-success')],
                        className='uk-text-small uk-margin-remove-top'
                    ),
                    Div(
                        [
                            Div(
                                Div(
                                    [
                                        Div('142M'),
                                        Div('71M', className='uk-margin-auto-vertical'),
                                        Div('0M', className='uk-flex uk-flex-column uk-flex-between uk-text-bolder',
                                            style={'font-size': '8px'})
                                    ]
                                ),
                                className='uk-width-auto'
                            )
                        ],
                        **{'data-uk-grid': 'true'},
                        className='uk-grid-divider uk-child-width-expand uk-grid-match uk-grid-small uk-margin-medium-top'
                    )
                ],
                className='uk-card-body'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'}
    )


def transactions():
    return Div(
        [
            Div(
                Div(
                    [
                        Div('Recent Transactions', className='uk-text-default uk-text-bolder'),
                        Div(
                            [
                                Span(**{'data-uk-icon': 'icon: table'}),
                                Span('Filter', className='uk-margin-small-left')
                            ],
                            className='uk-text-small uk-flex uk-flex-middle'
                        )
                    ],
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            # Div(
            #     Table(
            #         Thead(
            #             Tr(
            #                 [
            #                     Th('Type'),
            #                     Th('Amount'),
            #                     Th('Method')
            #                 ]
            #             )
            #         ),
            #         Tbody(
            #             [
            #                 Tr([
            #                     Td(
            #                         [
            #                             Span(
            #                                 **{
            #                                     'data-uk-icon': f'icon: {"plus-circle" if tx_type[0] == "Received" else "minus-circle"}; ratio: 1.5'
            #                                 },
            #                                 className=f'uk-text-{"success" if tx_type[0] == "Received" else "danger"}'
            #                             ),
            #                             Div([
            #                                 Div(title, className='uk-text-bolder'),
            #                                 Div(f'{tx_type[0]} • {tx_type[1]}', className='uk-text-small')
            #                             ], className='uk-margin-small-left')
            #                         ],
            #                         className='uk-flex uk-flex-middle'
            #                     ),
            #                     Td([
            #                         Div(f'R {amount[0]}', className='uk-text-bolder'),
            #                         Div(f'R {amount[1]}', className='uk-text-small')
            #                     ]),
            #                     Td([
            #                         Div(method[0], className='uk-text-bolder'),
            #                         Div(method[1], className='uk-text-small')
            #                     ])
            #                 ]) for title, tx_type, amount, method in [
            #                 ('Company', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Credit Card', '**** 3560')),
            #                 (
            #                     'Revenue', ('Received', 'Aug 24 2024'), (1500.00, 1371.81),
            #                     ('Bank Transfer', '**** 3560')),
            #                 ('Bonus', ('Received', 'Aug 24 2024'), (1500.00, 1371.81), ('Credit Card', '**** 3560')),
            #                 ('Dog food', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Bank Transfer', '**** 3560')),
            #                 ('Company', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Bank Transfer', '**** 3560'))
            #             ]
            #             ]
            #         ),
            #         className='uk-table uk-table-divider'
            #     ),
            #     className='uk-card-body'
            # ),
            Div(
                Nav(
                    Ul(
                        [
                            Li(
                                A([
                                    Span(**{'data-uk-pagination-previous': True}, className='uk-margin-small-right'),
                                    'Previous'
                                ], href='#')
                            ),
                            Li(
                                A([
                                    'Next',
                                    Span(**{'data-uk-pagination-next': True}, className='uk-margin-small-left')
                                ], href='#'),
                                className='uk-margin-auto-left'
                            )
                        ],
                        className='uk-pagination',
                        **{'data-uk-margin': 'true'}
                    )
                ),
                className='uk-card-footer'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'},
        id='transactions'
    )


def holdings():
    return Div(
        [
            Div(
                Div(
                    Div('Holdings', className='uk-text-default uk-text-bolder'),
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            Div([
                Div(
                    [
                        Div(
                            [
                                Div('Stocks (Equities)', className='uk-text-small'),
                                H2(
                                    'R8,167,514.57',
                                    className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'
                                ),
                                Div(
                                    [
                                        'Compared to last month ',
                                        Span('+24.17%', className='uk-text-success')
                                    ],
                                    className='uk-text-small uk-margin-remove-top'
                                )
                            ]
                        ),
                        Button(
                            'View All',
                            style={'background-color': '#88A9C3', 'color': '#091235'},
                            className='uk-button uk-button-small'
                        )
                    ],
                    className='uk-flex uk-flex-between uk-flex-middle'
                ),
                P(
                    'Apple Inc. (AAPL) is a multinational technology company based in Cupertino, California, best known for its '
                    'innovative hardware, software, and digital services. Listed on the NASDAQ stock exchange under the ticker '
                    'symbol AAPL, Apple is one of the most valuable companies in the world, consistently maintaining its '
                    'position as a leader in the tech industry.',
                    className='uk-text-small'
                )
            ], className='uk-card-body'),
            Div(
                Nav(
                    Ul(
                        [
                            Li(
                                A(
                                    Span(**{'data-uk-pagination-previous': True}, className='uk-margin-small-right'),
                                    'Bonds (Fixed Income Securities)',
                                    href='#'
                                )
                            ),
                            Li(
                                A(
                                    [
                                        'Real Estate',
                                        Span(**{'data-uk-pagination-next': True}, className='uk-margin-small-left')
                                    ],
                                    href='#'
                                ),
                                className='uk-margin-auto-left'
                            )
                        ],
                        className='uk-pagination',
                        **{'data-uk-margin': 'true'}
                    )
                ),
                className='uk-card-footer'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'},
        id='holdings'
    )


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

    return Div([
        Div([
            Div(
                [
                    Div(client_menu_card(profile), className='uk-width-1-5@m'),
                    Div(overview_card(), className='uk-width-1-3@m'),
                    Div(portfolio_value_card(), className='uk-width-1-3@m'),
                    # Div(assets_card()),  # Uncomment when ready to use
                    Div(transactions(), className='uk-width-1-2@m'),
                    Div(holdings(), className='uk-width-1-2@m')
                ],
                **{'data-uk-grid': 'true'},
                className='uk-child-width-1-4@m uk-grid-small uk-grid-match uk-flex-right',
                style={'padding-top': '16px'}
            ),
            ],className='uk-container'),
        ],style={'backgroundColor': '#88A9C3'})
