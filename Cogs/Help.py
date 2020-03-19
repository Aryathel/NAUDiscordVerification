import discord
from discord.ext import commands
import datetime
import random

"""
Honestly you really shouldn't play with this file.

If for some reason you absolutely need to change the help functionality,
DM Heroicos_HM#0310 on Discord.
"""
class TheHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = "Command Help",
            description = "A listing of all available commands sorted by grouping.\nTo learn more about specific commands, use `{0.clean_prefix}help <command>`".format(self),
            color = random.choice(self.context.bot.embed_colors)
        )
        for cog in mapping.keys():
            if cog:
                command_list = await self.filter_commands(mapping[cog], sort = True)
                if len(command_list) > 0:
                    embed.add_field(
                        name = cog.qualified_name,
                        value = "{0.description}\nCommands:\n".format(cog) + ", ".join("`{1.qualified_name}`".format(self, command) for command in command_list),
                        inline = False
                    )
        await self.get_destination().send(embed = embed)
        """
        else:
            embed = discord.Embed(
                description = "Help commands can only be used in bot channels.",
                color = random.choice(self.context.bot.embed_colors)
            )
            await self.get_destination().send(embed = embed)
        """

    async def send_cog_help(self, cog):
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = cog.qualified_name + " Help",
            description = "{0.description}\n".format(cog) + "To learn more about specific commands, use `{0.clean_prefix}help <command>`".format(self),
            color = random.choice(self.context.bot.embed_colors)
        )
        embed.add_field(
            name = "Commands",
            value = "\n".join("`{1.qualified_name}`".format(self, command) for command in cog.walk_commands() if not command.hidden),
            inline = False
        )
        await self.get_destination().send(embed = embed)
        """
        else:
            embed = discord.Embed(
                description = "Help commands can only be used in bot channels.",
                color = random.choice(self.context.bot.embed_colors)
            )
            await self.get_destination().send(embed = embed)
        """

    async def send_group_help(self, group):
        #if self.context.channel.name.startswith('bot'):
        command_list = group.walk_commands()
        command_activation = []
        command_example = []
        for command in command_list:
            if "`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help) not in command_activation and not command.hidden:
                command_activation.append("`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help))
                if command.brief:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`")
                else:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + "`")

        embed = discord.Embed(
            title = "{} Help".format(group.qualified_name.capitalize()),
            description = "{0.help}\n\nFor more information on each command, use `{1.clean_prefix}help [command]`.".format(group, self),
            color = random.choice(self.context.bot.embed_colors)
        )
        if group.aliases:
            embed.add_field(
                name = "Aliases",
                value = ", ".join('`{}`'.format(alias) for alias in group.aliases),
                inline = False
            )
        embed.add_field(
            name = "Commands",
            value = "\n".join(command_activation),
            inline = False
        )
        embed.add_field(
            name = "Examples",
            value = "\n".join(command_example)
        )
        await self.get_destination().send(embed = embed)
        """
        else:
            embed = discord.Embed(
                description = "Help commands can only be used in bot channels.",
                color = random.choice(self.context.bot.embed_colors)
            )
            await self.get_destination().send(embed = embed)
        """

    async def send_command_help(self, command):
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = "{0} Help".format(command.name.capitalize()),
            description = "{0.help}".format(command),
            color = random.choice(self.context.bot.embed_colors)
        )
        if command.aliases:
            embed.add_field(
                name = "Aliases",
                value = ", ".join('`{}`'.format(alias) for alias in command.aliases),
                inline = False
            )
        embed.add_field(
            name = "Usage",
            value = "`" + self.clean_prefix + command.qualified_name + " " + command.signature + "`",
            inline = False
        )
        if command.brief:
            embed.add_field(
                name = "Example",
                value = "`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`",
                inline = False
            )
        else:
            embed.add_field(
                name = "Example",
                value = "`" + self.clean_prefix + command.qualified_name + "`",
                inline = False
            )
        await self.get_destination().send(embed = embed)
        """
        else:
            embed = discord.Embed(
                description = "Help commands can only be used in bot channels.",
                color = random.choice(self.context.bot.embed_colors)
            )
            await self.get_destination().send(embed = embed)
        """

class LoadHelp(commands.Cog, name = "Help"):
    """
    Get command usage help.
    """
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = TheHelpCommand()
        bot.help_command.cog = self
        print("Loaded Help Cog.")

# Setup by loading the LoadHelp class, which loads the actual help commands.
def setup(bot):
    bot.add_cog(LoadHelp(bot))
