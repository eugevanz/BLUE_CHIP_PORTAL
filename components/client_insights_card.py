from dash import html, dcc

from utils import format_currency, custom_colours, supabase, all_accounts_balance, card_header, \
    all_prior_accounts_balance


def client_insights(width_class: str = None):
    """Generate the Client Insights card layout."""
    profiles_response = supabase.table('profiles').select('*').eq('profile_type', 'client').execute()
    profiles = profiles_response.data

    # Construct the layout
    return html.Div([
        dcc.Store(id='selected-profile-id'),  # Store to hold selected profile ID
        html.Div([
            # Card header: Insights summary
            html.Div([
                html.Div(['Client Insights'], className='uk-text-small'),
                format_currency(all_accounts_balance),
                html.Div(
                    card_header(all_accounts_balance, all_prior_accounts_balance),
                    className='uk-text-small uk-margin-remove-top'
                )
            ], className='uk-card-header'),
            # Card body: Profile table
            html.Div([
                html.Div([
                    html.Table([
                        html.Tbody([
                            # Create a row for each client
                            html.Tr([
                                # Client details
                                html.Td([
                                    html.A([
                                        html.Div(
                                            html.Img(
                                                className='uk-border-circle', width='60', height='60',
                                                src=client['profile_picture_url'] or '',
                                                alt='profile-pic'
                                            ) if client['profile_picture_url'] else html.Span(
                                                **{'data-uk-icon': 'icon: user; ratio: 3;'}),
                                            className='uk-width-auto'
                                        ),
                                        html.Div([
                                            html.H3([
                                                html.Span(client['first_name'] or 'First name',
                                                          className='uk-text-bolder'),
                                                html.Br(),
                                                client['last_name'] or 'Last name'
                                            ], className='uk-card-title uk-margin-remove-bottom'),
                                            html.Div(client['email'] or 'No email provided', style={'fontSize': '11px'})
                                        ], className='uk-width-expand')
                                    ], className='uk-grid-small uk-link-reset',
                                        **{'data-uk-grid': 'true'}, href=f'/edit/{str(client["id"])}/')
                                ], className='uk-flex uk-flex-middle uk-flex-between uk-margin-left uk-margin-right')
                            ], className='uk-animation-fade') for client in profiles
                        ]) if profiles else None  # Show table rows if profiles exist
                    ], className='uk-table uk-table-middle uk-table-divider uk-table-hover')
                ], **{'data-uk-overflow-auto': 'true'}, className='uk-height-large')
            ], className='uk-card-body uk-padding-remove'),
            html.Div([
                html.Form([
                    html.Span(**{'data-uk-search-icon': 'true'}),
                    dcc.Input(id='client-search', type='search', placeholder='Search', className='uk-search-input'),
                ], className='uk-search uk-search-default uk-width-1-1'),
            ], className='uk-card-footer')
        ], className='uk-card uk-card-default uk-light', style={'backgroundColor': custom_colours[0]})
    ], className=width_class, id='client-insights')
