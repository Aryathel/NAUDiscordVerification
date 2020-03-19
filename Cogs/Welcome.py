"""
Alright. Here is the meat of the program.

This looks overwhelming, being a 400+ line file,
but the vast majority of it is just creating and sending
very repetitive embedded messages to run communications with the user.
"""

import discord
from discord.ext import commands
import datetime
import random # for embeds
# Import my personal addons from the Resources folder.
from Resources.Data import save_data
from Resources.CheckEmail import check_email
from Resources.Enums import PlayerType
from Resources.Sheets import Sheets

class Welcome(commands.Cog, name = "Welcome"):
    """
    The user join listener that sends a welcome message.
    """
    def __init__(self, bot):
        self.bot = bot
        print("Loaded Welcome Cog.")

    # When a member joins the server, catch that event.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # If the member is not a bot.
        if not member.bot:
            # Create a starting embed to send to the user so get them going.
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

            # Send a message to the logs channel that a user has joined and is going through verification
            if self.bot.use_timestamp:
                embed = discord.Embed(
                    title = "User Joined",
                    description = f"User {member.mention} has joined the server and has been sent the verification prompt.",
                    color = random.choice(self.bot.embed_colors),
                    timestamp = datetime.datetime.now(datetime.timezone.utc)
                )
            else:
                embed = discord.Embed(
                    title = "User Joined",
                    description = f"User {member.mention} has joined the server and has been sent the verification prompt.",
                    color = random.choice(self.bot.embed_colors)
                )
            embed.set_author(
                name = member.name,
                icon_url = member.avatar_url
            )
            embed.set_footer(
                text = self.bot.footer_text,
                icon_url = self.bot.footer_icon
            )
            for log in self.bot.logs_channels:
                channel = self.bot.get_channel(log)
                await channel.send(embed = embed)

            """
            Write the starting data for the user to the `new_members` data entry.
            This is where all of the changes will happen and be stored during the
            verification process, so taht if the bot restarts, the data will not be lost.
            """
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
    """
    Ok, now that we have sent the prompt to begin the verification process
    It is time to start the dalogue with the user.
    To do that, we passively listen for any and all messages.
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        If the message author is not a bot and they are messaging in a DM channel
        And they are in the listings of `new_members` in the data
        """
        if not message.author.bot and isinstance(message.channel, discord.DMChannel) and 'new_members' in self.bot.data.keys() and str(message.author.id) in self.bot.data['new_members'].keys():
            """
            Then we start checking to see what step they are on.
            Basically, this is just a massive If/Else tree
            If the user doesn't have an email, then we will expet them to enter an email.
            If there is already an email, but not a first name, then we expect them to enter a first name
            That continues down all the verification questions in the order shown below:
              1. Email
              2. First Name
              3. Last Name
              4. School
              5. Major
              6. Gaming Platforms
              7. Competitive or Casual
            """
            # If the user has not yet had an email saved
            if not self.bot.data['new_members'][str(message.author.id)]['email']:
                # Check if the input they gave is a valid email using our custom function inmported from Resources/CheckEmail.py
                valid = check_email(message.content)
                # If the email is not valid
                if not valid:
                    # Respond with an X reaction
                    await message.add_reaction('❌')
                    # Create an error message explaining that the email was invalid.
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Invalid Email",
                            description = 'Please make sure you send a valid email.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Invalid Email",
                            description = 'Please make sure you send a valid email.',
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
                    await message.author.send(embed = embed)
                else:
                    # If it is valid, change the data
                    self.bot.data['new_members'][str(message.author.id)]['email'] = message.content
                    # If the email ends with `nau.edu`, in any combo of upper/lower case, set their school to NAU
                    if message.content.split('@')[-1].lower() == 'nau.edu':
                        self.bot.data['new_members'][str(message.author.id)]['school'] = 'NAU'
                    # Save this data
                    save_data(self.bot.data_file, self.bot.data)
                    # Add a check mark reaction
                    await message.add_reaction('✅')
                    # Compose a response confirming email registration and asking the next question
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Email Registered",
                            description = 'Next, please tell us your first name.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Email Registered",
                            description = 'Next, please tell us your first name.',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.add_field(
                        name = "Example",
                        value = "`Jon`"
                    )
                    embed.set_footer(
                        text = self.bot.footer_text + ' | [2/7]',
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)

            # If they have an email, but not a first name registered
            elif not self.bot.data['new_members'][str(message.author.id)]['first_name']:
                # If there are any numbers in the message, the name is invalid
                invalid = any(char.isdigit() for char in message.content)
                if invalid:
                    # Invalid prompting
                    await message.add_reaction('❌')
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Invalid First Name",
                            description = 'Your name can only contain letters.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Invalid First Name",
                            description = 'Your name can only contain letters.',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.add_field(
                        name = "Example",
                        value = "`Jon`"
                    )
                    embed.set_footer(
                        text = self.bot.footer_text + ' | [2/7]',
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)
                else:
                    # Save the name
                    self.bot.data['new_members'][str(message.author.id)]['first_name'] = message.content.lower().capitalize()
                    save_data(self.bot.data_file, self.bot.data)

                    # Confirmation and prompt for next question
                    await message.add_reaction('✅')
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "First Name Registered",
                            description = 'Next, please tell us your last name.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "First Name Registered",
                            description = 'Next, please tell us your last name.',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.add_field(
                        name = "Example",
                        value = "`Smith`"
                    )
                    embed.set_footer(
                        text = self.bot.footer_text + ' | [3/7]',
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)

            # If they have an email and first name, but no last name
            elif not self.bot.data['new_members'][str(message.author.id)]['last_name']:
                # Check for numbers in the message
                invalid = any(char.isdigit() for char in message.content)
                if invalid:
                    # Invalid prompting
                    await message.add_reaction('❌')
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Invalid Last Name",
                            description = 'Your name can only contain letters.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Invalid Last Name",
                            description = 'Your name can only contain letters.',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.add_field(
                        name = "Example",
                        value = "`Smith`"
                    )
                    embed.set_footer(
                        text = self.bot.footer_text + ' | [3/7]',
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)
                else:
                    # Save last name
                    self.bot.data['new_members'][str(message.author.id)]['last_name'] = message.content.lower().capitalize()
                    save_data(self.bot.data_file, self.bot.data)

                    # Confirmation
                    await message.add_reaction('✅')

                    # If they do not yet have a school registered, prompt them to input a school
                    if not self.bot.data['new_members'][str(message.author.id)]['school']:
                        if self.bot.use_timestamp:
                            embed = discord.Embed(
                                title = "Last Name Registered",
                                description = 'Next, please tell us what school you attend.',
                                color = random.choice(self.bot.embed_colors),
                                timestamp = datetime.datetime.now(datetime.timezone.utc)
                            )
                        else:
                            embed = discord.Embed(
                                title = "Last Name Registered",
                                description = 'Next, please tell us what school you attend.',
                                color = random.choice(self.bot.embed_colors)
                            )
                        embed.add_field(
                            name = "Example",
                            value = "`NAU`"
                        )
                        embed.set_footer(
                            text = self.bot.footer_text + ' | [4/7]',
                            icon_url = self.bot.footer_icon
                        )
                        await message.author.send(embed = embed)
                    else:
                        # If they already have the school registered, first confirm last name submission
                        if self.bot.use_timestamp:
                            embed = discord.Embed(
                                title = "Last Name Registered",
                                color = random.choice(self.bot.embed_colors),
                                timestamp = datetime.datetime.now(datetime.timezone.utc)
                            )
                        else:
                            embed = discord.Embed(
                                title = "Last Name Registered",
                                color = random.choice(self.bot.embed_colors)
                            )
                        embed.set_footer(
                            text = self.bot.footer_text + ' | [4/7]',
                            icon_url = self.bot.footer_icon
                        )
                        await message.author.send(embed = embed)
                        # Then confirm school submission
                        if self.bot.use_timestamp:
                            embed = discord.Embed(
                                title = f"School Registered as `{self.bot.data['new_members'][str(message.author.id)]['school']}`",
                                description = 'Next, please tell us your major.',
                                color = random.choice(self.bot.embed_colors),
                                timestamp = datetime.datetime.now(datetime.timezone.utc)
                            )
                        else:
                            embed = discord.Embed(
                                title = f"School Registered as `{self.bot.data['new_members'][str(message.author.id)]['school']}`",
                                description = 'Next, please tell us your major.',
                                color = random.choice(self.bot.embed_colors)
                            )
                        embed.add_field(
                            name = "Example",
                            value = "`Computer Science`"
                        )
                        embed.set_footer(
                            text = self.bot.footer_text + ' | [5/7]',
                            icon_url = self.bot.footer_icon
                        )
                        await message.author.send(embed = embed)

            # If they do not yet have a school
            elif not self.bot.data['new_members'][str(message.author.id)]['school']:
                # Save the school input (this is open ended)
                self.bot.data['new_members'][str(message.author.id)]['school'] = message.content
                save_data(self.bot.data_file, self.bot.data)

                # Confirm school input and prompt for next question
                await message.add_reaction('✅')
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = "School Registered",
                        description = 'Next, please tell us your major.',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = "School Registered",
                        description = 'Next, please tell us your major.',
                        color = random.choice(self.bot.embed_colors)
                    )
                embed.add_field(
                    name = "Example",
                    value = "`Computer Science`"
                )
                embed.set_footer(
                    text = self.bot.footer_text + ' | [5/7]',
                    icon_url = self.bot.footer_icon
                )
                await message.author.send(embed = embed)

            # If they have everything prior but no major
            elif not self.bot.data['new_members'][str(message.author.id)]['major']:
                # Save the message content as their major
                self.bot.data['new_members'][str(message.author.id)]['major'] = message.content
                save_data(self.bot.data_file, self.bot.data)

                # Confirm major input and prompt for next question
                await message.add_reaction('✅')
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = "Major Registered",
                        description = 'Next, please tell us what platforms you play games on.',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = "Major Registered",
                        description = 'Next, please tell us what platforms you play games on.',
                        color = random.choice(self.bot.embed_colors)
                    )
                embed.add_field(
                    name = "Example",
                    value = "`PC, Xbox`"
                )
                embed.set_footer(
                    text = self.bot.footer_text + ' | [6/7]',
                    icon_url = self.bot.footer_icon
                )
                await message.author.send(embed = embed)

            # If they have everything prior but no game systems registered
            elif not self.bot.data['new_members'][str(message.author.id)]['game_system']:
                # Save game systems
                self.bot.data['new_members'][str(message.author.id)]['game_system'] = message.content
                save_data(self.bot.data_file, self.bot.data)

                # Confirm game system input and prompt for last question
                await message.add_reaction('✅')
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = "Platforms Registered",
                        description = 'Lastly, please tell us whether you are a Casual or Competitive player.',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = "Platforms Registered",
                        description = 'Lastly, please tell us whether you are a Casual or Competitive player.',
                        color = random.choice(self.bot.embed_colors)
                    )
                embed.add_field(
                    name = "Example",
                    value = "`Competitive`"
                )
                embed.set_footer(
                    text = self.bot.footer_text + ' | [7/7]',
                    icon_url = self.bot.footer_icon
                )
                await message.author.send(embed = embed)

            # If they have not answered the last question yet
            elif not self.bot.data['new_members'][str(message.author.id)]['type_of_player']:
                # This try statement will fail if the value the user entered is not either `casual` or `competitive`
                try:
                    # Because this line tries to load it to an enum.
                    player_type = PlayerType(message.content.lower()).name

                    # Save the player type, but do not write it to the file. In case something goes wrong,
                    # this would not execute again to save their data to the sheet and give them the roles
                    # unless the `type_of_player` field is None
                    self.bot.data['new_members'][str(message.author.id)]['type_of_player'] = player_type

                    # Get some the information necessary to add either the student of non-student role
                    guild = self.bot.get_guild(self.bot.guild_id)
                    student_role = guild.get_role(self.bot.student_role_id)
                    non_student_role = guild.get_role(self.bot.non_student_role_id)
                    member = guild.get_member(message.author.id)

                    # Add the role depending on the school name
                    if self.bot.data['new_members'][str(message.author.id)]['school'] == 'NAU' and not student_role in member.roles:
                        await member.add_roles(student_role)
                    elif not self.bot.data['new_members'][str(message.author.id)]['school'] == 'NAU' and not non_student_role in member.roles:
                        await member.add_roles(non_student_role)

                    # Create a connection to the Google Sheet specified in Resources/Sheets.py
                    sheet = Sheets(self.bot.credentials_file, self.bot.token_file)
                    sheet.append_user(self.bot.data['new_members'][str(message.author.id)])

                    # Final message for the user that they have completed their verification.
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Registration Complete!",
                            description = 'Welcome to NAU Esports!\n\nIf you are a Campus Faculty Member at NAU please contact an Officer.',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Registration Complete!",
                            description = 'Welcome to NAU Esports!\n\nIf you are a Campus Faculty Member at NAU please contact an Officer.',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.set_footer(
                        text = self.bot.footer_text,
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)

                    # Send a message to the logs channel that a user has finished going through verification
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "User Verified",
                            description = f"User {member.mention} has finished verification.",
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "User Verified",
                            description = f"User {member.mention} has finished verification.",
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.set_author(
                        name = member.name,
                        icon_url = member.avatar_url
                    )
                    embed.set_footer(
                        text = self.bot.footer_text,
                        icon_url = self.bot.footer_icon
                    )
                    for log in self.bot.logs_channels:
                        channel = self.bot.get_channel(log)
                        await channel.send(embed = embed)

                    # Delete this user and their data from `new_members` in memory and in file, that way we arent bloating data sizes unnecessarily.
                    del self.bot.data['new_members'][str(message.author.id)]
                    save_data(self.bot.data_file, self.bot.data)

                # If their input is not a valid player type
                except ValueError:
                    # Tell them its not valid and what valid answers are
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "Invalid Player Type",
                            description = 'Please specify `casual` or `competitive` (your answer must be one of those words).',
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "Invalid Player Type",
                            description = 'Please specify `casual` or `competitive` (your answer must be one of those words).',
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.add_field(
                        name = "Example",
                        value = "`competitive`"
                    )
                    embed.set_footer(
                        text = self.bot.footer_text + ' | [7/7]',
                        icon_url = self.bot.footer_icon
                    )
                    await message.author.send(embed = embed)

# Setup. Adds the actual cog to the bot.
def setup(bot):
    bot.add_cog(Welcome(bot))
