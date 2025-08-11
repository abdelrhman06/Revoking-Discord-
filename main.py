import streamlit as st
import pandas as pd
import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log'),
        logging.StreamHandler()
    ]
)

class DiscordUserRemover:
    def __init__(self):
        self.bot = None
        self.is_connected = False
        self.removed_users = []
        self.failed_users = []
        
    async def create_bot(self, token, guild_id):
        """Create and connect Discord bot"""
        try:
            intents = discord.Intents.default()
            intents.members = True
            intents.guilds = True
            
            self.bot = commands.Bot(command_prefix='!', intents=intents)
            
            @self.bot.event
            async def on_ready():
                logging.info(f'Bot connected as {self.bot.user}')
                self.is_connected = True
                
            await self.bot.login(token)
            await self.bot.connect()
            
            # Wait for connection
            timeout = 10
            while not self.is_connected and timeout > 0:
                await asyncio.sleep(1)
                timeout -= 1
                
            if not self.is_connected:
                raise Exception("Failed to connect to Discord")
                
            return True
            
        except Exception as e:
            logging.error(f"Failed to create bot: {str(e)}")
            return False
    
    async def get_users_without_roles(self, guild_id):
        """Get list of users without any roles (except @everyone)"""
        if not self.bot or not self.is_connected:
            return []
        
        try:
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                return []
            
            users_without_roles = []
            for member in guild.members:
                # Check if user has any roles other than @everyone
                if len(member.roles) <= 1:  # @everyone is always present
                    users_without_roles.append(member.name)
            
            return users_without_roles
            
        except Exception as e:
            logging.error(f"Error getting users without roles: {str(e)}")
            return []
    
    async def remove_users(self, usernames, guild_id, action_type="kick"):
        """Remove users from Discord server"""
        if not self.bot or not self.is_connected:
            return False, "Bot not connected"
        
        try:
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                return False, f"Guild {guild_id} not found"
            
            self.removed_users = []
            self.failed_users = []
            
            for username in usernames:
                try:
                    # Find member by username (without discriminator) or display name
                    member = None
                    
                    # Try to find by username
                    for m in guild.members:
                        if m.name.lower() == username.lower() or m.display_name.lower() == username.lower():
                            member = m
                            break
                    
                    if member:
                        # Check if it's the bot itself
                        if member.id == self.bot.user.id:
                            self.failed_users.append(f"{username} (Cannot remove bot itself)")
                            continue
                            
                        if action_type == "kick":
                            await member.kick(reason="Bulk removal via bot")
                            self.removed_users.append(f"{member.name}#{member.discriminator}")
                            logging.info(f"Kicked user: {member.name}")
                        elif action_type == "ban":
                            await member.ban(reason="Bulk removal via bot")
                            self.removed_users.append(f"{member.name}#{member.discriminator}")
                            logging.info(f"Banned user: {member.name}")
                    else:
                        self.failed_users.append(f"{username} (User not found)")
                        logging.warning(f"User not found: {username}")
                        
                except Exception as e:
                    self.failed_users.append(f"{username} (Error: {str(e)})")
                    logging.error(f"Failed to remove {username}: {str(e)}")
                    
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
            
            return True, f"Process completed. Removed: {len(self.removed_users)}, Failed: {len(self.failed_users)}"
            
        except Exception as e:
            logging.error(f"Error in remove_users: {str(e)}")
            return False, str(e)
    
    async def disconnect(self):
        """Disconnect bot"""
        if self.bot:
            await self.bot.close()
            self.is_connected = False

def process_excel_file(uploaded_file):
    """Process uploaded Excel file and extract usernames"""
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)
        
        # Look for username column (case insensitive)
        username_col = None
        for col in df.columns:
            if 'username' in col.lower() or 'discord' in col.lower():
                username_col = col
                break
        
        if username_col is None:
            return None, "No username column found. Please ensure your Excel file has a column containing 'username' or 'discord'"
        
        # Extract usernames and remove empty values
        usernames = df[username_col].dropna().astype(str).tolist()
        usernames = [u.strip() for u in usernames if u.strip()]
        
        return usernames, f"Found {len(usernames)} usernames in column '{username_col}'"
        
    except Exception as e:
        return None, f"Error processing Excel file: {str(e)}"

