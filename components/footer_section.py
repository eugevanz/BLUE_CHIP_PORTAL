from dash import html


def footer(is_light: bool = True):
    return html.Div([
        html.Div([
            html.Hr(),
            html.Div([
                html.Div([
                    'BLUE CHIP INVESTMENTS'
                ], style={'fontFamily': 'Noto Sans, sans-serif', 'fontOpticalSizing': 'auto', 'fontWeight': '400',
                          'fontStyle': 'normal'}, className='uk-heading-small uk-margin-small-bottom uk-width-medium'),
                html.Div('Building Your Legacy with Trusted Growth', className='uk-text-small')
            ], className='uk-card uk-card-body'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            'Our Services'
                        ], className='uk-text-bolder uk-text-large uk-margin-small-bottom'),
                        html.Ul([
                            html.Li(html.A('Financial Planning', href='#')),
                            html.Li(html.A('Investment Management', href='#')),
                            html.Li(html.A('Retirement Planning', href='#')),
                            html.Li(html.A('Investment Analysis', href='#')),
                            html.Li(html.A('Insurance', href='#'))
                        ], className='uk-list uk-text-small')
                    ], className='uk-card uk-card-body')
                ], className='uk-width-auto'),
                html.Div([
                    html.Div([
                        html.Div([
                            'Explore'
                        ], className='uk-text-bolder uk-text-large uk-margin-small-bottom'),
                        html.Ul([
                            html.Li(html.A('About', href='#')),
                            html.Li(html.A('Services', href='#')),
                            html.Li(html.A('Careers', href='#')),
                            html.Li(html.A("FAQ's", href='#')),
                            html.Li(html.A('Partner', href='#'))
                        ], className='uk-list uk-text-small')
                    ], className='uk-card uk-card-body')
                ], className='uk-width-auto'),
                html.Div([
                    html.Div([
                        html.Div([
                            "Let's Talk"
                        ], className='uk-text-bolder uk-text-large uk-margin-small-bottom'),
                        html.P([
                            'We\'re Here to Help You Grow Your Wealth, Plan Your Future, and Achieve Your Financial '
                            'Goals'
                        ], className='uk-text-small'),
                        html.Button([
                            'Start'
                        ], className='uk-button uk-text-bolder',
                            style={'backgroundColor': '#091235', 'color': '#88A9C3'})
                    ], className='uk-card uk-card-body')
                ]),
                html.Div([
                    html.Div([
                        html.Div([
                            'Contact Us'
                        ], className='uk-text-bolder uk-text-large uk-margin-small-bottom'),
                        html.P([
                            html.Span(**{'data-uk-icon': 'icon: location'}, className='uk-icon uk-margin-small-right'),
                            'Unit 17, No.30 Surprise Road, Pinetown, 3610'
                        ], className='uk-text-small'),
                        html.P([
                            html.Span(**{'data-uk-icon': 'icon: receiver'}, className='uk-icon uk-margin-small-right'),
                            '0860 258 2447'
                        ], className='uk-text-small'),
                        html.P([
                            html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-icon uk-margin-small-right'),
                            'info@bluechipinvest.co.za'
                        ], className='uk-text-small')
                    ], className='uk-card uk-card-body')
                ], className='uk-width-expand')
            ], **{'data-uk-grid': 'true'}, className='uk-child-width-1-2 uk-child-width-1-4@m'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(**{'data-uk-icon': 'icon: facebook'}, className='uk-icon-button uk-icon'),
                        html.Span(**{'data-uk-icon': 'icon: linkedin'}, className='uk-icon-button uk-icon'),
                        html.Span(**{'data-uk-icon': 'icon: instagram'}, className='uk-icon-button uk-icon'),
                        html.Span(**{'data-uk-icon': 'icon: x'}, className='uk-icon-button uk-icon')
                    ], **{'data-uk-grid': 'true'}, className='uk-grid-small uk-child-width-auto')
                ], className='uk-grid-small')
            ], className='uk-card uk-card-body')
        ], className='uk-container')
    ], className=f'uk-section uk-section-large {"uk-light" if is_light else ""}')
