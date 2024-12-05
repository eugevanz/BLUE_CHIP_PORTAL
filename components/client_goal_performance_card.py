import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input, callback

from utils import custom_colours, lighter_colours, fig_layout, cur


def client_goal_performance(order: str = None, dark: bool = True):
    return html.Div([
        dcc.Store('name', data='client_goals'),
        dcc.Store('profile_id'),
        dcc.Store('column', data='current_savings'),
        html.Div([
            html.Div([
                html.Div('Client Goals performance', className='uk-text-small'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div(id='highest_'),
                            html.Div(id='mid_', className='uk-margin-auto-vertical'),
                            html.Div(id='lowest_')
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='goals_fig', style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(id='legend', className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]} if dark else {})
    ], className=order)


@callback(
    Output('goals_fig', 'figure'),
    Output('legend', 'children'),
    Input('profile_id', 'data')
)
def get_goals_fig(profile_id):
    client_goals = cur.execute('SELECT * FROM client_goals WHERE profile_id = ?', (profile_id,)).fetchall()

    goals_df = pd.DataFrame([{
        'Type': goal.goal_type,
        'Current Savings': goal.current_savings,
        'Target Amount': goal.target_amount
    } for goal in client_goals])
    goals_list = goals_df['Type'].tolist()
    goals_fig = px.bar(goals_df, x='Type', y=['Current Savings', 'Target Amount'], color_discrete_map={
        'Current Savings': custom_colours, 'Target Amount': lighter_colours
    })
    goals_fig.update_layout(**fig_layout)

    return goals_fig, [
        html.Div([
            html.Div(className='uk-border-circle',
                     style={'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'}),
            html.Div([item], className='uk-margin-small-left uk-text-small')
        ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in enumerate(goals_list)
    ]
