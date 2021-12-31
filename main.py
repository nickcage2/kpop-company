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

'''company = {
  'ceo': ctx.author.name,
  'money': 0,
  'idols': [],
  'trainees': []
}

company_id = companies.insert_one(company).inserted_id'''

client = commands.Bot(command_prefix = '?')

idols = []
talents = {}

file = open('./idols.txt', 'r')
lines = file.readlines()

for line in lines:
  line = line.replace('\n','')
  idol_talents = line.split(' ')
  name = idol_talents[0] + ' ' + idol_talents[1]
  del idol_talents[0]
  del idol_talents[0]
  idols.append(name)
  talents[name] = idol_talents

@client.event
async def on_ready():
  print('--------------')
  print('Bot is online.')
  print('--------------')
  
def create_embed(title, desc, fields = []): 
  #[{name :, value:, inline: True},{},{},etc]
  embed = discord.Embed(title=title, description=desc,color=0xFF9C9C)
 
  for field in fields:
    embed.add_field(
      name = field['name'],
      value = field['value'],
      inline = field['inline'])

  return embed

@client.command()
async def startup(ctx):
    
  try:
    personsCompany = companies.find_one({'ceo': ctx.author.name})
    if ctx.author.name in personsCompany.values():
      await ctx.send(embed = create_embed('No Monopolies', 'You already own a company.'))
      return
      
  except:
    company = {
      'ceo': ctx.author.name,
      'money': 0,
      'trainees': [],
      'recent_trans': []
    }

    companies.insert_one(company).inserted_id
    
    await ctx.send(embed = create_embed('Taking Off', 'Quite the entrepreneur, you are! Welcome to your new entertainment company, CEO ' + ctx.author.name + '.'))

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
async def free(ctx):
  bucks = companies.find_one({'ceo': ctx.author.name})['money']
  
  dollars = random.randrange(200,700)
  bucks += dollars

  query = {'ceo': ctx.author.name}
  update = {'$set': {'money': bucks}}
  companies.update_one(query, update)

  make_trans('+', dollars, ctx.author.name)

  await ctx.send(embed = create_embed('Good in the World','Someone gave you some K-Bucks out of the kindness in their heart.', [{'name': 'Added to Account:', 'value': str(dollars), 'inline': True}]))

@client.command()
async def account(ctx):
  recent = companies.find_one({'ceo': ctx.author.name})['recent_trans']

  bucks = companies.find_one({'ceo': ctx.author.name})['money']

  if bucks == 0:
    await ctx.send(embed = create_embed('Account', str(bucks) + ' K-Bucks'))
  if bucks > 0:
    await ctx.send(embed = create_embed('Account', str(bucks) + ' K-Bucks', [{'name': 'Recent Transactions', 'value': "\n".join(recent[:2]), 'inline': True}]))

@client.command()
async def audition(ctx):
  ceo_trainees = companies.find_one({'ceo': ctx.author.name})['trainees']
  
  temp_idols = idols

  #not deleting trainee out of temp_idols
  for trainee in ceo_trainees:
    if trainee in temp_idols:
      temp_idols.remove(trainee)

  msg2 = 'There\'s no one left that wants to join your company.'
  none_embed = create_embed('title', msg2)
 
  num_to_select = 3
  
  if len(temp_idols) == 2:
    num_to_select = 2
  elif len(temp_idols) == 1:
    num_to_select = 1
  elif len(temp_idols) == 0:
    await ctx.send(embed = none_embed)

  temp_idols = random.sample(temp_idols, num_to_select)

  iad = []
  idol_emojis = ['🌸', '🍑', '🦋']

  #loop through temp_idols
  for idol in temp_idols:
    temp_iat = {
      'name': idol_emojis[temp_idols.index(idol)] + ' ' + idol,
      'value': ', '.join(talents[idol]),
      'inline': True
    }
    iad.append(temp_iat)

  msg = 'Here\'s a list of the people that auditioned. Choose one to take in as a trainee.'
  
  idol_embed = create_embed('Auditionees', msg, iad)
  
  message = await ctx.send(embed = idol_embed)
  
  for idol in iad:
    await message.add_reaction(idol_emojis[iad.index(idol)])

  def filter(reaction, user):
    
    if reaction.emoji in idol_emojis and user.id == ctx.author.id:
      return True

    return False
    
  reaction = await client.wait_for('reaction_add', check = filter, timeout = 30)
  
  my_trainee = ''
  for idol in iad:
    if reaction[0].emoji == idol_emojis[iad.index(idol)]:
      my_trainee = iad[iad.index(idol)]['name'][1:]
  
  ceo_trainees.append(my_trainee)

  query = {'ceo': ctx.author.name}

  update = {'$set': {'trainees': ceo_trainees}}

  companies.update_one(query, update)

  await message.delete()

  new_msg = my_trainee + ' has joined your company as a trainee.'
  embed1 = create_embed('New Trainee', new_msg)
  await ctx.send(embed = embed1)

# make it sends a picture of the idol you recruit inside the embed, ask parker for help

my_secret = os.environ['TOKEN']
client.run(my_secret)