import discord
from discord.ext import commands
from commands.debut.actordebut import actordebut
from commands.debut.soloistdebut import soloistdebut

class debut(commands.Cog):
  def __init__(self, client, companies, create_embed, talents, confirmation, make_trans):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed
    self.talents = talents
    self.confirmation = confirmation
    self.make_trans = make_trans

  @commands.command()
  async def debut(self, ctx):
    
    try:
      trainees = self.companies.find_one({'ceo': ctx.author.name})['trainees']
    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
      return

    message = await ctx.send(embed = self.create_embed('Choose Act', 'What kind of act do you want to debut? \n\n 🎬 Actor \n\n 💃 Soloist \n\n 👯 Duo \n\n 👩‍👩‍👧‍👧 Group \n\n 🎸 Band', ctx.author.display_name, ctx.author.avatar_url))

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
    recognition = self.companies.find_one({'ceo': ctx.author.name})['recognition']

    #actor
    if reaction[0].emoji == '🎬':
      await actordebut(self, ctx, message, x, lower_x, trainees, recognition)
      
    elif  reaction[0].emoji == '💃':
      await soloistdebut(self, ctx, message, x, lower_x, trainees, recognition)





#####################################################

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

    msg = await ctx.send('**' + str(len(tal_list)) + ' Trainees' + '**')
    
    bot = msg.guild.get_member(924845351440105553)

    def filter(reaction, user):
      if (reaction.emoji == '▶️' or reaction.emoji == '◀️' or reaction.emoji == '🔒') and user.id == ctx.author.id and reaction.message == msg:
        return True
      return False
    
    i = 0
    max = 10
    num = 1
    if len(trainees10) == 1 and len(trainees10[0]) < 9:
      max = len(trainees10[0])

    

    while i <= cap:
      
      
      desc = ''

      w = 0
      
      while w < max:
        
        desc+= str(levels10[i][w]) + " ⭐ : " + trainees10[i][w] + "\n\n"
    
        w+= 1
        
      desc = desc[:-1]

      await msg.edit(embed = self.create_embed('Your Trainees:', 'Please press the "🔒" reaction when you\'re ready and then type the name of the person you wish to debut.\n\n' + desc, ctx.author.display_name, ctx.author.avatar_url).set_footer(text = str(num) + "/" + str(len(trainees10))))

      if i == 0:
        if max == 10 and len(trainees10) > 1:
          await msg.add_reaction('◀️')
          await msg.add_reaction('🔒')
          await msg.add_reaction('▶️')
          
          try:
            reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 120)
          except:
            return

          if reaction[0].emoji == '▶️':
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            i+= 1
            num+=1
            
            if i == len(trainees10) - 1:
              max = len(trainees10[len(trainees10)-1])
              continue
            continue
            
          elif reaction[0].emoji == '🔒':
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            
            i = len(trainees10)
            
            await msg.remove_reaction('🔒', bot)
            await msg.remove_reaction('▶️', bot)
            await msg.remove_reaction('◀️', bot)
            continue
        else:

          i+= 1
          continue
        
      
      elif i > 0 and i < len(trainees10) - 1:
        
        if len(trainees10) > i:

          try:
            reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 120)
          except:
            return
            
          if reaction[0].emoji == '▶️':
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            i+= 1
            num+= 1
            if i == len(trainees10) - 1:
              max = len(trainees10[len(trainees10)-1])
              continue
            continue

          elif reaction[0].emoji == '🔒':

            print(msg.guild.members)
            i = len(trainees10)
            await msg.remove_reaction('🔒', bot)
            await msg.remove_reaction('▶️', bot)
            await msg.remove_reaction('◀️', bot)
            continue

          else:
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            i-= 1
            num-= 1
            continue
        else:
          i+= 1
          continue
        
      elif i == len(trainees10) - 1:

        try:
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 120)
        except:
          return

        if reaction[0].emoji == '◀️':
          await msg.remove_reaction(reaction[0].emoji, ctx.author)
          num-= 1
          i-= 1
          max = 10
          continue
        elif reaction[0].emoji == '🔒':
          i = len(trainees10)
          await msg.remove_reaction('🔒', bot)
          await msg.remove_reaction('▶️', bot)
          await msg.remove_reaction('◀️', bot)
          continue