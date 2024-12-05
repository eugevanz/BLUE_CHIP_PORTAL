import base64

import dash
from dash import Dash, dcc, callback, Output, Input, State, html
from dash.html import Div
from shortnumbers import millify

from components.navbar import navbar
from utils import supabase, accounts_balance, prior_accounts_balance, supabase_admin, card_header, client_total_prior, \
    all_total_prior, cur, payouts_balance, prior_payouts_balance, client_goals_balance, prior_client_goals_balance, \
    investments_balance, prior_investments_balance, transactions_balance, prior_transactions_balance

app = Dash(
    external_scripts=[
        'https://cdn.jsdelivr.net/npm/uikit@3.21.12/dist/js/uikit.min.js',
        'https://cdn.jsdelivr.net/npm/uikit@3.21.12/dist/js/uikit-icons.min.js',
        'https://unpkg.com/hyperscript.org@0.9.12'
    ],
    external_stylesheets=[
        'https://cdn.jsdelivr.net/npm/charts.css/dist/charts.min.css',
        'https://cdn.jsdelivr.net/npm/uikit@3.21.12/dist/css/uikit.min.css',
        'https://fonts.googleapis.com',
        'https://fonts.gstatic.com',
        'https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap'
    ],
    use_pages=True
)
server = app.server

app.config.suppress_callback_exceptions = True
app._favicon = 'favico.ico'

app.layout = Div([
    dcc.Location(id='url'),
    dcc.Store(id='access_token', storage_type='session'),
    dcc.Store(id='profile_id', storage_type='session'),
    dcc.Store(id='profile_created_at', storage_type='session'),
    dcc.Store(id='profile_picture_url', storage_type='session'),
    dcc.Store(id='profile_first_name', storage_type='session'),
    dcc.Store(id='profile_last_name', storage_type='session'),
    dcc.Store(id='profile_type', storage_type='session'),
    dcc.Store(id='profile_email', storage_type='session'),
    dcc.Loading([dash.page_container], id='page-loading', type='circle', fullscreen=True)
])


@callback(
    Output('url', 'pathname'),
    Output('profile_id', 'data'),
    Output('profile_created_at', 'data'),
    Output('profile_picture_url', 'data'),
    Output('profile_first_name', 'data'),
    Output('profile_last_name', 'data'),
    Output('profile_type', 'data'),
    Output('profile_email', 'data'),
    Input('access_token', 'data')
)
def skip_login_page_if_token_exists(access_token):
    if access_token is None:
        return ('/', dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                dash.no_update)
    else:
        try:
            response = supabase.auth.get_user(jwt=access_token)
            if response and response.user:
                user_id = response.user.id
                # Query the public.profiles table for the user's profile type
                profile_response = supabase.table('profiles').select('*').eq('id', user_id).limit(1).single().execute()

                if 'error' in profile_response:
                    print(f"Error fetching profile: {profile_response['error']['message']}")
                    return ('/', dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                            dash.no_update, dash.no_update)

                profile = profile_response.data

                # Redirect based on profile type
                if profile['profile_type'] == 'admin':
                    return f'/admin/{response.user.id}/', profile['id'], profile['created_at'], profile[
                        'profile_picture_url'], profile['first_name'], profile['last_name'], profile[
                        'profile_type'], profile['email']
                elif profile['profile_type'] == 'client':
                    return f'/client_portal/{response.user.id}/', profile['id'], profile['created_at'], profile[
                        'profile_picture_url'], profile['first_name'], profile['last_name'], profile[
                        'profile_type'], profile['email']
                else:
                    print(f"Unknown profile type: {profile['profile_type']}")
                    return ('/', dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                            dash.no_update, dash.no_update)

        except Exception as e:
            print(f"Error with login: {e}")
            return ('/', dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                    dash.no_update)


