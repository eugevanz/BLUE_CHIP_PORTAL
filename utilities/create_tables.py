from os import environ

import libsql_experimental as libsql

TURSO_DATABASE_URL = environ.get('TURSO_DATABASE_URL')
TURSO_AUTH_TOKEN = environ.get('TURSO_AUTH_TOKEN')
conn = libsql.connect('blue-chip-invest.db')
cur = conn.cursor()


def create_profiles():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS profiles ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL, "
        "profile_picture_url TEXT DEFAULT "
        "'https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images/jurica-koletic"
        "-7YVZYZeITc8-unsplash_3_11zon.webp' NOT NULL,"
        "first_name TEXT DEFAULT 'First name' NOT NULL,"
        "last_name TEXT DEFAULT 'Last name' NOT NULL,"
        "phone_number TEXT DEFAULT '' NULL,"
        "profile_type TEXT DEFAULT 'client' NOT NULL,"
        "date_of_birth TEXT NULL,"
        "address TEXT DEFAULT '' NOT NULL,"
        "email TEXT DEFAULT 'email@address.com' NOT NULL);"
    )


def create_accounts():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS accounts ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "profile_id TEXT NOT NULL,"
        "account_number TEXT NOT NULL,"
        "account_type TEXT NOT NULL,"
        "balance REAL DEFAULT 0.0 NOT NULL,"
        "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE);"
    )


def create_client_goals():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS client_goals ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "profile_id TEXT NOT NULL,"
        "goal_type TEXT NOT NULL,"
        "target_amount REAL NOT NULL,"
        "current_savings REAL DEFAULT 0.0 NOT NULL,"
        "target_date TEXT NULL,"
        "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE);"
    )


def create_dividends_payouts():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS dividends_payouts ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "account_id TEXT NOT NULL,"
        "amount REAL NOT NULL,"
        "payment_date DATETIME NOT NULL,"
        "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE);"
    )


def create_investments():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS investments ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "account_id TEXT NOT NULL,"
        "investment_type TEXT NOT NULL,"
        "symbol TEXT NOT NULL,"
        "quantity REAL NOT NULL,"
        "purchase_price REAL NOT NULL,"
        "current_price REAL NOT NULL,"
        "purchase_date DATETIME NOT NULL,"
        "updated_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE);"
    )


def create_transactions():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS transactions ("
        "id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),"
        "created_at DATETIME DEFAULT (datetime('now')) NOT NULL,"
        "account_id TEXT NOT NULL,"
        "type TEXT NOT NULL,"
        "amount REAL NOT NULL,"
        "description TEXT NULL,"
        "FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE ON UPDATE CASCADE);"
    )
