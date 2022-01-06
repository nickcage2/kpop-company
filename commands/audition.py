import discord
from discord.ext import commands
import random

class audition(commands.Cog):
  def __init__(self, client, companies, create_embed, confirmation, talents, make_trans, idol_images):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed
    self.confirmation = confirmation
    self.talents = talents
    self.make_trans = make_trans
    self.idol_images = idol_images

  @commands.command()
  async def audition(self, ctx):
    try:
      personsCompany = self.companies.find_one({'ceo': ctx.author.name})
      if ctx.author.name in personsCompany.values():
        ceo_trainees = self.companies.find_one({'ceo': ctx.author.name})['trainees']

        true_idols = self.companies.find_one({'ceo': ctx.author.name})['idols']
        msg2 = 'There\'s no one left that wants to join your company.'
        none_embed = self.create_embed('Fiddlesticks', msg2, ctx.author.display_name, ctx.author.avatar_url)

        num_to_select = 3
        
        if len(true_idols) == 2:
          num_to_select = 2
        elif len(true_idols) == 1:
          num_to_select = 1
        if len(true_idols) == 0:
          await ctx.send(embed = none_embed)
          return

        conf = await self.confirmation(150, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

        if conf == True:

          bucks = self.companies.find_one({'ceo': ctx.author.name})['money']

          author_idols = random.sample(true_idols, num_to_select)

          iad = []
          idol_emojis = ['🌸', '🍑', '🦋']

          #loop through author_idols
          for idol in author_idols:
            temp_iat = {
              'name': idol_emojis[author_idols.index(idol)] + idol,
              'value': ', '.join(self.talents[idol]),
              'inline': True
            }
            iad.append(temp_iat)

          msg = 'Here\'s a list of the people that auditioned. Choose one to take in as a trainee.'
          
          idol_embed = self.create_embed('Auditionees', msg, ctx.author.display_name, ctx.author.avatar_url, iad)
          
          message = await ctx.send(embed = idol_embed)
          
          for idol in iad:
            await message.add_reaction(idol_emojis[iad.index(idol)])

          def filter(reaction, user):
            
            if reaction.emoji in idol_emojis and user.id == ctx.author.id:
              return True

            return False
            
          try:
            reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 30)
          
          except:
            await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
            return
        
          my_trainee = ''
          for idol in iad:
            if reaction[0].emoji == idol_emojis[iad.index(idol)]:
              my_trainee = iad[iad.index(idol)]['name'][1:]

          dollars = 150
          bucks -= dollars

          query = {'ceo': ctx.author.name}
          update = {'$set': {'money': bucks}}
          self.companies.update_one(query, update)

          self.make_trans('-', dollars, ctx.author.name)

          query = {'ceo': ctx.author.name}
          
          ceo_trainees[my_trainee] = 0

          update = {'$set': {'trainees': ceo_trainees}}
          self.companies.update_one(query, update)

          true_idols.remove(my_trainee)

          update = {'$set': {'idols': true_idols}}
          self.companies.update_one(query, update)


          await message.delete()

          new_msg = my_trainee + ' has joined your company as a trainee.'
          embed1 = self.create_embed('New Trainee', new_msg, ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Removed from Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}])

          embed1.set_thumbnail(url=self.idol_images[my_trainee])

          await ctx.send(embed = embed1)

    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))