@callback(
    Output('nav', 'children'),
    Input('url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)


@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Output('access_token', 'data', allow_duplicate=True),
    Output('profile_id', 'data', allow_duplicate=True),
    Output('profile_created_at', 'data', allow_duplicate=True),
    Output('profile_picture_url', 'data', allow_duplicate=True),
    Output('profile_first_name', 'data', allow_duplicate=True),
    Output('profile_last_name', 'data', allow_duplicate=True),
    Output('profile_type', 'data', allow_duplicate=True),
    Output('profile_email', 'data', allow_duplicate=True),
    Input('sign_out', 'n_clicks'),
    prevent_initial_call=True
)
def sign_out(n_clicks):
    if n_clicks:
        return '/', None, None, None, None, None, None, None, None
    else:
        raise dash.exceptions.PreventUpdate


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
    Output('access_token', 'data', allow_duplicate=True),
    Output('profile_id', 'data', allow_duplicate=True),
    Output('profile_created_at', 'data', allow_duplicate=True),
    Output('profile_picture_url', 'data', allow_duplicate=True),
    Output('profile_first_name', 'data', allow_duplicate=True),
    Output('profile_last_name', 'data', allow_duplicate=True),
    Output('profile_type', 'data', allow_duplicate=True),
    Output('profile_email', 'data', allow_duplicate=True),
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
                profile_response = supabase.table('profiles').select('*').eq('id', response.user.id).limit(
                    1).single().execute()
                profile = profile_response.data
                access_token = response.session.access_token

                if profile['profile_type'] == 'admin':
                    return f'/admin/{response.user.id}/', access_token, profile['id'], profile['created_at'], profile[
                        'profile_picture_url'], profile['first_name'], profile['last_name'], profile[
                        'profile_type'], profile['email']
                else:
                    return f'/client_portal/{response.user.id}/', access_token, profile['id'], profile[
                        'created_at'], profile['profile_picture_url'], profile['first_name'], profile[
                        'last_name'], profile['profile_type'], profile['email']

        except Exception as e:
            print(f'Admin Authentication error: {e}')
            raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output('invite-notifications', 'children'),
    State('form-invite-email', 'value'),
    Input('form-invite-button', 'n_clicks')
)
def send_invite(email, n_clicks):
    if n_clicks and email:
        try:
            response = supabase_admin.auth.admin.invite_user_by_email(email)
            print(response)
            if response and response.user:
                return html.Span(f'Invite sent to {response.user.email}',
                                 className='uk-text-success uk-text-bolder')
            else:
                return html.Span(f'Error sending invite: {response["error"]["message"]}',
                                 className='uk-text-danger uk-text-bolder')
        except Exception as e:
            return html.Span(f'Invitation error: {e}', className='uk-text-danger uk-text-bolder')


@callback(
    Output('card_header', 'children'),
    Input('is_client', 'data'),
    Input('profile_id', 'data'),
    Input('name', 'data')
)
def get_card_header(is_client, profile_id, name):
    if name == 'all':
        if is_client:
            total, prior = client_total_prior(profile_id=profile_id)
            return card_header(total, prior)
        else:
            total, prior = all_total_prior()
            return card_header(total, prior)
    elif name == 'accounts':
        return card_header(accounts_balance(profile_id=profile_id), prior_accounts_balance(profile_id=profile_id))
    elif name == 'dividends_payouts':
        return card_header(payouts_balance(profile_id=profile_id), prior_payouts_balance(profile_id=profile_id))
    elif name == 'client_goals':
        return card_header(client_goals_balance(profile_id=profile_id),
                           prior_client_goals_balance(profile_id=profile_id))
    elif name == 'investments':
        return card_header(investments_balance(profile_id=profile_id), prior_investments_balance(profile_id=profile_id))
    else:
        return card_header(transactions_balance(profile_id=profile_id),
                           prior_transactions_balance(profile_id=profile_id))


@callback(
    Output('highest_', 'children'),
    Output('mid_', 'children'),
    Output('lowest_', 'children'),
    Input('name', 'data'),
    Input('column', 'data'),
    Input('profile_id', 'data')
)
def get_y_axis(name, column, profile_id):
    table = cur.execute('SELECT * FROM ? WHERE profile_id = ?', (name, profile_id,)).fetchall()
    lowest_ = min(table, key=lambda x: x[column], default=None)[column]
    highest_ = max(table, key=lambda x: x[column], default=None)[column]
    mid_ = (highest_ + lowest_) / 2
    return f'R {millify(highest_)}', f'R {millify(mid_)}', f'R {millify(lowest_)}'


