import discord
import os
from discord.ext import commands
from pymongo import MongoClient

from commands.startup import startup
from commands.daily import daily
from commands.account import account
from commands.audition import audition
from commands.train import train
from commands.trainees import trainees
from commands.help import help
from commands.debut.debut import debut
from commands.updatecompanies import updatecompanies
from commands.collect import collect

#fix all the exceptions on the commands

my_id = os.environ['myid']

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
  line = line.replace('\n','').strip()
  idol_talents = line.split(' / ')
  name = idol_talents[0]
  idol_images[name] = idol_talents[1]
  del idol_talents[0]
  del idol_talents[0]
  idols.append(name)
  talents[name] = idol_talents[0].split(' ')

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
    emojis = await client.wait_for('reaction_add', check= emoji, timeout = 10)
  except:
    await send(embed = create_embed('Tick Tock', 'You ran out of time.', name, avatar_url))
    return 
    
  if emojis[0].emoji == '⛔':
    await confirm.delete()
    await send(embed=create_embed('Cancelled', 'The action was cancelled.', name, avatar_url))
    return False
    
  if emojis[0].emoji == '✅':
    await confirm.delete()
    if dollars > companies.find_one({'ceo': name})['money']:
      msg = 'You don\'t have enough K-Bucks to perform this transaction.'
      broke_embed = create_embed('You\'re Kinda Broke', msg, name, avatar_url)
      
      await send(embed=broke_embed)
      
      return False

    return True

def make_trans(addorsub, money, author): 
  # is either '+' or '-' 
  #money is integer 
  #author is ctx.author.name
  recent = companies.find_one({'ceo': author})['recent_trans']

  recent.insert(0, addorsub + ' ' + str(money))
  if len(recent) == 3:
    recent.pop(-1)

  query = {'ceo': author}
  update = {'$set': {'recent_trans': recent}}
  companies.update_one(query, update)

#cogs for all the commands

client.add_cog(startup(client, create_embed, idols, companies))

client.add_cog(daily(client, create_embed, companies, make_trans))

client.add_cog(account(client, companies, create_embed))

client.add_cog(audition(client, companies, create_embed, confirmation, talents, make_trans, idol_images))

client.add_cog(train(client, companies, create_embed, confirmation, make_trans))

client.add_cog(trainees(client, companies, create_embed))

client.add_cog(help(client, create_embed))

client.add_cog(debut(client, companies, create_embed, talents, confirmation, make_trans))

client.add_cog(updatecompanies(client, companies, idols, create_embed, my_id))

client.add_cog(collect(client, companies, create_embed, make_trans))

my_secret = os.environ['TOKEN']
client.run(my_secret)

#Empty Space String : "\u200b"