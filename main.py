import discord
import os
from discord.ext import commands
from pymongo import MongoClient
from Functions import confirmation, create_embed, make_trans

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