from dash import html, dcc

from utils import format_time, create_delete_item, custom_colours, cur


def client_goals_table(profile_id: str):
    client_goals = cur.execute('SELECT * FROM client_goals WHERE profile_id = ?', (profile_id,)).fetchall() or []

    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='client_goals'),
        html.Div([
            html.Div([
                html.Span(['Client Goals'], className='uk-text-bolder'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
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
                        ]) if client_goals else None
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[-1]})
    ])
