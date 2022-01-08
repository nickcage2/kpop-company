import discord
import random
import time

def get_rate(form):
  
  if form == 'single':
    return random.randrange(1, 100)
    
  if form == 'mini_album':
    return random.randrange(33, 100)

  if form == 'full_album':
    return random.randrange(66, 100)

def soloistpromotion(form, soloist, ceo, companies, level, recognition):
  #generate success rate
  rate = get_rate(form)
  rate_per = rate / 100.0
 
  single_profit = 300
  mini_album_profit = 600
  full_album_profit = 900

  promotion_len = int((time.time() / 60) + 300)
  
  success = rate + (rate_per * level) + (rate_per * recognition)
  success_per = success / 100.0

  if form == 'single':
    profit = single_profit + (single_profit * success_per)
    
  elif form == 'mini_album':
    profit = mini_album_profit + (mini_album_profit * success_per)
  
  elif form == 'full_album':
    profit = full_album_profit + (full_album_profit * success_per)
  
  promotions = companies.find_one({'ceo': ceo})['promotion']

  promotions[soloist] = [promotion_len, int(profit)]

  companies.update_one({'ceo': ceo}, {'$set': {'promotion': promotions}})