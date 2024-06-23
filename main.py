import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

bot = commands.Bot()


def get_games_from_file(file: str) -> list:
    try:
        with open(file, 'r') as f:
            games = f.readlines()
        return games
    except FileNotFoundError:
        return []


def write_games_to_file(file: str, game:str) -> None:
    with open(file, 'w') as f:
        f.write(game)


def append_game_to_file(file: str, game: str) -> None:
    with open(file, 'a') as f:
        f.write(game)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def get_active_games(interaction: nextcord.Interaction):
    games = [game.strip('\n') for game in get_games_from_file('active.txt')]
    await interaction.response.send_message(f'Active games: {games}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def get_backlog_games(interaction: nextcord.Interaction):
    games = [game.strip('\n') for game in get_games_from_file('backlog.txt')]
    await interaction.response.send_message(f'Backlogged games: {games}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def get_inactive_games(interaction: nextcord.Interaction):
    games = [game.strip('\n') for game in get_games_from_file('inactive.txt')]
    await interaction.response.send_message(f'Inactive games: {games}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def add_game_backlog(interaction: nextcord.Interaction, game: str):
    try:
        with open('backlog.txt', 'a') as file:
            file.write(f'{game}\n')

        await interaction.response.send_message(f'{game} has been added to list of backlogged games')
    except Exception as e:
        await interaction.response.send_message(f'There was an error processing your request: {e}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def add_game_active(interaction: nextcord.Interaction, game: str):
    try:
        backlog_games = get_games_from_file('backlog.txt')
        inactive_games = get_games_from_file('inactive_games.txt')

        game_to_remove = game + '\n'
        if game_to_remove in backlog_games:
            backlog_games.remove(game_to_remove)

            with open('backlog.txt', 'w') as file:
                file.writelines(backlog_games)

            with open('active.txt', 'a') as file:
                file.write(game + '\n')

            await interaction.response.send_message(f'{game} has been moved from backlog to active games')

        elif game_to_remove in inactive_games:
            inactive_games.remove(game_to_remove)

            with open('inactive.txt', 'w') as file:
                file.writelines(inactive_games)

            with open('active.txt', 'a') as file:
                file.write(game + '\n')

            await interaction.response.send_message(f'{game} has been moved from inactive to active games')

        else:
            with open('active.txt', 'a') as file:
                file.write(game + '\n')

            await interaction.response.send_message(f'{game} has been added to active games')

    except Exception as e:
        await interaction.response.send_message(f'There was an error processing your request: {e}')


@bot.slash_command(guild_ids=[GUILD_ID])
async def add_game_inactive(interaction: nextcord.Interaction, game: str):
    try:
        games = get_games_from_file('active.txt')

        game_to_remove = game + '\n'
        if game_to_remove in games:
            games.remove(game_to_remove)

            with open('active.txt', 'w') as file:
                file.writelines(games)

            with open('inactive.txt', 'a') as file:
                file.write(game + '\n')

            await interaction.response.send_message(
                f'{game} has been removed from the list of active games and added to inactive games')
        else:
            games = [game.strip('\n') for game in games]
            await interaction.response.send_message(f'{game} was not found in the list of active games\n'
                                                    f'Active games: {games}')
    except Exception as e:
        await interaction.response.send_message(f'There was an error processing your request: {e}')


bot.run(BOT_TOKEN)
