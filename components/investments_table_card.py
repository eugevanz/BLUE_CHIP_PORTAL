from dash import html

from utils import create_delete_item, format_time, Investment, format_currency


def investments_table(investments: [Investment], profile_id: str, investments_balance: float,
                      prior_investments_balance: float):
    if prior_investments_balance == 0:
        if investments_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (investments_balance - prior_investments_balance) / prior_investments_balance * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Span(['Investments'], className='uk-text-bolder'),
                format_currency(investments_balance),
                html.Div([
                    'Compared to last month ',
                    html.Span([
                        html.Span(['+' if total_difference > 0 else '']),
                        f'{total_difference:.2f}', '%'
                    ], className=f'uk-text-{"success" if total_difference > 0 else "danger"} uk-text-bolder')
                ], className='uk-text-small uk-margin-remove-top')
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
                        ])
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ], className='uk-flex uk-flex-column uk-height-1-1')
