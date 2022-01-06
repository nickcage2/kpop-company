import discord
from discord.ext import commands

class trainees(commands.Cog):
  def __init__(self, client, companies, create_embed):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed

  @commands.command()
  async def trainees(self, ctx):

    try:
      trainees = self.companies.find_one({'ceo': ctx.author.name})['trainees']
    
    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
      return

    high = len(trainees.keys()) - 1

    index = 1
    last = 10
    
    
    if len(trainees) == 0:
      await ctx.send(embed = self.create_embed('No Trainees', 'You don\'t have any trainees in your company.', ctx.author.display_name, ctx.author.avatar_url))

      return
      
    desc = list(trainees.keys())[0] + ' : ' + str(list(trainees.values())[0]) + ' ⭐'

    

    if len(trainees) == 1:
      msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      return

    while index < last:

      desc+= '\n\n' + list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'

      if index == high and high < 10:
        msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

        return

      elif index % 10 == 9 and index >= 10:
        msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

        await msg.add_reaction('◀️')
        await msg.add_reaction('▶️')

        def filter(reaction, user):
          if (reaction.emoji == '▶️' or reaction.emoji == '◀️') and user.id == ctx.author.id:
            return True
          return False

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
        except:
          await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return

        if reaction[0].emoji == '▶️':
          await msg.delete()

          if last + 10 > high:
            last = high
          else:
            last += 10

          index += 1
          desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'

        elif reaction[0].emoji == '◀️':
          await msg.delete()

          index -= 9
          last -= 10
          index += 1
          desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'

      elif index % 10 == 9 and index < 10:
        msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

        await msg.add_reaction('▶️')

        def filter(reaction, user):
          if reaction.emoji == '▶️' and user.id == ctx.author.id:
            return True
          return False

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)

          if reaction[0].emoji == '▶️':
            await msg.delete()

            index += 1
            desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
            if last + 10 > high:
              last = high
            else:
              last += 10

        except:
          await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return

      elif index == high:
        msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

        await msg.add_reaction('◀️')

        def filter(reaction, user):
          if reaction.emoji == '◀️' and user.id == ctx.author.id:
            return True
          return False
        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)

          if reaction[0].emoji == '◀️':
            await msg.delete()

            index -= 9
            last -= 10
            index += 1
            desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
        except:
          await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return

      index+= 1

      if index > high:
        index -= 1
        msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

        await msg.add_reaction('◀️')

        def filter(reaction, user):
          if reaction.emoji == '◀️' and user.id == ctx.author.id:
            return True
          return False
        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)

          if reaction[0].emoji == '◀️':
            await msg.delete()

            index -= 9
            last -= high % 10
            index += 1
            desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
        except:
          await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return