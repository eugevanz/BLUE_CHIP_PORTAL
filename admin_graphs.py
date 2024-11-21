import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from dash import html, dcc, callback, Output, Input
from shortnumbers import millify

from utils import format_time, portfolio_fig, portfolio_df, custom_colours, assets_fig, assets_df, fig_layout


def market_performance():
    msft_current_price = yf.Ticker('MSFT').info.get('currentPrice')
    msft_previous_close = yf.Ticker('MSFT').info.get('open')
    msft_change = ((msft_current_price - msft_previous_close) / msft_previous_close) * 100

    nasdaq_current_price = yf.Ticker('^IXIC').info.get('previousClose')
    nasdaq_previous_close = yf.Ticker('^IXIC').info.get('open')
    nasdaq_change = ((nasdaq_current_price - nasdaq_previous_close) / nasdaq_previous_close) * 100

    jones_current_price = yf.Ticker('^DJI').info.get('previousClose')
    jones_previous_close = yf.Ticker('^DJI').info.get('open')
    jones_change = ((jones_current_price - jones_previous_close) / jones_previous_close) * 100

    ftse_current_price = yf.Ticker('^FTSE').info.get('previousClose')
    ftse_previous_close = yf.Ticker('^FTSE').info.get('open')
    ftse_change = ((ftse_current_price - ftse_previous_close) / ftse_previous_close) * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('Market performance', className='uk-text-small'),
                        html.H2(id='current-price',
                                className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                        html.Div([
                            'Compared to previous close ',
                            html.Span(id='price-change', className='uk-text-bolder'), html.Span(['%'])
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    dcc.Dropdown([
                        {'label': 'S&P 500', 'value': '^GSPC'},
                        {'label': 'NASDAQ', 'value': '^IXIC'},
                        {'label': 'Dow Jones', 'value': '^DJI'},
                        {'label': 'FTSE 100', 'value': '^FTSE'},
                        {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                        {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                        {'label': 'Google (GOOGL)', 'value': 'GOOGL'}
                    ], '^GSPC', id='ticker-dropdown',
                        className='uk-select uk-form-small uk-form-blank uk-width-small', clearable=False)
                ], className='uk-flex uk-flex-between uk-flex-bottom')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='y-ticks', className='uk-flex uk-flex-column uk-height-medium',
                                 style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(id='market-graph', style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div(id='x-ticks', className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('MSFT', style={'fontSize': '11px'}),
                        html.Div(f'R {msft_current_price:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            f'{msft_change:,.2f}% ',
                            html.Span(**{'data-uk-icon': f'triangle-{"up" if msft_change > 0 else "down"}'},
                                      className=f'uk-text-{"success" if msft_change > 0 else "danger"}')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('NASDAQ', style={'fontSize': '11px'}),
                        html.Div(f'R {nasdaq_current_price:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            f'{nasdaq_change:,.2f}% ',
                            html.Span(**{'data-uk-icon': f'triangle-{"up" if nasdaq_change > 0 else "down"}'},
                                      className=f'uk-text-{"success" if nasdaq_change > 0 else "danger"}')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('Dow Jones', style={'fontSize': '11px'}),
                        html.Div(f'R {jones_current_price:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            f'{jones_change:,.2f}% ',
                            html.Span(**{'data-uk-icon': f'triangle-{"up" if jones_change > 0 else "down"}'},
                                      className=f'uk-text-{"success" if jones_change > 0 else "danger"}')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('FTSE 100', style={'fontSize': '11px'}),
                        html.Div(f'R {ftse_current_price:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            f'{ftse_change:,.2f}% ',
                            html.Span(**{'data-uk-icon': f'triangle-{"up" if ftse_change > 0 else "down"}'},
                                      className=f'uk-text-{"success" if ftse_change > 0 else "danger"}')
                        ], className='uk-text-small uk-margin-remove-top')
                    ])
                ], className='uk-flex uk-flex-between')
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default')
    ], className='uk-width-4-5@m')


@callback(
    Output('market-graph', 'figure'),
    Output('x-ticks', 'children'),
    Output('y-ticks', 'children'),
    Output('current-price', 'children'),
    Output('price-change', 'children'),
    Input('ticker-dropdown', 'value')
)
def update_market_figure(selected_ticker):
    ticker = yf.Ticker(selected_ticker)
    market_df = ticker.history(period='1mo')
    market_df.reset_index(inplace=True)

    market_fig = go.Figure(data=[
        go.Candlestick(
            x=market_df['Date'],
            open=market_df['Open'],
            high=market_df['High'],
            low=market_df['Low'],
            close=market_df['Close'],
            increasing_line_color=custom_colours[0],
            decreasing_line_color=custom_colours[1]
        )
    ])
    market_fig.update_layout({
        'xaxis': {'showticklabels': False, 'gridwidth': 1, 'gridcolor': 'LightGrey', 'nticks': 60,
                  'rangeslider': {'visible': False}},
        'yaxis': {'showticklabels': False, 'gridwidth': 1, 'gridcolor': 'LightGrey', 'nticks': 30},
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'showlegend': False,
        'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}
    })

    x_tick_elements = [
        html.Div([format_time(item)]) for item in [
            market_df.iloc[0]['Date'],
            market_df.iloc[int(len(market_df) * 0.25)]['Date'],
            market_df.iloc[int(len(market_df) * 0.75)]['Date'],
            market_df.iloc[-1]['Date']
        ]
    ]
    highest_high = market_df['High'].max()
    lowest_low = market_df['Low'].min()
    middle_value = (highest_high + lowest_low) / 2
    y_tick_elements = [
        html.Div([f'R {highest_high:,.2f}']),
        html.Div([f'R {middle_value:,.2f}'], className='uk-margin-auto-vertical'),
        html.Div([f'R {lowest_low:,.2f}'])
    ]

    current_price = ticker.info.get(
        'previousClose' if selected_ticker not in ['MSFT', 'AAPL', 'GOOGL'] else 'currentPrice')
    previous_price = ticker.info.get('open')
    price_change = ((current_price - previous_price) / previous_price) * 100

    return market_fig, x_tick_elements, y_tick_elements, f'R {current_price:,.2f}', f'{price_change:,.2f}'


def portfolio_performance():
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Portfolio Value', className='uk-text-small'),
                html.H2([f'R {9657083.35:,.2f}'],
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                         className='uk-text-small uk-margin-remove-top')
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
                        dcc.Graph(figure=portfolio_fig, style={'height': '300px'}, config={'displayModeBar': False}),
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-1-3@m')


def asset_performance():
    return html.Div([
        html.Div([
            html.Div([
                html.Div(['Asset Allocation'], className='uk-text-small'),
                html.H2([
                    html.Span(['+']), html.Span([f'{24.17}']), '%'
                ], className='uk-text-bolder uk-text-success uk-margin-remove-top uk-margin-remove-bottom '
                             'uk-text-truncate'),
                html.Div(['Quarterly Growth Rate'],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    dcc.Graph(figure=assets_fig, style={'height': '300px'}, config={'displayModeBar': False})
                ])
            ], className='uk-card-body'),
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
                    ], className='uk-flex uk-flex-middle uk-margin-right uk-margin-small-bottom') for i, item in
                    enumerate([(row['Asset'], row['Value']) for _, row in assets_df.iterrows()])
                ], className='uk-flex uk-flex-wrap', style={'fontSize': '11px'})
            ], className='uk-card-footer'),
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-1-3@m')


def performance_summary(accounts_balance: float, payouts_balance: float, client_goals_balance: float,
                        transactions_balance: float, investments_balance: float, prior_accounts_balance: float,
                        prior_payouts_balance: float, prior_client_goals_balance: float,
                        prior_transactions_balance: float, prior_investments_balance: float):
    total = sum([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    prior = sum([
        prior_accounts_balance, prior_payouts_balance, prior_client_goals_balance, prior_transactions_balance,
        prior_investments_balance
    ])

    lowest_ = min([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    highest_ = max([accounts_balance, payouts_balance, client_goals_balance, transactions_balance, investments_balance])
    mid_ = (highest_ + lowest_) / 2

    # Check for special cases
    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

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

    return html.Div([
        html.Div([
            html.Div([
                html.Div(['Performance Summary'], className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_)}']),
                            html.Div([f'R {millify(mid_)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=performance_fig, style={'height': '300px'}, config={'displayModeBar': False})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div([
                html.Div([
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
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-width-1-3@m')
