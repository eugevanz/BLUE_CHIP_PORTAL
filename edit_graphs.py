import pandas as pd
import plotly.express as px
from dash import html, dcc
from shortnumbers import millify

from utils import DividendOrPayout, format_time, Account, custom_colours, \
    Investment, fig_layout, ClientGoal, Transaction, lighter_colours


def dividend_performance(dividends_and_payouts: [DividendOrPayout] = None, total: float = 0, prior: float = 0,
                         order: str = None):
    lowest_payout, highest_payout, mid_payout = 0, 0, 0
    oldest_date, latest_date, mid_date = None, None, None
    payouts_fig = None

    if dividends_and_payouts:
        # Calculate payouts
        lowest_payout = min(dividends_and_payouts, key=lambda x: x.amount, default=None).amount
        highest_payout = max(dividends_and_payouts, key=lambda x: x.amount, default=None).amount
        mid_payout = (highest_payout + lowest_payout) / 2

        # Sort by payment_date to find the relevant dates
        sorted_payouts = sorted(dividends_and_payouts, key=lambda x: x.payment_date)
        if sorted_payouts:
            oldest_date = sorted_payouts[0].payment_date
            latest_date = sorted_payouts[-1].payment_date
            mid_date = sorted_payouts[len(sorted_payouts) // 2].payment_date

        payouts_df = pd.DataFrame({
            'Date': [payout.payment_date for payout in dividends_and_payouts],
            'Amount': [payout.amount for payout in dividends_and_payouts]
        })
        payouts_df['Date'] = pd.to_datetime(payouts_df['Date'])
        payouts_fig = px.line(payouts_df, x='Date', y='Amount', markers=True, line_shape='spline')
        payouts_fig.update_traces(line=dict(width=8), marker=dict(size=12), line_color=custom_colours[0])
        payouts_fig.update_layout(**fig_layout)

    # Calculate the percentage difference
    if prior == 0:
        total_difference = float('inf') if total != 0 else 0
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Dividend/Payout performance', className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_payout)}']),
                            html.Div([f'R {millify(mid_payout)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_payout)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=payouts_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([format_time(date)]) for date in [oldest_date, mid_date, latest_date] if date
                        ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'}, className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def account_performance(accounts: [Account] = None, total: float = 0, prior: float = 0,
                        order: str = None):
    lowest_account, highest_account, mid_account = 0, 0, 0
    account_fig = None

    if accounts is None:
        accounts = []
    else:
        lowest_account = min(accounts, key=lambda x: x.balance, default=None).balance
        highest_account = max(accounts, key=lambda x: x.balance, default=None).balance
        mid_account = (highest_account + lowest_account) / 2

        accounts_df = pd.DataFrame({
            'Date': [account.created_at for account in accounts],
            'Balance': [account.balance for account in accounts],
            'Type': [account.account_type for account in accounts]
        })
        accounts_df['Date'] = pd.to_datetime(accounts_df['Date'])
        account_fig = px.scatter(
            accounts_df, x="Date", y="Balance", size="Balance", color="Date",
            hover_data={'Date': True, 'Balance': True, 'Type': True}, size_max=60,
            color_discrete_sequence=custom_colours
        )
        account_fig.update_layout(**fig_layout)

    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Accounts performance', className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_account)}']),
                            html.Div([f'R {millify(mid_account)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_account)}'])
                        ], className='uk-flex uk-flex-column uk-height-medium',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=account_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle', style={
                                    'backgroundColor': custom_colours[i], 'width': '8px',
                                    'height': '8px'
                                }),
                                html.Div([account.account_type], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, account in
                            enumerate(accounts)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def investment_performance(investments: [Investment] = None, total: float = 0, prior: float = 0, order: str = None):
    lowest_price_investment, highest_price_investment, mid_price_investment = 0, 0, 0
    investment_fig = None

    if investments is None:
        investments = []
    else:
        lowest_price_investment = min(investments, key=lambda x: x.current_price, default=None).current_price
        highest_price_investment = max(investments, key=lambda x: x.current_price, default=None).current_price
        mid_price_investment = (highest_price_investment + lowest_price_investment) / 2

        investment_data = {
            'Investment': [investment.symbol for investment in investments],  # Use symbol as Investment name
            'Returns': [investment.current_price for investment in investments]  # Or another attribute you wish to plot
        }
        investments_df = pd.DataFrame(investment_data)
        investment_fig = px.bar(investments_df, x='Investment', y='Returns', color='Investment',
                                color_discrete_sequence=custom_colours)
        investment_fig.update_layout(**fig_layout)
    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Investments performance', className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_price_investment)}']),
                            html.Div([f'R {millify(mid_price_investment)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_price_investment)}'])
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=investment_fig, style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle', style={
                                    'backgroundColor': custom_colours[i], 'width': '8px',
                                    'height': '8px'
                                }),
                                html.Div([item.investment_type], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(investments)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def client_goal_performance(client_goals: [ClientGoal] = None, total: float = 0, prior: float = 0, order: str = None):
    goals_fig, goals_list = None, None
    lowest_target_amount, highest_target_amount, mid_price_investment = 0, 0, 0

    if client_goals:
        lowest_target_amount = min(client_goals, key=lambda x: x.current_savings, default=None).current_savings
        highest_target_amount = max(client_goals, key=lambda x: x.current_savings, default=None).current_savings
        mid_price_investment = (highest_target_amount + lowest_target_amount) / 2

        goals_df = pd.DataFrame([
            {
                'Type': goal.goal_type,
                'Current Savings': goal.current_savings,
                'Target Amount': goal.target_amount
            }
            for goal in client_goals
        ])
        goals_list = goals_df['Type'].tolist()
        goals_fig = px.bar(goals_df, x='Type', y=['Current Savings', 'Target Amount'], color_discrete_map={
            'Current Savings': custom_colours, 'Target Amount': lighter_colours
        })
        goals_fig.update_layout(**fig_layout)

    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Client Goals performance', className='uk-text-small'),
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
                            html.Div([f'R {millify(highest_target_amount)}']),
                            html.Div([f'R {millify(mid_price_investment)}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {millify(lowest_target_amount)}'])
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=goals_fig, style={'height': '150px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.Div(className='uk-border-circle',
                                         style={'backgroundColor': custom_colours[i], 'width': '8px',
                                                'height': '8px'}),
                                html.Div([item], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(
                                goals_list)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def transaction_performance(transactions: [Transaction] = None, total: float = 0, prior: float = 0, order: str = None):
    transact_fig, transact_df = None, None

    if transactions:
        transact_df = pd.DataFrame({
            'Amount': [transaction.amount for transaction in transactions],
            'Type': [transaction.type for transaction in transactions],
        }).groupby('Type')['Amount'].sum().reset_index()
        transact_fig = px.pie(transact_df, values='Amount', names='Type', color='Type', color_discrete_sequence=[
            custom_colours[0], custom_colours[1]
        ])
        transact_fig.update_layout(**fig_layout)

    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    return html.Div([
        html.Div([
            html.Div([
                html.Div('Transactions performance', className='uk-text-small'),
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
                            html.Div([
                                html.Div(className='uk-border-circle', style={
                                    'backgroundColor': custom_colours[i], 'width': '8px',
                                    'height': '8px'
                                }),
                                html.Div([
                                    html.Div([item[0]], className='uk-text-uppercase'),
                                    html.Div([f'R {item[1]:,.2f}'], className='uk-text-bolder')
                                ], className='uk-margin-small-left')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(list(transact_df.itertuples(index=False, name=None)))
                        ], className='uk-flex uk-flex-column uk-height-small',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div(
                        [dcc.Graph(figure=transact_fig, style={'height': '150px'}, config={'displayModeBar': False})])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)
