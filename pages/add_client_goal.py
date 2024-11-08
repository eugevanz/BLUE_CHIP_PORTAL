from datetime import date

import dash
from dash import dcc, callback, Output, State, Input, html
from sqlalchemy.orm import Session

from utils import ClientGoal, engine, navbar, client_goal_performance, account_performance, dividend_performance, \
    investment_performance, transaction_performance

dash.register_page(__name__, path_template='/add-client-goal/<profile_id>/', name='Add Client Goal')


def layout(profile_id: str):
    return html.Div([
        html.Div(id='goal-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        html.Div([
            dcc.Location(id='goal-url'),
            dcc.Store(id='profile-id-store', data=profile_id),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(['Add Client Goal']),
                            html.P(['Adding client goals involves setting up specific, measurable objectives tailored '
                                    'to each client’s financial plan. This process typically includes defining the '
                                    'goal (e.g., saving a certain amount by a target date), establishing milestones, '
                                    'and tracking progress over time. Visual representations, such as progress bars '
                                    'or gauge charts, are often used to display these goals within a dashboard, '
                                    'making it easy for both the client and advisor to monitor achievement levels. '],
                                   className='uk-text-meta'),

                            html.Div([
                                html.Div('Goal', className='uk-text-small'),
                                html.Div([
                                    dcc.Dropdown([
                                        {'label': option, 'value': option} for option in [
                                            'Retirement Savings', 'Emergency Fund', 'Education Fund', 'Home Purchase',
                                            'Debt Reduction', 'Vacation Fund', 'Investment Growth', 'Business Start-Up',
                                            'Charitable Giving', 'Wealth Accumulation', 'Major Purchase',
                                            'Health and Wellness', 'Estate Planning', 'Early Retirement',
                                            'Legacy Planning'
                                        ]
                                    ], placeholder='Select account type', style={'color': '#172031'}, id='goal_type')
                                ], className='uk-text-bolder uk-margin-remove-top')
                            ], className='uk-margin'),  # Field for goal type

                            html.Div([
                                html.Div('Current Savings', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Current Savings',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='current_savings'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Target Amount', className='uk-text-small'),
                                html.Div([
                                    html.Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                                    dcc.Input(
                                        type='number',
                                        placeholder='Target Amount',
                                        className='uk-input uk-text-bolder uk-form-width-large',
                                        id='target_amount'
                                    )
                                ], className='uk-margin-remove-top uk-inline')
                            ], className='uk-margin'),

                            html.Div([
                                html.Div('Target Date', className='uk-text-small'),
                                dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                                     id='target_date', date=date.today())
                            ], className='uk-margin'),

                            html.Button('Save', id='add-goa-btn', className='uk-button uk-button-primary uk-margin')
                        ], className='uk-card uk-card-body uk-margin-large-bottom')
                    ]),

                    client_goal_performance('uk-flex-first@l'),
                    account_performance(),
                    dividend_performance(),
                    investment_performance(),
                    transaction_performance()

                ], **{'data-uk-grid': 'masonry: pack'}, className='uk-child-width-1-2@m')
            ], className='uk-container')
        ], className='uk-section')
    ])


@callback(
    Output('goal-url', 'href'),
    State('profile-id-store', 'data'),
    State('goal_type', 'value'),
    State('current_savings', 'value'),
    State('target_amount', 'value'),
    Input('target_date', 'date'),
    Input('add-goa-btn', 'n_clicks')
)
def add_client_goal(profile_id, goal_type, current_savings, target_amount, target_date, n_clicks):
    with Session(engine) as session:
        if n_clicks and goal_type and current_savings and target_amount and target_date:
            session.add(ClientGoal(
                current_savings=current_savings, goal_type=goal_type, profile_id=profile_id,
                target_amount=target_amount, target_date=target_date
            ))
            session.commit()
            return f'/edit/{profile_id}/'


@callback(
    Output('goal-nav', 'children'),
    Input('goal-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)
