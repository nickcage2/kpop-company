import discord
from discord.ext import commands

class train(commands.Cog):
  def __init__(self, client, companies, create_embed, confirmation, make_trans):
    self.client = client
    self.companies = companies
    self.create_embed = create_embed
    self.confirmation = confirmation
    self.make_trans = make_trans

  @commands.command()
  async def train(self, ctx, target_trainee, name = ""):

    try:
      trainees = self.companies.find_one({'ceo': ctx.author.name})['trainees']
    except:
      await ctx.send(embed = self.create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
      return

    bucks = self.companies.find_one({'ceo': ctx.author.name})['money']
    
    target_trainee +=  name

    target_trainee = target_trainee.lower().replace(" ", "")
    trainees_dict = {}
    index = 0
    groups = []
    repeat_groups = []
    group_index = 0

    x = []
    for trainee in trainees.keys():
      groups.append(trainee[trainee.index('(')+1:-1])
      x.append(trainee.lower()[:trainee.index(" (")].replace(" ", ""))
      trainees_dict[trainee.lower().replace(" ", "")] = trainees[trainee]

    if target_trainee not in x:
      await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have a trainee by this name in your company.', ctx.author.display_name, ctx.author.avatar_url))

    if target_trainee in x:
      count = 0
      for trainee in trainees_dict:
        if trainee[:trainee.index("(")] == target_trainee:
          repeat_groups.append(groups[list(trainees_dict.keys()).index(trainee)])
          count+= 1
      
      if count > 1:
        emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        
        temp = 0
        fields = []

        name = target_trainee[0:1] + target_trainee[1:]
        value = emoji_list[0] + " " + repeat_groups[0]
        
        emoji_count = 1
        temp = 1
        
        while temp < count:
          value+= '\n' + emoji_list[emoji_count] + " " + repeat_groups[temp]

          temp+=1
          emoji_count+= 1

        emoji_count = 0

        fields.append({
          'name': name,
          'value': value,
          'inline': False
        })
        
        msg = await ctx.send(embed = self.create_embed('Unoriginal', 'You have multiple trainees with the same name, who did you mean?', ctx.author.display_name, ctx.author.avatar_url, fields))
        
        
        while count > 0:
          await msg.add_reaction(emoji_list[emoji_count])

          count-= 1
          emoji_count+= 1
        
        def filter(reaction, user):
          
          if reaction.emoji in emoji_list and user.id == ctx.author.id:
            return True

          return False
          
        try:
          reactions = await self.client.wait_for('reaction_add', check = filter, timeout = 30)
        except:
          await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return

        for emoji in emoji_list:
          if reactions[0].emoji == emoji:
            group_index = emoji_list.index(emoji)

      group = repeat_groups[group_index]

      key = target_trainee + '(' + group.lower().replace(" ", "") + ')'
      index = list(trainees_dict.keys()).index(key)
      person = list(trainees.keys())[index]
      
      
      temp_trainees = trainees
      temp_trainees.pop(person)

      level = trainees_dict[key]
      dollars = 50 * level + 50

      conf = await self.confirmation(dollars, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

      if conf == True:
        
        bucks -= dollars

        query = {'ceo': ctx.author.name}
        update = {'$set': {'money': bucks}}
        self.companies.update_one(query, update)

        self.make_trans('-', dollars, ctx.author.name)

        level += 1

        temp_trainees[person] = level
        
        update = {'$set': {'trainees': temp_trainees}}
        self.companies.update_one(query, update)

        await ctx.send(embed = self.create_embed('Let\'s Power Up', person + ' has moved up a level.', ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Removed from Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}]))