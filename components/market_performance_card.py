import plotly.graph_objects as go
import yfinance as yf
from dash import html, dcc, callback, Output, Input

from utils import custom_colours, format_time


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
                    ], className='uk-light'),
                    dcc.Dropdown([
                        {'label': 'S&P 500', 'value': '^GSPC'},
                        {'label': 'NASDAQ', 'value': '^IXIC'},
                        {'label': 'Dow Jones', 'value': '^DJI'},
                        {'label': 'FTSE 100', 'value': '^FTSE'},
                        {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                        {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                        {'label': 'Google (GOOGL)', 'value': 'GOOGL'}
                    ], '^GSPC', id='ticker-dropdown',
                        className='uk-width-small', clearable=False)
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
            ], className='uk-card-body uk-light'),
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
            ], className='uk-card-footer uk-light')
        ], className='uk-card uk-card-default', style={'backgroundColor': custom_colours[0]})
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
            increasing_line_color=custom_colours[1],
            decreasing_line_color=custom_colours[-2]
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
