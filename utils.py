import calendar
import uuid
from datetime import datetime
from os import environ

import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html
from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey, func, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from supabase import create_client

# TURSO_DATABASE_URL = environ.get('TURSO_DATABASE_URL')
# # https://blue-chip-invest-eugevanz.aws-us-east-1.turso.io
# TURSO_AUTH_TOKEN = environ.get('TURSO_AUTH_TOKEN')
# # eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzM0MzI2NzQsImlkIjoiYjRmOGFjMzYtNjIxNy00NWRjLWJlYTgtYWM3MjlmNDkzYT
# # JhIn0.V1yYnrFHEJok_8ieZjHYv_yEv0kp3OxsoQjHa4tvKsQKH3RnG6qDq4Xj-hb9XRu7fvg_Bz0sKpwf2vpw9IGECQ
# conn = libsql.connect('blue-chip-invest.db')
# cur = conn.cursor()

SUPABASE_URL = environ.get('SUPABASE_URL')
SUPABASE_KEY = environ.get('SUPABASE_KEY')
SUPABASE_SERVICE_ROLE_KEY = environ.get('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_PASSWORD = environ.get('SUPABASE_PASSWORD')
supabase = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
supabase_admin = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_SERVICE_ROLE_KEY)

engine = create_engine(
    f'postgresql://postgres.oujdrprpkkwxeavzbaow:'
    f'{SUPABASE_PASSWORD}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres',
    pool_size=50
)
# session = sessionmaker(bind=engine)()
Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    profile_picture_url = Column(
        String,
        default='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica-koletic'
                '-7YVZYZeITc8-unsplash_3_11zon.webp'
    )
    first_name = Column(String, default='First name')
    last_name = Column(String, default='Last name')
    phone_number = Column(String, default='', nullable=True)
    profile_type = Column(String, default='client', nullable=True)
    date_of_birth = Column(DateTime, nullable=True)  # Assuming this is a date
    address = Column(String, default='', nullable=True)
    email = Column(String, default='email@address.com')

    # Relationships with other models
    accounts = relationship('Account', cascade='all, delete-orphan', backref='profile')
    client_goals = relationship('ClientGoal', cascade='all, delete-orphan', backref='profile')


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID type
    created_at = Column(DateTime, default=func.now())
    profile_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'))  # ForeignKey to Profile
    account_number = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships with other models
    transactions = relationship('Transaction', cascade='all, delete-orphan', backref='account')
    investments = relationship('Investment', cascade='all, delete-orphan', backref='account')
    dividends_or_payouts = relationship('DividendOrPayout', cascade='all, delete-orphan', backref='account')


class ClientGoal(Base):
    __tablename__ = 'client_goals'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID type
    created_at = Column(DateTime, default=func.now())
    profile_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'))  # ForeignKey to Profile
    goal_type = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_savings = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DividendOrPayout(Base):
    __tablename__ = 'dividends_and_payouts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID type
    created_at = Column(DateTime, default=func.now())
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id', ondelete='CASCADE'))  # ForeignKey to Account
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)


class Investment(Base):
    __tablename__ = 'investments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID type
    created_at = Column(DateTime, default=func.now())
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id', ondelete='CASCADE'))  # ForeignKey to Account
    investment_type = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID type
    created_at = Column(DateTime, default=func.now())
    account_id = Column(UUID(as_uuid=True),
                        ForeignKey('accounts.id', ondelete='CASCADE', onupdate='CASCADE'))  # ForeignKey to Account
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)


Base.metadata.create_all(engine, checkfirst=True)

format_time = lambda x: x.strftime('%b %d, %Y')
current_month_start = datetime(datetime.now().year, datetime.now().month, 1).strftime('%Y-%m-%d')

# Custom color palette
custom_colours = ['#88A9C3', '#091235', '#FC8C3A', '#F7EDB5', '#FFCD06', '#9ACF97', '#4B8EA9', '#7F7F7F', '#BCBD22',
                  '#17BECF', '#AEC7E8', '#899B98', '#9D0208', '#28282B']
