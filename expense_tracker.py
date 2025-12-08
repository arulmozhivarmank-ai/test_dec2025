import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import json
import os

# Set the page title and configuration
st.set_page_config(
    page_title='CGT Monthly Expense Tracker',
    page_icon='💰',
    layout='wide'
)

# Default credentials
DEFAULT_USERID = "admin"
DEFAULT_PASSWORD = "password"  # Change this to your desired default password
PASSWORD_FILE = 'credentials.json'

# Initialize authentication in session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'userid' not in st.session_state:
    st.session_state.userid = None
if 'show_change_password' not in st.session_state:
    st.session_state.show_change_password = False

def load_credentials():
    """Load credentials from JSON file"""
    if os.path.exists(PASSWORD_FILE):
        try:
            with open(PASSWORD_FILE, 'r') as f:
                creds = json.load(f)
                return creds.get('userid', DEFAULT_USERID), creds.get('password', DEFAULT_PASSWORD)
        except:
            return DEFAULT_USERID, DEFAULT_PASSWORD
    return DEFAULT_USERID, DEFAULT_PASSWORD

def save_credentials(userid, password):
    """Save credentials to JSON file"""
    creds = {
        'userid': userid,
        'password': password
    }
    with open(PASSWORD_FILE, 'w') as f:
        json.dump(creds, f, indent=2)

def check_credentials(userid, password):
    """Check if credentials are valid"""
    stored_userid, stored_password = load_credentials()
    return userid == stored_userid and password == stored_password

