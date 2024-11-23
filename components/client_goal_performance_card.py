import pandas as pd
import plotly.express as px
from dash import html, dcc
from shortnumbers import millify

from utils import ClientGoal, custom_colours, lighter_colours, fig_layout


def client_goal_performance(client_goals: [ClientGoal] = None, total: float = 0, prior: float = 0, order: str = None):
    goals_fig, goals_list = None, None
    lowest_target_amount, highest_target_amount, mid_price_investment = 0, 0, 0

    if client_goals:
        lowest_target_amount = min(client_goals, key=lambda x: x.current_savings, default=None).current_savings
        highest_target_amount = max(client_goals, key=lambda x: x.current_savings, default=None).current_savings
        mid_price_investment = (highest_target_amount + lowest_target_amount) / 2

        goals_df = pd.DataFrame([
            {
                'Type': goal.goal_type,
                'Current Savings': goal.current_savings,
                'Target Amount': goal.target_amount
            }
            for goal in client_goals
        ])
        goals_list = goals_df['Type'].tolist()
        goals_fig = px.bar(goals_df, x='Type', y=['Current Savings', 'Target Amount'], color_discrete_map={
            'Current Savings': custom_colours, 'Target Amount': lighter_colours
        })
        goals_fig.update_layout(**fig_layout)

    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Client Goals performance', className='uk-text-small'),
                html.H2([f'R {total:,.2f}'.replace(',', ' ')],
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span([
                    html.Span(['+' if total_difference > 0 else '']),
                    f'{total_difference:.2f}', '%'
                ], className=f'uk-text-{"success" if total_difference > 0 else "danger"}')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {millify(highest_target_amount)}']),
                            html.Div([f'R {millify(mid_price_investment)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_target_amount)}'])
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=goals_fig, style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle',
                                         style={'backgroundColor': custom_colours[i], 'width': '8px',
                                                'height': '8px'}),
                                html.Div([item], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(
                                goals_list)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)
