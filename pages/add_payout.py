from datetime import date, datetime

import dash
from dash import dcc, callback, Output, State, Input, html
from dash.html import Span, Button
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import engine, Account, DividendOrPayout, account_fig, continents_list, custom_colours, \
    fig_layout, dates_list, payouts_fig, format_time, investment_fig, investment_list, goals_fig, goals_list, \
    transact_fig, transact_df

dash.register_page(__name__, path_template='/add-payout/<profile_id>/')


def layout(profile_id: str):
    with Session(engine) as session:
        accounts = session.scalars(select(Account).where(Account.profile_id == profile_id)).all()

    account_fig.update_layout(**fig_layout)
    payouts_fig.update_layout(**fig_layout)
    investment_fig.update_layout(**fig_layout)
    goals_fig.update_layout(**fig_layout)
    transact_fig.update_layout(**fig_layout)

    return html.Div([
        dcc.Location(id='payout-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(['Add Dividend/Payout']),
                        html.P(['Adding a dividend or payout typically involves recording a financial transaction '
                                'associated with an investment account to document income received from holdings, '
                                'like stocks or funds, that distribute earnings to account holders.'],
                               className='uk-text-meta'),

                        html.Div([
                            html.Div('Account', className='uk-text-small'),
                            html.Div([
                                dcc.Dropdown([
                                    {'label': account.account_number, 'value': str(account.id)} for account in accounts
                                ], placeholder='Select account', style={'color': '#172031'}, id='account_id')
                            ], className='uk-text-bolder uk-margin-remove-top')
                        ], className='uk-margin'),

                        html.Div([
                            html.Div('Payout Date', className='uk-text-small'),
                            html.Div([
                                Span(className='uk-form-icon', **{'data-uk-icon': 'icon: calendar'}),
                                dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                     id='payment_date', date=date.today())
                            ], className='uk-margin-remove-top uk-inline')
                        ], className='uk-margin'),

                        html.Div([
                            html.Div('Amount', className='uk-text-small'),
                            dcc.Input(
                                type='number',
                                placeholder='Amount',
                                className='uk-input uk-text-bolder uk-width-1-1',
                                id='amount'
                            )
                        ], className='uk-margin'),

                        Button('Save', id='add-pay-btn',
                               className='uk-button uk-button-primary uk-margin uk-margin-large-bottom')
                    ], className='uk-card uk-card-body')
                ]),

                html.Div([
                    html.Div([
                        html.Div(['Dividend/Payout performance'], className='uk-card-header'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([f'R {100000:,.2f}']),
                                        html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                                        html.Div([f'R {10000:,.2f}'])
                                    ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                                ], className='uk-width-auto'),
                                html.Div([
                                    dcc.Graph(figure=payouts_fig, style={'height': '300px'}),
                                    html.Hr(),
                                    html.Div([
                                        html.Div([format_time(datetime.strptime(item, '%Y-%m-%d'))]) for item in
                                        [dates_list[0], dates_list[len(dates_list) // 2], dates_list[-1]]
                                    ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                                ])
                            ], **{'data-uk-grid': 'true'},
                                className='uk-grid-divider uk-child-width-expand uk-grid-small')
                        ], className='uk-card-body')
                    ], className='uk-card uk-card-default')
                ], className='uk-flex-first@l'),

                html.Div([
                    html.Div([
                        html.Div(['Accounts performance'], className='uk-card-header'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([f'R {100000:,.2f}']),
                                        html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                                        html.Div([f'R {10000:,.2f}'])
                                    ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                                ], className='uk-width-auto'),
                                html.Div([
                                    dcc.Graph(figure=account_fig, style={'height': '300px'}),
                                    html.Hr(),
                                    html.Div([
                                        html.Div([
                                            html.Div(className='uk-border-circle', style={
                                                'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
                                            }),
                                            html.Div([continent], className='uk-margin-small-left uk-text-small')
                                        ], className='uk-flex uk-flex-middle uk-margin-right') for i, continent in
                                        enumerate(
                                            continents_list)
                                    ], className='uk-flex uk-flex-wrap')
                                ])
                            ], **{'data-uk-grid': 'true'},
                                className='uk-grid-divider uk-child-width-expand uk-grid-small')
                        ], className='uk-card-body')
                    ], className='uk-card uk-card-default')
                ]),

                html.Div([
                    html.Div([
                        html.Div(['Investments performance'], className='uk-card-header'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([f'R {100000:,.2f}']),
                                        html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                                        html.Div([f'R {10000:,.2f}'])
                                    ], className='uk-flex uk-flex-column uk-height-small', style={'fontSize': '8px'})
                                ], className='uk-width-auto'),
                                html.Div([
                                    dcc.Graph(figure=investment_fig, style={'height': '150px'}),
                                    html.Hr(),
                                    html.Div([
                                        html.Div([
                                            html.Div(className='uk-border-circle', style={
                                                'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
                                            }),
                                            html.Div([item], className='uk-margin-small-left uk-text-small')
                                        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in enumerate(
                                            investment_list)
                                    ], className='uk-flex uk-flex-wrap')
                                ])
                            ], **{'data-uk-grid': 'true'},
                                className='uk-grid-divider uk-child-width-expand uk-grid-small')
                        ], className='uk-card-body')
                    ], className='uk-card uk-card-default')
                ]),

                html.Div([
                    html.Div([
                        html.Div(['Transactions performance'], className='uk-card-header'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div(className='uk-border-circle', style={
                                                'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
                                            }),
                                            html.Div([
                                                html.Div([item[0]], className='uk-text-uppercase'),
                                                html.Div([f'R {item[1]:,.2f}'], className='uk-text-bolder')
                                            ], className='uk-margin-small-left')
                                        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in enumerate(
                                            list(transact_df.itertuples(index=False, name=None)))
                                    ], className='uk-flex uk-flex-column uk-height-small', style={'fontSize': '8px'})
                                ], className='uk-width-auto'),
                                html.Div([dcc.Graph(figure=transact_fig, style={'height': '150px'})])
                            ], **{'data-uk-grid': 'true'},
                                className='uk-grid-divider uk-child-width-expand uk-grid-small')
                        ], className='uk-card-body')
                    ], className='uk-card uk-card-default')
                ]),

                html.Div([
                    html.Div([
                        html.Div(['Client Goals performance'], className='uk-card-header'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([f'R {100000:,.2f}']),
                                        html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                                        html.Div([f'R {10000:,.2f}'])
                                    ], className='uk-flex uk-flex-column uk-height-small', style={'fontSize': '8px'})
                                ], className='uk-width-auto'),
                                html.Div([
                                    dcc.Graph(figure=goals_fig, style={'height': '150px'}),
                                    html.Hr(),
                                    html.Div([
                                        html.Div([
                                            html.Div(className='uk-border-circle',
                                                     style={'backgroundColor': custom_colours[i], 'width': '8px',
                                                            'height': '8px'}),
                                            html.Div([item], className='uk-margin-small-left uk-text-small')
                                        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in enumerate(
                                            goals_list)
                                    ], className='uk-flex uk-flex-wrap')
                                ])
                            ], **{'data-uk-grid': 'true'},
                                className='uk-grid-divider uk-child-width-expand uk-grid-small')
                        ], className='uk-card-body')
                    ], className='uk-card uk-card-default')
                ])

            ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')

        ], className='uk-container')
    ], className='uk-section')


@callback(
    Output('payout-url', 'href'),
    State('profile-id-store', 'data'),
    State('account_id', 'value'),
    Input('payment_date', 'date'),
    State('amount', 'value'),
    Input('add-pay-btn', 'n_clicks'),
    prevent_initial_callback=True
)
def post(profile_id, account_id, payment_date, amount, n_clicks):
    with Session(engine) as session:
        if n_clicks and account_id and payment_date and amount:
            session.add(DividendOrPayout(
                account_id=account_id, amount=amount, payment_date=payment_date
            ))
            session.commit()
            return f'/edit/{profile_id}/'
