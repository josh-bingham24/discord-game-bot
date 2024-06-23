import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(guild_ids=[GUILD_ID])
async def hello(interaction: nextcord.Interaction):
    await interaction.channel.send('Hello!')

@bot.slash_command(guild_ids=[GUILD_ID])
async def addgame(interaction: nextcord.Interaction, game_name: str):
    try:
        with open('active.txt', 'a') as file:
            file.write(f'{game_name}\n')

        await interaction.response.send_message(f'{game_name} has been added to list of active games')
    except Exception:
        await interaction.response.send_message(f'There was an error processing your request: {Exception}')


# @bot.slash_command(guild_ids=[GUILD_ID])
# async def getactivegames(interaction: nextcord.Interaction):

@bot.slash_command(guild_ids=[GUILD_ID])
async def removegame(interaction: nextcord.Interaction, game_name: str):
    try:
        # Read all games from active.txt
        with open('active.txt', 'r') as file:
            games = file.readlines()

        # Remove the specified game name if it exists
        game_to_remove = game_name + '\n'
        if game_to_remove in games:
            games.remove(game_to_remove)

            # Write the updated list back to active.txt
            with open('active.txt', 'w') as file:
                file.writelines(games)

            # Append the removed game name to finished.txt
            with open('finished.txt', 'a') as file:
                file.write(game_name + '\n')

            await interaction.response.send_message(
                f'Game "{game_name}" has been removed from the list of active games and added to finished games.')
        else:
            await interaction.response.send_message(f'Game "{game_name}" was not found in the list of active games.')
    except Exception as e:
        await interaction.response.send_message(f'There was an error processing your request: {e}')

bot.run(BOT_TOKEN)