lighter_colours = ['#ACC3D5', '#535972', '#FDAE75', '#F9F2CB', '#FFDC51', '#B8DDB6', '#81B0C3', '#A5A5A5', '#D0D164',
                   '#5DD2DD', '#C6D8EF', '#ACB9B7', '#BA4E52', '#68686B']
fig_layout = {
    'xaxis': {'showticklabels': False, 'visible': False},
    'yaxis': {'showticklabels': False, 'visible': False},
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',  # Use rgba for transparency
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'showlegend': False,
    'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
    'font': {'size': 11, 'weight': 'bold'}
}

# Set a seed for reproducibility
np.random.seed(42)

# Generate a custom date range for the data
date_range = pd.date_range(start="2024-01-01", periods=100, freq="B")  # Business days

# Generate synthetic stock data
initial_open = 150
price_changes = np.random.normal(0, 2, size=len(date_range))  # Random daily changes
open_prices = initial_open + np.cumsum(price_changes)  # Cumulative sum for continuity

# Simulate high, low, and close prices
high_prices = open_prices + np.random.uniform(0, 5, size=len(date_range))
low_prices = open_prices - np.random.uniform(0, 5, size=len(date_range))
close_prices = open_prices + np.random.uniform(-2, 2, size=len(date_range))

portfolio_df = pd.DataFrame({
    'Month': pd.date_range(start="2024-01-01", periods=12, freq="ME"),
    'Asset A': np.random.uniform(1000, 5000, size=12).cumsum(),
    'Asset B': np.random.uniform(500, 2000, size=12).cumsum(),
    'Asset C': np.random.uniform(2000, 8000, size=12).cumsum(),
    'Asset D': np.random.uniform(1000, 3000, size=12).cumsum(),
    'Asset E': np.random.uniform(300, 1500, size=12).cumsum(),
    'Asset F': np.random.uniform(500, 2500, size=12).cumsum()
})
portfolio_fig = px.area(
    portfolio_df.melt(id_vars=['Month'], var_name='Asset', value_name='Value'), x='Month', y='Value', color='Asset',
    labels={'Value': 'Portfolio Value (Currency)', 'Month': 'Month'}, template='plotly_dark',
    color_discrete_sequence=custom_colours
)
portfolio_fig.update_layout(**fig_layout)

assets_df = pd.DataFrame({
    'Asset': ['Asset A', 'Asset B', 'Asset C', 'Asset D', 'Asset E', 'Asset F', 'Asset G'],
    'Value': np.random.uniform(1000, 10000, size=7)  # Generate random values for each asset
}).sort_values(by='Value', ascending=False)
assets_fig = px.pie(assets_df, names='Asset', values='Value', color_discrete_sequence=custom_colours)
assets_fig.update_layout(**fig_layout)


def handle_api_response(_func_):
    def wrapper(*args, **kwargs):
        try:
            response = _func_(*args, **kwargs)
            if response and response.data:
                return response.data
            else:
                print(f'No data returned for function {_func_.__name__}')
        except Exception as e:
            print(f'Error fetching data from {_func_.__name__}: {e}')
        return html.Div('no data')  # Return None in case of error or no data

    return wrapper


@handle_api_response
def get_profile_details_by_email(profile_email: str):
    return supabase_admin.rpc('get_profile_details_by_email', {'profile_email': profile_email}).execute()


@handle_api_response
def get_clients():
    return supabase_admin.rpc('get_all_profiles').execute()


dt_object = lambda timestamp: datetime.strptime(
    timestamp, '%Y-%m-%dT%H:%M:%S.%f%z'
).strftime('%B %d, %Y') if timestamp else datetime.now().strftime('%B %d, %Y')

