import dash
from dash import Dash, dcc, callback, Output, Input
from dash.html import Div
from sqlalchemy.orm import Session

from components.navbar import navbar
from utils import supabase, engine

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

app.layout = Div([
    dcc.Location(id='url'),
    dcc.Store(id='access_token', storage_type='session'),
    dcc.Store(id='profile-id-store'),
    dcc.Loading([dash.page_container], id='page-loading', type='circle', fullscreen=True)
])


@callback(
    Output('url', 'pathname'),
    Input('access_token', 'data'),
    Input('url', 'pathname')
)
def skip_login_page_if_token_exists(access_token, current_path):
    try:
        response = supabase.auth.get_user(jwt=access_token)
        if response and response.user:
            admin_users = ['travis@bluechipinvest.co.za', 'eugevanz@gmail.com', 'raymondanthony.m@gmail.com']

            if response.user.email in admin_users:
                with Session(engine) as session:
                    session.commit()
                    if current_path == dash.page_registry['pages.home']['path']:
                        return f'/admin/{response.user.id}/'
                    else:
                        return current_path
            else:
                return f'/client_portal/{response.user.id}/'

    except Exception as e:
        print(e)
        return dash.page_registry['pages.home']['path']


@callback(
    Output('nav', 'children'),
    Input('url', 'pathname')
)
def show_current_location(pathname):
    return navbar(pathname)


@callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('access_token', 'data', allow_duplicate=True)],
    Input('sign_out', 'n_clicks'),
    prevent_initial_call=True
)
def sign_out(n_clicks):
    if n_clicks:
        return ['/', None]
    else:
        return [dash.no_update, dash.no_update]


if __name__ == '__main__':
    app.run(debug=True)
