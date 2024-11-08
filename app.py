import dash
from dash import Dash, dcc, callback, Output, Input
from dash.html import Div
from sqlalchemy.orm import Session

from utils import supabase, engine, Profile

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

app.config.suppress_callback_exceptions = True

app.layout = Div([
    dcc.Location(id='url'),
    dcc.Store(id='access_token', storage_type='session'),
    dcc.Store(id='profile-id-store'),
    # nav(),
    dash.page_container
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
                    clients = session.query(Profile).all()
                    session.commit()
                    if current_path == dash.page_registry['pages.home']['path']:
                        return dash.page_registry['pages.admin']['path']
                    else:
                        return current_path
            else:
                return dash.page_registry['pages.admin']['path']

    except Exception as e:
        print(e)
        return dash.page_registry['pages.home']['path']


# @app.route('/')
# def get(sess):
#     try:
#         response = supabase.auth.get_user(sess['access_token'])
#         return Title('Blue Chip Invest'), nav(user=response.user), admin.page()
#     except Exception as e:
#         print(f'Authentication error: {e}')
#         user = None
#     return Title('Blue Chip Invest'), nav(), home.page()
#
#
# @app.route('/')
# def post(sess, data: dict):
#     if data['sign_out'] and data['sign_out'] == 'signed-out':
#         try:
#             response = supabase.auth.sign_out()
#             print(response)
#             if response is None: sess['access_token'] = None
#         except Exception as e:
#             print(f'Signing out error: {e}')
#
#     return Title('Blue Chip Invest'), nav(), home.page()
#
#
# @app.route('/admin/', methods=['post'])
# def admin(data: dict, req: Request, sess):
#     try:
#         if data:
#             response = supabase.auth.verify_otp(
#                 {'email': data['form-username'], 'token': data['form-code'], 'type': 'email'}
#             )
#             sess['access_token'] = response.session.access_token
#         else:
#             response = supabase.auth.get_user(jwt=sess['access_token'])
#
#         if response and response.user:
#             admin_users = ['travis@bluechipinvest.co.za', 'eugevanz@gmail.com', 'raymondanthony.m@gmail.com']
#
#             if response.user.email in admin_users:
#                 return Title('Admin'), nav(user=response.user, current_path=req.url.path), admin.page()
#             else:
#                 return Title('Client'), nav(user=response.user, current_path=req.url.path), client_portal.page
#         else:
#             print(response)
#     except Exception as e:
#         return P(f'Admin Authentication error: {e}', cls='uk-text-danger uk-text-bolder')
#
#
# @app.route('/send-invite/')
# def post(data: dict):
#     try:
#         response = supabase_admin.auth.admin.invite_user_by_email(data['form-invite-name'])
#         if response and response.user:
#             return P(f'Invite sent to {data["form-invite-name"]}', cls='uk-text-success uk-text-bolder')
#         else:
#             return P(f'Error sending invite: {response["error"]["message"]}', cls='uk-text-danger uk-text-bolder')
#     except Exception as e:
#         return P(f'Invitation error: {e}', cls='uk-text-danger uk-text-bolder')
#
#
# @app.route('/edit-client/')
# def post(data: dict, req: Request, sess):
#     user, client = None, []
#     try:
#         response = supabase.auth.get_user(sess['access_token'])
#         user = response.user
#
#         client = Session(engine).scalars(select(Profile).where(Profile.email.in_([data['email']]))).first()
#
#     except Exception as e:
#         print(f'Edit Client Authentication error: {e}')
#
#     return Title('Edit Client'), nav(user=user, current_path=req.url.path), edit_client.page(client=client)
#
#
# @app.route('/update-client/', methods=['POST'])
# def post(data: dict):
#     with Session(engine) as session:
#         try:
#             if data['target'] == 'accounts':
#                 session.add(Account(
#                     profile_id=data['profile_id'],
#                     account_number=data['account_number'],
#                     account_type=data['account_type'],
#                     balance=data['balance']
#                 ))
#                 session.commit()  # Commit immediately after adding account
#                 return edit_client.slider_item_account(id=data['profile_id'])
#
#             elif data['target'] == 'investments':
#                 session.add(Investment(
#                     account_id=data['account_id'],
#                     investment_type=data['investment_type'],
#                     symbol=data['symbol'],
#                     quantity=data['quantity'],
#                     purchase_price=data['purchase_price'],
#                     current_price=data['current_price'],
#                     purchase_date=data['purchase_date'],
#                     updated_at=data['updated_at']
#                 ))
#                 session.commit()  # Commit immediately after adding investment
#                 return edit_client.slider_item_investments(profile_id=data['profile_id'])
#
#             elif data['target'] == 'transactions':
#                 session.add(Transaction(
#                     account_id=data['account_id'],
#                     type=data['type'],
#                     amount=data['amount'],
#                     description=data['description']
#                 ))
#                 session.commit()  # Commit immediately after adding transaction
#                 return edit_client.slider_item_transactions(profile_id=data['profile_id'])
#
#             elif data['target'] == 'client_goals':
#                 session.add(ClientGoal(
#                     current_savings=data['current_savings'],
#                     goal_type=data['goal_type'],
#                     profile_id=data['profile_id'],
#                     target_amount=data['target_amount'],
#                     target_date=data['target_date'],
#                     updated_at=data['updated_at']
#                 ))
#                 session.commit()  # Commit immediately after adding client goal
#                 return edit_client.slider_item_client_goals(profile_id=data['profile_id'])
#
#             else:  # This is for dividends or payouts
#                 dividend_payout = DividendOrPayout(
#                     account_id=data['account_id'],
#                     amount=data['amount'],
#                     payment_date=data['payment_date']
#                 )
#                 session.add(dividend_payout)
#                 session.commit()  # Commit immediately after adding dividend payout
#                 return edit_client.slider_item_payouts(profile_id=data['profile_id'])
#
#         except Exception as e:
#             session.rollback()  # Rollback in case of error
#             print(f"Error occurred: {e}")
#             return json.dumps({"error": str(e)}), 400
#
#
# @app.route('/delete-for-client/{table}/{update_id}/{profile_id}/', methods=['DELETE'])
# def delete(table: str, update_id: str, profile_id: str):
#     with Session(engine) as session:
#         if table == 'accounts':
#             session.delete(session.query(Account).filter_by(id=update_id).first())
#             session.commit()  # Commit immediately after adding account
#             return edit_client.slider_item_account(id=profile_id)
#         if table == 'investments':
#             session.delete(session.query(Investment).filter_by(id=update_id).first())
#             session.commit()  # Commit immediately after adding investment
#             return edit_client.slider_item_investments(profile_id=profile_id)
#         if table == 'transactions':
#             session.delete(session.query(Transaction).filter_by(id=update_id).first())
#             session.commit()  # Commit immediately after adding transaction
#             return edit_client.slider_item_transactions(profile_id=profile_id)
#         if table == 'client_goals':
#             session.delete(session.query(ClientGoal).filter_by(id=update_id).first())
#             session.commit()  # Commit immediately after adding client goal
#             return edit_client.slider_item_client_goals(profile_id=profile_id)
#         if table == 'dividends_and_payouts': session.delete(
#             session.query(DividendOrPayout).filter_by(id=update_id).first())
#
#         session.commit()
#
#
# @app.route('/select-date', methods=['POST'])
# def post(data: dict):
#     selected_date = data['date']
#     # Here you can do something with the selected date, like saving it or processing it
#     return json.dumps(selected_date)
#
#
# @app.route('/calendar', methods=['POST'])
# def calendar(data: dict):
#     year = data.get('year', datetime.now().year)
#     month = data.get('month', datetime.now().month)
#
#     # Your logic to generate the calendar view
#     calendar_html = calendar_view(year, month)  # Define this function as needed
#
#     return calendar_html
#
#
# @app.route('/slider-item/{item_type}/{profile_id}/', methods=['GET'])
# def get_slider_item(item_type: str, profile_id: str):
#     if item_type == 'accounts':
#         return edit_client.slider_item_account(id=profile_id)
#
#     elif item_type == 'investments':
#         return edit_client.slider_item_investments(profile_id=profile_id)
#
#     elif item_type == 'transactions':
#         return edit_client.slider_item_transactions(profile_id=profile_id)
#
#     elif item_type == 'client-goals':
#         return edit_client.slider_item_client_goals(profile_id=profile_id)
#
#     elif item_type == 'payouts':
#         return edit_client.slider_item_payouts(profile_id=profile_id)
#
#     else:
#         return json.dumps({"error": "Invalid item type"})


if __name__ == '__main__':
    app.run(debug=True)
