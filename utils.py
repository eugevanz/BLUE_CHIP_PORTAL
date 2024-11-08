import calendar
import uuid
from datetime import datetime
from os import environ

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey, func, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from supabase import create_client

SUPABASE_URL = environ.get('SUPABASE_URL')
SUPABASE_KEY = environ.get('SUPABASE_KEY')
SUPABASE_SERVICE_ROLE_KEY = environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
supabase_admin = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_SERVICE_ROLE_KEY)
SUPABASE_PASSWORD = environ.get('SUPABASE_PASSWORD')

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
    profile_picture_url = Column(String, nullable=True)
    first_name = Column(String, default='', nullable=True)
    last_name = Column(String, default='', nullable=True)
    phone_number = Column(String, default='', nullable=True)
    profile_type = Column(String, default='client', nullable=True)
    date_of_birth = Column(DateTime, nullable=True)  # Assuming this is a date
    address = Column(String, default='', nullable=True)
    email = Column(String, default='', nullable=True)

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

# Custom color palette
custom_colours = ['#88A9C3', '#2b4257', '#fc8c3a', '#f7edb5', '#ffcd06', '#9acf97', '#4b8ea9', '#7f7f7f', '#bcbd22',
                  '#17becf', '#aec7e8', '#899b98']
lighter_colours = ['#A6BFD4', '#4F677A', '#FCAE6E', '#FBF6D8', '#FFDA4E', '#B3D7B5', '#71A4BA', '#A8A8A8', '#D3D538',
                   '#63D8E4', '#D1E4F2', '#AAB7B4']
fig_layout = {
    'xaxis': {'showticklabels': False, 'visible': False},
    'yaxis': {'showticklabels': False, 'visible': False},
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',  # Use rgba for transparency
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'showlegend': False,
    'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}
}

accounts_df = px.data.gapminder()
continents_list = accounts_df['continent'].unique().tolist()
account_fig = px.scatter(
    accounts_df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
    log_x=True, size_max=60, color_discrete_sequence=custom_colours
)
account_fig.update_layout(**fig_layout)

payouts_df = px.data.stocks().head(12)
dates_list = payouts_df['date'].tolist()
payouts_fig = px.line(payouts_df, x='date', y='GOOG', markers=True, line_shape='spline')
payouts_fig.update_traces(line=dict(width=8), marker=dict(size=12), line_color=custom_colours[0])
payouts_fig.update_layout(**fig_layout)

investments_df = pd.DataFrame({
    'Investment': ['Investment A', 'Investment B', 'Investment C', 'Investment D', 'Investment E'],
    'Returns': [12.5, 8.3, 15.2, 5.7, 9.1]  # hypothetical percentage returns
})
investment_list = investments_df['Investment'].tolist()
investment_fig = px.bar(investments_df, x='Investment', y='Returns', color='Investment',
                        color_discrete_sequence=custom_colours)
investment_fig.update_layout(**fig_layout)

goals_df = pd.DataFrame([
    {'name': 'Goal 1', 'current': 30, 'target': 100},
    {'name': 'Goal 2', 'current': 60, 'target': 80},
    {'name': 'Goal 3', 'current': 50, 'target': 90},
    {'name': 'Goal 4', 'current': 70, 'target': 120},
    {'name': 'Goal 5', 'current': 20, 'target': 50}
])
goals_list = goals_df['name'].tolist()
goals_fig = px.bar(goals_df, x='name', y=['current', 'target'], color_discrete_map={
    'current': custom_colours, 'target': lighter_colours
})
goals_fig.update_layout(**fig_layout)

transact_df = pd.DataFrame({
    'amount': [100, 150, 200, 150, 300, 400, 100, 250, 300, 150,
               100, 200, 100, 300, 400, 150, 250, 100, 200, 300,
               250, 300, 350, 100, 200, 150, 400, 200, 300, 350,
               200, 100, 250, 150, 300, 400, 300, 150, 100, 200],
    'type': ['debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit',
             'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit',
             'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit',
             'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit', 'debit', 'credit']
}).groupby('type')['amount'].sum().reset_index()
transact_fig = px.pie(transact_df, values='amount', names='type', color='type', color_discrete_sequence=[
    custom_colours[0], custom_colours[1]
])
transact_fig.update_layout(**fig_layout)

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

