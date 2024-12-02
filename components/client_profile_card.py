from dash import html, dcc

from utils import Profile


def client_profile(profile: Profile):
    # Fallback values
    default_picture_url = ('https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica'
                           '-koletic-7YVZYZeITc8-unsplash_3_11zon.webp')

    pro_data = {
        'picture_url': profile.profile_picture_url or default_picture_url,
        'first_name': profile.first_name or 'First Name',
        'last_name': profile.last_name or 'Last Name',
        'created_at': profile.created_at.strftime("%B %d, %Y") if profile.created_at else 'Unknown',
        'email': profile.email or 'No email provided'
    }

    return html.Div([
        dcc.Store('profile-pic-store', data=pro_data['picture_url']),
        html.Div([
            html.Img(className='uk-border-circle uk-margin', width='64', height='64',
                     src=pro_data['picture_url'], alt='profile-pic'),
            dcc.Input(
                className='uk-form-blank uk-h3 uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate',
                value=pro_data['first_name'],
                debounce=True,
                id='first_name'),
            dcc.Input(className='uk-form-blank uk-h3 uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate',
                      value=pro_data['last_name'], debounce=True, id='last_name'),
            html.Div([pro_data['email']], className='uk-text-small uk-margin-remove-top uk-text-truncate')
        ], className='uk-card uk-card-body uk-flex uk-flex-column uk-light')
    ], className='uk-width-1-4@m')
