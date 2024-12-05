import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Output, Input
from shortnumbers import millify

from utils import custom_colours, accounts_balance, client_goals_balance, investments_balance, payouts_balance, \
    transactions_balance, fig_layout, all_total_prior


def performance_summary(is_client: bool = False, width_class: str = None):
    total, _ = all_total_prior()

    return html.Div([
        dcc.Store('is_client', data=is_client),
        dcc.Store('profile_id'),
        dcc.Store('name', data='all'),
        html.Div([
            html.Div([
                html.Div(['Performance Summary'], className='uk-text-small'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {millify(total)}']),
                            html.Div([f'R {millify(total / 2)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(10_000)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='performance_fig', className='uk-height-medium', config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(['Over the lifetime of the portfolio'], style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div(id='card-footer', className='uk-card-footer')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]})
    ], className=width_class, id='performance-summary')


@callback(
    Output('performance_fig', 'figure'),
    Output('card-footer', 'children'),
    Input('is_client', 'data'),
    Input('profile_id', 'data')
)
def get_performance_fig(is_client, profile_id):
    card_footer = lambda df: html.Div([
        html.Div([
            html.Div(className='uk-border-circle', style={
                'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
            }),
            html.Div([
                html.Div([item], className='uk-text-uppercase'),
                html.Div([f'R {value:,.2f}'], className='uk-text-bolder')
            ], className='uk-margin-small-left')
        ], className='uk-flex uk-flex-middle uk-margin-right uk-margin-small-bottom') for i, item, value in
        [(i, row[0], row[1]) for i, row in enumerate(performance_df.itertuples(index=False, name=None))]
    ], className='uk-flex uk-flex-wrap', style={'fontSize': '11px'})

    if is_client:
        performance_df = pd.DataFrame({
            'Metric': ['Account Balance', 'Goal Progress', 'Investment Balance', 'Dividends', 'Total Transactions'],
            'Total Value': [accounts_balance(profile_id=profile_id), client_goals_balance(profile_id=profile_id),
                            investments_balance(profile_id=profile_id), payouts_balance(profile_id=profile_id),
                            transactions_balance(profile_id=profile_id)]
        })
        performance_fig = px.bar(
            performance_df, x='Metric', y='Total Value', color='Metric',
            color_discrete_sequence=custom_colours
        )
        performance_fig.update_layout(**fig_layout)

        return performance_fig, card_footer(performance_df)
    else:
        performance_df = pd.DataFrame({
            'Metric': ['Account Balance', 'Goal Progress', 'Investment Balance', 'Dividends', 'Total Transactions'],
            'Total Value': [accounts_balance, client_goals_balance, investments_balance, payouts_balance,
                            transactions_balance]
        })
        performance_fig = px.bar(
            performance_df, x='Metric', y='Total Value', color='Metric',
            color_discrete_sequence=custom_colours
        )
        performance_fig.update_layout(**fig_layout)

        return performance_fig, card_footer(performance_df)
