import discord
from discord.ext import commands

class startup(commands.Cog):
  def __init__(self, client, create_embed, idols, companies):
    self.client = client
    self.create_embed = create_embed
    self.idols = idols
    self.companies = companies

  @commands.command()
  async def startup(self, ctx):
    try:
      personsCompany = self.companies.find_one({'ceo': ctx.author.name})
      if ctx.author.name in personsCompany.values():
        await ctx.send(embed = self.create_embed('No Monopolies', 'You already own a company.', ctx.author.display_name, ctx.author.avatar_url))
      
    except:
      company = {
        'ceo': ctx.author.name,
        'money': 0,
        'recognition': 0,
        'trainees': {},
        'employees': [],
        'idols': self.idols,
        'recent_trans': [],
        'actors': {},
        'groups': {},
        'duos': {},
        'soloists': {},
        'bands': {},
        'promotion': {}
      }

      self.companies.insert_one(company).inserted_id
      
      await ctx.send(embed = self.create_embed('Taking Off', 'Quite the entrepreneur, you are! Welcome to your new entertainment company, CEO ' + ctx.author.name + '.', ctx.author.display_name, ctx.author.avatar_url))