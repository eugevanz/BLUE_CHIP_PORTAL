from os import environ

import supabase
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import create_client

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SUPABASE_URL = environ.get('SUPABASE_URL')
SUPABASE_KEY = environ.get('SUPABASE_KEY')
SUPABASE_SERVICE_ROLE_KEY = environ.get('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_PASSWORD = environ.get('SUPABASE_PASSWORD')
supabase_ = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
supabase_admin = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_SERVICE_ROLE_KEY)


# PAGES Routes


@app.get("/admin/", response_class=HTMLResponse)
def admin(request: Request):
    profile_data = {
        "profile_picture_url": request.cookies.get("profile_picture_url"),
        "first_name": request.cookies.get("first_name"),
        "last_name": request.cookies.get("last_name"),
        "email": request.cookies.get("email")
    }
    return templates.TemplateResponse(request=request, name="admin.html", context=profile_data)


@app.get("/client/", response_class=HTMLResponse)
def client(request: Request):
    profile_data = {
        "profile_picture_url": request.cookies.get("profile_picture_url"),
        "first_name": request.cookies.get("first_name"),
        "last_name": request.cookies.get("last_name"),
        "email": request.cookies.get("email")
    }
    return templates.TemplateResponse(request=request, name="client.html", context=profile_data)


# LOGON
@app.get("/sign_out/")
def sign_out(response: Response):
    supabase_admin.auth.sign_out()
    response.delete_cookie("profile_picture_url")
    response.delete_cookie("first_name")
    response.delete_cookie("last_name")
    response.delete_cookie("profile_type")
    response.delete_cookie("email")
    response.delete_cookie("access_token")

    return RedirectResponse("/")


@app.post("/request_otp/", response_class=HTMLResponse)
def request_otp(email: str = Form(...)):
    response = supabase_admin.auth.sign_in_with_otp({"email": email, "options": {"should_create_user": False}})

    if response and response.user is None:
        return HTMLResponse(content=f"""<form action="/verify_otp/" method="post" class="uk-margin">
            <h3 class="uk-card-title uk-text-bolder uk-margin-remove-bottom">Ready to sign-in?</h3>
            <p class="uk-text-small uk-margin-remove-top" style="color: #091235;">
                Please enter the <strong>verification code</strong> that was sent to your email. This code is required
                to verify your identity and complete the login process.
            </p>
            <div class="uk-text-small">One-time PIN</div>
            <div class="uk-inline">
                <span class="uk-form-icon" uk-icon="icon: lock"></span>
                <input class="uk-input uk-form-width-large" name="sent_code" type="text">
            </div>
            <input name="sent_email" type="hidden" value="{email}" required>
            <p class="uk-text-meta">Please enter your OTP and click Sign In.</p>
            <button class="uk-button uk-button-large uk-light" style="background-color:#091235;">Sign In</button>
        </form>""")
    else:
        return HTMLResponse(
            content=f"<p class='uk-text-danger' id='send_code_notifications'>{response.error_message}</p>")


@app.post("/verify_otp/", response_class=HTMLResponse)
async def verify_otp(response: Response, sent_email: str = Form(...), sent_code: str = Form(...)):
    auth_response = supabase_admin.auth.verify_otp({"email": sent_email, "token": sent_code, "type": "email"})

    if auth_response and auth_response.user:
        profile_response = supabase_.table("profiles").select("*").eq(
            "id", auth_response.user.id
        ).limit(1).execute()
        profile = profile_response.data[0]
        response.set_cookie(key="profile_picture_url", value=profile['profile_picture_url'])
        response.set_cookie(key="first_name", value=profile['first_name'])
        response.set_cookie(key="last_name", value=profile['last_name'])
        response.set_cookie(key="profile_type", value=profile['profile_type'])
        response.set_cookie(key="email", value=profile['email'])
        response.set_cookie(key="access_token", value=auth_response.session.access_token, httponly=True, secure=True)

        return RedirectResponse("/admin/") if profile["profile_type"] == "admin" else RedirectResponse("/client/")
    else:
        RedirectResponse("/login/")


# ACCOUNT Routes
@app.get("/select_all_from_accounts_where_profile_id/{profile_id}/")
def select_all_from_accounts_where_profile_id(profile_id):
    response = supabase_.table("accounts").select('*').eq("profile_id", profile_id).execute()
    if response:
        return {"accounts": response.data}
    else:
        return {"accounts": []}


