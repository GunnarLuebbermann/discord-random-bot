from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks
import random
from datetime import datetime

# LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot with specified intents
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.user_list = []
        self.show_all_users_command()
        self.add_user_command()
        self.delete_user_command()
        self.random_user_command()

    async def on_ready(self):
        print(f'Bot is ready. Logged in as {self.user}')
        await self.tree.sync()  # Synchronize commands with Discord

# SHOW ALL USERS INSIDE LIST
    def show_all_users_command(self):
        @self.tree.command(name='show_all_users', description='Show all users inside list')
        async def show_all_users(interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("You have no admin")
            if self.user_list:
                embed = discord.Embed(title="User List", description="\n".join(self.user_list), color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('The user list is empty.')

# ADD NEW USER TO LIST
    def add_user_command(self):
        @self.tree.command(name='add_user', description='Add a user to the list')
        async def add_user(interaction: discord.Interaction, user: str):
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("You have no admin")
            self.user_list.append(user)
            await interaction.response.send_message(f'User {user} added.')

# DELETE USER FROM LIST
    def delete_user_command(self):
        @self.tree.command(name='delete_user', description='Delete a user from the list')
        async def delete_user(interaction: discord.Interaction, user: str):
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("You have no admin")
            try:
                self.user_list.remove(user)
                await interaction.response.send_message(f'User {user} removed.')
            except ValueError:
                await interaction.response.send_message(f'User {user} not found in list.')

# CHOOSE RANDOM USER
    def random_user_command(self):
        @self.tree.command(name='random_user', description='Choose a random user from the list')
        async def random_user(interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("You have no admin")
            if self.user_list:
                random_user = random.choice(self.user_list)
                await interaction.response.send_message(f'Random user: {random_user}')
            else:
                await interaction.response.send_message('User list is empty, no one to choose.')

# Initialize bot
bot = MyBot()

# Run the bot with your token
bot.run(TOKEN)