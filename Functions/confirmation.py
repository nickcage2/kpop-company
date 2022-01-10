import discord
from Functions import create_embed
from main import client, companies

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