import base64
from typing import Dict, Type

import dash
from dash import dcc, Output, callback, Input, State, html, ALL
from dash.exceptions import PreventUpdate
from sqlalchemy.orm import Session

from utils import (
    Profile, Account, Investment, Transaction, ClientGoal,
    engine, DividendOrPayout, format_time, supabase_admin, navbar, table_item_decorator, create_table_header,
    create_table_wrapper, profile_data
)

dash.register_page(__name__, path_template='/edit/<profile_id>/', name='Edit Profile')


def create_delete_item(type_id: str, item_id: str):
    return html.Td([
        html.A(**{'data-uk-icon': 'icon: trash; ratio: 0.8'}, className='uk-icon-button uk-text-danger'),
        html.Div([
            html.Div('Are you sure?', className='uk-card-body uk-text-center'),
            html.Div([
                html.Div([
                    html.Button('Cancel', className='uk-button uk-button-primary uk-drop-close'),
                    html.Button('Delete', className='uk-button uk-button-danger',
                                id={'type': type_id, 'index': item_id})
                ], **{'data-uk-margin': 'true'})
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default',
            **{'data-uk-dropdown': 'mode: click; pos: top-left; shift: false; flip: false'})
    ])


@table_item_decorator
def accounts_table(accounts: [Account]):
    """Generates the account management UI for a given client profile."""
    header = create_table_header([
        html.Th('', className=f'uk-table-shrink'),
        html.Th('Balance', className=f'uk-table-expand'),
        html.Th('Account Type', className=f'uk-table-expand'),
        html.Th('Account', className=f'uk-table-expand'),
        html.Th('Last Update', className=f'uk-table-expand')
    ], style={'backgroundColor': '#2A3A58'})
    body = html.Tbody([
        html.Tr([
            create_delete_item(type_id='delete_account', item_id=str(account.id)),
            html.Td(f'R {account.balance:,.2f}'),
            html.Td(account.account_type, className='uk-text-bolder uk-text-uppercase'),
            html.Td(account.account_number),
            html.Td(format_time(account.updated_at), className='uk-text-muted')
        ], className='uk-animation-fade') for account in accounts
    ]) if accounts else None

    return create_table_wrapper(header, body, "No accounts found")


@table_item_decorator
def investments_table(investments: [Investment]):
    """Generates the investment management UI for a given client profile."""
    header = create_table_header([
        html.Th('', className=f'uk-table-shrink'),
        html.Th('Investment', className=f'uk-table-expand'),
        html.Th('Amount', className=f'uk-table-expand'),
        html.Th('Purchase Price', className=f'uk-table-expand'),
        html.Th('Current Price', className=f'uk-table-expand'),
        html.Th('Last Updated', className=f'uk-table-expand')
    ], style={'backgroundColor': '#2A3A58'})
    body = html.Tbody([
        html.Tr([
            create_delete_item(type_id='delete_investment', item_id=str(investment.id)),
            html.Td(html.Span(investment.investment_type, className='uk-text-bolder uk-text-uppercase')),
            html.Td(investment.quantity),
            html.Td(f'R {investment.purchase_price:,.2f}'),
            html.Td(f'R {investment.current_price:,.2f}'),
            html.Td(format_time(investment.purchase_date))
        ], className='uk-animation-fade') for investment in investments
    ])

    return create_table_wrapper(header, body, "No accounts found")


@table_item_decorator
def transactions_table(transactions: [Transaction]):
    """Generates the transaction management UI for a given client profile."""
    header = create_table_header([
        html.Th('', className=f'uk-table-shrink'),
        html.Th('Description', className=f'uk-table-expand'),
        html.Th('Transaction Type', className=f'uk-table-expand'),
        html.Th('Amount', className=f'uk-table-expand'),
        html.Th('Last Updated', className=f'uk-table-expand')
    ], style={'backgroundColor': '#2A3A58'})
    body = html.Tbody([
        html.Tr([
            create_delete_item(type_id='delete_transaction', item_id=str(transaction.id)),
            html.Td(transaction.description),
            html.Td(transaction.type,
                    className=f'uk-text-{"success" if transaction.type == "debit" else "danger"}'),
            html.Td(f'R {transaction.amount:,.2f}'),
            html.Td(format_time(transaction.created_at))
        ], className='uk-animation-fade') for transaction in transactions
    ])

    return create_table_wrapper(header, body, "No accounts found")


@table_item_decorator
def client_goals_table(client_goals: [ClientGoal]):
    """Generates the client goals management UI for a given client profile."""
    header = create_table_header([
        html.Th('', className=f'uk-table-shrink'),
        html.Th('Current Savings', className=f'uk-table-expand'),
        html.Th('Target Amount', className=f'uk-table-expand'),
        html.Th('Goal', className=f'uk-table-expand'),
        html.Th('Target Date', className=f'uk-table-expand')
    ], style={'backgroundColor': '#2A3A58'})
    body = html.Tbody([
        html.Tr([
            create_delete_item(type_id='delete_goal', item_id=str(goal.id)),
            html.Td(f'R {goal.current_savings:,.2f}'),
            html.Td(f'R {goal.target_amount:,.2f}'),
            html.Td(html.Span(goal.goal_type, className='uk-text-bolder uk-text-uppercase')),
            html.Td(format_time(goal.target_date))
        ], className='uk-animation-fade') for goal in client_goals
    ])

    return create_table_wrapper(header, body, "No accounts found")


@table_item_decorator
def payouts_table(dividends_and_payouts: [DividendOrPayout]):
    """Generates the payouts management UI for a given client profile."""
    header = create_table_header([
        html.Th('', className=f'uk-table-shrink'),
        html.Th('Payment Date', className=f'uk-table-expand'),
        html.Th('Amount', className=f'uk-table-expand')
    ], style={'backgroundColor': '#2A3A58'})

    body = html.Tbody([
        html.Tr([
            create_delete_item(type_id='delete_payout', item_id=str(payout.id)),
            html.Td(format_time(payout.payment_date)),
            html.Td(f'R {payout.amount:,.2f}')
        ], className='uk-animation-fade') for payout in dividends_and_payouts
    ])

    return create_table_wrapper(header, body, "No accounts found")


def user_profile(profile: Profile):
    # Fallback values
    default_picture_url = ('https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                           '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp')

    profile_data = {
        'picture_url': profile.profile_picture_url or default_picture_url,
        'first_name': profile.first_name or 'First Name',
        'last_name': profile.last_name or 'Last Name',
        'created_at': profile.created_at.strftime("%B %d, %Y") if profile.created_at else 'Unknown',
        'email': profile.email or 'No email provided'
    }

    return html.Div([
        dcc.Store('profile-pic-store', data=profile_data['picture_url']),
        html.Div([
            html.Div([
                html.Img(
                    src=profile_data['picture_url'],
                    alt='Profile Picture',
                    className='uk-cover',
                    **{'data-uk-cover': 'true'},
                    id='profile_pic'
                ),
                html.Canvas(width='256', height='256'),
                dcc.Upload(
                    html.A(**{'data-uk-icon': 'icon: pencil; ratio: 1.5'}),
                    className='uk-position-bottom-right uk-padding',
                    id='upload-image'
                )
            ], className='uk-cover-container uk-inline')
        ], className='uk-width-2-5'),
        html.Div([
            html.Div([
                dcc.Input(
                    className='uk-form-blank uk-text-bolder uk-width-1-1 uk-h2 uk-margin-remove uk-text-secondary',
                    value=profile_data['first_name'],
                    debounce=True,
                    id='first_name'
                ),
                dcc.Input(
                    className='uk-form-blank uk-text-bolder uk-width-1-1 uk-h2 uk-margin-remove-top',
                    value=profile_data['last_name'],
                    debounce=True,
                    id='last_name'
                ),
                html.Div([
                    f'Member since {profile_data["created_at"]}',
                    html.Div(
                        profile_data['email'],
                        className='uk-text-bolder',
                        style={'fontSize': '11px'}
                    )
                ], className='uk-text-small')
            ], className='uk-card uk-card-body uk-light uk-inline')
        ], className='uk-width-3-5')
    ], className='uk-grid-collapse uk-grid-match', **{'data-uk-grid': 'true'})


def create_confirm_overlay():
    return html.Div([
        html.Div([
            'Are you sure you want to delete this item?'
        ], className='uk-card uk-card-body uk-card-default uk-position-cover uk-overflow-auto')
    ], **{'data-uk-dropdown': 'mode: click'})


def create_section_card(title, table_component, add_link, profile_id, total=0, prior=0):
    if prior == 0:
        if total == 0:
            total_difference = 0  # No change if both are zero
        else:
            total_difference = float('inf')  # Represent as an infinite increase if prior_total is zero but total is not
    else:
        total_difference = (total - prior) / prior * 100

    header = html.Div([
        html.H2([f'R {total:,.2f}'.replace(",", " ")],
                className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
        html.Div(['Compared to last month ', html.Span([
            html.Span(['+' if total_difference > 0 else '']), f'{total_difference:.2f}', '%'
        ], className=f'uk-text-{"success" if total_difference > 0 else "danger"}')],
                 className='uk-text-small uk-margin-remove-top')
    ])

    return html.Div([
        html.Div([
            html.Div([html.Span([title], className='uk-text-bolder'), header],
                     className='uk-card-header uk-flex uk-flex-between uk-flex-bottom'),
            html.Div(table_component, className='uk-card-body'),
            html.Div(
                html.A([
                    html.Span(**{
                        'data-uk-icon': 'icon: plus; ratio: 0.6'
                    }, className='uk-margin-small-right'),
                    f'Add {title}'
                ], className='uk-button uk-button-text uk-flex uk-flex-middle',
                    href=f'{add_link}/{profile_id}/'),
                className='uk-card-footer'
            )
        ], className='uk-card uk-card-default dropdown uk-light', style={'backgroundColor': '#2A3A58'})
    ])


def layout(profile_id: str):
    """Creates the layout for a client's profile page."""
    data = profile_data(profile_id)
    profile = data['profile']
    accounts = data['accounts']
    accounts_balance = data['accounts_balance']
    prior_accounts_balance = data['prior_accounts_balance']
    dividends_and_payouts = data['dividends_and_payouts']
    payouts_balance = data['payouts_balance']
    prior_payouts_balance = data['prior_payouts_balance']
    client_goals = data['client_goals']
    client_goals_balance = data['client_goals_balance']
    prior_client_goals_balance = data['prior_client_goals_balance']
    transactions = data['transactions']
    transactions_balance = data['transactions_balance']
    prior_transactions_balance = data['prior_transactions_balance']
    investments = data['investments']
    investments_balance = data['investments_balance']
    prior_investments_balance = data['prior_investments_balance']

    sections = [
        ('Accounts', accounts_table(accounts), '/add-account', accounts_balance, prior_accounts_balance),
        ('Investments', investments_table(investments), '/add-investment', investments_balance,
         prior_investments_balance),
        ('Transactions', transactions_table(transactions), '/add-transaction', transactions_balance,
         prior_transactions_balance),
        ('Client Goals', client_goals_table(client_goals), '/add-client-goal', client_goals_balance,
         prior_client_goals_balance),
        ('Dividends/Payouts', payouts_table(dividends_and_payouts), '/add-payout', payouts_balance,
         prior_payouts_balance)
    ]

    return html.Div([
        html.Div(id='edit-nav',
                 **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'}),
        dcc.Location(id='edit-url'),
        html.Div([
            dcc.Store('profile-id-store', data=profile_id),
            html.Div(id='refresh-trigger', style={'display': 'none'}),
            html.Div(
                html.Div([
                    html.Div(user_profile(profile)),
                    *[create_section_card(title, component, link, profile_id, total, prior)
                      for title, component, link, total, prior in sections]
                ], className="uk-child-width-1-2@m", **{'data-uk-grid': 'masonry: pack'}),
                className='uk-container'
            )
        ], className='uk-section', style={'backgroundColor': '#88A9C3'})
    ])


@callback(
    Output('profile_pic', 'src'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('profile-id-store', 'data'),
    State('profile-pic-store', 'data'),
    prevent_initial_callback=True
)
def update_profile_pic(contents, filename, profile_id, profile_pic):
    if not contents: return profile_pic

    # MAX_FILE_SIZE = 5 * 1024 * 1024
    content_type, content_string = contents.split(',')
    if not content_type.startswith('data:image/'): return profile_pic

    try:
        data = base64.b64decode(content_string)
        response = supabase_admin.storage.from_('profile_pics').upload(
            filename,
            data,
            file_options={'content-type': content_type, 'upsert': 'true'}
        )

        if response:
            public_url = supabase_admin.storage.from_('profile_pics').get_public_url(filename)
            with Session(engine) as session:
                profile = session.query(Profile).filter_by(id=profile_id).first()
                if profile:
                    profile.profile_picture_url = public_url
                    session.commit()
                    return public_url
    except Exception as e:
        print(f"Error updating profile picture: {e}")

    return profile_pic


@callback(
    State('profile-id-store', 'data'),
    Input('first_name', 'value'),
    Input('last_name', 'value')
)
def update_name(profile_id, first_name, last_name):
    if not any([first_name, last_name]):
        raise PreventUpdate

    with Session(engine) as session:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if first_name is not None:
            profile.first_name = first_name
        if last_name is not None:
            profile.last_name = last_name
        session.commit()


@callback(
    Output('edit-nav', 'children'),
    Input('edit-url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)


# Model mapping dictionary
MODEL_MAPPING: Dict[str, Type[Account | Investment | Transaction | ClientGoal | DividendOrPayout]] = {
    'delete_account': Account,
    'delete_investment': Investment,
    'delete_transaction': Transaction,
    'delete_goal': ClientGoal,
    'delete_payout': DividendOrPayout
}


def create_delete_callback(delete_type: str):
    """
    Factory function to create delete callbacks for different models.

    Args:
        delete_type (str): The type of delete operation (e.g., 'delete_account')
    """
    model = MODEL_MAPPING[delete_type]

    @callback(
        Output('edit-url', 'href', allow_duplicate=True),
        Input({'type': delete_type, 'index': ALL}, 'n_clicks'),
        State({'type': delete_type, 'index': ALL}, 'id'),
        State('profile-id-store', 'data'),
        prevent_initial_call=True
    )
    def delete_handler(n_clicks, ids, profile_id):
        if not n_clicks or not any(n_clicks):
            raise PreventUpdate

        clicked_index = next((i for i, clicks in enumerate(n_clicks) if clicks), None)
        if clicked_index is None:
            raise PreventUpdate

        item_id = ids[clicked_index]['index']
        with Session(engine) as session:
            session.delete(session.query(model).filter_by(id=item_id).first())
            session.commit()
            return f'/edit/{profile_id}/'

    return delete_handler


# Create all delete callbacks
delete_account = create_delete_callback('delete_account')
delete_investment = create_delete_callback('delete_investment')
delete_transaction = create_delete_callback('delete_transaction')
delete_goal = create_delete_callback('delete_goal')
delete_payout = create_delete_callback('delete_payout')