@app.post("/insert_account/")
def insert_account(account_type: str = Form(...), balance: float = Form(...)):
    account_number = f"ACC{int(accounts[-1][3:]) + 1}"
    if request.method == 'POST':
        profile_id = request.args.get('profile_id', None)
        account_number = request.args.get('account_number', None)
        account_type = request.args.get('account_type', None)
        balance = request.args.get('balance', None)

        if profile_id and account_number and account_type and balance:
            try:
                response = supabase.table('accounts').insert({
                    'profile_id': profile_id, 'account_number': account_number, 'account_type': account_type,
                    'balance': balance
                }).execute()
                # Check if the response was successful
                if response.status_code == 201:
                    return {'message': 'Account added successfully'}
                else:
                    return {'message': 'Failed to add account', 'error': response.error_message}
            except Exception as e:
                return {'message': 'An error occurred', 'error': str(e)}


@app.route('/delete_from_accounts/<item_id>/')
def delete_from_accounts(item_id: str):
    response = supabase.table('accounts').delete().eq('id', item_id).execute()
    if response.error:
        raise {'message': 'Failed to delete account', 'error': response.error_message}
    if response.data:
        return {'message': f'Account with ID {item_id} deleted successfully'}
    else:
        raise {'message': 'Failed to delete account', 'error': 'Account not found'}


# CLIENT GOAL Routes
@app.route('/select_all_from_client_goals_where_profile_id/<profile_id>/')
def select_all_from_client_goals_where_profile_id(profile_id: str):
    response = supabase.table('client_goals').select('*').eq('profile_id', profile_id).execute()
    rows = response.data
    if rows:
        return {'client_goals': rows}
    else:
        return {'client_goals': []}


@app.route('/insert_client_goal/', methods=['POST'])
def insert_client_goal():
    if request.method == 'POST':
        profile_id = request.args.get('profile_id', None)
        goal_type = request.args.get('goal_type', None)
        target_amount = request.args.get('target_amount', None)
        current_savings = request.args.get('current_savings', None)
        target_date = request.args.get('target_date', None)

        if profile_id and goal_type and target_amount and current_savings and target_date:
            try:
                response = supabase.table('client_goals').insert({
                    'profile_id': profile_id, 'goal_type': goal_type, 'target_amount': target_amount, 'current_savings':
                        current_savings, 'target_date': target_date
                }).execute()
                # Check if the response was successful
                if response.status_code == 201:
                    return {'message': 'Client Goal added successfully'}
                else:
                    return {'message': 'Failed to add Client Goal', 'error': response.error_message}
            except Exception as e:
                return {'message': 'An error occurred', 'error': str(e)}


@app.route('/delete_from_client_goals/<item_id>/')
def delete_from_client_goals(item_id: str):
    response = supabase.table('client_goals').delete().eq('id', item_id).execute()
    if response.error:
        raise {'message': 'Failed to delete client goal', 'error': response.error_message}
    if response.data:
        return {'message': f'Client Goal with ID {item_id} deleted successfully'}
    else:
        raise {'message': 'Failed to delete Client Goal', 'error': 'Client Goal not found'}


# DIVIDENDS AND PAYOUTS Routes
@app.route('/select_all_from_dividends_payouts_where_profile_id/<account_id>/')
def select_all_from_dividends_payouts_where_profile_id(account_id: str):
    response = supabase.table('dividends_and_payouts').select('*').eq('account_id', account_id).execute()
    rows = response.data
    if rows:
        return {'dividends_and_payouts': rows}
    else:
        return {'dividends_and_payouts': []}


@app.route('/insert_dividend_payout/', methods=['POST'])
def insert_dividend_payout():
    if request.method == 'POST':
        account_id = request.args.get('account_id', None)
        amount = request.args.get('amount', None)
        payment_date = request.args.get('payment_date', None)

        if account_id and amount and payment_date:
            try:
                response = supabase.table('dividends_and_payouts').insert({
                    'account_id': account_id, 'amount': amount, 'payment_date': payment_date
                }).execute()
                # Check if the response was successful
                if response.status_code == 201:
                    return {'message': 'Dividend/Payout added successfully'}
                else:
                    return {'message': 'Failed to add Dividend/Payout', 'error': response.error_message}
            except Exception as e:
                return {'message': 'An error occurred', 'error': str(e)}


