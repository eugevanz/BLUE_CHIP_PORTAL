from datetime import datetime
from os import environ
from typing import Optional, List

import libsql_experimental as libsql
from pydantic import BaseModel, Field, UUID4


class Account(BaseModel):
    id: UUID4 = Field(..., description="Unique identifier for the account (primary key).")
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the account was created (nullable)."
    )
    profile_id: Optional[UUID4] = Field(
        default=None,
        description="Foreign key referencing the profile (nullable)."
    )
    account_number: str = Field(
        ...,
        description="Unique account number (not nullable)."
    )
    account_type: str = Field(
        ...,
        description="Type of account (not nullable)."
    )
    balance: Optional[float] = Field(
        default=None,
        description="Current balance of the account (nullable)."
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the account was last updated (nullable)."
    )


class Accounts(BaseModel):
    accounts: List[Account]


class ClientGoal(BaseModel):
    id: Optional[str] = Field(default=None, description="Unique identifier for the goal, generated as a lower hex.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the goal was created.")
    profile_id: str = Field(..., description="Foreign key referencing the profile associated with this goal.")
    goal_type: str = Field(..., description="Type of goal (e.g., retirement, education).")
    target_amount: float = Field(..., description="Target amount to achieve the goal.")
    current_savings: float = Field(default=0.0, description="Current savings towards the goal.")
    target_date: Optional[str] = Field(default=None, description="Target date to achieve the goal, nullable.")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the goal was last updated.")


class ClientGoals(BaseModel):
    client_goals: List[ClientGoal]


class DividendPayout(BaseModel):
    id: Optional[str] = Field(default=None, description="Unique identifier for the payout, generated as a lower hex.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the payout was recorded.")
    account_id: str = Field(..., description="Foreign key referencing the account receiving the payout.")
    amount: float = Field(..., description="Amount of the dividend or payout.")
    payment_date: datetime = Field(..., description="Date of the dividend or payout.")


class DividendPayouts(BaseModel):
    dividends_payouts: List[DividendPayout]


class Investment(BaseModel):
    id: Optional[str] = Field(default=None,
                              description="Unique identifier for the investment, generated as a lower hex.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the investment was recorded.")
    account_id: str = Field(..., description="Foreign key referencing the account holding the investment.")
    investment_type: str = Field(..., description="Type of investment (e.g., stocks, bonds).")
    symbol: str = Field(..., description="Ticker symbol or identifier for the investment.")
    quantity: float = Field(..., description="Quantity of the investment.")
    purchase_price: float = Field(..., description="Price per unit at the time of purchase.")
    current_price: float = Field(..., description="Current price per unit.")
    purchase_date: datetime = Field(..., description="Date when the investment was purchased.")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the investment was last updated.")


class Investments(BaseModel):
    investments: List[Investment]


