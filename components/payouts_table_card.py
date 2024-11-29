from dash import html

from utils import DividendOrPayout, format_currency, create_delete_item, format_time


def payouts_table(dividends_and_payouts: [DividendOrPayout], profile_id: str, payouts_balance: float,
                  prior_payouts_balance: float):
    if prior_payouts_balance == 0:
        if payouts_balance == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (payouts_balance - prior_payouts_balance) / prior_payouts_balance * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Span(['Dividends/Payouts'], className='uk-text-bolder'),
                format_currency(payouts_balance),
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
                                html.Th('Payment Date', className=f'uk-table-expand'),
                                html.Th('Amount', className=f'uk-table-expand')
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                create_delete_item(type_id='delete_payout', item_id=str(payout.id)),
                                html.Td(format_time(payout.payment_date)),
                                html.Td(f'R {payout.amount:,.2f}')
                            ]) for payout in dividends_and_payouts
                        ])
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], className='uk-overflow-auto uk-height-large')
            ], className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{
                        'data-uk-icon': 'icon: plus; ratio: 0.6'
                    }, className='uk-margin-small-right'),
                    'Add Dividends/Payouts'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'/add-payout/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': '#2A3A58'})
    ])
