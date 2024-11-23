import dash
from dash import dcc, callback, Output, Input, State, html

from utils import supabase

dash.register_page(__name__, path='/', name='Welcome to Blue Chip Investments')


def layout():
    """Creates the layout for the login page."""
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Img(
                        src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                            '/Blue%20Chip%20Invest%20Logo.001.png',
                        width='60', height='60'),
                    html.Div(['BLUE CHIP INVESTMENTS'],
                             style={'fontFamily': '"Noto Sans", sans-serif', 'fontOpticalSizing': 'auto',
                                    'fontWeight': '400', 'fontStyle': 'normal', 'lineHeight': '22px',
                                    'color': '#091235', 'width': '164px'})
                ], className='uk-logo uk-flex'),
                html.Div(['Welcome to Blue Chip Investments'])
            ], className='uk-grid-large uk-flex-bottom uk-padding-small', **{'data-uk-grid': 'true'})
        ], className='uk-card uk-card-body'),
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


@callback(
    Output('send-code-notifications', 'children'),
    Output('otp-input-container', 'style'),
    Output('email-input-container', 'style'),
    Input('request-otp-btn', 'n_clicks'),
    State('login-email', 'value'),
    prevent_initial_call=True
)
def request_otp(n_clicks, login_email):
    """Send OTP code for email verification upon button click."""
    if n_clicks and login_email:
        try:
            response = supabase.auth.sign_in_with_otp({
                'email': login_email,
                'options': {'should_create_user': False}
            })

            if response and response.user is None:
                return "", {'display': 'block'}, {'display': 'none'}
            else:
                error_message = response.error.message
                return html.P(f'Error sending OTP: {error_message}',
                              className='uk-text-danger uk-text-bolder uk-margin'), dash.no_update, dash.no_update

        except Exception as e:
            return html.P(f'Authentication error: {str(e)}',
                          className='uk-text-danger uk-text-bolder uk-margin'), dash.no_update, dash.no_update

    return html.P('Please enter your email and click Send Code.',
                  className='uk-text-small'), dash.no_update, dash.no_update


@callback(
    Output('url', 'href', allow_duplicate=True),
    Output('access_token', 'data'),
    Input('verify-code-btn', 'n_clicks'),
    State('login-email', 'value'),
    State('sent-code', 'value'),
    prevent_initial_call=True
)
def verify_otp(n_clicks, login_email, sent_code):
    """Verify the OTP sent to the user's email."""
    if n_clicks and sent_code:
        try:
            response = supabase.auth.verify_otp({
                'email': login_email,
                'token': sent_code,
                'type': 'email'
            })

            if response and response.user:
                admin_users = ['travis@bluechipinvest.co.za', 'eugevanz@gmail.com', 'raymondanthony.m@gmail.com']
                user_email = response.user.email
                access_token = response.session.access_token

                if user_email in admin_users:
                    return f'/admin/{response.user.id}/', access_token
                else:
                    return f'/client_portal/{response.user.id}/', access_token

        except Exception as e:
            print(f'Admin Authentication error: {e}')
            return dash.no_update, dash.no_update

    return dash.no_update, dash.no_update
