import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import json
import os

# Set the page title and configuration
st.set_page_config(
    page_title='Monthly Expense Tracker',
    page_icon='💰',
    layout='wide'
)

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

# Initialize session state for expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Load expenses from file if it exists
EXPENSE_FILE = 'expenses.json'

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

# Load expenses on startup
if not st.session_state.expenses:
    st.session_state.expenses = load_expenses()

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
    
    # Calculate metrics
    total_expenses = month_df['amount'].sum()
    avg_daily = month_df.groupby(month_df['date'].dt.day)['amount'].sum().mean()
    num_transactions = len(month_df)
    top_subcategory = month_df.groupby('subcategory')['amount'].sum().idxmax()
    top_subcategory_amount = month_df.groupby('subcategory')['amount'].sum().max()
    
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

