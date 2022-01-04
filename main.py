import discord
import os
from discord.ext import commands
import random
from pymongo import MongoClient

uri = os.environ['mongodb_uri']
mongoDB = MongoClient(uri)

db = mongoDB.companiesDB

try:
  mongoDB.server_info()
  print('Connected to DB')
except Exception: 
  print('Can\'t connect to DB')
  
companies = db.companies

client = commands.Bot(command_prefix = '?')

client.remove_command('help')

idols = []
talents = {}
idol_images = {}

file = open('./idols.txt', 'r')
lines = file.readlines()

for line in lines:
  line = line.replace('\n','')
  idol_talents = line.split(' / ')
  name = idol_talents[0]
  idol_images[name] = idol_talents[1]
  del idol_talents[0]
  del idol_talents[0]
  idols.append(name)
  talents[name] = idol_talents[0].split(' ')

for company in companies.find({}):
  update = {'$set': {'idols': idols}}
  companies.update_one(company, update)
  new_idols = idols
  
  for trainee in company['trainees'].keys():
    new_idols.remove(trainee)
    update = {'$set': {'idols': new_idols}}

  companies.update_one(company, update)


@client.event
async def on_ready():
  print('--------------')
  print('Bot is online.')
  print('--------------')
  
def create_embed(title, desc, display_name, avatar_url, fields = []): 
  #[{'name':, 'value':, 'inline': True},{},{},etc]
  #ctx.author.display_name, ctx.author.avatar_url,
  embed = discord.Embed(title=title, description=desc,color=0xFF9C9C).set_author(name=display_name, icon_url=avatar_url)

  for field in fields:
    embed.add_field(
      name = field['name'],
      value = field['value'],
      inline = field['inline'])

  return embed

async def confirmation(dollars, name, avatar_url, send, author_id):
  #ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id
  con_msg = 'Doing this will cost ' + str(dollars) + ' K-Bucks. Do you wish to continue?'
  con_embed = create_embed('Confirm', con_msg, name, avatar_url, [{'name': '✅ Yes', 'value': 'Confirms the transaction.', 'inline': True}, {'name': '⛔ No', 'value': 'Cancels the transaction.', 'inline': True}])

  confirm = await send(embed=con_embed)
  await confirm.add_reaction('✅')
  await confirm.add_reaction('⛔')
  
  def emoji(reaction, user):
    if reaction.emoji == '⛔' or reaction.emoji == '✅':
      if user.id == author_id:
        return True
    return False
    
  try:
    emojis = await client.wait_for('reaction_add', check= emoji, timeout = 30)
  except:
    await send(embed = create_embed('Tick Tock', 'You ran out of time.', name, avatar_url))
    return 
    
  if emojis[0].emoji == '⛔':
    await confirm.delete()
    await send(embed=create_embed('Cancelled', 'The audition was cancelled.', name, avatar_url))
    return False
    
  if emojis[0].emoji == '✅':
    await confirm.delete()
    if dollars > companies.find_one({'ceo': name})['money']:
      msg = 'You don\'t have enough K-Bucks to perform this transaction.'
      broke_embed = create_embed ('You\'re Kinda Broke', msg, name, avatar_url)
      
      await send(embed=broke_embed)
      
      return False

    return True


def make_trans(addorsub, money, author): 
  # is either '+' or '-' 
  #money is integer 
  #author is ctx.author.name
  recent = companies.find_one({'ceo': author})['recent_trans']

  recent.insert(0, addorsub + ' ' + str(money))

  query = {'ceo': author}
  update = {'$set': {'recent_trans': recent}}
  companies.update_one(query, update)

@client.command()
async def startup(ctx):
  try:
    personsCompany = companies.find_one({'ceo': ctx.author.name})
    if ctx.author.name in personsCompany.values():
      await ctx.send(embed = create_embed('No Monopolies', 'You already own a company.', ctx.author.display_name, ctx.author.avatar_url))
      
  except:
    company = {
      'ceo': ctx.author.name,
      'money': 0,
      'trainees': {},
      'idols': idols,
      'recent_trans': []
    }

    companies.insert_one(company).inserted_id
    
    await ctx.send(embed = create_embed('Taking Off', 'Quite the entrepreneur, you are! Welcome to your new entertainment company, CEO ' + ctx.author.name + '.', ctx.author.display_name, ctx.author.avatar_url))

@client.command()
async def daily(ctx):
  try:
    personsCompany = companies.find_one({'ceo': ctx.author.name})
    if ctx.author.name in personsCompany.values():     
      bucks = companies.find_one({'ceo': ctx.author.name})['money']
      
      dollars = 1000
      bucks += dollars

      query = {'ceo': ctx.author.name}
      update = {'$set': {'money': bucks}}
      companies.update_one(query, update)

      make_trans('+', dollars, ctx.author.name)

      await ctx.send(embed = create_embed('Good in the World','Someone gave you some K-Bucks out of the kindness in their heart.',ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Added to Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}]))

  except:
    await ctx.send(embed = create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))

