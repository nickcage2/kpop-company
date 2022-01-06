import discord
from discord.ext import commands

class daily(commands.Cog):
  def __init__(self, client, create_embed, companies, make_trans):
    self.client = client
    self.create_embed = create_embed
    self.companies = companies
    self.make_trans = make_trans

  @commands.command()
  async def daily(self, ctx):
    try:
      personsCompany = self.companies.find_one({'ceo': ctx.author.name})
      if ctx.author.name in personsCompany.values():     
        bucks = self.companies.find_one({'ceo': ctx.author.name})['money']
        
        dollars = 1000
        bucks += dollars

        query = {'ceo': ctx.author.name}
        update = {'$set': {'money': bucks}}
        self.companies.update_one(query, update)

        self.make_trans('+', dollars, ctx.author.name)

        await ctx.send(embed = self.create_embed('Good in the World','Someone gave you some K-Bucks out of the kindness in their heart.',ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Added to Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}]))

    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))