class Transaction(BaseModel):
    id: Optional[str] = Field(default=None,
                              description="Unique identifier for the transaction, generated as a lower hex.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           description="Timestamp when the transaction was recorded.")
    account_id: str = Field(..., description="Foreign key referencing the account associated with the transaction.")
    type: str = Field(..., description="Type of transaction (e.g., deposit, withdrawal).")
    amount: float = Field(..., description="Amount of money involved in the transaction.")
    description: Optional[str] = Field(default=None, description="Optional description of the transaction.")


class Transactions(BaseModel):
    transactions: List[Transaction]
#
#
# def create_profiles():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS profiles ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL, "
#             "profile_picture_url TEXT DEFAULT "
#             "'https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica-koletic"
#             "-7YVZYZeITc8-unsplash_3_11zon.webp' NOT NULL,"
#             "first_name TEXT DEFAULT 'First name' NOT NULL,"
#             "last_name TEXT DEFAULT 'Last name' NOT NULL,"
#             "phone_number TEXT DEFAULT '' NULL,"
#             "profile_type TEXT DEFAULT 'client' NOT NULL,"
#             "date_of_birth TEXT NULL,"
#             "address TEXT DEFAULT '' NOT NULL,"
#             "email TEXT DEFAULT 'email@address.com' NOT NULL);"
#         )

#
# def create_accounts():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS accounts ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "profile_id TEXT NOT NULL,"
#             "account_number TEXT NOT NULL,"
#             "account_type TEXT NOT NULL,"
#             "balance REAL DEFAULT 0.0 NOT NULL,"
#             "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE);"
#         )

#
# def delete_from_accounts(item_id: str):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(f'DELETE FROM accounts WHERE id = ?', (item_id,))

#
# def create_client_goals():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS client_goals ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "profile_id TEXT NOT NULL,"
#             "goal_type TEXT NOT NULL,"
#             "target_amount REAL NOT NULL,"
#             "current_savings REAL DEFAULT 0.0 NOT NULL,"
#             "target_date TEXT NULL,"
#             "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE);"
#         )
#
#
# def select_all_from_client_goals_where_profile_id(profile_id: str) -> [tuple]:
#     with conn:
#         cur = conn.cursor()
#         rows = cur.execute('SELECT * FROM client_goals WHERE profile_id = ?', (profile_id,)).fetchall()
#         return [ClientGoal.model_validate(dict(client_goal) for client_goal in rows)]
#
#
# def insert_client_goals(client_goal: ClientGoal):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             'INSERT INTO client_goals (profile_id, goal_type, target_amount, current_savings, target_date) '
#             'VALUES (:profile_id, :goal_type, :target_amount, :current_savings, :target_date)',
#             (client_goal.model_dump())
#         )
#
#
# def delete_from_client_goals(item_id: str):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(f'DELETE FROM client_goals WHERE id = ?', (item_id,))
#
#
# def create_dividends_payouts():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS dividends_payouts ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "account_id TEXT NOT NULL,"
#             "amount REAL NOT NULL,"
#             "payment_date DATETIME NOT NULL,"
#             "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE);"
#         )
#
#
# def select_all_from_dividends_payouts_where_profile_id(profile_id: str) -> [tuple]:
#     with conn:
#         cur = conn.cursor()
#         rows = cur.execute(
#             'SELECT dp.* FROM dividends_and_payouts dp JOIN accounts a ON dp.account_id = a.id WHERE a.profile_id = ? '
#             'ORDER BY dp.payment_date ASC', (profile_id,)
#         ).fetchall()
#         return [DividendPayout.model_validate(dict(dividend_payout) for dividend_payout in rows)]
#
#
# def insert_dividends_payouts(dividend_payout: DividendPayout):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             'INSERT INTO dividends_payouts (account_id, amount, payment_date) '
#             'VALUES (:account_id, :amount, :payment_date)',
#             (dividend_payout.model_dump())
#         )
#
#
# def delete_from_dividends_payouts(item_id: str):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(f'DELETE FROM dividends_payouts WHERE id = ?', (item_id,))
#
#
# def create_investments():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS investments ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "account_id TEXT NOT NULL,"
#             "investment_type TEXT NOT NULL,"
#             "symbol TEXT NOT NULL,"
#             "quantity REAL NOT NULL,"
#             "purchase_price REAL NOT NULL,"
#             "current_price REAL NOT NULL,"
#             "purchase_date DATETIME NOT NULL,"
#             "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE);"
#         )
#
#
# def select_all_from_investments_where_profile_id(profile_id: str) -> [tuple]:
#     with conn:
#         cur = conn.cursor()
#         rows = cur.execute(
#             'SELECT i.* FROM investments i JOIN accounts a ON i.account_id = a.id WHERE a.profile_id = ?',
#             (profile_id,)
#         ).fetchall()
#         return [Investment.model_validate(dict(investment) for investment in rows)]
#
#
# def insert_investments(investment: Investment):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             'INSERT INTO investments (account_id, investment_type, symbol, quantity, purchase_price, current_price, '
#             'purchase_date) VALUES (:account_id, :investment_type, :symbol, :quantity, :purchase_price, '
#             ':current_price, purchase_date)',
#             (investment.model_dump())
#         )
#
#
# def delete_from_investments(item_id: str):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(f'DELETE FROM investments WHERE id = ?', (item_id,))
#
#
# def create_transactions():
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS transactions ("
#             "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
#             "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
#             "account_id TEXT NOT NULL,"
#             "type TEXT NOT NULL,"
#             "amount REAL NOT NULL,"
#             "description TEXT NULL,"
#             "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE ON UPDATE CASCADE);"
#         )
#
#
# def select_all_from_transactions_where_profile_id(profile_id: str) -> [tuple]:
#     with conn:
#         cur = conn.cursor()
#         rows = cur.execute(
#             'SELECT t.* FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE a.profile_id = ?',
#             (profile_id,)
#         ).fetchall()
#         return [Transaction.model_validate(dict(transaction) for transaction in rows)]
#
#
# def insert_transactions(transaction: Transaction):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(
#             'INSERT INTO transactions (account_id, type, amount, description) VALUES (:account_id, :type, :amount, '
#             'description)',
#             (transaction.model_dump())
#         )
#
#
# def delete_from_transactions(item_id: str):
#     with conn:
#         cur = conn.cursor()
#         cur.execute(f'DELETE FROM transactions WHERE id = ?', (item_id,))
