from dash import html, dcc

from utils import create_delete_item, format_time, custom_colours, cur


def investments_table(profile_id: str):
    investments = cur.execute(
        'SELECT i.* FROM investments i JOIN accounts a ON i.account_id = a.id WHERE a.profile_id = ?', (profile_id,)
    ).fetchall() or []

    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='investments'),
        html.Div([
            html.Div([
                html.Span(['Investments'], className='uk-text-bolder'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('', className=f'uk-table-shrink'),
                                html.Th('Investment', className=f'uk-table-expand'),
                                html.Th('Amount', className=f'uk-table-expand'),
                                html.Th('Purchase Price', className=f'uk-table-expand'),
                                html.Th('Current Price', className=f'uk-table-expand'),
                                html.Th('Last Updated', className=f'uk-table-expand')
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                create_delete_item(type_id='delete_investment', item_id=str(investment.id)),
                                html.Td(html.Span(investment.investment_type,
                                                  className='uk-text-bolder uk-text-uppercase')),
                                html.Td(investment.quantity),
                                html.Td(f'R {investment.purchase_price:,.2f}'),
                                html.Td(f'R {investment.current_price:,.2f}'),
                                html.Td(format_time(investment.purchase_date))
                            ]) for investment in investments
                        ]) if investments else None
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], className='uk-overflow-auto uk-height-large')
            ], className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{
                        'data-uk-icon': 'icon: plus; ratio: 0.6'
                    }, className='uk-margin-small-right'),
                    'Add Investments'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'/add-investment/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[-1]})
    ], className='uk-flex uk-flex-column uk-height-1-1')