def main():
    st.set_page_config(
        page_title="Discord User Remover",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Discord User Remover Bot")
    st.markdown("Upload an Excel file with Discord usernames to remove them from your server")
    
    # Initialize session state
    if 'remover' not in st.session_state:
        st.session_state.remover = DiscordUserRemover()
    if 'usernames' not in st.session_state:
        st.session_state.usernames = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # Configuration from environment or Streamlit secrets
    bot_token = os.getenv("DISCORD_BOT_TOKEN") or st.secrets.get("DISCORD_BOT_TOKEN", "")
    guild_id = os.getenv("DISCORD_GUILD_ID") or st.secrets.get("DISCORD_GUILD_ID", "1393935478503243917")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Bot Configuration")
        
        # Show connection status
        st.info("🔐 Bot Token: Hidden (Configured)")
        st.info(f"🏠 Server ID: {guild_id}")
        
        # Action type
        action_type = st.selectbox(
            "Action Type",
            ["kick", "ban"],
            help="Choose whether to kick or ban users"
        )
        
        # User filter options
        st.subheader("🎯 User Filter Options")
        
        filter_option = st.selectbox(
            "Remove Users Based On:",
            [
                "Excel File List", 
                "Users Without Roles",
                "Both (Excel + No Roles)"
            ],
            help="Choose how to select users for removal"
        )
        
        # Test connection
        if st.button("🔌 Test Connection"):
            if not bot_token:
                st.error("❌ Bot token not found in secrets!")
            else:
                with st.spinner("Testing connection..."):
                    try:
                        # Simple validation
                        if bot_token.startswith("MT") and len(bot_token) > 50:
                            # Test Discord bot creation
                            import discord
                            intents = discord.Intents.default()
                            intents.members = True
                            intents.guilds = True
                            
                            # Create temporary bot for testing
                            test_bot = discord.Client(intents=intents)
                            
                            @test_bot.event
                            async def on_ready():
                                st.success("✅ Connection successful!")
                                await test_bot.close()
                            
                            # Quick token validation
                            try:
                                # This will validate the token format
                                import base64
                                token_parts = bot_token.split('.')
                                if len(token_parts) == 3:
                                    # Decode the first part to get bot ID
                                    bot_id = base64.b64decode(token_parts[0] + '==').decode('utf-8')
                                    st.success(f"✅ Token validated! Bot ID: {bot_id}")
                                    st.success(f"✅ Server ID: {guild_id}")
                                    st.info("🤖 Ready to use!")
                                else:
                                    st.error("❌ Invalid token format")
                            except Exception as token_err:
                                st.error(f"❌ Token validation failed: {str(token_err)}")
                        else:
                            st.error("❌ Invalid token format. Token should start with 'MT' and be longer than 50 characters.")
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if filter_option in ["Excel File List", "Both (Excel + No Roles)"]:
            st.header("📊 Upload Excel File")
            
            uploaded_file = st.file_uploader(
                "Choose an Excel file",
                type=['xlsx', 'xls'],
                help="Excel file should contain a column with Discord usernames"
            )
            
            if uploaded_file is not None:
                with st.spinner("Processing Excel file..."):
                    usernames, message = process_excel_file(uploaded_file)
                    
                if usernames:
                    st.success(message)
                    st.session_state.usernames = usernames
                    
                    # Preview usernames
                    st.subheader("👥 Preview Usernames from Excel")
                    preview_df = pd.DataFrame(usernames[:10], columns=["Discord Username"])
                    st.dataframe(preview_df, use_container_width=True)
                    
                    if len(usernames) > 10:
                        st.info(f"Showing first 10 usernames. Total: {len(usernames)}")
                    
                else:
                    st.error(message)
                    st.session_state.usernames = []
            else:
                st.session_state.usernames = []
        
        # Users without roles section
        if filter_option in ["Users Without Roles", "Both (Excel + No Roles)"]:
            st.header("👤 Users Without Roles")
            
            if st.button("🔍 Find Users Without Roles"):
                with st.spinner("Scanning server for users without roles..."):
                    async def get_no_role_users():
                        success = await st.session_state.remover.create_bot(bot_token, guild_id)
                        if success:
                            users = await st.session_state.remover.get_users_without_roles(guild_id)
                            await st.session_state.remover.disconnect()
                            return users
                        return []
                    
                    try:
                        no_role_users = asyncio.run(get_no_role_users())
                        if no_role_users:
                            st.session_state.no_role_users = no_role_users
                            st.success(f"Found {len(no_role_users)} users without roles")
                            
                            # Preview users without roles
                            st.subheader("👥 Users Without Roles Preview")
                            preview_df = pd.DataFrame(no_role_users[:10], columns=["Discord Username"])
                            st.dataframe(preview_df, use_container_width=True)
                            
                            if len(no_role_users) > 10:
                                st.info(f"Showing first 10 users. Total: {len(no_role_users)}")
                        else:
                            st.info("No users without roles found")
                            st.session_state.no_role_users = []
                    except Exception as e:
                        st.error(f"Error finding users: {str(e)}")
                        st.session_state.no_role_users = []
            
            # Initialize if not exists
            if 'no_role_users' not in st.session_state:
                st.session_state.no_role_users = []
    
    with col2:
        st.header("📈 Statistics")
        
        # Excel file statistics
        if filter_option in ["Excel File List", "Both (Excel + No Roles)"] and st.session_state.usernames:
            st.metric("Excel File Users", len(st.session_state.usernames))
        
        # No role users statistics
        if filter_option in ["Users Without Roles", "Both (Excel + No Roles)"] and 'no_role_users' in st.session_state:
            st.metric("Users Without Roles", len(st.session_state.no_role_users))
        
        # Total users to process
        total_users = 0
        if filter_option == "Excel File List":
            total_users = len(st.session_state.usernames) if st.session_state.usernames else 0
        elif filter_option == "Users Without Roles":
            total_users = len(st.session_state.no_role_users) if 'no_role_users' in st.session_state else 0
        elif filter_option == "Both (Excel + No Roles)":
            excel_users = len(st.session_state.usernames) if st.session_state.usernames else 0
            no_role_users = len(st.session_state.no_role_users) if 'no_role_users' in st.session_state else 0
            # Combine and remove duplicates
            combined_users = set(st.session_state.usernames if st.session_state.usernames else [])
            combined_users.update(st.session_state.no_role_users if 'no_role_users' in st.session_state else [])
            total_users = len(combined_users)
        
        if total_users > 0:
            st.metric("Total Users to Process", total_users)
            
        if hasattr(st.session_state.remover, 'removed_users'):
            st.metric("Successfully Removed", len(st.session_state.remover.removed_users))
            st.metric("Failed Attempts", len(st.session_state.remover.failed_users))
    
    # Determine if we have users to process
    has_users_to_process = False
    users_to_process = []
    
    if filter_option == "Excel File List" and st.session_state.usernames:
        has_users_to_process = True
        users_to_process = st.session_state.usernames
    elif filter_option == "Users Without Roles" and 'no_role_users' in st.session_state and st.session_state.no_role_users:
        has_users_to_process = True
        users_to_process = st.session_state.no_role_users
    elif filter_option == "Both (Excel + No Roles)":
        # Combine both lists and remove duplicates
        combined_users = set()
        if st.session_state.usernames:
            combined_users.update(st.session_state.usernames)
        if 'no_role_users' in st.session_state and st.session_state.no_role_users:
            combined_users.update(st.session_state.no_role_users)
        if combined_users:
            has_users_to_process = True
            users_to_process = list(combined_users)
    
    # Action buttons
    if has_users_to_process:
        st.header("🚀 Execute Actions")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button(f"🗑️ {action_type.title()} All Users", type="primary", disabled=st.session_state.processing):
                st.session_state.processing = True
                st.session_state.current_users_to_process = users_to_process
                
        with col2:
            if st.button("🛑 Stop Process", disabled=not st.session_state.processing):
                st.session_state.processing = False
                st.info("Process stopped by user")
        
        # Execute removal process - REAL DISCORD API
        if st.session_state.processing:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Connecting to Discord...")
                
                import discord
                import asyncio
                import threading
                from concurrent.futures import ThreadPoolExecutor
                
                # Initialize results storage
                if not hasattr(st.session_state.remover, 'removed_users'):
                    st.session_state.remover.removed_users = []
                if not hasattr(st.session_state.remover, 'failed_users'):
                    st.session_state.remover.failed_users = []
                
                st.session_state.remover.removed_users = []
                st.session_state.remover.failed_users = []
                
                current_users = getattr(st.session_state, 'current_users_to_process', [])
                total_users = len(current_users)
                
                # Create results containers
                results = {"removed": [], "failed": [], "completed": False}
                
                async def discord_bot_operations():
                    try:
                        # Setup Discord bot
                        intents = discord.Intents.default()
                        intents.members = True
                        intents.guilds = True
                        
                        client = discord.Client(intents=intents)
                        
                        @client.event
                        async def on_ready():
                            try:
                                # Get guild
                                guild = client.get_guild(int(guild_id))
                                if not guild:
                                    results["failed"].append("Server not found")
                                    await client.close()
                                    return
                                
                                # Process each user
                                for i, username in enumerate(current_users):
                                    try:
                                        # Find member by username
                                        member = None
                                        for m in guild.members:
                                            if (m.name.lower() == username.lower() or 
                                                m.display_name.lower() == username.lower()):
                                                member = m
                                                break
                                        
                                        if member:
                                            # Don't remove bot itself
                                            if member.id == client.user.id:
                                                results["failed"].append(f"{username} (Cannot remove bot)")
                                                continue
                                            
                                            # Perform action
                                            if action_type == "kick":
                                                await member.kick(reason="Bulk removal via bot")
                                                results["removed"].append(f"{member.name}#{member.discriminator}")
                                            elif action_type == "ban":
                                                await member.ban(reason="Bulk removal via bot", delete_message_days=0)
                                                results["removed"].append(f"{member.name}#{member.discriminator}")
                                                
                                        else:
                                            results["failed"].append(f"{username} (User not found)")
                                        
                                        # Small delay to respect rate limits
                                        await asyncio.sleep(1)
                                        
                                    except discord.Forbidden:
                                        results["failed"].append(f"{username} (No permission)")
                                    except discord.HTTPException as e:
                                        results["failed"].append(f"{username} (Discord error: {str(e)})")
                                    except Exception as e:
                                        results["failed"].append(f"{username} (Error: {str(e)})")
                                
                                results["completed"] = True
                                
                            except Exception as e:
                                results["failed"].append(f"Bot error: {str(e)}")
                            finally:
                                await client.close()
                        
                        # Start bot
                        await client.start(bot_token)
                        
                    except Exception as e:
                        results["failed"].append(f"Connection error: {str(e)}")
                        results["completed"] = True
                
                # Run Discord operations in thread
                def run_discord_ops():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(discord_bot_operations())
                    except Exception as e:
                        results["failed"].append(f"Thread error: {str(e)}")
                        results["completed"] = True
                    finally:
                        loop.close()
                
                # Start Discord bot in separate thread
                bot_thread = threading.Thread(target=run_discord_ops)
                bot_thread.daemon = True
                bot_thread.start()
                
                # Wait and show progress
                progress_bar.progress(0.1)
                status_text.text(f"Starting {action_type} process...")
                
                # Monitor progress
                timeout = 300  # 5 minutes timeout
                start_time = time.time()
                
                while not results["completed"] and (time.time() - start_time) < timeout:
                    # Update progress based on results
                    processed = len(results["removed"]) + len(results["failed"])
                    if total_users > 0:
                        progress = 0.1 + (0.8 * processed / total_users)
                        progress_bar.progress(min(progress, 0.9))
                    
                    if processed > 0:
                        status_text.text(f"Processed {processed}/{total_users} users...")
                    
                    time.sleep(2)
                
                # Final results
                st.session_state.remover.removed_users = results["removed"]
                st.session_state.remover.failed_users = results["failed"]
                
                progress_bar.progress(1.0)
                status_text.text("Process completed!")
                
                # Show final results
                removed_count = len(results["removed"])
                failed_count = len(results["failed"])
                
                if removed_count > 0:
                    st.success(f"✅ Successfully {action_type}ed {removed_count} users from Discord!")
                
                if failed_count > 0:
                    st.warning(f"⚠️ Failed to process {failed_count} users")
                
                if removed_count == 0 and failed_count == 0:
                    st.info("No users were processed")
                
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
            finally:
                st.session_state.processing = False
                status_text.empty()
    
    # Results section
    if hasattr(st.session_state.remover, 'removed_users') and (st.session_state.remover.removed_users or st.session_state.remover.failed_users):
        st.header("📋 Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.remover.removed_users:
                st.subheader("✅ Successfully Removed")
                removed_df = pd.DataFrame(st.session_state.remover.removed_users, columns=["Username"])
                st.dataframe(removed_df, use_container_width=True)
        
        with col2:
            if st.session_state.remover.failed_users:
                st.subheader("❌ Failed to Remove")
                failed_df = pd.DataFrame(st.session_state.remover.failed_users, columns=["Username (Reason)"])
                st.dataframe(failed_df, use_container_width=True)
        
        # Download results
        if st.button("📥 Download Results"):
            results_data = {
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * (len(st.session_state.remover.removed_users) + len(st.session_state.remover.failed_users)),
                'Username': st.session_state.remover.removed_users + st.session_state.remover.failed_users,
                'Status': ['Success'] * len(st.session_state.remover.removed_users) + ['Failed'] * len(st.session_state.remover.failed_users)
            }
            
            results_df = pd.DataFrame(results_data)
            csv = results_df.to_csv(index=False)
            
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name=f"discord_removal_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>⚠️ <strong>Warning:</strong> This tool will permanently remove users from your Discord server. Use with caution.</p>
            <p>Make sure you have proper permissions and authorization before removing users.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 