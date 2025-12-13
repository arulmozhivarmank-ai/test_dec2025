import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Database file path
DB_FILE = 'expense_tracker.db'

# JSON file paths for migration
EXPENSE_FILE = 'expenses.json'
CREDITS_FILE = 'credits.json'
PASSWORD_FILE = 'credentials.json'

def get_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create credentials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create credits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_credits_date ON credits(date)')
    
    conn.commit()
    conn.close()
    
    # Perform migration if JSON files exist
    migrate_json_to_db()

def migrate_json_to_db():
    """Migrate data from JSON files to database (one-time operation)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if migration has already been done
    cursor.execute('SELECT COUNT(*) FROM credentials')
    has_credentials = cursor.fetchone()[0] > 0
    
    cursor.execute('SELECT COUNT(*) FROM expenses')
    has_expenses = cursor.fetchone()[0] > 0
    
    cursor.execute('SELECT COUNT(*) FROM credits')
    has_credits = cursor.fetchone()[0] > 0
    
    # Migrate credentials
    if not has_credentials and os.path.exists(PASSWORD_FILE):
        try:
            with open(PASSWORD_FILE, 'r') as f:
                creds = json.load(f)
                cursor.execute(
                    'INSERT INTO credentials (userid, password) VALUES (?, ?)',
                    (creds.get('userid', 'admin'), creds.get('password', 'password'))
                )
                print(f"✅ Migrated credentials from {PASSWORD_FILE}")
        except Exception as e:
            print(f"⚠️ Could not migrate credentials: {e}")
    
    # Migrate expenses
    if not has_expenses and os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, 'r') as f:
                expenses = json.load(f)
                for expense in expenses:
                    cursor.execute(
                        'INSERT INTO expenses (date, category, subcategory, description, amount) VALUES (?, ?, ?, ?, ?)',
                        (
                            expense.get('date'),
                            expense.get('category', 'Uncategorized'),
                            expense.get('subcategory', expense.get('category', 'Uncategorized')),
                            expense.get('description', ''),
                            expense.get('amount', 0.0)
                        )
                    )
                print(f"✅ Migrated {len(expenses)} expenses from {EXPENSE_FILE}")
        except Exception as e:
            print(f"⚠️ Could not migrate expenses: {e}")
    
    # Migrate credits
    if not has_credits and os.path.exists(CREDITS_FILE):
        try:
            with open(CREDITS_FILE, 'r') as f:
                credits = json.load(f)
                for credit in credits:
                    cursor.execute(
                        'INSERT INTO credits (date, description, amount) VALUES (?, ?, ?)',
                        (
                            credit.get('date'),
                            credit.get('description', ''),
                            credit.get('amount', 0.0)
                        )
                    )
                print(f"✅ Migrated {len(credits)} credits from {CREDITS_FILE}")
        except Exception as e:
            print(f"⚠️ Could not migrate credits: {e}")
    
    conn.commit()
    conn.close()

# ============================================================================
# CREDENTIAL OPERATIONS
# ============================================================================

def get_credentials() -> Tuple[str, str]:
    """Get stored credentials"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT userid, password FROM credentials LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row['userid'], row['password']
    else:
        # Return default credentials if none exist
        return 'admin', 'password'

def update_credentials(userid: str, password: str):
    """Update or insert credentials"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if credentials exist
    cursor.execute('SELECT id FROM credentials LIMIT 1')
    row = cursor.fetchone()
    
    if row:
        # Update existing
        cursor.execute(
            'UPDATE credentials SET userid = ?, password = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (userid, password, row['id'])
        )
    else:
        # Insert new
        cursor.execute(
            'INSERT INTO credentials (userid, password) VALUES (?, ?)',
            (userid, password)
        )
    
    conn.commit()
    conn.close()

# ============================================================================
# EXPENSE OPERATIONS
# ============================================================================

def get_all_expenses() -> List[Dict]:
    """Get all expenses from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, date, category, subcategory, description, amount FROM expenses ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    
    expenses = []
    for row in rows:
        expenses.append({
            'id': row['id'],
            'date': row['date'],
            'category': row['category'],
            'subcategory': row['subcategory'],
            'description': row['description'],
            'amount': row['amount']
        })
    
    return expenses

def add_expense(date: str, category: str, subcategory: str, description: str, amount: float) -> int:
    """Add a new expense to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO expenses (date, category, subcategory, description, amount) VALUES (?, ?, ?, ?, ?)',
        (date, category, subcategory, description, amount)
    )
    
    expense_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return expense_id

def delete_expense(expense_id: int) -> bool:
    """Delete an expense by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted

def delete_expense_by_details(date: str, category: str, subcategory: str, description: str, amount: float) -> bool:
    """Delete an expense by matching details (for backward compatibility)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Find matching expense
    cursor.execute(
        '''SELECT id FROM expenses 
           WHERE date = ? AND category = ? AND subcategory = ? AND description = ? AND ABS(amount - ?) < 0.01
           LIMIT 1''',
        (date, category, subcategory, description, amount)
    )
    
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM expenses WHERE id = ?', (row['id'],))
        deleted = True
    else:
        deleted = False
    
    conn.commit()
    conn.close()
    
    return deleted

def clear_all_expenses() -> int:
    """Delete all expenses"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM expenses')
    count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return count

# ============================================================================
# CREDIT OPERATIONS
# ============================================================================

def get_all_credits() -> List[Dict]:
    """Get all credits from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, date, description, amount FROM credits ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    
    credits = []
    for row in rows:
        credits.append({
            'id': row['id'],
            'date': row['date'],
            'description': row['description'],
            'amount': row['amount']
        })
    
    return credits

def add_credit(date: str, description: str, amount: float) -> int:
    """Add a new credit to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO credits (date, description, amount) VALUES (?, ?, ?)',
        (date, description, amount)
    )
    
    credit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return credit_id

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def backup_json_files():
    """Create backups of JSON files before migration"""
    for filename in [EXPENSE_FILE, CREDITS_FILE, PASSWORD_FILE]:
        if os.path.exists(filename):
            backup_name = f"{filename}.backup"
            if not os.path.exists(backup_name):
                import shutil
                shutil.copy(filename, backup_name)
                print(f"📦 Created backup: {backup_name}")

# Initialize database on module import
if __name__ == "__main__":
    print("Initializing database...")
    backup_json_files()
    init_database()
    print("✅ Database initialized successfully!")
