# Deploy to Streamlit Community Cloud

This guide will help you deploy your CGT Monthly Expense Tracker to Streamlit Community Cloud.

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Code repository: `https://github.com/arulmozhivarmank-ai/test_dec2025`

## 🚀 Quick Deployment Steps

### Step 1: Push Your Code to GitHub

Your repository is already set up! Just commit and push the latest changes:

```bash
cd /Users/arul/git_projects/test_dec2025

# Add all new files (database.py and .gitignore)
git add database.py .gitignore expense_tracker.py

# Commit changes
git commit -m "Add database integration for expense tracker"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
   - Sign in with your GitHub account

2. **Click "New app"** button

3. **Fill in the deployment form:**
   - **Repository**: `arulmozhivarmank-ai/test_dec2025`
   - **Branch**: `main`
   - **Main file path**: `expense_tracker.py`
   - **App URL**: Choose a custom name (e.g., `cgt-expense-tracker`)

4. **Click "Deploy"**

5. **Wait 1-2 minutes** for deployment to complete

6. **Your app is live!** 🎉
   - Access at: `https://your-app-name.streamlit.app`

---

## 💾 Database on Streamlit Cloud

**Good News**: The SQLite database works perfectly on Streamlit Cloud!

- Database file (`expense_tracker.db`) is created automatically on first run
- Data persists across app sessions
- Each user gets their own isolated database

> [!IMPORTANT]
> **Data Persistence**: Streamlit Cloud's file system is ephemeral. If the app is redeployed or restarted, the database will be reset. For production use with permanent data storage, consider:
> - Using Streamlit Cloud's secrets for database credentials
> - Connecting to an external database (PostgreSQL, MySQL, etc.)
> - Using cloud storage services

---

## 📁 Files Included in Deployment

Your repository should have these files:
- ✅ `expense_tracker.py` - Main application
- ✅ `database.py` - Database operations
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Documentation
- ✅ `.gitignore` - Excludes local files

**Note**: Database files (`.db`), backups (`.backup`), and credentials are excluded via `.gitignore` and will be created fresh on the cloud.

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **App won't deploy** | Check that `expense_tracker.py` is in root directory |
| **Import errors** | Verify `requirements.txt` has all dependencies |
| **Database errors** | Check logs - database auto-creates on first run |
| **App crashes** | View logs in Streamlit Cloud dashboard |

---

## 🔄 Updating Your Deployed App

Streamlit Cloud auto-deploys when you push to GitHub:

```bash
# Make your changes, then:
git add .
git commit -m "Your update message"
git push origin main
```

The app updates automatically within 1-2 minutes! 🚀

---

## 🔐 Default Login Credentials

After deployment, use these credentials:
- **User ID**: `admin`
- **Password**: `password`

> [!WARNING]
> **Change the default password immediately** after first login using the "Change Password" option on the login page!

---

## 📊 App Features

Your deployed app includes:
- 🔐 Secure authentication
- 💰 Expense tracking with categories
- 💳 Credit/income tracking
- 📈 Interactive charts and analytics
- 📥 CSV export functionality
- 💾 SQLite database storage
- 🎨 Modern, responsive UI

---

## 🌐 Sharing Your App

Once deployed, share your app URL with anyone:
- Public URL: `https://your-app-name.streamlit.app`
- No installation required for users
- Works on any device with a browser

---

## 📞 Support

For issues with Streamlit Cloud deployment:
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/streamlit-community-cloud)
