from dash import html, dcc


def client_profile(profile):
    return html.Div([
        dcc.Store('profiled', data=profile['id']),
        dcc.Store(id='notification-store'),
        html.Div([
            html.Img(className='uk-border-circle uk-margin', width='64', height='64',
                     src=profile['profile_picture_url'], alt='profile-pic'),
            dcc.Input(className='uk-form-blank uk-h3 uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom '
                                'uk-text-truncate', debounce=True, id='first_name', value=profile['first_name']),
            dcc.Input(className='uk-form-blank uk-h3 uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate',
                      debounce=True, id='last_name', value=profile['last_name']),
            html.Div([profile['email']], className='uk-text-small uk-margin-remove-top uk-text-truncate')
        ], className='uk-card uk-card-body uk-flex uk-flex-column uk-light')
    ], className='uk-width-1-4@m')