market_df = pd.DataFrame({
    "Date": date_range,
    "Open": open_prices,
    "High": high_prices,
    "Low": low_prices,
    "Close": close_prices
}).head(30)
market_fig = go.Figure(data=[
    go.Candlestick(
        x=market_df['Date'], open=market_df['Open'], high=market_df['High'], low=market_df['Low'],
        close=market_df['Close'], increasing_line_color=custom_colours[0], decreasing_line_color=custom_colours[1]
    )
])
market_fig.update_layout(**fig_layout)


def indicator_fig(value: float = 400576.67):
    fig = go.Figure(go.Indicator(
        mode='number',
        value=value,
        number={'prefix': "R ", 'font': {'color': custom_colours[0]}},
        domain={'x': [0, 1], 'y': [0, 1]})
    )
    fig.update_layout(**fig_layout)

    return fig


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


def create_table_header(columns, sticky=True):
    """Utility function to create consistent table headers"""
    return html.Thead([
        html.Tr([
            html.Th(col, className=f'uk-table-{"shrink" if i == 0 else "expand"}')
            for i, col in enumerate(columns)
        ])
    ], **{'data-uk-sticky': 'end: !.uk-height-max-large' if sticky else None}, className='uk-background-secondary')


def create_table_wrapper(header, body, empty_message="No data available"):
    """Utility function to create consistent table wrappers"""
    return html.Div([
        html.Div([
            html.Table([
                header,
                body if body else html.Tbody(html.Tr(html.Td(
                    empty_message,
                    colSpan=len(header.children[0].children),
                    className='uk-text-muted uk-text-center'
                )))
            ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
        ], className='uk-overflow-auto uk-height-max-large')
    ])


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
        ], className='uk-flex uk-flex-middle uk-text-danger uk-margin-top')
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
                        *calculator_group4,
                    ],
                    className='uk-nav uk-navbar-dropdown-nav'
                )
            ],
            className='uk-navbar-dropdown uk-width-large'
        )
    )


def find_path_by_name(pathname):
    # Split the pathname into segments and remove empty strings
    segments = [segment for segment in pathname.split('/') if segment]

    # Prepend 'edit' if any of the specified segments are present
    if any(segment in segments for segment in
           ['add-account', 'add-client-goal', 'add-investment', 'add-payout', 'add-transaction']):
        segments.insert(0, 'edit')

    # Always insert 'admin' at the beginning
    segments.insert(0, 'admin') if 'admin' not in segments else None

    breadcrumbs = []
    profile_id = None

    # Determine the profile ID from the segments
    for segment in segments:
        # Check if the segment is a profile ID
        if not any(f'/{segment}/' in page['path'] for page in dash.page_registry.values()):
            profile_id = segment
            break  # Exit the loop once the profile ID is found

    # Build breadcrumbs
    for segment in segments:
        for page in dash.page_registry.values():
            # If the segment matches the page path, add to breadcrumbs
            if f'/{segment}/' in page['path']:
                breadcrumbs.append((page['name'], f'/{segment}/'))

                # If the segment is one of the add operations, include the profile_id
                if segment in ['add-account', 'add-client-goal', 'add-investment', 'add-payout',
                               'add-transaction', 'edit'] and profile_id:
                    # Update the last breadcrumb to include profile_id
                    breadcrumbs[-1] = (page['name'], f'/{segment}/{profile_id}')

    return breadcrumbs


def navbar(pathname: str):
    return html.Div([
        html.Nav([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(
                                src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                                    '/Blue%20Chip%20Invest%20Logo.001.png',
                                width='60', height='60'),
                            html.Div(['BLUE CHIP INVESTMENTS'],
                                     style={'font-family': '"Noto Sans", sans-serif', 'font-optical-sizing': 'auto',
                                            'font-weight': '400', 'font-style': 'normal', 'line-height': '22px',
                                            'color': '#091235', 'width': '164px'})
                        ], className='uk-navbar-item uk-logo'),
                        html.Nav([
                            html.Ul([
                                html.Li([html.A(name, href=path)]) for name, path in find_path_by_name(pathname)
                            ], className='uk-breadcrumb')
                        ]),
                    ], className='uk-navbar-left uk-flex-bottom')
                ], **{'data-uk-navbar': 'true'})
            ], className='uk-container')
        ], className='uk-navbar-container')
    ], **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'})