account_types = [
    'Savings Account', 'Investment Account', 'Retirement Account',
    'Brokerage Account', 'Trust Account', 'Custodial Account',
    'Taxable Account', 'Tax-Deferred Account', 'Tax-Exempt Account',
    'Money Market Account', 'Certificate of Deposit (CD) Account',
    'Mutual Fund Account', 'Pension Account',
    'Self-Directed Investment Account', 'High-Yield Savings Account',
    'Fixed-Income Account', 'Annuity Account', 'Forex Trading Account',
    'Commodities Trading Account'
]


def calc_input(label, icon, description):
    return html.Div(
        [
            html.Div(
                [
                    html.Span(**{'data-uk-icon': f'icon: {icon}'}, className='uk-form-icon'),
                    dcc.Input(placeholder=label, type='text', className='uk-input'),
                ],
                className='uk-inline'
            ),
            html.Div(description, className='uk-text-small uk-padding-small uk-padding-remove-top'),
        ],
        className='uk-margin'
    )


nav_link = lambda href, title: html.Li(
    html.A(title, href=href, **{'data-uk-toggle': 'true'})
)

return_button = html.A(
    html.Span(**{'data-uk-icon': 'icon: chevron-left; ratio: 1.5'}),
    href='#'
)

calculator_group1 = [nav_link(href, title) for href, title in [
    ("#potential-interest-calculators", "Simple Interest Calculator"),
    ("#potential-interest-calculators", "Compound Interest Calculator"),
    ("#potential-interest-calculators", "Savings Interest Calculator")
]]
calculator_group2 = [nav_link(href, title) for href, title in [
    ("#return-on-investment-calculators", "Basic ROI Calculator"),
    ("#return-on-investment-calculators", "Annualised ROI Calculator"),
    ("#return-on-investment-calculators", "Adjusted ROI for Taxes and Fees")
]]
calculator_group3 = [nav_link(href, title) for href, title in [
    ("#loan-amortisation-calculators", "Fixed-Rate Loan Amortization Calculator"),
    ("#loan-amortisation-calculators", "Adjustable-Rate Loan Amortization Calculator"),
    ("#loan-amortisation-calculators", "Mortgage Loan Amortization Calculator"),
    ("#loan-amortisation-calculators", "Car Loan Amortization Calculator")
]]
calculator_group4 = [nav_link(href, title) for href, title in [
    ("#other-relevant-financial-metrics-calculators", "Net Present Value (NPV) Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Internal Rate of Return (IRR) Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Debt-to-Income Ratio Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Break-Even Point Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Future Value (FV) Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Cash Flow Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Payback Period Calculator"),
    ("#other-relevant-financial-metrics-calculators", "Profit Margin Calculator")
]]


def table_item_decorator(funct):
    def wrapper(*args, **kwargs):
        try:
            return funct(*args, **kwargs)
        except Exception as e:
            print(f"Error generating component: {e}")
            return html.Div("An error occurred.", className='uk-alert uk-alert-danger')

    return wrapper


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


def create_table_header(columns, style=None):
    """Utility function to create consistent table headers"""
    return html.Thead([
        html.Tr(columns)
    ], **{'data-uk-sticky': 'end: !.uk-height-max-large'}, className='uk-background-default', style=style)


def create_table_wrapper(body, header=None, empty_message="No data available"):
    """Utility function to create consistent table wrappers"""
    return html.Div([
        html.Div([
            html.Table([
                header,
                body if body else html.Tbody(html.Tr(html.Td(
                    empty_message,
                    colSpan=len(header.children[0].children) if header else None,
                    className='uk-text-muted uk-text-center'
                )))
            ], className='uk-table uk-table-middle uk-table-divider uk-table-hover uk-height-1-1')
        ], className='uk-overflow-auto uk-flex-1')
    ], className='uk-flex uk-flex-column uk-height-1-1')


def add_save_button(name: str, target: str):
    return html.Div(
        [
            html.Button(
                [
                    html.Span(**{'data-uk-icon': 'icon: plus'}, className='uk-margin-small-right'),
                    name
                ],
                data_uk_toggle=f'target: #{target}-modal',
                className='uk-button uk-button-default uk-button-small uk-flex uk-flex-middle'
            )
        ],
        className='uk-margin-medium-top'
    )


