# This script creates a Discord bot that can clear messages in a channel.
# It uses the discord.py library.
# To run this bot, you need to:
# 1. Install the library: pip install -U discord.py
# 2. Create a bot application on the Discord Developer Portal.
# 3. Get your bot's token and set it as an environment variable named 'DISCORD_TOKEN'.
# 4. Invite the bot to your server with the 'Manage Messages' permission.

import os
import discord
from discord.ext import commands

# Define the intents for the bot.
# message_content is required to read and process the content of messages.
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with a command prefix and intents.
# We are using a command prefix, but will also manually handle the !a34 clear command.
bot = commands.Bot(command_prefix='!', intents=intents)

# This event is called when the bot has successfully connected to Discord.
@bot.event
async def on_ready():
    """
    Prints a message to the console when the bot is ready.
    """
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# This event is called every time a message is sent in any channel the bot can see.
@bot.event
async def on_message(message):
    """
    Handles incoming messages and checks for the clear command.
    """
    # Ignore messages sent by the bot itself to prevent command loops.
    if message.author == bot.user:
        return

    # Split the message content into a list of words.
    parts = message.content.split()

    # Check if the message starts with the command "!a34 clear".
    # We use a case-insensitive check for the command.
    if len(parts) >= 3 and parts[0].lower() == '!a34' and parts[1].lower() == 'clear':
        try:
            # Check if the user has the 'Manage Messages' permission.
            if not message.author.guild_permissions.manage_messages:
                await message.channel.send("You don't have the required permissions to do that.")
                return
            
            # Check if the bot has the 'Manage Messages' permission.
            if not message.guild.me.guild_permissions.manage_messages:
                await message.channel.send("I don't have the required permissions to clear messages.")
                return

            # Get the quantity of messages to clear from the third part of the command.
            quantity = int(parts[2])

            # Ensure the quantity is a positive number.
            if quantity <= 0:
                await message.channel.send("Please provide a positive number of messages to clear.")
                return

            # Delete the command message itself before purging the rest.
            await message.delete()

            # Purge the specified number of messages from the channel.
            # We add 1 to the quantity to account for the command message itself.
            deleted = await message.channel.purge(limit=quantity)
            
            # Send a confirmation message that will be automatically deleted after 5 seconds.
            response = await message.channel.send(f'Successfully cleared {len(deleted)} messages.')
            await response.delete(delay=5)

        except ValueError:
            # Handle cases where the quantity provided is not a valid number.
            await message.channel.send("Please provide a valid number of messages to clear.")
            
        except Exception as e:
            # Catch any other potential errors and send a message to the channel.
            print(f"An error occurred: {e}")
            await message.channel.send(f"An error occurred while trying to clear messages: {e}")

    # Process other commands if any, using the built-in command handler.
    # This is a good practice if you want to add more commands later.
    await bot.process_commands(message)

# Get the bot token from the environment variable.
# It is highly recommended to use an environment variable for security.
# If the environment variable is not found, you can hardcode the token here for testing purposes,
# but do not do this in a production environment.
# Example: token = 'YOUR_BOT_TOKEN_HERE'
token = os.getenv('DISCORD_TOKEN')

if token:
    # Run the bot with the provided token.
    bot.run(token)
else:
    # Print an error message if the token is not found.
    print("Error: DISCORD_TOKEN environment variable not found. Please set it.")