@callback(
    Output('total_summary', 'children'),
    Input('is_client', 'data'),
    Input('profile_id', 'data'),
    Input('name', 'data')
)
def format_currency(is_client, profile_id, name):
    total, _ = all_total_prior()
    formatted_string = millify(total, precision=2)

    if name == 'all':
        if is_client:
            total, _ = client_total_prior(profile_id=profile_id)
            formatted_string = millify(total, precision=2)
    elif name == 'account_performance':
        formatted_string = millify(accounts_balance(profile_id=profile_id), precision=2)
    elif name == 'dividends_payouts':
        formatted_string = millify(payouts_balance(profile_id=profile_id), precision=2)
    elif name == 'client_goals':
        formatted_string = millify(client_goals_balance(profile_id=profile_id), precision=2)
    elif name == 'investments':
        formatted_string = millify(investments_balance(profile_id=profile_id), precision=2)
    elif name == 'transactions':
        formatted_string = millify(transactions_balance(profile_id=profile_id), precision=2)

    # Use regex to split the string into number and unit
    import re
    match = re.match(r'([\d.,]+)(.*)', formatted_string)
    if match:
        number, unit = match.groups()
        return html.Div([
            html.Span(['R '], className='uk-h3 uk-text-bolder'),
            html.Span([number], className='uk-h2 uk-text-bolder'),  # Larger style for the numeric part
            html.Span([unit], className='uk-h3 uk-text-bolder')  # Regular style for the unit
        ], className='uk-margin-remove-top uk-margin-remove-bottom')
    return html.Span(formatted_string)  # Fallback if string doesn't match the pattern


@callback(
    Output('picture_url', 'src'),
    Output('profile_first_name', 'children'),
    Output('profile_last_name', 'children'),
    Output('profile_email', 'children'),
    Input('profile_picture_url', 'data'),
    Input('first_name', 'data'),
    Input('last_name', 'data'),
    Input('email', 'data')
)
def get_profile(picture_url, first_name, last_name, email):
    return picture_url, first_name, last_name, email


@callback(
    Output('notification-store', 'data'),
    State('profiled', 'data'),
    Input('first_name', 'value'),
    Input('last_name', 'value'),
    prevent_initial_call=True
)
def update_name(profile_id, first_name, last_name):
    if not any([first_name, last_name]):
        raise dash.exceptions.PreventUpdate
    messages = []
    try:
        if first_name:
            supabase.table('profiles').update({'first_name': first_name}).eq('id', profile_id).execute()
            messages.append(f"First name updated to {first_name}.")

        if last_name:
            supabase.table('profiles').update({'last_name': last_name}).eq('id', profile_id).execute()
            messages.append(f"Last name updated to {last_name}.")

        return {"message": " ".join(messages), "type": "success"}
    except Exception as e:
        return {"message": f"Update failed: {str(e)}", "type": "danger"}


app.clientside_callback(
    """
    function(data) {
        if (data && data.message) {
            UIkit.notification({
                message: data.message,
                status: data.type || 'primary',
                pos: 'top-right',
                timeout: 5000
            });
        }
        return '';
    }
    """,
    Output('notification-trigger', 'children'),  # Empty div to trigger JS
    Input('notification-store', 'data')
)


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
            filename, data, file_options={'content-type': content_type, 'upsert': 'true'}
        )

        if response:
            public_url = supabase_admin.storage.from_('profile_pics').get_public_url(filename)
            supabase.table('profiles').update({'profile_picture_url': public_url}).eq('id', profile_id).execute()
            return public_url
    except Exception as e:
        print(f"Error updating profile picture: {e}")

    return profile_pic


if __name__ == '__main__':
    app.run(debug=True)
