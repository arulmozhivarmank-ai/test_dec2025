# 💰 CGT Monthly Expense Tracker

A comprehensive web application built with Streamlit for tracking and visualizing monthly expenses. This application helps you manage your expenses with detailed categorization, interactive charts, and data export capabilities.

## Features

### ✨ Core Functionality

- **➕ Add Expenses**: Easily add new expenses with date, category, subcategory, description, and amount
- **📊 Monthly Analytics**: View detailed metrics including total expenses, average daily expenses, transaction count, and top spending categories
- **📈 Interactive Visualizations**: 
  - Pie chart showing expense distribution by subcategory
  - Line chart displaying daily spending trends
  - Horizontal bar chart for category breakdown
  - Monthly comparison chart (when multiple months available)
- **🗑️ Expense Management**: Delete individual expenses directly from the table
- **💾 Data Persistence**: Automatic saving to JSON file (`expenses.json`)
- **📥 CSV Export**: Export expense details for the selected month as CSV file
- **📱 Responsive Design**: Modern, clean UI with custom styling

### 🎨 Categories & Subcategories

The application supports the following expense categories:

#### 🏗️ Maintenance Expenses
- MAINT-CIV (Civil Maintenance)
- MAINT-ELE (Electrical Maintenance)
- MAINT-STP (STP Maintenance)
- MAINT-GEN (General Maintenance)
- MAINT-HK (Housekeeping Maintenance)
- MAINT-CLB (Club Maintenance)

#### 👨‍🌾 Staff Payments
- SAL-INT (Internal Salary)
- SAL-EXT (External Salary)
- SAL-BONUS (Bonus Payments)
- SAL-CONV (Conveyance)

#### 🛒 Purchases
- PUR-MTRL (Materials)
- PUR-ELEC (Electronics)
- PUR-GARD (Garden Supplies)
- PUR-OFF (Office Supplies)
- PUR-HK (Housekeeping Supplies)
- PUR-WATER (Water)
- PUR-PRINT (Printing)

#### 💳 Cash Flow / Credit Transactions
- CASH-WD (Cash Withdrawal)
- CASH-CR (Cash Credit)
- CREDIT (Credit Transactions)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arulmozhivarmank-ai/test_dec2025.git
   cd test_dec2025
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or use pip3:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run expense_tracker.py
   ```

4. **Access the application**:
   The application will automatically open in your default web browser at `http://localhost:8501`

## Usage

### Adding an Expense

1. Use the sidebar on the left to add a new expense
2. Select the date (defaults to today)
3. Choose the **Account Category** from the dropdown
4. Select the appropriate **Sub Category**
5. Enter a description for the expense
6. Enter the amount in ₹ (Indian Rupees)
7. Click **"Add Expense"** button

### Viewing Expenses

- The main dashboard displays all expenses for the selected month
- Use the **"Select Month"** dropdown to view expenses for different months
- View key metrics at the top:
  - Total Expenses
  - Average Daily Expense
  - Number of Transactions
  - Top Sub Category

### Visualizations

- **Expenses by Category**: Pie chart showing the distribution of expenses across subcategories
- **Daily Expenses Trend**: Line chart tracking daily spending throughout the month
- **Category Breakdown**: Horizontal bar chart comparing expenses by subcategory
- **Monthly Comparison**: Bar chart comparing total expenses across multiple months (if available)

### Managing Expenses

- **Delete an Expense**: Click the 🗑️ button next to any expense in the Expense Details table
- **Clear All Expenses**: Use the **"Clear All Expenses"** button in the sidebar (use with caution!)

### Exporting Data

- Click the **"⬇️ Export CSV"** button above the Expense Details table
- The CSV file will include all expenses for the selected month with columns:
  - Date
  - Category
  - Sub Category
  - Description
  - Amount

### Summary Statistics

Click on the **"📊 Summary Statistics"** expander to view:
- Total expenses for the month
- Number of transactions
- Average transaction amount
- Largest and smallest expenses
- Category breakdown table with totals, counts, and averages

## Project Structure

```
test_dec2025/
├── expense_tracker.py    # Main application file
├── expenses.json         # Data storage file (auto-generated)
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── DEPLOYMENT.md        # Deployment documentation
```

## Technology Stack

- **Streamlit**: Web framework for building the application
- **Pandas**: Data manipulation and analysis
- **Plotly Express**: Interactive data visualization
- **JSON**: Data persistence

## Dependencies

- `pandas>=2.0.0`
- `streamlit>=1.40.0`
- `numpy>=1.24.0`
- `plotly>=5.17.0`

## Data Storage

Expenses are automatically saved to `expenses.json` in the project root directory. The file is created automatically when you add your first expense. The data persists between application restarts.

## Customization

The application includes custom CSS styling for:
- Metric cards with rounded corners
- Colored labels for better visibility
- Highlighted Total Expenses metric (green background)
- Styled price values for better readability

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to:
1. Open an issue describing the problem or feature request
2. Submit a pull request with your changes

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on the GitHub repository.

---

**Note**: This application is designed for tracking expenses in Indian Rupees (₹). The currency symbol can be modified in the code if needed for other currencies.