def dividend_performance(order: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Dividend/Payout performance', className='uk-text-small'),
                html.H2('R8,167,514.57',
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {100000:,.2f}']),
                            html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {10000:,.2f}'])
                        ], className='uk-flex uk-flex-column uk-height-medium',
                            style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=payouts_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([format_time(datetime.strptime(item, '%Y-%m-%d'))]) for item in
                            [dates_list[0], dates_list[len(dates_list) // 2], dates_list[-1]]
                        ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def account_performance(order: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Accounts performance', className='uk-text-small'),
                html.H2('R8,167,514.57',
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {100000:,.2f}']),
                            html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {10000:,.2f}'])
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
                                html.Div([continent], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, continent in
                            enumerate(continents_list)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def investment_performance(order: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Investments performance', className='uk-text-small'),
                html.H2('R8,167,514.57',
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {100000:,.2f}']),
                            html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {10000:,.2f}'])
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
                                html.Div([item], className='uk-margin-small-left uk-text-small')
                            ], className='uk-flex uk-flex-middle uk-margin-right') for i, item in
                            enumerate(
                                investment_list)
                        ], className='uk-flex uk-flex-wrap')
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body')
        ], className='uk-card uk-card-default')
    ], className=order)


def client_goal_performance(order: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Client Goals performance', className='uk-text-small'),
                html.H2('R8,167,514.57',
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
                         className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {100000:,.2f}']),
                            html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {10000:,.2f}'])
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


def transaction_performance(order: str = None):
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Transactions performance', className='uk-text-small'),
                html.H2('R8,167,514.57',
                        className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div(['Compared to last month ', html.Span('+24.17%', className='uk-text-success')],
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


def market_performance():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('Market performance', className='uk-text-small'),
                        html.H2(f'R {8167514.57:,.2f}',
                                className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                        html.Div([
                            'Compared to last month ', html.Span('+24.17%', className='uk-text-success')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Select([
                        html.Option([label], value=value) for label, value in [
                            ('S&P 500', 'S&P 500'), ('NASDAQ', 'NASDAQ'), ('Dow Jones', 'Dow Jones'),
                            ('FTSE 100', 'FTSE 100')
                        ]
                    ], className='uk-select uk-form-small uk-form-blank uk-width-small', id='instrument')
                ], className='uk-flex uk-flex-between uk-flex-bottom')
            ], className='uk-card-header'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([f'R {100000:,.2f}']),
                            html.Div([f'R {500000:,.2f}'], className='uk-margin-auto-vertical'),
                            html.Div([f'R {10000:,.2f}'])
                        ], className='uk-flex uk-flex-column uk-height-medium', style={'fontSize': '8px'})
                    ], className='uk-width-auto'),
                    html.Div([
                        dcc.Graph(figure=market_fig, style={'height': '300px'}, config={'displayModeBar': False}),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                format_time(item)
                            ]) for item in [
                                market_df.iloc[0]['Date'],
                                market_df.iloc[int(len(market_df) * 0.25)]['Date'],
                                market_df.iloc[int(len(market_df) * 0.75)]['Date'],
                                market_df.iloc[-1]['Date']
                            ]
                        ], className='uk-flex uk-flex-between', style={'fontSize': '8px'})
                    ])
                ], **{'data-uk-grid': 'true'},
                    className='uk-grid-divider uk-child-width-expand uk-grid-small')
            ], className='uk-card-body'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('S&P 500', style={'fontSize': '11px'}),
                        html.Div(f'R {4376.95:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            '0.73% ', html.Span(**{'data-uk-icon': 'triangle-up'}, className='uk-text-success')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('NASDAQ', style={'fontSize': '11px'}),
                        html.Div(f'R {14628.02:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            '-1.46% ', html.Span(**{'data-uk-icon': 'triangle-down'}, className='uk-text-danger')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('Dow Jones', style={'fontSize': '11px'}),
                        html.Div(f'R {34588.87:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            '0.52% ', html.Span(**{'data-uk-icon': 'triangle-up'}, className='uk-text-success')
                        ], className='uk-text-small uk-margin-remove-top')
                    ]),
                    html.Div([
                        html.Div('FTSE 100', style={'fontSize': '11px'}),
                        html.Div(f'R {7044.03:,.2f}',
                                 className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                           'uk-text-truncate'),
                        html.Div([
                            '0.20% ', html.Span(**{'data-uk-icon': 'triangle-up'}, className='uk-text-success')
                        ], className='uk-text-small uk-margin-remove-top')
                    ])
                ], className='uk-flex uk-flex-between')
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default')
    ], className='uk-width-3-4@m')

    # def potential_interest_calculators():
    #     return html.Div(
    #         [
    #             html.Button(type='button', **{'data-uk-close': 'true'}, className='uk-modal-close-full uk-close-large'),
    #             html.Div(
    #                 [
    #                     html.Div(
    #                         [
    #                             H3(
    #                                 'Potential Interest Calculators',
    #                                 style={'font-family': '"Playfair Display SC", serif', 'font-weight': '700', 'font-style': 'normal'},
    #                                 className='uk-text-uppercase uk-text-bolder'
    #                             ),
    #                             html.Div(
    #                                 '''These are tools designed to help individuals or businesses estimate the amount of
    #                                 interest they could earn or owe over time based on various financial scenarios. These
    #                                 calculators typically focus on interest accumulated from savings, loans, or investments and
    #                                 can be tailored for specific financial goals.''',
    #                                 className='uk-text-small uk-width-2-3@s'
    #                             )
    #                         ],
    #                         className='uk-text-center'
    #                     ),
    #                     html.Div(
    #                         [
    #                             html.Div(
    #                                 [
    #                                     H4('Simple Interest Calculator'),
    #                                     Form(
    #                                         Fieldset(
    #                                             [
    #                                                 calc_input(label='Principal (P)', icon='bag',
    #                                                            description='The initial amount of money that is being invested or loaned.'),
    #                                                 calc_input(label='Interest Rate (R)', icon='arrow-up-right',
    #                                                            description='The annual interest rate, usually provided as a percentage (e.g., 5%)'),
    #                                                 calc_input(label='Time (T)', icon='clock',
    #                                                            description='The time period for which the interest is calculated, typically in years.'),
    #                                                 html.Div(
    #                                                     [
    #                                                         html.Div('Result', className='uk-text-bolder uk-text-small'),
    #                                                         html.Hr(),
    #                                                         html.Div(
    #                                                             html.Span('0.00', className='uk-text-bolder'),
    #                                                             ' per year'
    #                                                         ),
    #                                                         html.Hr()
    #                                                     ],
    #                                                     className='uk-margin'
    #                                                 )
    #                                             ],
    #                                             className='uk-fieldset'
    #                                         )
    #                                     )
    #                                 ],
    #                                 className='uk-card uk-card-default uk-card-body uk-light',
    #                                 style={'background-color': '#091235'}
    #                             ),
    #                             html.Div(
    #                                 [
    #                                     H4('Compound Interest Calculator'),
    #                                     Form(
    #                                         Fieldset(
    #                                             [
    #                                                 calc_input(label='Principal (P)', icon='bag',
    #                                                            description='The initial amount of money that is being invested or loaned.'),
    #                                                 calc_input(label='Interest Rate (R)', icon='arrow-up-right',
    #                                                            description='The annual interest rate, usually provided as a percentage (e.g., 5%)'),
    #                                                 calc_input(label='Time (T)', icon='clock',
    #                                                            description='The time period for which the interest is calculated, typically in years.'),
    #                                                 calc_input(label='Compounding Frequency (n)', icon='calendar',
    #                                                            description='The number of times the interest is compounded per year (e.g., annually, semi-annually, quarterly, monthly, daily).'),
    #                                                 html.Div('Common values for compounding frequency:',
    #                                                     className='uk-text-small uk-padding-small uk-padding-remove-top'),
    #                                                 html.Div(
    #                                                     html.Ul(
    #                                                         [
    #                                                             html.Li('Annually (n = 1)'),
    #                                                             html.Li('Semi-Annually (n = 2)'),
    #                                                             html.Li('Quarterly (n = 4)'),
    #                                                             html.Li('Monthly (n = 12)'),
    #                                                             html.Li('Daily (n = 365)')
    #                                                         ],
    #                                                         className='uk-list uk-list-collapse uk-list-disc'
    #                                                     ),
    #                                                     className='uk-text-small uk-padding-small uk-padding-remove-top'
    #                                                 ),
    #                                                 html.Div(
    #                                                     [
    #                                                         html.Div('Result', className='uk-text-bolder uk-text-small'),
    #                                                         html.Hr(),
    #                                                         html.Div(
    #                                                             html.Span('0.00', className='uk-text-bolder'),
    #                                                             ' per year'
    #                                                         ),
    #                                                         html.Hr()
    #                                                     ],
    #                                                     className='uk-margin'
    #                                                 )
    #                                             ],
    #                                             className='uk-fieldset'
    #                                         )
    #                                     )
    #                                 ],
    #                                 className='uk-card uk-card-default uk-card-body uk-light',
    #                                 style={'background-color': '#091235'}
    #                             ),
    #                             html.Div(
    #                                 [
    #                                     H4('Savings Interest Calculator'),
    #                                     Form(
    #                                         Fieldset(
    #                                             [
    #                                                 calc_input(label='Principal (P)', icon='bag',
    #                                                            description='The initial amount of money that is being invested or loaned.'),
    #                                                 calc_input(label='Monthly Contributions (C)', icon='mail',
    #                                                            description='The amount of money added to the account each month, if applicable.'),
    #                                                 calc_input(label='Annual Interest Rate (R)', icon='mail',
    #                                                            description='The interest rate provided by the savings account, usually expressed as a percentage.'),
    #                                                 calc_input(label='Time (T)', icon='clock',
    #                                                            description='The duration for which the savings will accumulate interest, typically measured in years.'),
    #                                                 calc_input(label='Compounding Frequency (n)', icon='calendar',
    #                                                            description='The number of times the interest is compounded per year (e.g., annually, semi-annually, quarterly, monthly, daily).'),
    #                                                 html.Div('Common values for compounding frequency:',
    #                                                     className='uk-text-small uk-padding-small uk-padding-remove-top'),
    #                                                 html.Div(
    #                                                     html.Ul(
    #                                                         [
    #                                                             html.Li('Annually (n = 1)'),
    #                                                             html.Li('Semi-Annually (n = 2)'),
    #                                                             html.Li('Quarterly (n = 4)'),
    #                                                             html.Li('Monthly (n = 12)'),
    #                                                             html.Li('Daily (n = 365)')
    #                                                         ],
    #                                                         className='uk-list uk-list-collapse uk-list-disc'
    #                                                     ),
    #                                                     className='uk-text-small uk-padding-small uk-padding-remove-top'
    #                                                 ),
    #                                                 html.Div(
    #                                                     [
    #                                                         html.Div('Result', className='uk-text-bolder uk-text-small'),
    #                                                         html.Hr(),
    #                                                         html.Div(
    #                                                             html.Span('0.00', className='uk-text-bolder'),
    #                                                             ' per year'
    #                                                         ),
    #                                                         html.Hr()
    #                                                     ],
    #                                                     className='uk-margin'
    #                                                 )
    #                                             ],
    #                                             className='uk-fieldset'
    #                                         )
    #                                     )
    #                                 ],
    #                                 className='uk-card uk-card-default uk-card-body uk-light',
    #                                 style={'background-color': '#091235'}
    #                             )
    #                         ],
    #                         **{'data-uk-grid': 'masonry: pack'},
    #                         className='uk-child-width-1-2@m uk-margin-medium-top'
    #                     )
    #                 ],
    #                 className='uk-container'
    #             )
    #         ],
    #         className='uk-section uk-section-medium',
    #         id='potential-interest-calculators',
    #         **{'data-uk-modal': 'true'},
    #         className='uk-modal-full'
    #     )


