import discord
from discord.ext import commands

class debut(commands.Cog):
  def __init__(self, client, companies, create_embed, talents):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed
    self.talents = talents

  @commands.command()
  async def debut(self, ctx):

    try:
      trainees = self.companies.find_one({'ceo': ctx.author.name})['trainees']
    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
      return

    message = await ctx.send(embed = self.create_embed('__title empty__', 'What kind of act do you want to debut? \n\n 🎬 Actor \n\n 💃 Soloist \n\n 👯 Duo \n\n 👩‍👩‍👧‍👧 Group \n\n 🎸 Band', ctx.author.display_name, ctx.author.avatar_url))

    await message.add_reaction('🎬')
    await message.add_reaction('💃')
    await message.add_reaction('👯')
    await message.add_reaction('👩‍👩‍👧‍👧')
    await message.add_reaction('🎸')

    emojis = ['🎬', '💃', '👯', '👩‍👩‍👧‍👧', '🎸']

    def filter(reaction, user):
      if reaction.emoji in emojis and user.id == ctx.author.id:
        return True
      return False

    try:
      reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 30)

    except:
      await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
      return

    x = {}
    lower_x = {}

    #actor
    if reaction[0].emoji == '🎬':
      await message.delete()
      
      actors = self.companies.find_one({'ceo': ctx.author.name})['actors']
      
      for trainee in trainees:
        if 'Acting' in self.talents[trainee]:
          x[trainee] = trainees[trainee]
          lower_x[trainee.lower()] = trainees[trainee]

      if len(x) == 0:
        await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have any trainees that can debut as an actor.', ctx.author.display_name, ctx.author.avatar_url))
        return
      
      await self.trainees_list(ctx, x)
      
      def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
        
      message = await self.client.wait_for('message', timeout=30, check=check)

      inp = message.content.lower()

      if inp in list(lower_x.keys()):
        name = list(x.keys())[list(lower_x.keys()).index(inp)]
        actors[name] = list(x.values())[list(lower_x.keys()).index(inp)]

        query = {'ceo': ctx.author.name}
        update = {'$set': {'actors': actors}}
        self.companies.update_one(query, update)

        trainees.pop(name)

        update = {'$set': {'trainees': trainees}}
        self.companies.update_one(query, update)
      return

    #solist
    if reaction[0].emoji == '💃':
      await ctx.send('You\'re debuting a soloist.')

    #duo
    if reaction[0].emoji == '👯':
      await ctx.send('You\'re debuting a duo.')

    #group
    if reaction[0].emoji == '👩‍👩‍👧‍👧':
      await ctx.send('You\'re debuting a group.')

    #band
    if reaction[0].emoji == '🎸':
      await ctx.send('You\'re debuting a band.')







########################################################

  async def trainees_list(self, ctx, tal_list):

    cap = len(tal_list) / 10
    index = 0
    trainees10 = []
    levels10 = []

    if len(tal_list) == 0:
      await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have any trainees in your company.', ctx.author.display_name, ctx.author.avatar_url))

    while index < cap:
      ten = slice(index*10, index*10+10)
      trainees10.append(list(tal_list.keys())[ten])
      levels10.append(list(tal_list.values())[ten])
      index+= 1
    
    def filter(reaction, user):
          if (reaction.emoji == '▶️' or reaction.emoji == '◀️') and user.id == ctx.author.id:
            return True
          return False
    
    i = 0
    max = 10
    while i <= cap:
      desc = ''
      w = 0
      
      while w < max:
        
        desc+= trainees10[i][w] + " : " + str(levels10[i][w]) + " ⭐\n\n"
        w+= 1
        
      desc = desc[:-1]

      msg = await ctx.send(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      if i == 0:
        await msg.add_reaction('▶️')

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
        except:
          return

        if reaction[0].emoji == '▶️':
          await msg.delete()
          i+= 1
          
          if i == len(trainees10) - 1:
            max = len(trainees10[len(trainees10)-1])

          continue
      
      elif i > 0 and i < len(trainees10) - 1:
        await msg.add_reaction('◀️')
        await msg.add_reaction('▶️')

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
        except:
          return
          
        if reaction[0].emoji == '▶️':
          await msg.delete()
          i+= 1

          if i == len(trainees10) - 1:
            max = len(trainees10[len(trainees10)-1])
            
          continue
        else:
          await msg.delete()
          i-= 1
          continue
        
      elif i == len(trainees10) - 1:
        await msg.add_reaction('◀️')

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
        except:
          return

        if reaction[0].emoji == '◀️':
          await msg.delete()
          i-= 1
          max = 10
          continue   