from Functions.soloistpromotion import soloistpromotion

async def soloistdebut(self, ctx, message, x, lower_x, trainees, recognition):
  await message.delete()
  
  soloists = self.companies.find_one({'ceo': ctx.author.name})['soloists']
  
  for trainee in trainees:
    if 'Rap' in self.talents[trainee] or 'Vocal' in self.talents[trainee]:
      name = trainee
      try:
        if trainee.index('(') >= 0:
          name = trainee[0:trainee.index('(')-1]
      except:
        print("")
      x[trainee] = trainees[trainee]
      lower_x[name.lower()] = trainees[trainee]

  if len(x) == 0:
    await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have any trainees that can debut as a soloist.', ctx.author.display_name, ctx.author.avatar_url))
    return
  
  await self.trainees_list(ctx, x)
  #delete this message after we get the name
  
  def check(msg):
    return msg.channel == ctx.channel and msg.author == ctx.author
    
  try:  
    message = await self.client.wait_for('message', timeout=30, check=check)
  except:
    return

  inp = message.content.lower()
  print(inp)
  if inp in list(lower_x.keys()):

    name = list(x.keys())[list(lower_x.keys()).index(inp)]
    soloists[name] = list(x.values())[list(lower_x.keys()).index(inp)]

    level = list(x.values())[list(lower_x.keys()).index(inp)]

    fields = [{
    'name': '📄 Single',
    'value': '300 K-Bucks\n Low chance of success.',
    'inline': True
    },{
    'name': '📒 Mini-Album',
    'value': '600 K-Bucks\n Medium chance of success.',
    'inline': True
    },{
    'name': '📚 Full Album',
    'value': '900 K-Bucks\n High chance of success.',
    'inline': True
    }]
  
    message1 = await ctx.send(embed = self.create_embed('Media', 'What kind of album do you want them to debut with?', ctx.author.display_name, ctx.author.avatar_url, fields))

    await message1.add_reaction('📄')
    await message1.add_reaction('📒')
    await message1.add_reaction('📚')

    emojis1 = ['📄', '📒', '📚']

    def filter(reaction, user):
      if reaction.emoji in emojis1 and user.id == ctx.author.id:
        return True
      return False

    try:
      reaction1 = await self.client.wait_for('reaction_add', check = filter, timeout = 30)

    except:
      await ctx.send(embed = self.create_embed('Tick Tock', 'You ran out of time.', ctx.author.display_name, ctx.author.avatar_url))
      return
    
    #web_drama
    if reaction1[0].emoji == '📄':
      form = 'single'
      dollars = 300

    #movie
    if reaction1[0].emoji == '📒':
      form = 'mini_album'
      dollars = 600

    #drama
    if reaction1[0].emoji == '📚':
      form = 'full_album'
      dollars = 900
      
    await message1.delete()

    response = await self.confirmation(dollars, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

    if response == True:
      self.make_trans('-', dollars, ctx.author.name)

      ceo = ctx.author.name
      
      query = {'ceo': ctx.author.name}
      update = {'$set': {'soloists': soloists}}
      self.companies.update_one(query, update)

      trainees.pop(name)

      update = {'$set': {'trainees': trainees}}
      self.companies.update_one(query, update)

      recognition += 1
      update = {'$set': {'recognition': recognition}}
      self.companies.update_one(query, update)

      await ctx.send(embed = self.create_embed('Road to Stardom', name + ' has debuted. Check back in 5 hours to claim your profits.',ctx.author.display_name, ctx.author.avatar_url).set_footer(text='Use "?collect"'))

      soloistpromotion(form, name, ceo, self.companies, level, recognition)