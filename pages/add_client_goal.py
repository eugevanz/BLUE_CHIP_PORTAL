from datetime import date

import dash
from dash import dcc, callback, Output, State, Input
from dash.html import Div, Button, Span
from sqlalchemy.orm import Session

from utils import ClientGoal, engine

dash.register_page(__name__, path_template='/add-client-goal/<profile_id>/')


def layout(profile_id: str):
    return Div([
        dcc.Location(id='client-goals-url'),
        dcc.Store(id='profile-id-store', data=profile_id),
        Div([
            Div([
                Div([
                    Div('Goal', className='uk-text-small'),
                    Div([
                        dcc.Dropdown([
                            {'label': option, 'value': option} for option in [
                                'Retirement Savings', 'Emergency Fund', 'Education Fund', 'Home Purchase',
                                'Debt Reduction', 'Vacation Fund', 'Investment Growth', 'Business Start-Up',
                                'Charitable Giving', 'Wealth Accumulation', 'Major Purchase',
                                'Health and Wellness', 'Estate Planning', 'Early Retirement', 'Legacy Planning'
                            ]
                        ], placeholder='Select account type', style={'color': '#172031'}, id='goal_type')
                    ], className='uk-text-bolder uk-margin-remove-top')
                ], className='uk-margin'),  # Field for goal type

                Div([
                    Div('Current Savings', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                        dcc.Input(
                            type='number',
                            placeholder='Current Savings',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='current_savings'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Div([
                    Div('Target Amount', className='uk-text-small'),
                    Div([
                        Span(className='uk-form-icon', **{'data-uk-icon': f'icon: bag'}),
                        dcc.Input(
                            type='number',
                            placeholder='Target Amount',
                            className='uk-input uk-form-blank uk-text-bolder uk-form-width-large',
                            id='target_amount'
                        )
                    ], className='uk-margin-remove-top uk-inline')
                ], className='uk-margin'),

                Div([
                    Div('Target Date', className='uk-text-small'),
                    dcc.DatePickerSingle(month_format='MMMM D, YYYY', className='uk-width-large',
                                         id='target_date', date=date.today())
                ], className='uk-margin'),

                Button('Save', id='add-goa-btn', className='uk-button uk-button-primary uk-margin')
            ])
        ], className='uk-container')
    ], className='uk-section')


@callback(
    Output('client-goals-url', 'href'),
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
