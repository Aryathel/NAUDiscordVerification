import discord
from discord.ext import commands
import datetime
from math import trunc
import random
from pytz import timezone
from Resources.Data import save_data

class General(commands.Cog, name = "General"):
    """
    A few simple commands that are for testing and upkeep.
    """
    def __init__(self, bot):
        self.bot = bot
        print("Loaded General Cog.")

    # Restrict the command to be only usable in a server
    @commands.guild_only()
    @commands.command(name='uptime', help = 'Returns the amount of time the bot has been online.')
    async def uptime(self, ctx):
        if self.bot.delete_commands:
            await ctx.message.delete()

        # Do some number crunching to get the uptime amounts in seconds, minutes, and hours
        seconds = trunc((datetime.datetime.now(datetime.timezone.utc) - self.bot.start_time).total_seconds())
        hours = trunc(seconds / 3600)
        seconds = trunc(seconds - (hours * 3600))
        minutes = trunc(seconds / 60)
        seconds = trunc(seconds - (minutes * 60))

        # Format an embedded message with that information
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":alarm_clock: {} Uptime".format(self.bot.user.name),
                description = "{} Hours\n{} Minutes\n{} Seconds".format(hours, minutes, seconds),
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":alarm_clock: {} Uptime".format(self.bot.user.name),
                description = "{} Hours\n{} Minutes\n{} Seconds".format(hours, minutes, seconds),
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        # Send that embed in the location that the command was used
        await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command(name='ping', aliases=['pong'], help = 'Gets the current latency of the bot.')
    async def ping(self, ctx):
        if self.bot.delete_commands:
            await ctx.message.delete()

        # Send starting message.
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Calculating ping time...",
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Calculating ping time...",
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )

        m = await ctx.send(embed = embed)
        # Create followup embed to show the ping time (difference between original message time and response message time)
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Message latency is {} ms\nDiscord API Latency is {} ms".format(trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000), trunc(self.bot.latency * 1000)),
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Message latency is {} ms\nDiscord API Latency is {} ms".format(trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000), trunc(self.bot.latency * 1000)),
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        # Edit original response to include times.
        await m.edit(embed = embed)

    @commands.guild_only()
    @commands.command(name = "prefix", help = "Changes the command prefix for the bot.", brief = "?")
    async def prefix(self, ctx, prefix: str):
        # Keep track of old prefix for update message
        old = self.bot.prefix
        # Save new prefix
        self.bot.config['Prefix'] = prefix
        with open('./Config.yml', 'w') as file:
            self.bot.yaml.dump(self.bot.config, file)

        # Update prefix in local memory
        self.bot.prefix = prefix
        # Update game status to show proper new prefix
        if self.bot.show_game_status:
            game = discord.Game(name = self.bot.game_to_show.format(prefix = self.bot.prefix))
            await self.bot.change_presence(activity = game)

        # Create embed to inform of prefix update
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = "Prefix Updated",
                description = f"New Prefix: `{self.bot.prefix}`",
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = "Prefix Updated",
                description = f"New Prefix: `{self.bot.prefix}`",
                color = random.choice(self.bot.embed_colors)
            )
        embed.add_field(
            name = "New",
            value = f"{self.bot.prefix}command"
        )
        embed.add_field(
            name = "Old",
            value = f"{old}command"
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        await ctx.send(embed = embed)

    # Catches errors in the prefix command
    @prefix.error
    async def feature_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed = discord.Embed(title = "Insufficient Permissions", color = random.choice(self.bot.embed_colors)))
        else:
            await ctx.send(embed = discord.Embed(title = "Command Failed", description = str(error), color = random.choice(self.bot.embed_colors)))

    # The dangerous command which strips the student and non-student roles from every student and re-sends them the verification survey
    # I HIGHLY RECOMMEND LEAVING THIS COMMENTED OUT 99% OF THE TIME TO AVOID UNFORTUNATE MISTAKES.
    # This is just the exact same beginning steps as in the `Welcome.py` file in the `Cogs` folder, so I won't bother commenting this.
    @commands.command(name = "auth-everyone", help = "Removes all student and non-student roles and re-sends authentication information to all members.", brief = "")
    async def auth_everyone(self, ctx):
        student_role = ctx.guild.get_role(self.bot.student_role_id)
        non_student_role = ctx.guild.get_role(self.bot.non_student_role_id)
        for member in ctx.guild.members:
            if non_student_role in member.roles:
                await member.remove_roles(non_student_role)
            if student_role in member.roles:
                await member.remove_roles(student_role)

            if not member.bot:
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = "Welcome to NAU Esports!",
                        description = 'To get started, please tell us your email.',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = "Welcome to NAU Esports!",
                        description = 'To get started, please tell us your email.',
                        color = random.choice(self.bot.embed_colors)
                    )
                embed.add_field(
                    name = "Example",
                    value = "`your-email@nau.edu`"
                )
                embed.set_footer(
                    text = self.bot.footer_text + ' | [1/7]',
                    icon_url = self.bot.footer_icon
                )
                await member.send(content = member.mention, embed = embed)

                if not 'new_members' in self.bot.data.keys():
                    self.bot.data['new_members'] = {}

                self.bot.data['new_members'][str(member.id)] = {
                    "id": str(member.id),
                    "name": str(member.name),
                    "avatar_url": str(member.avatar_url),
                    "email": None,
                    "first_name": None,
                    "last_name": None,
                    "school": None,
                    "major": None,
                    "game_system": None,
                    "type_of_player": None
                }

                save_data(self.bot.data_file, self.bot.data)

# This little function is called whenever Discord.py adds a cog.
# This just ties the `main.py` bot to the commands here in General.
def setup(bot):
    bot.add_cog(General(bot))