def calendar_view(year=None, month=None):
    """Display a calendar view for a given month and year."""
    # Get the current year and month if not provided
    if year is None or month is None:
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month

    # Calculate the number of days in the month and the first day of the month
    days_in_month = calendar.monthrange(year, month)[1]
    days_list = list(range(1, days_in_month + 1))
    first_day_of_month = calendar.monthrange(year, month)[0] + 1

    # Fill the days list with empty strings for alignment
    days_list = [''] * first_day_of_month + days_list

    def highlight_date(day):
        return 'color: #CD5B45;' if day == datetime.now().day and month == datetime.now().month else None

    # Create the month header
    month_header = html.Div(f'{calendar.month_name[month]} {year}', className='uk-text-small uk-margin')

    # Days of the week header
    days_header = html.Div(
        *[html.Div(html.Span(day, className='uk-text-muted uk-text-small')) for day in
          ['S', 'M', 'T', 'W', 'T', 'F', 'S']],
        className='uk-grid-small uk-child-width-expand uk-text-center', **{'data-uk-grid': 'true'}
    )

    # Create week rows
    weeks = [
        html.Div(
            *[
                html.Div(
                    html.A(
                        day,  # The current day from the list
                        className='uk-text-bolder',
                        style=highlight_date(day),  # Highlight the current day
                        # hx_post='/select-date',  # URL to handle the date selection
                        # hx_target='#selected-date',  # Target element to update with the selected date
                        # hx_vals=json.dumps({'date': f'{year}-{month:02d}-{day:02d}'}),  # Pass the selected date
                        # hx_swap='innerHTML'  # Update the inner HTML of the target
                    ) if day else html.Div('', className='uk-text-muted')  # Empty div for non-days
                ) for day in (days_list[i:i + 7] + [''] * (7 - len(days_list[i:i + 7])))  # Fill the week with days
            ],
            className='uk-grid-small uk-child-width-expand uk-text-center', **{'data-uk-grid': 'true'}
        )
        for i in range(0, len(days_list), 7)  # Chunking the days into weeks
    ]

    # Navigation for the previous and next months
    # previous_month = (datetime(year, month, 1) - timedelta(days=1))
    # next_month = (datetime(year, month, 1) + timedelta(days=31)).replace(day=1)

    # Navigation controls
    navigation = html.Div(
        html.Nav(
            html.Ul(
                html.Li(
                    html.A(
                        html.Span(**{'data-uk-pagination-previous': 'true'}, className='uk-margin-small-right'),
                        'Previous',
                        # hx_get='/calendar',  # URL to fetch the calendar
                        # hx_target='#calendar-container',  # ID of the container to update
                        # hx_swap='innerHTML',  # Replace inner HTML of the target
                        # hx_vals=json.dumps({'year': previous_month.year, 'month': previous_month.month})
                    )
                ),
                html.Li(
                    html.A(
                        'Next',
                        html.Span(**{'data-uk-pagination-next': 'true'}, className='uk-margin-small-left'),
                        # hx_get='/calendar',  # URL to fetch the calendar
                        # hx_target='#calendar-container',  # ID of the container to update
                        # hx_swap='innerHTML',  # Replace inner HTML of the target
                        # hx_vals=json.dumps({'year': next_month.year, 'month': next_month.month})
                    ),
                    className='uk-margin-auto-left'
                ),
                className='uk-pagination', **{'data-uk-margin': 'true'}
            ),
            className='uk-margin-medium-top'
        )
    )

    # Placeholder for selected date
    selected_date_display = html.Div(id='selected-date', className='uk-text-center uk-text-large uk-margin-top')

    # Return the full calendar view
    return html.Div(
        [month_header, days_header, *weeks, navigation, selected_date_display]
    )