@app.route('/delete_from_dividends_and_payouts/<item_id>/')
def delete_from_dividends_and_payouts(item_id: str):
    response = supabase.table('dividends_and_payouts').delete().eq('id', item_id).execute()
    if response.error:
        raise {'message': 'Failed to delete dividend/payout', 'error': response.error_message}
    if response.data:
        return {'message': f'Dividend/Payout with ID {item_id} deleted successfully'}
    else:
        raise {'message': 'Failed to delete Dividend/Payout', 'error': 'Dividend/Payout not found'}


# INVESTMENTS Routes
@app.route('/select_all_from_investments_where_profile_id/<account_id>/')
def select_all_from_investments_where_profile_id(account_id: str):
    response = supabase.table('investments').select('*').eq('account_id', account_id).execute()
    rows = response.data
    if rows:
        return {'investments': rows}
    else:
        return {'investments': []}


@app.route('/insert_investment/', methods=['POST'])
def insert_investment():
    if request.method == 'POST':
        account_id = request.args.get('account_id', None)
        investment_type = request.args.get('investment_type', None)
        symbol = request.args.get('symbol', None)
        quantity = request.args.get('quantity', None)
        purchase_price = request.args.get('purchase_price', None)
        current_price = request.args.get('current_price', None)
        purchase_date = request.args.get('purchase_date', None)

        if (account_id and investment_type and symbol and quantity and purchase_price and current_price and
                purchase_date):
            try:
                response = supabase.table('investments').insert({
                    'account_id': account_id, 'investment_type': investment_type, 'symbol': symbol,
                    'quantity': quantity,
                    'purchase_price': purchase_price, 'current_price': current_price, 'purchase_date': purchase_date
                }).execute()
                # Check if the response was successful
                if response.status_code == 201:
                    return {'message': 'Investment added successfully'}
                else:
                    return {'message': 'Failed to add Investments', 'error': response.error_message}
            except Exception as e:
                return {'message': 'An error occurred', 'error': str(e)}


@app.route('/delete_from_investments/<item_id>/')
def delete_from_investments(item_id: str):
    response = supabase.table('investments').delete().eq('id', item_id).execute()
    if response.error:
        raise {'message': 'Failed to delete investment', 'error': response.error_message}
    if response.data:
        return {'message': f'Investment with ID {item_id} deleted successfully'}
    else:
        raise {'message': 'Failed to delete Investment', 'error': 'Investment not found'}


# TRANSACTIONS Routes
@app.route('/select_all_from_transactions_where_profile_id/<account_id>/')
def select_all_from_transactions_where_profile_id(account_id: str):
    response = supabase.table('transactions').select('*').eq('account_id', account_id).execute()
    rows = response.data
    if rows:
        return {'transactions': rows}
    else:
        return {'transactions': []}


@app.route('/insert_transaction/', methods=['POST'])
def insert_transaction():
    if request.method == 'POST':
        account_id = request.args.get('account_id', None)
        trn_type = request.args.get('trn_type', None)
        amount = request.args.get('amount', None)
        description = request.args.get('description', None)

        if account_id and trn_type and amount and description:
            try:
                response = supabase.table('transactions').insert({
                    'account_id': account_id, 'type': trn_type, 'amount': amount, 'description': description
                }).execute()
                # Check if the response was successful
                if response.status_code == 201:
                    return {'message': 'Transaction added successfully'}
                else:
                    return {'message': 'Failed to add Transaction', 'error': response.error_message}
            except Exception as e:
                return {'message': 'An error occurred', 'error': str(e)}


@app.route('/delete_from_transactions/<item_id>/')
def delete_from_transactions(item_id: str):
    response = supabase.table('transactions').delete().eq('id', item_id).execute()
    if response.error:
        return {'message': 'Failed to delete transaction', 'error': response.error_message}
    if response.data:
        return {'message': f'Transaction with ID {item_id} deleted successfully'}
    else:
        return {'message': 'Failed to delete Transaction', 'error': 'Transaction not found'}


