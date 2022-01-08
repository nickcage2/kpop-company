from discord.ext import commands
import time

class collect(commands.Cog):
  def __init__(self, client, companies, create_embed, make_trans):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed
    self.make_trans = make_trans

  @commands.command()
  async def collect(self, ctx):
    promotion = self.companies.find_one({'ceo': ctx.author.name})['promotion']

    k = []
    name = []
    m_int = []
    total = 0

    n = []

    if len(promotion) == 0:
      await ctx.send('You don\'t have any promotions to collect from.')
      return

    for collection in promotion:
      if promotion[collection][0] <= int(time.time() / 60):
        m_int.append(int(promotion[collection][1]))
        
        name.append(list(promotion.keys())[list(promotion.keys()).index(collection)])

        person_and_profit = list(promotion.keys())[list(promotion.keys()).index(collection)] + " : " + str(int(promotion[collection][1])) + " K-Bucks"

        k.append(person_and_profit)
      else:
        hour = int((promotion[collection][0] - int(time.time() / 60)) / 60)
        minute = (int(promotion[collection][0]) - int(time.time() / 60)) % 60

        hr_name = ' Hrs '
        min_name = ' Mins'

        if hour == 1:
          hr_name = ' Hr '

        if minute == 1:
          min_name = ' Min'
          
        n.append(list(promotion.keys())[list(promotion.keys()).index(collection)] + " : " + str(hour) + hr_name + str(minute) + min_name)

    if len(name) == 0:
      mess = '\n\n'.join(n)
      await ctx.send(embed = self.create_embed('What You Waiting For', mess, ctx.author.display_name, ctx.author.avatar_url))
      return

    for integer in m_int:
      total += integer

    msg = '\n\n'.join(k)
        
    message = await ctx.send(embed = self.create_embed('Promotions are Finished', msg, ctx.author.display_name, ctx.author.avatar_url))

    await message.add_reaction('💎')

    def filter(reaction, user):
      if reaction.emoji == '💎' and user.id == ctx.author.id:
        return True
      return False

    try:
      reaction = await self.client.wait_for('reaction_add', check = filter, timeout = 300)
    except:
      return
      
    if reaction[0].emoji == '💎':
      await message.delete()
      
      bucks = self.companies.find_one({'ceo': ctx.author.name})['money']

      bucks += total

      query = {'ceo': ctx.author.name}
      update = {'$set': {'money': bucks}}
      self.companies.update_one(query, update)

      self.make_trans('+', total, ctx.author.name)

      for person in name:
        dickt = promotion
        dickt.pop(person)

      update = {'$set': {'promotion': dickt}}
      self.companies.update_one(query, update)

      await ctx.send(embed = self.create_embed('Collected', str(total) + ' K-Bucks were added to your account.', ctx.author.display_name, ctx.author.avatar_url))
      