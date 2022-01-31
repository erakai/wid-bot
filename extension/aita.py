"""
Author: Kai (Not Eric (Not Lance (Not Russell)))
"""

import config
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from discord.commands import slash_command
from util.reddit_scraper import get_aita

class AitaView(View):
    def __init__(self, post):
        super().__init__()
        self.post = post

    @discord.ui.button(label='YTA', style=ButtonStyle.red)
    async def yta_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response('YTA', self.post["sdec"], self.post["decision"]), ephemeral=True)

    @discord.ui.button(label='NTA', style=ButtonStyle.green)
    async def nta_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response('NTA', self.post["sdec"], self.post["decision"]), ephemeral=True)

    @discord.ui.button(label='ESH', style=ButtonStyle.blurple)
    async def esh_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response('ESH', self.post["sdec"], self.post["decision"]), ephemeral=True)

    @discord.ui.button(label='INFO', style=ButtonStyle.grey)
    async def info_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response('INFO', self.post["sdec"], self.post["decision"]), ephemeral=True)

    def get_response(self, guess, decision, text):
        if (decision == "None"): return "Unable to locate a top comment with a valid decision. {text}"
        if (guess == decision): return f"{guess} was **correct**! {text}"
        return f"{guess} was **incorrect**! {text}"

class AITA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description="Are they the Asshole?")
    async def aita(self, ctx: discord.ApplicationContext):
        try:
            # holy fucking shi ti commands without this response the entire thing beraks cause if you dont respond in 3 seconds the slash commands falls through and because i have intractions on the butotns the error i got is "unkown interaction" which is incredibly uselessd adn tells you nothing so the only solution is to find a stackoverflow post about thie error in ajvascript with 2 upvotes and see somethign taht says that you need a response immedaitely so discord doesnt berak it 
            await ctx.defer()
            post = await get_aita()
        except Exception as e:
            return await ctx.respond('Unable to find an asshole. Try the mirror.', ephemeral=True)  
        
        embed = discord.Embed(
            title=post['title'],
            url=f"https://reddit.com{post['link']}",
            description=post['desc']
        )
        embed.set_footer(text=f"{post['upvotes']} upvotes")
        embed.set_author(name=post['author'])

        view = AitaView(post) 
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(AITA(bot))