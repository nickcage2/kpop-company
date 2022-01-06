import discord
from discord.ext import commands

class account(commands.Cog):
  def __init__(self, client, companies, create_embed):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed

  @commands.command()
  async def account(self, ctx):
    try:
      personsCompany = self.companies.find_one({'ceo': ctx.author.name})
      if ctx.author.name in personsCompany.values():
        recent = self.companies.find_one({'ceo': ctx.author.name})['recent_trans']

        bucks = self.companies.find_one({'ceo': ctx.author.name})['money']

        if bucks == 0:
          await ctx.send(embed = self.create_embed('Account', str(bucks) + ' K-Bucks', ctx.author.display_name, ctx.author.avatar_url))
        if bucks > 0:
          await ctx.send(embed = self.create_embed('Account', str(bucks) + ' K-Bucks', ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Recent Transactions', 'value': "\n".join(recent), 'inline': True}]))

    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))