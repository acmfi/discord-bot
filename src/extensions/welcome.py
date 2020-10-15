import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('src/static/mensaje_bienvenida.txt', 'r') as f:
            self.welcome_message = f.read()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Sends a greeting message privately when a new user joins the server

        Args: 
            member(discord.Member): the very same member who joined the server
        """
        embed_message = discord.Embed(
            colour=discord.Colour.gold(),
            description=self.welcome_message
        )
        embed_message.set_author(name=f"From ACM to {member.display_name}: ",
                                 icon_url='https://gitam.edu/assets/images/chapters/acm_logo.png'),
        # set_image pone las fotos de abajo
        embed_message.set_image(
            url='https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif'),
        embed_message.set_thumbnail(
            url='https://pbs.twimg.com/profile_images/511946781509169152/ilKrXwzp_400x400.png'),
        embed_message.set_footer(
            text='\"Advancing Computing as a Science & Profession\"')

        await member.send(embed=embed_message)


def setup(bot):
    bot.add_cog(Welcome(bot))
