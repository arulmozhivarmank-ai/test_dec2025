# Deploy to Streamlit Cloud

This guide will help you deploy your Monthly Expense Tracker to Streamlit Cloud (free and easy!).

## Prerequisites

- A GitHub account
- Your code pushed to a GitHub repository

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

If you haven't already, create a GitHub repository and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Add expense tracker app"

# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Click "Sign in" and authenticate with your GitHub account

2. **Click "New app"**

3. **Fill in the deployment form:**
   - **Repository**: Select your GitHub repository
   - **Branch**: Select `main` (or `master`)
   - **Main file path**: Enter `expense_tracker.py`
   - **App URL**: Choose a custom subdomain (optional)

4. **Click "Deploy"**

5. **Wait for deployment** (usually takes 1-2 minutes)

6. **Your app is live!** 🎉
   - Access it at: `https://YOUR-APP-NAME.streamlit.app`

## Important Notes

- **Data Persistence**: The `expenses.json` file will be stored in the app's file system, but data may be lost if the app restarts. For production use, consider using a database.

- **File Structure**: Make sure your repository has:
  - `expense_tracker.py` (main app file)
  - `requirements.txt` (dependencies)

- **Requirements**: Streamlit Cloud automatically installs packages from `requirements.txt`

## Troubleshooting

- **App won't deploy**: Check that `expense_tracker.py` is in the root directory
- **Import errors**: Verify all dependencies are in `requirements.txt`
- **App crashes**: Check the logs in Streamlit Cloud dashboard

## Updating Your App

Simply push changes to your GitHub repository, and Streamlit Cloud will automatically redeploy:

```bash
git add .
git commit -m "Update app"
git push
```

That's it! Your app will update automatically. 🚀
