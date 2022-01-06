import discord
from discord.ext import commands

class help(commands.Cog):
  def __init__(self, client, create_embed):
    self.client = client
    self.create_embed = create_embed

  @commands.command()
  async def help(self, ctx):
    fields = [{
      'name': '?startup',
      'value': 'Start your own company.',
      'inline': True
    }, {
      'name': '?daily',
      'value': 'Recieve your daily K-Bucks.',
      'inline': True
    }, {
      'name': '\u200b',
      'value': '\u200b',
      'inline': True
    }, {
      'name': '?account',
      'value': 'Check your account balance and recent transactions.',
      'inline': True
    }, {
      'name': '?audition',
      'value': 'Host an audition and choose someone to join your company as a trainee.',
      'inline': True
    }, {
      'name': '\u200b',
      'value': '\u200b',
      'inline': True
    }, {
      'name': '?trainees',
      'value': 'Check a list of trainees in your company.',
      'inline': True
    }, {
      'name': '?train (trainee name)',
      'value': 'Train a trainee and put them on the next level.',
      'inline': True
    }, {
      'name': '\u200b',
      'value': '\u200b',
      'inline': True
    }]

    title = ""
    desc = ""
    
    await ctx.send(embed = self.create_embed(title, desc, ctx.author.display_name, ctx.author.avatar_url, fields))