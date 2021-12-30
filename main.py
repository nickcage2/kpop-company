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
  print("Connected to DB")
except Exception: 
  print("Can't connect to DB")
companies = db.companies

"""company = {
  "ceo": ctx.message.author.name,
  "money": 0,
  "idols": [],
  "trainees": []
}

company_id = companies.insert_one(company).inserted_id"""

client = commands.Bot(command_prefix = '?')

idols = []
talents = {}

file = open('./idols.txt', 'r')
lines = file.readlines()

for line in lines:
  line = line.replace("\n","")
  idol_talents = line.split(" ")
  name = idol_talents[0] + " " + idol_talents[1]
  del idol_talents[0]
  del idol_talents[0]
  idols.append(name)
  talents[name] = idol_talents


trainees = []
money = 0

##.setfield(name='',value='',inline=bool)
#.setFields({name='',value='',inline=bool},{name='',value='',inline=bool})

@client.event
async def on_ready():
  print('--------------')
  print('Bot is online.')
  print('--------------')
  
def create_embed(title, desc, fields = []): 
  #[{name :, value:, inline:},{},{},etc]
  embed = discord.Embed(title=title, description=desc,color=0xFF9C9C)
 
  for field in fields:
    embed.add_field(
      name = field["name"],
      value = field["value"],
      inline = field["inline"])

  return embed


@client.command()
async def startup(ctx):
  personsCompany = companies.find_one({"ceo": ctx.message.author.name})

  if ctx.message.author.name in personsCompany.values():
    await ctx.send("You already own a company.")
    return

  company = {
    "ceo": ctx.message.author.name,
    "money": 0,
    "idols": [],
    "trainees": []
  }

  companies.insert_one(company).inserted_id
  
  await ctx.send("You have started your company! Welcome to " + ctx.message.author.name + "'s company!")

@client.command()
async def loan(ctx):
  
  await ctx.send("You have")

@client.command()
async def money(ctx):
  
  await ctx.send("You have")

@client.command()
async def audition(ctx):
  num_to_select = 3
  random_idols = random.sample(idols, num_to_select)
  first_random_idol = random_idols[0]
  second_random_idol = random_idols[1]
  third_random_idol = random_idols[2]

  msg = 'Here\'s a list of the people that auditioned. Choose one to take in as a trainee.'
  
  idol = [{
    "name": '🌸 ' + first_random_idol,
    "value": ", ".join(talents[first_random_idol]),
    "inline": True
  }, {
    "name": '🍑 ' + second_random_idol,
    "value": ", ".join(talents[second_random_idol]),
    "inline": True
  }, {
    "name": '🦋 ' + third_random_idol,
    "value": ", ".join(talents[third_random_idol]),
    "inline": True
  }]

  idol_embed = create_embed('Auditionees', msg, idol)
  
  message = await ctx.send(embed = idol_embed)
  
  await message.add_reaction('🌸')
  await message.add_reaction('🍑')
  await message.add_reaction('🦋')

my_secret = os.environ['TOKEN']
client.run(my_secret)