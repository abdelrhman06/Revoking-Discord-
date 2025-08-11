# 🚀 Deployment Guide - Discord User Remover Bot

## 📋 Pre-Deployment Checklist

- ✅ Discord Bot created and configured
- ✅ Bot invited to server with proper permissions
- ✅ Bot token available
- ✅ Server ID (Guild ID) noted: `1393935478503243917`

## 🐙 GitHub Deployment

### 1. Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Discord User Remover Bot"

# Set main branch
git branch -M main

# Add remote origin
git remote add origin git@github.com:abdelrhman06/Revoking-Discord-.git

# Push to GitHub
git push -u origin main
```

### 2. Verify Repository

Check that these files are included:
- ✅ `main.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Documentation
- ✅ `.gitignore` - Git ignore file
- ✅ `.streamlit/secrets_template.toml` - Secrets template
- ❌ `.streamlit/secrets.toml` - (Should be ignored by git)

## ☁️ Streamlit Cloud Deployment

### 1. Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 2. Deploy App

1. **Click "New app"**
2. **Configure deployment**:
   - Repository: `abdelrhman06/Revoking-Discord-`
   - Branch: `main`
   - Main file path: `main.py`
3. **Click "Deploy!"**

### 3. Configure Secrets

1. **Go to app settings** (gear icon)
2. **Navigate to "Secrets"** tab
3. **Add the following secrets**:

```toml
DISCORD_BOT_TOKEN = "YOUR_ACTUAL_BOT_TOKEN_HERE"
DISCORD_GUILD_ID = "1393935478503243917"
```

4. **Save secrets**
5. **Restart app** if needed

## 🔧 Post-Deployment Setup

### 1. Test the Application

1. **Access your deployed app** at the provided URL
2. **Test connection** using the "Test Connection" button
3. **Upload a sample Excel file** to verify functionality
4. **Test user discovery** for users without roles

### 2. Security Considerations

- ✅ Bot token is stored securely in Streamlit secrets
- ✅ Secrets are not exposed in the code
- ✅ `.streamlit/secrets.toml` is in `.gitignore`
- ✅ Guild ID is configurable via secrets

### 3. App Monitoring

Monitor your app through:
- **Streamlit Cloud dashboard** - Check app status and logs
- **Discord bot logs** - Monitor bot activities
- **Server member changes** - Track removal operations

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "Improper token has been passed"
- **Solution**: Verify bot token in Streamlit secrets
- **Check**: Token format should be: `MTxxxxx.xxxxxx.xxxxxxxxxxxxxxxxxxxxxxxx`

#### 2. "Guild not found"
- **Solution**: Verify server ID in secrets
- **Check**: Ensure bot is invited to the correct server

#### 3. "Permission denied"
- **Solution**: Check bot permissions in Discord server
- **Required**: Kick Members, Ban Members, View Channels

#### 4. App not starting
- **Solution**: Check app logs in Streamlit Cloud
- **Check**: Verify all dependencies in requirements.txt

## 📱 Usage URLs

After deployment, your app will be available at:
- **Streamlit Cloud**: `https://share.streamlit.io/abdelrhman06/revoking-discord-/main/main.py`
- **Custom domain** (if configured): Your custom URL

## 🔄 Updating the App

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy your app when you push changes to the main branch.

## 📊 App Features Available

Once deployed, users can access:

1. **🎯 User Filter Options**:
   - Excel File List
   - Users Without Roles  
   - Both (Combined)

2. **⚡ Actions**:
   - Kick users
   - Ban users
   - Bulk operations

3. **📈 Real-time Statistics**:
   - Users found
   - Operation progress
   - Success/failure counts

4. **💾 Export Results**:
   - Download CSV reports
   - Operation logs

## 🔐 Security Best Practices

1. **Never commit secrets** to git
2. **Regularly rotate** bot tokens
3. **Monitor app access** logs
4. **Use bot permissions** principle of least privilege
5. **Backup member lists** before bulk operations

---

## ✅ Deployment Complete!

Your Discord User Remover Bot is now live and ready to use! 🎉 