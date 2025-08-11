# 🤖 Discord User Remover Bot

A professional Streamlit-based tool for bulk removing Discord users from your server using Excel files.

## ✨ Features

- **Excel File Upload**: Upload Excel files containing Discord usernames
- **Bulk User Removal**: Kick or ban multiple users at once
- **Real-time Progress**: Live progress tracking and status updates
- **Results Download**: Export removal results as CSV
- **Error Handling**: Comprehensive error logging and user feedback
- **Safe Operation**: Test connections before executing actions

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Discord Bot with appropriate permissions
- Discord Server with Developer Mode enabled

### 2. Installation

```bash
# Clone or download the project
cd discord-user-remover

# Install dependencies
pip install -r requirements.txt
```

### 3. Discord Bot Setup

1. **Create Discord Application**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to "Bot" section and click "Add Bot"
   - Copy the bot token (you'll need this later)

2. **Set Bot Permissions**:
   - In the Bot section, enable these permissions:
     - `Kick Members`
     - `Ban Members`
     - `Read Messages`
     - `View Channels`
   - Enable these Privileged Gateway Intents:
     - `Server Members Intent`
     - `Message Content Intent`

3. **Invite Bot to Server**:
   - Go to "OAuth2" > "URL Generator"
   - Select "bot" in Scopes
   - Select required permissions (Kick Members, Ban Members)
   - Copy generated URL and invite bot to your server

### 4. Configuration

1. **Copy Environment File**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**:
   ```env
   DISCORD_BOT_TOKEN=your_actual_bot_token
   DISCORD_GUILD_ID=your_server_id
   ```

3. **Get Server ID**:
   - Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
   - Right-click on your server name and select "Copy ID"

### 5. Configure Secrets

**For Local Development:**
1. Copy `.streamlit/secrets_template.toml` to `.streamlit/secrets.toml`
2. Edit `.streamlit/secrets.toml` and add your actual Discord bot token
3. The Guild ID is already set to: `1393935478503243917`

**For Streamlit Cloud Deployment:**
1. Go to your app settings in Streamlit Cloud
2. Navigate to "Secrets" section  
3. Add these secrets:
   ```toml
   DISCORD_BOT_TOKEN = "your_actual_token"
   DISCORD_GUILD_ID = "1393935478503243917"
   ```

### 6. Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Excel File Format

Your Excel file should contain a column with Discord usernames. The tool automatically detects columns containing:
- "username"
- "discord"
- "DiscordUsername"

### Example Excel Structure:

| DiscordUsername | Name          | Email              |
|----------------|---------------|--------------------|
| john_doe       | John Doe      | john@example.com   |
| jane_smith     | Jane Smith    | jane@example.com   |
| bob_wilson     | Bob Wilson    | bob@example.com    |

## 🔧 Usage Instructions

1. **Configure Bot**:
   - Enter your Discord Bot Token in the sidebar
   - Enter your Server ID (Guild ID)
   - Choose action type (Kick or Ban)
   - Test the connection

2. **Upload Excel File**:
   - Use the file uploader to select your Excel file
   - Review the detected usernames in the preview

3. **Execute Actions**:
   - Click "Kick All Users" or "Ban All Users"
   - Monitor the progress bar and status updates
   - Review results when complete

4. **Download Results**:
   - Click "Download Results" to get a CSV report
   - Contains timestamps, usernames, and success/failure status

## ⚠️ Important Notes

### Security Considerations
- **Keep your bot token secure** - never share it publicly
- **Test with a small group first** before bulk operations
- **Backup your member list** before performing bulk removals
- **Verify permissions** - ensure bot has necessary permissions

### Rate Limiting
- The tool includes built-in delays to respect Discord's rate limits
- Large operations may take time to complete safely
- Monitor the logs for any rate limit warnings

### Error Handling
- Users not found in the server will be logged as failed
- Permission errors are captured and reported
- All operations are logged to `discord_bot.log`

## 📝 Logs and Troubleshooting

### Log Files
- `discord_bot.log` - Contains all bot operations and errors
- Results can be downloaded as CSV from the interface

### Common Issues

1. **Bot not connecting**:
   - Verify bot token is correct
   - Check if bot is invited to the server
   - Ensure bot has necessary permissions

2. **Users not found**:
   - Verify usernames are spelled correctly
   - Check if users are still in the server
   - Ensure usernames don't include discriminators (#1234)

3. **Permission errors**:
   - Verify bot has Kick Members/Ban Members permissions
   - Check if bot's role is higher than target users
   - Ensure bot has Server Members Intent enabled

## 🛡️ Safety Features

- **Connection testing** before executing actions
- **Progress tracking** with ability to stop mid-process
- **Detailed logging** of all operations
- **Error reporting** for failed operations
- **Backup recommendations** in documentation

## 📋 System Requirements

- Python 3.8+
- Internet connection
- Discord Bot Token
- Discord Server with appropriate permissions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is for educational and authorized use only. Ensure you have proper authorization before removing users from Discord servers.

## ⚡ Performance Notes

- Tool is designed to handle large user lists efficiently
- Built-in rate limiting prevents Discord API abuse
- Async operations for better performance
- Memory-efficient Excel processing

## 🌐 Streamlit Cloud Deployment

### Quick Deploy to Streamlit Cloud:

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Create new app**:
   - Repository: `your-username/Revoking-Discord-`
   - Branch: `main`
   - Main file path: `main.py`

4. **Add Secrets** in app settings:
   ```toml
   DISCORD_BOT_TOKEN = "your_actual_discord_bot_token"
   DISCORD_GUILD_ID = "1393935478503243917"
   ```

5. **Deploy** and your app will be live!

### 🔧 Local Development:

```bash
# Clone the repository
git clone https://github.com/your-username/Revoking-Discord-.git
cd Revoking-Discord-

# Install dependencies
pip install -r requirements.txt

# Configure secrets
cp .streamlit/secrets_template.toml .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your actual bot token

# Run the app
streamlit run main.py
```

---

**⚠️ Disclaimer**: This tool should only be used by server administrators with proper authorization. Always backup your member list before performing bulk operations. 