import discord
import random
import time

def get_rate(form):
  
  if form == 'web_drama':
    return random.randrange(1, 100)
    
  if form == 'movie':
    return random.randrange(33, 100)

  if form == 'drama':
    return random.randrange(66, 100)

def actorpromotion(form, actor, ceo, companies, level, recognition):
  #generate success rate
  rate = get_rate(form)
  rate_per = rate / 100.0
 
  web_drama_profit = 300
  movie_profit = 600
  drama_profit = 900

  promotion_len = int((time.time() / 60) + 300)
  
  success = rate + (rate_per * level) + (rate_per * recognition)
  success_per = success / 100.0

  if form == 'web_drama':
    profit = web_drama_profit + (web_drama_profit * success_per)
    
  elif form == 'movie':
    profit = movie_profit + (movie_profit * success_per)
  
  elif form == 'drama':
    profit = drama_profit + (drama_profit * success_per)
  
  promotions = companies.find_one({'ceo': ceo})['promotion']

  promotions[actor] = [promotion_len, int(profit)]

  companies.update_one({'ceo': ceo}, {'$set': {'promotion': promotions}})