def sign_out_button():
    return html.Li(
        html.A([
            html.Span(**{'data-uk-icon': 'icon: sign-out'}, className='uk-margin-small-right'),
            'Sign Out'
        ], className='uk-flex uk-flex-middle uk-button uk-margin-top uk-text-bolder',
            style={'color': 'white', 'backgroundColor': custom_colours[-2]}, id='sign_out', n_clicks=0)
    )


def precision_financial_tools():
    return html.Li(
        [
            html.A(
                'Financial Tools',
                html.Span(**{'data-uk-navbar-parent-icon': 'true'}),
                aria_haspopup='true',
                href='#',
                role='button'
            )
        ],
        html.Div(
            [
                html.Ul(
                    [
                        html.Li('Potential Interest Calculators', className='uk-nav-header'),
                        *calculator_group1,
                        html.Li(className='uk-nav-divider'),
                        html.Li('Return on Investment (ROI) Calculators', className='uk-nav-header'),
                        *calculator_group2,
                        html.Li(className='uk-nav-divider'),
                        html.Li('Loan Amortisation Calculators', className='uk-nav-header'),
                        *calculator_group3,
                        html.Li(className='uk-nav-divider'),
                        html.Li('Other Relevant Financial Metrics Calculators', className='uk-nav-header'),
                        [nav_link(href, title) for href, title in [
                            ("#other-relevant-financial-metrics-calculators", "Net Present Value (NPV) Calculator"),
                            ("#other-relevant-financial-metrics-calculators",
                             "Internal Rate of Return (IRR) Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Debt-to-Income Ratio Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Break-Even Point Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Future Value (FV) Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Cash Flow Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Payback Period Calculator"),
                            ("#other-relevant-financial-metrics-calculators", "Profit Margin Calculator")
                        ]],
                    ],
                    className='uk-nav uk-navbar-dropdown-nav'
                )
            ],
            className='uk-navbar-dropdown uk-width-large'
        )
    )