def login_page():
    """Display login page"""
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    .login-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        max-width: 420px;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    .login-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
    }
    h1 {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        font-weight: 300;
    }
    .login-title {
        text-align: center;
        color: #667eea;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    .login-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
    }
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #e1e5e9 !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    .stExpander {
        border-radius: 12px !important;
        border: 1px solid #e1e5e9 !important;
        background: rgba(255, 255, 255, 0.8) !important;
    }
    .stExpander > div:first-child {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown('<h1 class="login-title">💰 CGT Expense Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Secure access to your financial dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Login form
    with st.form("login_form"):
        st.markdown("### 🔐 Please Sign In")
        userid = st.text_input("👤 User ID", placeholder="Enter your user ID", key="login_userid")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
        submit_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)

        if submit_button:
            if check_credentials(userid, password):
                st.session_state.authenticated = True
                st.session_state.userid = userid
                st.success("🎉 Login successful! Redirecting...")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid user ID or password. Please try again.")
    
    st.markdown("---")
    
    # Password change section
    with st.expander("🔑 Change Password"):
        with st.form("change_password_form"):
            st.markdown("### 🔄 Update Your Credentials")
            stored_userid, stored_password = load_credentials()

            change_userid = st.text_input("👤 User ID", value=stored_userid, key="change_userid")
            old_password = st.text_input("🔒 Current Password", type="password", placeholder="Enter current password", key="old_password")
            new_password = st.text_input("🆕 New Password", type="password", placeholder="Enter new password", key="new_password")
            confirm_password = st.text_input("✅ Confirm New Password", type="password", placeholder="Confirm new password", key="confirm_password")

            change_button = st.form_submit_button("💾 Update Password", type="primary", use_container_width=True)

            if change_button:
                # Validate inputs
                if not change_userid or not old_password or not new_password or not confirm_password:
                    st.error("❌ Please fill in all fields.")
                elif not check_credentials(change_userid, old_password):
                    st.error("❌ Current password is incorrect.")
                elif new_password != confirm_password:
                    st.error("❌ New password and confirm password do not match.")
                elif len(new_password) < 4:
                    st.error("❌ New password must be at least 4 characters long.")
                else:
                    # Save new credentials
                    save_credentials(change_userid, new_password)
                    st.success("✅ Password changed successfully! Please login with your new password.")
                    st.session_state.show_change_password = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Check authentication
if not st.session_state.authenticated:
    login_page()
    st.stop()

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    h1 {
        color: #1f77b4;
    }
    /* Change label backgrounds from white to light blue */
    label {
        background-color: #e3f2fd !important;
    }
    .stSelectbox label,
    .stTextInput label,
    .stDateInput label,
    .stNumberInput label {
        background-color: #e3f2fd !important;
        color: #1565c0 !important;
        font-weight: 500;
    }
    /* Change Total Expenses label background color */
    div[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricLabel"] {
        background-color: #e8f5e9 !important;
        color: #1b5e20 !important;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    /* Change metric value (price) background color for visibility */
    [data-testid="stMetricValue"] {
        background-color: #f5f5f5 !important;
        color: #1976d2 !important;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    /* Change price text in expense table for visibility */
    div[data-testid="column"]:nth-of-type(4) p {
        background-color: #e3f2fd !important;
        color: #0d47a1 !important;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for expenses and credits
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'credits' not in st.session_state:
    st.session_state.credits = []

# Load expenses from file if it exists
EXPENSE_FILE = 'expenses.json'
CREDITS_FILE = 'credits.json'

def load_expenses():
    """Load expenses from JSON file"""
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=2, default=str)

def load_credits():
    """Load credits from JSON file"""
    if os.path.exists(CREDITS_FILE):
        try:
            with open(CREDITS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_credits(credits):
    """Save credits to JSON file"""
    with open(CREDITS_FILE, 'w') as f:
        json.dump(credits, f, indent=2, default=str)

# Load expenses and credits on startup
if not st.session_state.expenses:
    st.session_state.expenses = load_expenses()

if not st.session_state.credits:
    st.session_state.credits = load_credits()

# Title
st.title("💰 CGT Monthly Expense Tracker")
st.markdown("Track and visualize your monthly expenses")

# Category definitions
CATEGORY_OPTIONS = {
    "🏗️ Maintenance Expenses": [
        "MAINT-CIV",
        "MAINT-ELE",
        "MAINT-STP",
        "MAINT-GEN",
        "MAINT-HK",
        "MAINT-CLB",
    ],
    "👨‍🌾 Staff Payments": [
        "SAL-INT",
        "SAL-EXT",
        "SAL-BONUS",
        "SAL-CONV",
    ],
    "🛒 Purchases": [
        "PUR-MTRL",
        "PUR-ELEC",
        "PUR-GARD",
        "PUR-OFF",
        "PUR-HK",
        "PUR-WATER",
        "PUR-PRINT",
    ],
    "💳 Cash Flow / Credit Transactions": [
        "CASH-WD",
        "CASH-CR",
        "CREDIT",
    ],
}

# Sidebar for adding expenses
with st.sidebar:
    # User info and logout
    st.markdown(f"**Logged in as:** {st.session_state.userid}")
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.userid = None
        st.rerun()
    st.markdown("---")
    
    st.header("➕ Add New Expense")
    
    expense_date = st.date_input("Date", value=date.today())
    expense_category = st.selectbox(
        "Account Category",
        list(CATEGORY_OPTIONS.keys())
    )
    expense_subcategory = st.selectbox(
        "Sub Category",
        CATEGORY_OPTIONS[expense_category]
    )
    expense_description = st.text_input("Description")
    expense_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Add Expense", type="primary"):
        if expense_amount > 0 and expense_description:
            new_expense = {
                "date": expense_date.isoformat(),
                "category": expense_category,
                "subcategory": expense_subcategory,
                "description": expense_description,
                "amount": float(expense_amount)
            }
            st.session_state.expenses.append(new_expense)
            save_expenses(st.session_state.expenses)
            st.success(f"Added ₹{expense_amount:.2f} for {expense_description}!")
            st.rerun()
        else:
            st.error("Please enter a valid amount and description")
    
    st.markdown("---")
    
    # Add Credit section
    st.header("💳 Add Credit")
    credit_date = st.date_input("Credit Date", value=date.today(), key="credit_date")
    credit_amount = st.number_input("Credit Amount (₹)", min_value=0.0, step=0.01, format="%.2f", key="credit_amount")
    credit_description = st.text_input("Credit Description", key="credit_description")
    
    if st.button("Add Credit", type="primary", key="add_credit"):
        if credit_amount > 0 and credit_description:
            new_credit = {
                "date": credit_date.isoformat(),
                "description": credit_description,
                "amount": float(credit_amount)
            }
            st.session_state.credits.append(new_credit)
            save_credits(st.session_state.credits)
            st.success(f"Added credit ₹{credit_amount:.2f} for {credit_description}!")
            st.rerun()
        else:
            st.error("Please enter a valid amount and description")
    
    st.markdown("---")
    
    # Clear all expenses button
    if st.button("🗑️ Clear All Expenses", type="secondary"):
        if st.session_state.expenses:
            st.session_state.expenses = []
            save_expenses([])
            st.success("All expenses cleared!")
            st.rerun()

# Main content area
if st.session_state.expenses:
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.expenses)
    df['date'] = pd.to_datetime(df['date'])
    if 'category' not in df.columns:
        df['category'] = "Uncategorized"
    if 'subcategory' not in df.columns:
        df['subcategory'] = df['category']
    df['month'] = df['date'].dt.to_period('M')
    df['month_str'] = df['month'].astype(str)
    
    # Month selector
    months = sorted(df['month_str'].unique(), reverse=True)
    selected_month = st.selectbox("Select Month", months, index=0)
    
    # Filter data for selected month
    month_df = df[df['month_str'] == selected_month].copy()
    
    # Process credits data
    if st.session_state.credits:
        credits_df = pd.DataFrame(st.session_state.credits)
        credits_df['date'] = pd.to_datetime(credits_df['date'])
        credits_df['month'] = credits_df['date'].dt.to_period('M')
        credits_df['month_str'] = credits_df['month'].astype(str)
        month_credits_df = credits_df[credits_df['month_str'] == selected_month].copy()
        total_credits = month_credits_df['amount'].sum()
    else:
        total_credits = 0.0
    
    # Calculate metrics
    total_expenses = month_df['amount'].sum()
    avg_daily = month_df.groupby(month_df['date'].dt.day)['amount'].sum().mean()
    num_transactions = len(month_df)
    top_subcategory = month_df.groupby('subcategory')['amount'].sum().idxmax()
    top_subcategory_amount = month_df.groupby('subcategory')['amount'].sum().max()
    
    # Calculate balance
    balance = total_credits - total_expenses
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    with col2:
        st.metric("Avg Daily Expense", f"₹{avg_daily:.2f}")
    with col3:
        st.metric("Transactions", num_transactions)
    with col4:
        st.metric("Top Sub Category", f"{top_subcategory}\n₹{top_subcategory_amount:.2f}")
    
    # Display balance after expenses
    st.markdown("---")
    st.subheader("💰 Balance Summary")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("Total Credits", f"₹{total_credits:,.2f}")
    with col2:
        st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    with col3:
        # Display balance
        st.metric("Balance", f"₹{balance:,.2f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expenses by Category")
        category_sum = month_df.groupby('subcategory')['amount'].sum().sort_values(ascending=False)
        fig_pie = px.pie(
            values=category_sum.values,
            names=category_sum.index,
            title=f"Expense Distribution - {selected_month}",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Daily Expenses Trend")
        daily_expenses = month_df.groupby(month_df['date'].dt.day)['amount'].sum()
        fig_line = px.line(
            x=daily_expenses.index,
            y=daily_expenses.values,
            title=f"Daily Spending - {selected_month}",
            labels={'x': 'Day of Month', 'y': 'Amount (₹)'},
            markers=True
        )
        fig_line.update_layout(
            xaxis_title="Day of Month",
            yaxis_title="Amount (₹)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Category breakdown bar chart
    st.subheader("Category Breakdown")
    category_sum = month_df.groupby('subcategory')['amount'].sum().sort_values(ascending=True)
    fig_bar = px.bar(
        x=category_sum.values,
        y=category_sum.index,
        orientation='h',
        title=f"Expenses by Category - {selected_month}",
        labels={'x': 'Amount (₹)', 'y': 'Category'},
        color=category_sum.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Monthly comparison (if multiple months available)
    if len(months) > 1:
        st.subheader("Monthly Comparison")
        monthly_totals = df.groupby('month_str')['amount'].sum().sort_index()
        fig_comparison = px.bar(
            x=monthly_totals.index,
            y=monthly_totals.values,
            title="Total Expenses by Month",
            labels={'x': 'Month', 'y': 'Total Amount (₹)'},
            color=monthly_totals.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.markdown("---")
    
    # Expense table
    st.subheader(f"Expense Details - {selected_month}")
    
    # Sort by date descending
    month_df_sorted = month_df.sort_values('date', ascending=False).reset_index(drop=True)

    # Download CSV for current month
    export_cols = ['date', 'category', 'subcategory', 'description', 'amount']
    export_df = month_df_sorted.copy()
    export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
    csv_bytes = export_df[export_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Export CSV",
        data=csv_bytes,
        file_name=f"expenses_{selected_month}.csv",
        mime="text/csv"
    )
    
    # Create a table with delete buttons
    for display_idx, (df_idx, row) in enumerate(month_df_sorted.iterrows()):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2.5, 2.5, 3, 2, 1])
        with col1:
            st.write(row['date'].strftime('%Y-%m-%d'))
        with col2:
            st.write(row['category'])
        with col3:
            st.write(row['subcategory'])
        with col4:
            st.write(row['description'])
        with col5:
            st.write(f"₹{row['amount']:.2f}")
        with col6:
            # Find the expense in the original list by matching all fields
            expense_to_delete = {
                "date": row['date'].date().isoformat(),
                "category": row['category'],
                "subcategory": row['subcategory'],
                "description": row['description'],
                "amount": row['amount']
            }
            if st.button("🗑️", key=f"delete_{df_idx}_{display_idx}"):
                # Remove the matching expense from the list
                for i, exp in enumerate(st.session_state.expenses):
                    if (exp.get('date') == expense_to_delete['date'] and
                        exp.get('category') == expense_to_delete['category'] and
                        exp.get('subcategory', exp.get('category')) == expense_to_delete['subcategory'] and
                        exp.get('description') == expense_to_delete['description'] and
                        abs(exp.get('amount', 0) - expense_to_delete['amount']) < 0.01):
                        st.session_state.expenses.pop(i)
                        save_expenses(st.session_state.expenses)
                        st.rerun()
                        break
    
    # Summary statistics
    with st.expander("📊 Summary Statistics"):
        st.write(f"**Total Expenses in {selected_month}:** ₹{total_expenses:,.2f}")
        st.write(f"**Number of Transactions:** {num_transactions}")
        st.write(f"**Average Transaction Amount:** ₹{month_df['amount'].mean():.2f}")
        st.write(f"**Largest Expense:** ₹{month_df['amount'].max():.2f}")
        st.write(f"**Smallest Expense:** ₹{month_df['amount'].min():.2f}")
        
        st.write("\n**Category Breakdown:**")
        # Category breakdown (by Account Category)
        category_stats = month_df.groupby('category').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        category_stats.columns = ['Total', 'Count', 'Average']
        # Format currency columns
        category_stats_display = category_stats.copy()
        category_stats_display['Total'] = category_stats_display['Total'].apply(lambda x: f"₹{x:,.2f}")
        category_stats_display['Average'] = category_stats_display['Average'].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(category_stats_display, use_container_width=True)
    
else:
    st.info("👆 Start tracking your expenses by adding your first expense in the sidebar!")
    st.markdown("""
    ### Features:
    - ➕ Add expenses with date, category, description, and amount
    - 📊 View monthly expense summaries and trends
    - 📈 Visualize expenses with interactive charts
    - 🗑️ Delete individual expenses
    - 💾 Automatic data persistence
    """)

