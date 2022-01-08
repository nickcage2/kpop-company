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

    cap = len(trainees) / 10
    index = 0
    trainees10 = []
    levels10 = []

    if len(trainees) == 0:
      await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have any trainees in your company.', ctx.author.display_name, ctx.author.avatar_url))

    while index < cap:
      ten = slice(index*10, index*10+10)
      trainees10.append(list(trainees.keys())[ten])
      levels10.append(list(trainees.values())[ten])
      index+= 1

    msg = await ctx.send('**' + str(len(trainees)) + ' Trainees' + '**')
    def filter(reaction, user):
          if (reaction.emoji == '▶️' or reaction.emoji == '◀️') and user.id == ctx.author.id and reaction.message == msg:
            return True
          return False
    
    i = 0
    max = 10
    
    if len(trainees10) == 1 and len(trainees10[0]) < 9:
      max = len(trainees10[0])

    
    num = 1
    while i <= cap:
      
      desc = ''
      w = 0
      
      while w < max:
        
        desc+= str(levels10[i][w]) + " ⭐  :  " + trainees10[i][w] + "\n\n"
        w+= 1
        
      desc = desc[:-1]
    
      await msg.edit(embed = self.create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url).set_footer(text='Page: ' + str(num) + '/' + str(len(trainees10))))

      if i == 0:
        if max == 10 and len(trainees10) > 1:
          await msg.add_reaction('◀️')
          await msg.add_reaction('▶️')

          try:
            reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
          except:
            return


          if reaction[0].emoji == '▶️':
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            i+= 1
            num += 1
            if i == len(trainees10) - 1:
              max = len(trainees10[len(trainees10)-1])
              continue
            continue
        else:
          i+= 1
          continue
        
      
      elif i > 0 and i < len(trainees10) - 1:
        if len(trainees10) > i:

          try:
            reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
          except:
            return
            
          if reaction[0].emoji == '▶️':
            await msg.remove_reaction(reaction[0].emoji, ctx.author)
            i+= 1
            num +=1
            if i == len(trainees10) - 1:
              max = len(trainees10[len(trainees10)-1])
              continue
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
          reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
        except:
          return

        if reaction[0].emoji == '◀️':
          await msg.remove_reaction(reaction[0].emoji, ctx.author)
          i-= 1
          num-= 1
          max = 10
          continue   