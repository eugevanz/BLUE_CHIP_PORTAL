from dash import html, dcc

from utils import assets_df, custom_colours, assets_fig


def asset_performance(width_class: str = 'uk-width-1-4@m'):
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
    ], className=width_class)
