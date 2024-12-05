import dash
from dash import dcc, html

dash.register_page(__name__, path='/', name='Welcome to Blue Chip Investments')


def layout():
    """Creates the layout for the login page."""
    return html.Div([
        html.Div([
            # Background image section
            html.Div(
                style={
                    'backgroundImage': 'url('
                                       'https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public'
                                       '/website_images/marten-bjork-6dW3xyQvcYE-unsplash_6_11zon.webp)',
                    'filter': 'grayscale(90%)'
                },
                **{'data-uk-height-viewport': 'true'},
                className='uk-background-cover uk-visible@m'
            ),

            # Main content section
            html.Div([
                # Logo
                html.Img(
                    src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/Blue%20Chip'
                        '%20Invest%20Logo.001.png',
                    width='128', height='128'
                ),
                # Title
                html.Div(
                    'BLUE CHIP INVESTMENTS',
                    style={
                        'fontFamily': '"Noto Sans", sans-serif',
                        'fontOpticalSizing': 'auto',
                        'fontWeight': '400',
                        'fontStyle': 'normal'
                    },
                    className='uk-heading-small uk-width-medium uk-margin-remove-top'
                ),
                # Subtitle
                html.Div('Building Your Legacy with Trusted Growth', className='uk-text-small uk-margin-large-bottom'),
                html.Div([
                    html.H3('Welcome Back', className='uk-card-title uk-text-bolder uk-margin-remove-bottom'),
                    html.P(
                        [
                            'Please enter your ', html.Strong('email address'),
                            ' to log in. A magic link will be sent to your email, allowing you to securely access your '
                            'account.'
                        ],
                        className='uk-text-small uk-margin-remove-top',
                        style={'color': '#091235'}
                    ),
                    html.Div('Email', className='uk-text-small'),
                    html.Div([
                        html.Span(className='uk-form-icon', **{'data-uk-icon': 'icon: mail'}),
                        dcc.Input(className='uk-input uk-form-width-large', type='email', id='login-email')
                    ], className='uk-inline'),
                    html.P('Please enter your email and click Send Code.', className='uk-text-meta'),
                    html.Button('Send Code', className='uk-button uk-button-large uk-light',
                                style={'backgroundColor': '#091235'}, id='request-otp-btn')
                ], id='email-input-container', className='uk-margin'),

                html.Div([
                    html.H3('Ready to sign-in?', className='uk-card-title uk-text-bolder uk-margin-remove-bottom'),
                    html.P([
                        'Please enter the ', html.Strong('verification code'),
                        ' that was sent to your email. This code is required to verify your identity and complete the '
                        'login process.'
                    ], className='uk-text-small uk-margin-remove-top', style={'color': '#091235'}),
                    html.Div('One-time PIN', className='uk-text-small'),
                    html.Div([
                        html.Span(className='uk-form-icon', **{'data-uk-icon': 'icon: lock'}),
                        dcc.Input(className='uk-input uk-form-width-large', type='text', id='sent-code')
                    ], className='uk-inline'),
                    html.P('Please enter your OTP and click Sign In.', className='uk-text-meta'),
                    html.Button('Sign In', className='uk-button uk-button-large uk-light',
                                style={'backgroundColor': '#091235'}, id='verify-code-btn')
                ], id='otp-input-container', style={'display': 'none'}, className='uk-margin'),

                html.P(id='send-code-notifications')
            ], className='uk-padding-large')
        ], **{'data-uk-grid': 'true'}, className='uk-grid-collapse uk-child-width-1-2@m')
    ])