def footer():
    return html.Div(
        html.Div(
            html.Hr(),
            html.Div(
                html.Div(
                    'BLUE CHIP INVESTMENTS',
                    style={'font-family': 'Noto Sans, sans-serif', 'font-optical-sizing': 'auto',
                           'font-weight': '400', 'font-style': 'normal'},
                    className='uk-heading-small uk-margin-small-bottom uk-width-medium',
                    # _get='/home/',
                    # hx_target='#page'
                ),
                html.Div('Building Your Legacy with Trusted Growth', className='uk-text-small'),
                className='uk-card uk-card-body'
            ),
            html.Div(
                html.Div(
                    html.Div(
                        html.Div(
                            'Our Services',
                            className='uk-text-bolder uk-text-large uk-margin-small-bottom',
                            style={'color': '#88A9C3'}
                        ),
                        html.Ul(
                            [
                                html.Li(html.A('Financial Planning', href='#')),
                                html.Li(html.A('Investment Management', href='#')),
                                html.Li(html.A('Retirement Planning', href='#')),
                                html.Li(html.A('Investment Analysis', href='#')),
                                html.Li(html.A('Insurance', href='#'))
                            ],
                            className='uk-list uk-text-small'
                        ),
                        className='uk-card uk-card-body'
                    ),
                    className='uk-width-auto'
                ),
                html.Div(
                    html.Div(
                        html.Div(
                            'Explore',
                            className='uk-text-bolder uk-text-large uk-margin-small-bottom',
                            style={'color': '#88A9C3'}
                        ),
                        html.Ul(
                            [
                                html.Li(html.A('About', href='#')),
                                html.Li(html.A('Services', href='#')),
                                html.Li(html.A('Careers', href='#')),
                                html.Li(html.A("FAQ's", href='#')),
                                html.Li(html.A('Partner', href='#'))
                            ],
                            className='uk-list uk-text-small'
                        ),
                        className='uk-card uk-card-body'
                    ),
                    className='uk-width-auto'
                ),
                html.Div(
                    html.Div(
                        html.Div(
                            "Let's Talk",
                            className='uk-text-bolder uk-text-large uk-margin-small-bottom',
                            style={'color': '#88A9C3'}
                        ),
                        html.P(
                            'We\'re Here to Help You Grow Your Wealth, Plan Your Future, and Achieve Your Financial '
                            'Goals',
                            className='uk-text-small uk-light'
                        ),
                        html.Button(
                            'Start',
                            className='uk-button uk-light uk-text-bolder',
                            style={'background-color': '#88A9C3', 'color': '#091235'},
                            # hx_get='/contact-us/', hx_target='#page', hx_push_url='/home/'
                        ),
                        className='uk-card uk-card-body'
                    )
                ),
                **{'data-uk-grid': 'true'},
                className='uk-child-width-1-2 uk-child-width-1-3@l'
            ),
            html.Div(
                html.Div(
                    html.Div(
                        html.Div(
                            **{'data-uk-icon': 'icon: location; ratio: 1.8'},
                            className='uk-icon',
                            style={'color': '#88A9C3'}
                        ),
                        html.Div('Location', className='uk-text-large uk-text-bolder uk-light'),
                        html.Div('Unit 17, No.30 Surprise Road, Pinetown, 3610',
                                 className='uk-text-small uk-light'),
                        className='uk-card uk-card-body'
                    )
                ),
                html.Div(
                    html.Div(
                        html.Div(
                            **{'data-uk-icon': 'icon: receiver; ratio: 1.8'},
                            className='uk-icon'
                        ),
                        html.Div('Phone', className='uk-text-large uk-text-bolder uk-light'),
                        html.Div('0860 258 2447', className='uk-text-small uk-light'),
                        className='uk-card uk-card-body'
                    )
                ),
                html.Div(
                    html.Div(
                        html.Div(
                            **{'data-uk-icon': 'icon: mail; ratio: 1.8'},
                            className='uk-icon'
                        ),
                        html.Div('Email', className='uk-text-large uk-text-bolder'),
                        html.Div('info@', html.Br(), 'bluechipinvest.co.za', className='uk-text-small'),
                        className='uk-card uk-card-body'
                    )
                ),
                html.Div(
                    html.Div(
                        html.Div(
                            **{'data-uk-icon': 'icon: social; ratio: 1.8'},
                            className='uk-icon'
                        ),
                        html.Div('Social', className='uk-text-large uk-text-bolder',
                                 style={'margin-bottom': '4px'}),
                        html.Div(
                            html.Div(
                                [
                                    html.Span(**{'data-uk-icon': 'icon: facebook'}, className='uk-icon-button uk-icon'),
                                    html.Span(**{'data-uk-icon': 'icon: linkedin'}, className='uk-icon-button uk-icon'),
                                    html.Span(**{'data-uk-icon': 'icon: instagram'},
                                              className='uk-icon-button uk-icon'),
                                    html.Span(**{'data-uk-icon': 'icon: x'}, className='uk-icon-button uk-icon')
                                ],
                                **{'data-uk-grid': 'true'},
                                className='uk-grid-small uk-child-width-auto'
                            ),
                            className='uk-grid-small'
                        ),
                        className='uk-card uk-card-body'
                    )
                ),
                **{'data-uk-grid': 'true'},
                className='uk-child-width-1-2 uk-child-width-1-4@l'
            ),
            className='uk-container'
        ),
        className='uk-section uk-section-large uk-light', style={'background-color': '#091235'}
    )


def editor_graph_layout():
    df = px.data.gapminder()
    fig = px.scatter(
        df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
        log_x=True, size_max=60
    )

    return html.Div([
        dcc.Graph(figure=fig)
    ])
