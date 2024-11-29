from dash import html

from utils import ClientGoal, format_time, create_delete_item, format_currency


def client_goals_table(client_goals: [ClientGoal], profile_id: str, client_goals_balance: float,
                       prior_client_goals_balance: float):
    if prior_client_goals_balance == 0:
        if client_goals_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (client_goals_balance - prior_client_goals_balance) / prior_client_goals_balance * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Span(['Client Goals'], className='uk-text-bolder'),
                format_currency(client_goals_balance),
                html.Div([
                    'Compared to last month ',
                    html.Span([
                        html.Span(['+' if total_difference > 0 else '']),
                        f'{total_difference:.2f}', '%'
                    ], className=f'uk-text-{"success" if total_difference > 0 else "danger"} uk-text-bolder')
                ], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('', className=f'uk-table-shrink'),
                                html.Th('Current Savings', className=f'uk-table-expand'),
                                html.Th('Target Amount', className=f'uk-table-expand'),
                                html.Th('Goal', className=f'uk-table-expand'),
                                html.Th('Target Date', className=f'uk-table-expand')
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                create_delete_item(type_id='delete_goal', item_id=str(goal.id)),
                                html.Td(f'R {goal.current_savings:,.2f}'),
                                html.Td(f'R {goal.target_amount:,.2f}'),
                                html.Td(html.Span(goal.goal_type, className='uk-text-bolder uk-text-uppercase')),
                                html.Td(format_time(goal.target_date))
                            ]) for goal in client_goals
                        ])
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], className='uk-overflow-auto uk-height-large')
            ], className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{'data-uk-icon': 'icon: plus; ratio: 0.6'}, className='uk-margin-small-right'),
                    'Add goal'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'/add-client-goal/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ])
