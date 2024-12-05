from dash import html, dcc

from utils import create_delete_item, format_time, custom_colours, cur


def payouts_table(profile_id: str):
    dividends_payouts = cur.execute(
        'SELECT dp.* FROM dividends_payouts dp JOIN accounts a ON dp.account_id = a.id WHERE a.profile_id = ?',
        (profile_id,)
    ).fetchall() or []

    return html.Div([
        dcc.Store('profile_id', data=profile_id),
        dcc.Store('name', data='dividends_payouts'),
        html.Div([
            html.Div([
                html.Span(['Dividends/Payouts'], className='uk-text-bolder'),
                html.Span(id='total_summary'),
                html.Div(id='card_header', className='uk-text-small uk-margin-remove-top')
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
                            ]) for payout in dividends_payouts
                        ]) if dividends_payouts else None
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
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[-1]})
    ])