@client.command()
async def account(ctx):
  try:
    personsCompany = companies.find_one({'ceo': ctx.author.name})
    if ctx.author.name in personsCompany.values():
      recent = companies.find_one({'ceo': ctx.author.name})['recent_trans']

      bucks = companies.find_one({'ceo': ctx.author.name})['money']

      if bucks == 0:
        await ctx.send(embed = create_embed('Account', str(bucks) + ' K-Bucks', ctx.author.display_name, ctx.author.avatar_url))
      if bucks > 0:
        await ctx.send(embed = create_embed('Account', str(bucks) + ' K-Bucks', ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Recent Transactions', 'value': "\n".join(recent[:2]), 'inline': True}]))

  except:
    await ctx.send(embed = create_embed('Fiddlesticks', 'You don\'t have a company Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))

@client.command()
async def audition(ctx):
  try:
    personsCompany = companies.find_one({'ceo': ctx.author.name})
    if ctx.author.name in personsCompany.values():
      ceo_trainees = companies.find_one({'ceo': ctx.author.name})['trainees']

      true_idols = companies.find_one({'ceo': ctx.author.name})['idols']
      msg2 = 'There\'s no one left that wants to join your company.'
      none_embed = create_embed('Fiddlesticks', msg2, ctx.author.display_name, ctx.author.avatar_url)

      num_to_select = 3
      
      if len(true_idols) == 2:
        num_to_select = 2
      elif len(true_idols) == 1:
        num_to_select = 1
      if len(true_idols) == 0:
        await ctx.send(embed = none_embed)
        return

      conf = await confirmation(200, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

      if conf == True:

        bucks = companies.find_one({'ceo': ctx.author.name})['money']

        author_idols = random.sample(true_idols, num_to_select)

        iad = []
        idol_emojis = ['🌸', '🍑', '🦋']

        #loop through author_idols
        for idol in author_idols:
          temp_iat = {
            'name': idol_emojis[author_idols.index(idol)] + idol,
            'value': ', '.join(talents[idol]),
            'inline': True
          }
          iad.append(temp_iat)

        msg = 'Here\'s a list of the people that auditioned. Choose one to take in as a trainee.'
        
        idol_embed = create_embed('Auditionees', msg, ctx.author.display_name, ctx.author.avatar_url, iad)
        
        message = await ctx.send(embed = idol_embed)
        
        for idol in iad:
          await message.add_reaction(idol_emojis[iad.index(idol)])

        def filter(reaction, user):
          
          if reaction.emoji in idol_emojis and user.id == ctx.author.id:
            return True

          return False
          
        try:
          reaction = await client.wait_for('reaction_add', check = filter, timeout = 30)
        
        except:
          await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
          return
      
        my_trainee = ''
        for idol in iad:
          if reaction[0].emoji == idol_emojis[iad.index(idol)]:
            my_trainee = iad[iad.index(idol)]['name'][1:]

        dollars = 10
        bucks -= dollars

        query = {'ceo': ctx.author.name}
        update = {'$set': {'money': bucks}}
        companies.update_one(query, update)

        make_trans('-', dollars, ctx.author.name)

        query = {'ceo': ctx.author.name}
        
        ceo_trainees[my_trainee] = 0

        update = {'$set': {'trainees': ceo_trainees}}
        companies.update_one(query, update)

        true_idols.remove(my_trainee)

        update = {'$set': {'idols': true_idols}}
        companies.update_one(query, update)


        await message.delete()

        new_msg = my_trainee + ' has joined your company as a trainee.'
        embed1 = create_embed('New Trainee', new_msg, ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Removed from Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}])

        embed1.set_thumbnail(url=idol_images[my_trainee])

        await ctx.send(embed = embed1)

  except:
    await ctx.send(embed = create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))

@client.command()
async def trainees(ctx):

  try:
    trainees = companies.find_one({'ceo': ctx.author.name})['trainees']
  
  except:
    await ctx.send(embed = create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
    return

  high = len(trainees.keys()) - 1

  index = 1
  last = 10
  
  
  if len(trainees) == 0:
    await ctx.send(embed = create_embed('No Trainees', 'You don\'t have any trainees in your company.', ctx.author.display_name, ctx.author.avatar_url))

    return
    
  desc = list(trainees.keys())[0] + ' : ' + str(list(trainees.values())[0]) + ' ⭐'

  

  if len(trainees) == 1:
    msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

    return

  while index < last:

    desc+= '\n\n' + list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'

    if index == high and high < 10:
      msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      return

    elif index % 10 == 9 and index >= 10:
      msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      await msg.add_reaction('◀️')
      await msg.add_reaction('▶️')

      def filter(reaction, user):
        if (reaction.emoji == '▶️' or reaction.emoji == '◀️') and user.id == ctx.author.id:
          return True
        return False

      try:
        reaction = await client.wait_for('reaction_add', check = filter, timeout = 300)
      except:
        await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
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
      msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      await msg.add_reaction('▶️')

      def filter(reaction, user):
        if reaction.emoji == '▶️' and user.id == ctx.author.id:
          return True
        return False

      try:
        reaction = await client.wait_for('reaction_add', check = filter, timeout = 300)

        if reaction[0].emoji == '▶️':
          await msg.delete()

          index += 1
          desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
          if last + 10 > high:
            last = high
          else:
            last += 10

      except:
        await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
        return

    elif index == high:
      msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      await msg.add_reaction('◀️')

      def filter(reaction, user):
        if reaction.emoji == '◀️' and user.id == ctx.author.id:
          return True
        return False
      try:
        reaction = await client.wait_for('reaction_add', check = filter, timeout = 300)

        if reaction[0].emoji == '◀️':
          await msg.delete()

          index -= 9
          last -= 10
          index += 1
          desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
      except:
        await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
        return

    index+= 1

    if index > high:
      index -= 1
      msg = await ctx.send(embed=create_embed('Your Trainees:', desc, ctx.author.display_name, ctx.author.avatar_url))

      await msg.add_reaction('◀️')

      def filter(reaction, user):
        if reaction.emoji == '◀️' and user.id == ctx.author.id:
          return True
        return False
      try:
        reaction = await client.wait_for('reaction_add', check = filter, timeout = 300)

        if reaction[0].emoji == '◀️':
          await msg.delete()

          index -= 9
          last -= high % 10
          index += 1
          desc = list(trainees.keys())[index] + ' : ' + str(list(trainees.values())[index]) + ' ⭐'
      except:
        await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
        return


@client.command()
async def train(ctx, target_trainee):

  try:
    trainees = companies.find_one({'ceo': ctx.author.name})['trainees']
  except:
    await ctx.send(embed = create_embed('Fiddlesticks', 'You don\'t have a company. Try "?startup" to start your own.', ctx.author.display_name, ctx.author.avatar_url))
    return

  bucks = companies.find_one({'ceo': ctx.author.name})['money']

  
  target_trainee = target_trainee.lower().replace(" ", "")
  trainees_dict = {}
  index = 0
  groups = []
  repeat_groups = []
  group_index = 0

  x = []
  for trainee in trainees.keys():
    groups.append(trainee[trainee.index('(')+1:-1])
    x.append(trainee.lower()[:trainee.index(" (")])
    trainees_dict[trainee.lower().replace(" ", "")] = trainees[trainee]
    
  print(trainees_dict)
    
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
      
      msg = await ctx.send(embed = create_embed('Unoriginal', 'You have multiple trainees with the same name, who did you mean?', ctx.author.display_name, ctx.author.avatar_url, fields))
      
      
      while count > 0:
        await msg.add_reaction(emoji_list[emoji_count])

        count-= 1
        emoji_count+= 1
      
      def filter(reaction, user):
        
        if reaction.emoji in emoji_list and user.id == ctx.author.id:
          return True

        return False
        
      try:
        reactions = await client.wait_for('reaction_add', check = filter, timeout = 30)
      except:
        await ctx.send(embed = create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
        return

      for emoji in emoji_list:
        if reactions[0].emoji == emoji:
          group_index = emoji_list.index(emoji)

    group = repeat_groups[group_index]
    print(group)

    key = target_trainee + '(' + group.lower().replace(" ", "") + ')'
    print(key)
    index = list(trainees_dict.keys()).index(key)
    person = list(trainees.keys())[index]
    
    
    temp_trainees = trainees
    temp_trainees.pop(person)

    level = trainees_dict[key]
    dollars = 50 * level + 50

    conf = await confirmation(dollars, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

  if conf == True:
    
    bucks -= dollars

    query = {'ceo': ctx.author.name}
    update = {'$set': {'money': bucks}}
    companies.update_one(query, update)

    make_trans('-', dollars, ctx.author.name)

    level += 1

    temp_trainees[person] = level
    
    update = {'$set': {'trainees': temp_trainees}}
    companies.update_one(query, update)

    await ctx.send(embed = create_embed('Let\'s Power Up', person + ' has moved up a level.', ctx.author.display_name, ctx.author.avatar_url, [{'name': 'Removed from Account:', 'value': str(dollars) + ' K-Bucks', 'inline': True}]))

#can only train a trainee per (time limit)

my_secret = os.environ['TOKEN']
client.run(my_secret)

#Empty Space String : "\u200b"