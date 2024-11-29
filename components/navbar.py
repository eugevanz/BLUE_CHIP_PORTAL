import yfinance as yf
from dash import html


def get_symbol_data(symbol, is_commodity=False):
    current_price = yf.Ticker(symbol).info.get('previousClose' if is_commodity else 'currentPrice')
    previous_close = yf.Ticker(symbol).info.get('open')

    return dict(
        symbol=yf.Ticker(symbol).info.get('shortName'),
        current_price=yf.Ticker(symbol).info.get('previousClose' if is_commodity else 'currentPrice'),
        change=((current_price - previous_close) / previous_close) * 100
    )


def navbar(paths: list):
    tickers = [
        get_symbol_data(symbol, is_commodity=False if symbol in [
            'MSFT', 'GOOGL', 'AAPL'
        ] else True) for symbol in [
            'MSFT', 'GOOGL', 'AAPL', '^GSPC', '^FTSE', '^DJI', '^IXIC'
        ]
    ]

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(
                            src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                                '/Blue%20Chip%20Invest%20Logo.001.png',
                            width='60', height='60'),
                        html.Div(['BLUE CHIP INVESTMENTS'],
                                 style={'fontFamily': '"Noto Sans", sans-serif',
                                        'fontOpticalSizing': 'auto',
                                        'fontWeight': '400', 'fontStyle': 'normal', 'lineHeight': '22px',
                                        'color': '#091235', 'width': '164px'})
                    ], className='uk-logo uk-flex')
                ], className='uk-width-auto'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(ticker['symbol'],
                                         style={'fontSize': '11px', 'height': '14px', 'overflow': 'hidden'}),
                                html.Div(f'R {ticker["current_price"]:,.2f}',
                                         className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                                html.Div([
                                    f'{ticker["change"]:,.2f}% ',
                                    html.Span(
                                        **{
                                            'data-uk-icon': f'triangle-{"up" if ticker["change"] > 0 else "down"}'},
                                        className=f'uk-text-{"success" if ticker["change"] > 0 else "danger"}')
                                ], className='uk-text-small uk-margin-remove-top')
                            ]) for ticker in tickers
                        ], className='uk-slider-items uk-child-width-1-2 uk-child-width-1-4@s '
                                     'uk-child-width-1-6@m uk-grid')
                    ], **{'data-uk-slider': 'autoplay: true'})
                ], className='uk-width-expand')
            ], **{'data-uk-grid': 'true'},
                className='uk-grid-medium uk-flex-middle uk-child-width-1-2@m'),
            html.Hr(),
            html.Div([
                html.Nav([
                    html.Ul([
                        html.Li([
                            html.A([title], href=href) if index < len(paths) - 1 else html.Span([title])
                        ]) for index, (title, href) in enumerate(paths)
                    ], className='uk-breadcrumb')
                ])
            ], className='uk-width-1-1')
        ], className='uk-container')
    ], className='uk-section-xsmall')
