import discord
import os
from discord.ext import commands
import random

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

#.set_image
##.setFooter
#.setColor
##.setfield(name='',value='',inline=bool)
#.setFields({name='',value='',inline=bool},{name='',value='',inline=bool})

@client.event
async def on_ready():
  print('--------------')
  print('Bot is online.')
  print('--------------')

@client.command()
async def audition(ctx):
  num_to_select = 3
  random_idols = random.sample(idols, num_to_select)
  first_random_idol = random_idols[0]
  second_random_idol = random_idols[1]
  third_random_idol = random_idols[2]

  msg = 'Here\'s a list of the people that auditioned. Choose one to take in as a trainee.'

  embed = discord.Embed(title='Auditionees', description=msg)
  
  embed.add_field(name= '🌸 ' + first_random_idol,value=", ".join(talents[first_random_idol]),inline=True)
  embed.add_field(name= '🍑 ' + second_random_idol,value=", ".join(talents[second_random_idol]),inline=True)
  embed.add_field(name= '🦋 ' + third_random_idol,value=", ".join(talents[third_random_idol]),inline=True)

  message = await ctx.send(embed = embed)
  
  await message.add_reaction('🌸')
  await message.add_reaction('🍑')
  await message.add_reaction('🦋')

my_secret = os.environ['TOKEN']
client.run(my_secret)