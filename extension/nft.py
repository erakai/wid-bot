"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Infrastructure for the Widmark Clan crypto branch NFT exchange
"""

import config
import discord
from discord.ext import commands
from util.smart_contract import ensure_wallet, mint_nft, nft, show, own_nft

class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    nft_group = discord.SlashCommandGroup('nft', 'Commands related to NFTs', guild_ids=[config.GUILD_ID])

    @nft_group.command(description="Retrieve a user's NFT wallet.")
    async def wallet(self,
        ctx: discord.ApplicationContext,
        user:  discord.Member=None, nft_id: int=None):
        await ctx.defer()
        
        if not user: user = ctx.author

        user_wallet = ensure_wallet(user)

        if(user_wallet):
            nft = user_wallet[(nft_id or -1)% len(user_wallet)]
            embed = discord.Embed(title=f"{user.nick or user.name}\'s latest NFT!", description=f'Chance to get: {nft["rarity"]}%')
            file = show(nft)
            embed.set_image(url=f'attachment://{nft["address"]}.png')
            embed.set_footer(text=str(nft["address"]))
            await ctx.respond(embed=embed, file=file)

        else:
            await ctx.respond(f'{user.nick or user.name} has no NFTs!')

    @nft_group.command(description="Mint an NFT on the Widcoin blockchain.")
    async def mint(self,
        ctx: discord.ApplicationContext):
        await ctx.defer()
        try:
            nft = mint_nft()
            user = ctx.author

            own_nft(user, nft)

            embed = discord.Embed(title=f"{user.nick or user.name} just minted a new NFT!", description=f'Chance to get: {nft["rarity"]}%')
            file = show(nft)
            embed.set_image(url=f'attachment://{nft["address"]}.png')
            embed.set_footer(text=str(nft["address"]))
            await ctx.respond(embed=embed, file=file)
        except Exception as e:
            print(e)
            await ctx.respond('A skill issue prevented the minting of an NFT')


def setup(bot):
    bot.add_cog(Crypto(bot))