import dash
from dash import html
from sqlalchemy.orm import Session

from utils import Profile, engine


def navbar(pathname: str):
    # if pathname == '/':
    #     return [('Home', '/')]

    # Split the pathname into segments and remove empty strings
    # segments = [segment for segment in pathname.split('/') if segment]
    #
    # profile_id = segments[-1]
    # email = None
    # with Session(engine) as session:
    #     profile = session.query(Profile).filter_by(id=profile_id).first()
    #     if profile:
    #         email = profile.email
    #
    # # Prepend 'edit' if any of the specified segments are present
    # add_operations = {'add-account', 'add-client-goal', 'add-investment', 'add-payout', 'add-transaction'}
    # if any(segment in add_operations for segment in segments):
    #     segments.insert(0, 'edit')
    #
    # # Always insert 'admin' at the beginning if not present
    # if 'admin' not in segments and 'home' not in segments and 'client_portal' not in segments:
    #     segments.insert(0, 'admin')

    # Initialize breadcrumbs and profile_id
    location = next((page['name'] for page in dash.page_registry.values() if page['path'] == pathname), None)
    # profile_id = None
    #
    # # Cache page paths for faster lookup
    # page_paths = {page['path']: page['name'] for page in dash.page_registry.values()}
    #
    # # Identify the profile ID
    # for segment in segments:
    #     if f"/{segment}/" not in page_paths:
    #         profile_id = segment
    #         break
    #
    # # Build breadcrumbs
    # for segment in segments:
    #     for page_path, page_name in page_paths.items():
    #         if f"/{segment}/" in page_path:
    #             # Include the profile_id for specific operations
    #             if segment in add_operations | {'edit'} and profile_id:
    #                 breadcrumbs.append((page_name, f"{page_path.rstrip('/')}/{profile_id}"))
    #             else:
    #                 breadcrumbs.append((page_name, page_path))
    #             break  # Stop searching once a match is found

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
                                     style={'fontFamily': '"Noto Sans", sans-serif', 'fontOpticalSizing': 'auto',
                                            'fontWeight': '400', 'fontStyle': 'normal', 'lineHeight': '22px',
                                            'color': '#091235', 'width': '164px'})
                        ], className='uk-navbar-item uk-logo'),
                        html.Div([location]),
                    ], className='uk-navbar-left'),
                    html.Div([
                        html.Ul([
                            html.Li([html.A(href='', **{'data-uk-icon': 'icon: home'})]),
                            html.Li([html.A(href='', **{'data-uk-icon': 'icon: users'})])
                        ], className='uk-iconnav'),
                    ], className='uk-navbar-right')
                ], **{'data-uk-navbar': 'true'})
            ], className='uk-padding')
        ], className='uk-navbar-container')
    ], **{'data-uk-sticky': 'sel-target: .uk-navbar-container; className-active: uk-navbar-sticky'})