# PROFILES Routes
@app.route('/update_profile/', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        profile_id = request.args.get('profile_id', None)
        profile_picture_url = request.args.get('profile_picture_url', None)
        first_name = request.args.get('first_name', None)
        last_name = request.args.get('last_name', None)

        update_data = {}
        if profile_picture_url is not None:
            update_data['profile_picture_url'] = profile_picture_url
        if first_name is not None:
            update_data['first_name'] = first_name
        if last_name is not None:
            update_data['last_name'] = last_name

        if not update_data:
            return {'message': 'No fields provided for update'}
        # Perform the update
        response = supabase.table('profiles').update(update_data).eq('id', profile_id).execute()

        if response.error:
            return {'message': 'Failed to update profile', 'error': response.error_message}
        # Check if the profile was updated
        if response.data:
            return {'message': 'Profile updated successfully', 'updated_data': response.data}
        else:
            return {'message': 'Profile not found'}


# UTILITY Routes
@app.route('/send_invite/')
def send_invite(email: str):
    response = supabase_admin.auth.admin.invite_user_by_email(email)
    if response and response.user:
        return {'message': f'Invite sent to {response.user.email}'}
    else:
        return {'message': f'Error sending invite: {response["error"]["message"]}'}


# PARTIAL Routes
@app.route('/card_header/')
def card_header():
    total = request.args.get('total', None)
    prior = request.args.get('prior', None)

    if total and prior:
        difference = (float(total) - float(prior)) / float(prior) * 100 if float(prior) != 0 and float(
            total) != 0 else 0
        return f"""<div>
            Compared to last month 
            <span class="uk-text-bolder">
                <span>{'+' if difference > 0 else ''}</span> {difference:.2f} %
            </span>
        </div>"""


@app.route('/navbar/')
def navbar():
    return '''<div class="uk-section-xsmall">
      <div class="uk-container">
        <div data-uk-grid="true" class="uk-grid-medium uk-flex-middle uk-child-width-1-2@m">
          <div class="uk-width-auto">
            <div class="uk-logo uk-flex">
              <div>
                <img src="https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/Blue%20Chip%20Invest%20Logo.001.png" width="60" height="60">
                <div style="font-family: 'Noto Sans', sans-serif; font-optical-sizing: auto; font-weight: 400; font-style: normal; line-height: 22px; color: #88A9C3; width: 164px;">
                  BLUE CHIP INVESTMENTS
                </div>
              </div>
            </div>
          </div>
          <div class="uk-width-expand">
            <div data-uk-slider="autoplay: true; autoplay-interval: 3000" class="uk-slider-items uk-child-width-1-2 uk-child-width-1-4@s uk-child-width-1-6@m uk-grid">
              <!-- Ticker Information (Example for MSFT) -->
              <div>
                <div style="font-size: 11px; height: 14px; overflow: hidden;">MSFT</div>
                <div class="uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate">R 3500.00</div>
                <div class="uk-text-small uk-margin-remove-top">
                  1.5% <span data-uk-icon="triangle-up" class="uk-text-success"></span>
                </div>
              </div>
              <!-- Repeat for other tickers (GOOGL, AAPL, etc.) -->
              <div>
                <div style="font-size: 11px; height: 14px; overflow: hidden;">GOOGL</div>
                <div class="uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate">R 2700.00</div>
                <div class="uk-text-small uk-margin-remove-top">
                  -0.5% <span data-uk-icon="triangle-down" class="uk-text-danger"></span>
                </div>
              </div>
              <!-- Add other tickers similarly... -->
            </div>
          </div>
        </div>
        <hr>
        <div>
          <nav>
            <ul class="uk-breadcrumb">
              <!-- Example breadcrumb items -->
              <li><a href="/">Home</a></li>
              <li><a href="/investments">Investments</a></li>
              <li><span>Current</span></li>
            </ul>
          </nav>
        </div>
      </div>
    </div>'''
    #
    #
    # @callback(
    #     Output('highest_', 'children'),
    #     Output('mid_', 'children'),
    #     Output('lowest_', 'children'),
    #     Input('name', 'data'),
    #     Input('column', 'data'),
    #     Input('profile_id', 'data')
    # )
    # def get_y_axis(name, column, profile_id):
    #     table = cur.execute('SELECT * FROM ? WHERE profile_id = ?', (name, profile_id,)).fetchall()
    #     lowest_ = min(table, key=lambda x: x[column], default=None)[column]
    #     highest_ = max(table, key=lambda x: x[column], default=None)[column]
    #     mid_ = (highest_ + lowest_) / 2
    #     return f'R {millify(highest_)}', f'R {millify(mid_)}', f'R {millify(lowest_)}'
    #
    #
    # @callback(
    #     Output('total_summary', 'children'),
    #     Input('is_client', 'data'),
    #     Input('profile_id', 'data'),
    #     Input('name', 'data')
    # )
    # def format_currency(is_client, profile_id, name):
    #     total, _ = all_total_prior()
    #     formatted_string = millify(total, precision=2)
    #
    #     if name == 'all':
    #         if is_client:
    #             total, _ = client_total_prior(profile_id=profile_id)
    #             formatted_string = millify(total, precision=2)
    #     elif name == 'account_performance':
    #         formatted_string = millify(accounts_balance(profile_id=profile_id), precision=2)
    #     elif name == 'dividends_payouts':
    #         formatted_string = millify(payouts_balance(profile_id=profile_id), precision=2)
    #     elif name == 'client_goals':
    #         formatted_string = millify(client_goals_balance(profile_id=profile_id), precision=2)
    #     elif name == 'investments':
    #         formatted_string = millify(investments_balance(profile_id=profile_id), precision=2)
    #     elif name == 'transactions':
    #         formatted_string = millify(transactions_balance(profile_id=profile_id), precision=2)
    #
    #     # Use regex to split the string into number and unit
    #     import re
    #     match = re.match(r'([\d.,]+)(.*)', formatted_string)
    #     if match:
    #         number, unit = match.groups()
    #         return html.Div([
    #             html.Span(['R '], className='uk-h3 uk-text-bolder'),
    #             html.Span([number], className='uk-h2 uk-text-bolder'),  # Larger style for the numeric part
    #             html.Span([unit], className='uk-h3 uk-text-bolder')  # Regular style for the unit
    #         ], className='uk-margin-remove-top uk-margin-remove-bottom')
    #     return html.Span(formatted_string)  # Fallback if string doesn't match the pattern
    #
    #
    # @callback(
    #     Output('picture_url', 'src'),
    #     Output('profile_first_name', 'children'),
    #     Output('profile_last_name', 'children'),
    #     Output('profile_email', 'children'),
    #     Input('profile_picture_url', 'data'),
    #     Input('first_name', 'data'),
    #     Input('last_name', 'data'),
    #     Input('email', 'data')
    # )
    # def get_profile(picture_url, first_name, last_name, email):
    #     return picture_url, first_name, last_name, email
    #
    #
    # @callback(
    #     Output('notification-store', 'data'),
    #     State('profiled', 'data'),
    #     Input('first_name', 'value'),
    #     Input('last_name', 'value'),
    #     prevent_initial_call=True
    # )
    # def update_name(profile_id, first_name, last_name):
    #     if not any([first_name, last_name]):
    #         raise dash.exceptions.PreventUpdate
    #     messages = []
    #     try:
    #         if first_name:
    #             supabase.table('profiles').update({'first_name': first_name}).eq('id', profile_id).execute()
    #             messages.append(f"First name updated to {first_name}.")
    #
    #         if last_name:
    #             supabase.table('profiles').update({'last_name': last_name}).eq('id', profile_id).execute()
    #             messages.append(f"Last name updated to {last_name}.")
    #
    #         return {"message": " ".join(messages), "type": "success"}
    #     except Exception as e:
    #         return {"message": f"Update failed: {str(e)}", "type": "danger"}
    #
    #
    # app.clientside_callback(
    #     """
    #     function(data) {
    #         if (data && data.message) {
    #             UIkit.notification({
    #                 message: data.message,
    #                 status: data.type || 'primary',
    #                 pos: 'top-right',
    #                 timeout: 5000
    #             });
    #         }
    #         return '';
    #     }
    #     """,
    #     Output('notification-trigger', 'children'),  # Empty div to trigger JS
    #     Input('notification-store', 'data')
    # )
    #
    #
    # @callback(
    #     Output('profile_pic', 'src'),
    #     Input('upload-image', 'contents'),
    #     State('upload-image', 'filename'),
    #     State('profile-id-store', 'data'),
    #     State('profile-pic-store', 'data'),
    #     prevent_initial_callback=True
    # )
    # def update_profile_pic(contents, filename, profile_id, profile_pic):
    #     if not contents: return profile_pic
    #
    #     # MAX_FILE_SIZE = 5 * 1024 * 1024
    #     content_type, content_string = contents.split(',')
    #     if not content_type.startswith('data:image/'): return profile_pic
    #
    #     try:
    #         data = base64.b64decode(content_string)
    #         response = supabase_admin.storage.from_('profile_pics').upload(
    #             filename, data, file_options={'content-type': content_type, 'upsert': 'true'}
    #         )
    #
    #         if response:
    #             public_url = supabase_admin.storage.from_('profile_pics').get_public_url(filename)
    #             supabase.table('profiles').update({'profile_picture_url': public_url}).eq('id', profile_id).execute()
    #             return public_url
    #     except Exception as e:
    #         print(f"Error updating profile picture: {e}")
    #
    #     return profile_pic


if __name__ == '__main__':
    app.run(debug=True)
