import discord
from discord.ext import commands
import datetime
from ruamel.yaml import YAML
import random
import os
from Resources.Data import save_data, load_data

yaml = YAML()

# Read in the Config.yml file with a special module that allows me to preserve comments
with open("./Config.yml", 'r') as file:
    config = yaml.load(file)

# Read in permissions settings.
with open("./Permissions.yml", 'r') as file:
    permissions = yaml.load(file)

# The function which allows the command prefix to be changed dynamically.
def get_prefix(client, message):
    with open("./Config.yml", 'r') as file:
        config = yaml.load(file)
    prefix = config['Prefix']
    return prefix

# Create the actual bot instance.
bot = commands.AutoShardedBot(command_prefix = get_prefix, description = "NAU's Welcome Bot", case_insensitive = True)

# I made a custom help command so I remove the default one here.
# Find the custom on in ~/Cogs/Help.py
bot.remove_command('help')

# Setting the main config settings from variables
bot.TOKEN = config['TOKEN']
bot.prefix = config['Prefix']
bot.logs_channels = config['Log Channels']
bot.embed_colors = config['Embed Colors']
bot.footer_icon = config['Footer Icon URL']
bot.footer_text = config['Footer Text']
bot.online_message = config['Online Message']
bot.restarting_message = config['Restarting Message']
bot.data_file = os.path.abspath(config['Data File'])
bot.credentials_file = os.path.abspath(config['Google API Credentials File'])
bot.token_file = os.path.abspath(config['Token File'])
bot.permissions = permissions
bot.config = config
bot.yaml = yaml

# Setting the message options and some other smaller options from config variables
bot.use_timestamp = config['Options']['Embed Timestamp']
bot.delete_commands = config['Options']['Delete Commands']
bot.show_command_author = config['Options']['Show Author']
bot.show_game_status = config['Options']['Game Status']['Active']
bot.game_to_show = config['Options']['Game Status']['Game']
bot.student_role_id = config['Student Role ID']
bot.non_student_role_id = config['Non Student Role ID']
bot.guild_id = config['Guild ID']

# Initialize the data (either reads it from the Data File in Config.yml or creates the file if it doesn't exist)
if os.path.exists(bot.data_file):
    with open(bot.data_file, 'r') as file:
        content = file.read()
        if len(content) == 0:
            bot.data = {}
            save_data(bot.data_file, bot.data)
        else:
            bot.data = load_data(bot.data_file)
else:
    bot.data = {}
    save_data(bot.data_file, bot.data)

# Listing the other Cogs
# You can find each cog at ~/Cogs/{NAME}.py
extensions = [
    'Cogs.General',
    'Cogs.Help',
    'Cogs.Welcome'
]

print('Connecting to Discord...')

# Command is called when the bot comes online
@bot.event
async def on_ready():
    # Load the commands and listeners from the cogs above
    # Each cog has it's own print statements for when it has been loaded
    for extension in extensions:
        bot.load_extension(extension)

    # Print the connection confirmation
    print('Logged in as {0} and connected to Discord! (ID: {0.id})'.format(bot.user))

    # Set the bots `Playing ___` status if that is enabled
    if bot.show_game_status:
        game = discord.Game(name = bot.game_to_show.format(prefix = bot.prefix))
        await bot.change_presence(activity = game)

    # Creating a message stating that the bot is online
    if bot.use_timestamp:
        embed = discord.Embed(
            title = bot.online_message.format(username = bot.user.name),
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = bot.online_message.format(username = bot.user.name),
            color = random.choice(bot.embed_colors)
        )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

    # Send the online message to all registered log channels
    for log in bot.logs_channels:
        channel = bot.get_channel(log)
        await channel.send(content = None, embed = embed)

    # Record the bot's start time so that I can calculate uptime later
    bot.start_time = datetime.datetime.now(datetime.timezone.utc)

# A universal check. Kindof hard to explain.
# Basically, every command, before it can happen, will have to pass this check first
# It checks the command name, then finds the same name in the Permissions.yml file
# It takes all Roles listed in the Permissions.yml file and checks them here
# If no entry in the Permissions.yml file is found for a command, it will assume
# that anyone can use the command. Otherwise, only the listed roles can use the command.
# Oh yeah, and by default anyone who has administrator permissions in the server can use any commands
@bot.check
async def command_permissions(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    else:
        name = ctx.command.name
        if ctx.command.parent:
            command = ctx.command
            parent_exists = True
            while parent_exists == True:
                name = ctx.command.parent.name + '-' + name
                command = ctx.command.parent
                if not command.parent:
                    parent_exists = False
        if name in ctx.bot.permissions.keys():
            for permission in ctx.bot.permissions[name]:
                try:
                    role = ctx.guild.get_role(permission['id'])
                    if role in ctx.author.roles:
                        return True
                except Exception as e:
                    print(e)
            return False
        else:
            return True

# The command that restarts the bot from discord.
# I will use this command to explain the Discord command structure
# First we use a decorator to name the command with the following args
#   name - This names the command, you will use the command as {prefix}{name}
#   aliases - a list/array of strings which allow for other {name}s to be used for the same command
#   help - the string which gets used in the Help command, also good for notes for yourself
#   brief - used to show the example in the help message. if the command is `!restart` and it takes an argument,
#       we would put the argument example in brief, `!restart ?` (this does not actually apply to this command)
# The function can be named whatever you want it is not related, just make sure it doesnt have the same name as another command,
#   or it will overwrite that command
@bot.command(name = "restart", help = "Restarts the bot.", brief = "")
async def restart(ctx):
    # Creating an embedded message. I almost always use the same format when creating one
    if bot.use_timestamp:
        embed = discord.Embed(
            title = bot.restarting_message.format(username = bot.user.name),
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = bot.restarting_message.format(username = bot.user.name),
            color = random.choice(bot.embed_colors)
        )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

    # Send the embedded message to all logs channels
    for log in bot.logs_channels:
        channel = bot.get_channel(log)
        await channel.send(content = None, embed = embed)

    # Add a checkmark reaction to the original command the user executed to show confirmation
    await ctx.message.add_reaction('✅')

    # Stop the bot. This closes the program, after which the batch executable file loops the program
    # I am making a .sh file for the same purpose as the batch file rn.
    await bot.close()

# Add error management for the bot as a whole. If a user does not have permission to use a command,
# this will blanked monitor that.
@restart.error
async def restart_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed = discord.Embed(title = "Insufficient Permissions", color = random.choice(bot.embed_colors)))

# This will monitor all Discord errors from the bot as a whole.
# Prevents spamming the console when people spell commands wrong
# or use a command that doesnt exist
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(title = "Command not found.", color = random.choice(bot.embed_colors)))
    else:
        print(error)

# Actually run the bot.
bot.run(bot.TOKEN, bot = True, reconnect = True)
