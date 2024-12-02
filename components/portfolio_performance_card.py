from dash import html, dcc
from shortnumbers import millify

from utils import format_time, portfolio_fig, portfolio_df, custom_colours, format_currency


def portfolio_performance(width_class: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Portfolio Value', className='uk-text-small'),
                format_currency(9657083.35),
                html.Div([
                    'Compared to last month ',
                    html.Span('+24.17%', className='uk-text-success uk-text-bolder')
                ], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {millify(100000)}']),
                            html.Div([f'R {millify(500000)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(10000)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=portfolio_fig, className='uk-height-medium', config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                format_time(item)
                            ]) for item in [
                                portfolio_df['Month'].iloc[0],
                                portfolio_df['Month'].iloc[int(len(portfolio_df) * 0.5)],
                                portfolio_df['Month'].iloc[-1]
                            ]
                        ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(className='uk-border-circle', style={
                            'backgroundColor': custom_colours[i], 'width': '8px', 'height': '8px'
                        }),
                        html.Div([item], className='uk-margin-small-left uk-text-uppercase')
                    ], className='uk-flex uk-flex-middle uk-margin-right uk-margin-small-bottom') for i, item in
                    enumerate(portfolio_df.columns[1:])
                ], className='uk-flex uk-flex-wrap', style={'fontSize': '11px'})
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[-1]})
    ], className=width_class)
