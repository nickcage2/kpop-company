import discord
from discord.ext import commands
import os

class updatecompanies(commands.Cog):
  def __init__(self, client, companies, idols, create_embed, my_id):
    self.client = client
    self.companies = companies
    self.idols = idols
    self.create_embed = create_embed
    self.my_id = my_id

  @commands.command()
  async def updatecompanies(self, ctx):
    count = 0
    while count < 2:
      if str(ctx.author.id) == str(self.my_id):
        for company in self.companies.find({}):
          update = {'$set': {'idols': self.idols}}
          self.companies.update_one(company, update)
          new_idols = self.idols

          for trainee in company['employees']:
            if trainee in new_idols:
              new_idols.remove(trainee)
              update = {'$set': {'idols': new_idols}}

          self.companies.update_one(company, update)

      else:
        await ctx.send(embed = self.create_embed ('⛔', 'You do not have permission to access this command.', ctx.author.display_name, ctx.author.avatar_url))
        return
      count += 1

    await ctx.send(embed = self.create_embed('Updated', 'The list of idols has been updated.', ctx.author.display_name, ctx.author.avatar_url))