# create_accounts()
# create_profiles()
# create_dividends_payouts()
# create_client_goals()
# create_transactions()
# create_investments()
#
#
# def all_profile_data():
#     # Fetch all client profiles
#     profiles = cur.execute('SELECT * FROM profiles WHERE profile_type = ?', ('client',)).fetchall()
#
#     # Fetch all accounts and calculate balances
#     accounts = cur.execute('SELECT * FROM accounts ORDER BY updated_at DESC').fetchall()
#     accounts_balance = sum(row['balance'] for row in accounts if row['balance'] is not None)
#     prior_accounts_balance = cur.execute(
#         'SELECT SUM(balance) FROM accounts WHERE created_at < ?', (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch all dividends and payouts and calculate balances
#     account_ids = [row['id'] for row in accounts]
#     placeholders = ', '.join('?' for _ in account_ids)
#     if account_ids:
#         dividends_and_payouts = cur.execute(
#             f'SELECT * FROM dividends_payouts WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         dividends_and_payouts = []
#     payouts_balance = sum(row['amount'] for row in dividends_and_payouts if row['amount'] is not None)
#     prior_payouts_balance = cur.execute(
#         'SELECT SUM(amount) FROM dividends_payouts WHERE created_at < ?', (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch all client goals and calculate balances
#     client_goals = cur.execute('SELECT * FROM client_goals').fetchall()
#     client_goals_balance = sum(row['current_savings'] for row in client_goals if row['current_savings'] is not None)
#     prior_client_goals_balance = cur.execute(
#         'SELECT SUM(current_savings) FROM client_goals WHERE created_at < ?', (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch all transactions and calculate balances
#     if account_ids:
#         placeholders = ', '.join('?' for _ in account_ids)
#         transactions = cur.execute(
#             f'SELECT * FROM transactions WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         transactions = []
#     transactions_balance = sum(row['amount'] for row in transactions if row['amount'] is not None)
#     prior_transactions_balance = cur.execute(
#         'SELECT SUM(amount) FROM transactions WHERE created_at < ?', (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch all investments and calculate balances
#     if account_ids:
#         placeholders = ', '.join('?' for _ in account_ids)
#         investments = cur.execute(
#             f'SELECT * FROM investments WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         investments = []
#     investments_balance = sum(row['current_price'] for row in investments if row['current_price'] is not None)
#     prior_investments_balance = cur.execute(
#         'SELECT SUM(current_price) FROM investments WHERE created_at < ?', (current_month_start,)
#     ).fetchone()[0] or 0
#
#     cur.close()
#
#     return {
#         'profiles': [dict(row) for row in profiles],
#         'accounts': [dict(row) for row in accounts],
#         'accounts_balance': accounts_balance,
#         'prior_accounts_balance': prior_accounts_balance,
#         'dividends_and_payouts': [dict(row) for row in dividends_and_payouts],
#         'payouts_balance': payouts_balance,
#         'prior_payouts_balance': prior_payouts_balance,
#         'client_goals': [dict(row) for row in client_goals],
#         'client_goals_balance': client_goals_balance,
#         'prior_client_goals_balance': prior_client_goals_balance,
#         'transactions': [dict(row) for row in transactions],
#         'transactions_balance': transactions_balance,
#         'prior_transactions_balance': prior_transactions_balance,
#         'investments': [dict(row) for row in investments],
#         'investments_balance': investments_balance,
#         'prior_investments_balance': prior_investments_balance,
#     }
#
#
# def profile_data(profile_id: str):
#     # Fetch the specific profile
#     profile = cur.execute('SELECT * FROM profiles WHERE id = ?', (profile_id,)).fetchone()
#
#     # Fetch accounts for the profile and calculate balances
#     accounts = cur.execute(
#         'SELECT * FROM accounts WHERE profile_id = ? ORDER BY updated_at DESC', (profile_id,)
#     ).fetchall()
#     accounts_balance = sum(row['balance'] for row in accounts if row['balance'] is not None)
#     prior_accounts_balance = cur.execute(
#         'SELECT SUM(balance) FROM accounts WHERE profile_id = ? AND created_at < ?',
#         (profile_id, current_month_start)
#     ).fetchone()[0] or 0
#
#     # Fetch dividends and payouts for the accounts and calculate balances
#     create_dividends_payouts()
#     account_ids = [row['id'] for row in accounts]
#     placeholders = ', '.join('?' for _ in account_ids)
#     if account_ids:
#         dividends_and_payouts = cur.execute(
#             f'SELECT * FROM dividends_payouts WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         dividends_and_payouts = []
#     payouts_balance = sum(row['amount'] for row in dividends_and_payouts if row['amount'] is not None)
#     prior_payouts_balance = cur.execute(
#         f'SELECT SUM(amount) FROM dividends_payouts WHERE account_id IN ({placeholders}) AND created_at < ?',
#         tuple(account_ids) + (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch client goals for the profile and calculate balances
#     client_goals = cur.execute('SELECT * FROM client_goals WHERE profile_id = ?', (profile_id,)).fetchall()
#     client_goals_balance = sum(row['current_savings'] for row in client_goals if row['current_savings'] is not None)
#     prior_client_goals_balance = cur.execute(
#         'SELECT SUM(current_savings) FROM client_goals WHERE profile_id = ? AND created_at < ?',
#         (profile_id, current_month_start)
#     ).fetchone()[0] or 0
#
#     # Fetch transactions for the accounts and calculate balances
#     if account_ids:
#         placeholders = ', '.join('?' for _ in account_ids)
#         transactions = cur.execute(
#             f'SELECT * FROM transactions WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         transactions = []
#     transactions_balance = sum(row['amount'] for row in transactions if row['amount'] is not None)
#     prior_transactions_balance = cur.execute(
#         f'SELECT SUM(amount) FROM transactions WHERE account_id IN ({placeholders}) AND created_at < ?',
#         tuple(account_ids) + (current_month_start,)
#     ).fetchone()[0] or 0
#
#     # Fetch investments for the accounts and calculate balances
#     if account_ids:
#         placeholders = ', '.join('?' for _ in account_ids)
#         investments = cur.execute(
#             f'SELECT * FROM investments WHERE account_id IN ({placeholders})', tuple(account_ids)
#         ).fetchall()
#     else:
#         investments = []
#     investments_balance = sum(row['current_price'] for row in investments if row['current_price'] is not None)
#     prior_investments_balance = cur.execute(
#         f'SELECT SUM(current_price) FROM investments WHERE account_id IN ({placeholders}) AND created_at < ?',
#         tuple(account_ids) + (current_month_start,)
#     ).fetchone()[0] or 0
#
#     cur.close()
#
#     return {
#         'profile': dict(profile) if profile else None,
#         'accounts': [dict(row) for row in accounts],
#         'accounts_balance': accounts_balance,
#         'prior_accounts_balance': prior_accounts_balance,
#         'dividends_and_payouts': [dict(row) for row in dividends_and_payouts],
#         'payouts_balance': payouts_balance,
#         'prior_payouts_balance': prior_payouts_balance,
#         'client_goals': [dict(row) for row in client_goals],
#         'client_goals_balance': client_goals_balance,
#         'prior_client_goals_balance': prior_client_goals_balance,
#         'transactions': [dict(row) for row in transactions],
#         'transactions_balance': transactions_balance,
#         'prior_transactions_balance': prior_transactions_balance,
#         'investments': [dict(row) for row in investments],
#         'investments_balance': investments_balance,
#         'prior_investments_balance': prior_investments_balance,
#     }
#
#
# def editor_graph_layout():
#     df = px.data.gapminder()
#     fig = px.scatter(
#         df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
#         log_x=True, size_max=60
#     )
#
#     return html.Div([
#         dcc.Graph(figure=fig)
#     ])
#
#
# def client_total_prior(profile_id: str):
#     return (
#         sum([
#             accounts_balance(profile_id=profile_id), payouts_balance(profile_id=profile_id),
#             client_goals_balance(profile_id=profile_id), transactions_balance(profile_id=profile_id),
#             investments_balance(profile_id=profile_id)
#         ]),
#         sum([
#             prior_accounts_balance(profile_id=profile_id), prior_payouts_balance(profile_id=profile_id),
#             prior_client_goals_balance(profile_id=profile_id), prior_transactions_balance(profile_id=profile_id),
#             prior_investments_balance(profile_id=profile_id)
#         ])
#     )
#
#
# def all_total_prior():
#     return (
#         sum([
#             all_accounts_balance, all_payouts_balance, all_client_goals_balance, all_transactions_balance,
#             all_investments_balance
#         ]),
#         sum([
#             all_prior_accounts_balance, all_prior_payouts_balance, all_prior_client_goals_balance,
#             all_prior_transactions_balance, all_prior_investments_balance
#         ])
#     )
#
#
# def card_header(total, prior):
#     difference = (total - prior) / prior * 100 if prior != 0 and total != 0 else 0
#     return [
#         'Compared to last month ',
#         html.Span([
#             html.Span(['+' if difference > 0 else '']),
#             f'{difference:.2f}'.replace(',', ' '), '%'
#         ], className='uk-text-bolder')
#     ]
#
#
# accounts_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(balance) AS accounts_balance FROM accounts WHERE profile_id = ?', (profile_id,)
# ).fetchone()[0] or 0
# prior_accounts_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(balance) FROM accounts WHERE created_at < ? and profile_id = ?',
#     (current_month_start, profile_id,)
# ).fetchone()[0] or 0
# payouts_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(dp.amount) AS payouts_balance FROM dividends_payouts dp JOIN accounts a ON dp.account_id = '
#     'a.id WHERE a.profile_id = ?', (profile_id,)
# ).fetchone()[0] or 0
# prior_payouts_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(dp.amount) AS payouts_balance FROM dividends_payouts dp JOIN accounts a ON dp.account_id = '
#     'a.id WHERE dp.created_at < ? and a.profile_id = ?', (current_month_start, profile_id,)
# ).fetchone()[0] or 0
# client_goals_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(current_savings) AS client_goals_balance FROM client_goals WHERE profile_id = ?', (profile_id,)
# ).fetchone()[0] or 0
# prior_client_goals_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(current_savings) AS client_goals_balance FROM client_goals WHERE created_at < ? and '
#     'profile_id = ?', (current_month_start, profile_id,)
# ).fetchone()[0] or 0
# transactions_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(t.amount) AS transactions_balance FROM transactions t JOIN accounts a ON t.account_id = a.id '
#     'WHERE a.profile_id = ?', (profile_id,)
# ).fetchone()[0] or 0
# prior_transactions_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(t.amount) AS transactions_balance FROM transactions t JOIN accounts a ON t.account_id = a.id '
#     'WHERE t.created_at < ? and a.profile_id = ?', (current_month_start, profile_id,)
# ).fetchone()[0] or 0
# investments_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(i.current_price * i.quantity) AS investments_balance FROM investments i JOIN accounts a ON '
#     'i.account_id = a.id WHERE a.profile_id = ?', (profile_id,)
# ).fetchone()[0] or 0
# prior_investments_balance = lambda profile_id: cur.execute(
#     'SELECT SUM(i.current_price * i.quantity) AS investments_balance FROM investments i JOIN accounts a ON '
#     'i.account_id = a.id WHERE i.created_at < ? and a.profile_id = ?', (current_month_start, profile_id,)
# ).fetchone()[0] or 0
#
# all_accounts_balance = cur.execute(
#     'SELECT SUM(balance) AS accounts_balance FROM accounts GROUP BY profile_id'
# ).fetchall() or 0
# all_prior_accounts_balance = cur.execute(
#     'SELECT profile_id, SUM(balance) FROM accounts WHERE created_at < ? GROUP BY profile_id',
#     (current_month_start,)
# ).fetchall()
# all_payouts_balance = cur.execute(
#     'SELECT SUM(dp.amount) AS payouts_balance FROM dividends_payouts dp JOIN accounts a ON dp.account_id = a.id'
# ).fetchone()[0] or 0
# all_prior_payouts_balance = cur.execute(
#     'SELECT SUM(dp.amount) AS payouts_balance FROM dividends_payouts dp JOIN accounts a ON dp.account_id = '
#     'a.id WHERE dp.created_at < ?', (current_month_start,)
# ).fetchone()[0] or 0
# all_client_goals_balance = cur.execute(
#     'SELECT SUM(current_savings) AS client_goals_balance FROM client_goals'
# ).fetchone()[0] or 0
# all_prior_client_goals_balance = cur.execute(
#     'SELECT SUM(current_savings) AS client_goals_balance FROM client_goals WHERE created_at < ?',
#     (current_month_start,)
# ).fetchone()[0] or 0
# all_transactions_balance = cur.execute(
#     'SELECT SUM(t.amount) AS transactions_balance FROM transactions t JOIN accounts a ON t.account_id = a.id',
# ).fetchone()[0] or 0
# all_prior_transactions_balance = cur.execute(
#     'SELECT SUM(t.amount) AS transactions_balance FROM transactions t JOIN accounts a ON t.account_id = a.id '
#     'WHERE t.created_at < ?', (current_month_start,)
# ).fetchone()[0] or 0
# all_investments_balance = cur.execute(
#     'SELECT SUM(i.current_price * i.quantity) AS investments_balance FROM investments i JOIN accounts a ON '
#     'i.account_id = a.id'
# ).fetchone()[0] or 0
# all_prior_investments_balance = cur.execute(
#     'SELECT SUM(i.current_price * i.quantity) AS investments_balance FROM investments i JOIN accounts a ON '
#     'i.account_id = a.id WHERE i.created_at < ?', (current_month_start,)
# ).fetchone()[0] or 0
