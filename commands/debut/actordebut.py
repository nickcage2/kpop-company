from Functions.actorpromotion import actorpromotion

async def actordebut(self, ctx, message, x, lower_x, trainees, recognition):
  await message.delete()
  
  actors = self.companies.find_one({'ceo': ctx.author.name})['actors']
  
  for trainee in trainees:
    if 'Acting' in self.talents[trainee]:
      name = trainee
      try:
        if trainee.index('(') >= 0:
          name = trainee[0:trainee.index('(')-1]
      except:
        print("")
      x[trainee] = trainees[trainee]
      lower_x[name.lower()] = trainees[trainee]

  if len(x) == 0:
    await ctx.send(embed = self.create_embed('Error 404', 'You don\'t have any trainees that can debut as an actor.', ctx.author.display_name, ctx.author.avatar_url))
    return
  print(x)
  await self.trainees_list(ctx, x)
  #delete this message after we get the name
  
  def check(msg):
    return msg.channel == ctx.channel and msg.author == ctx.author
    
  message = await self.client.wait_for('message', timeout=30, check=check)

  inp = message.content.lower()

  if inp in list(lower_x.keys()):

    name = list(x.keys())[list(lower_x.keys()).index(inp)]
    actors[name] = list(x.values())[list(lower_x.keys()).index(inp)]

    level = list(x.values())[list(lower_x.keys()).index(inp)]

    fields = [{
    'name': '💻 Web-Drama',
    'value': '300 K-Bucks\n Low chance of success.',
    'inline': True
    },{
    'name': '🎞️ Movie',
    'value': '600 K-Bucks\n Medium chance of success.',
    'inline': True
    },{
    'name': '📺 Drama',
    'value': '900 K-Bucks\n High chance of success.',
    'inline': True
    }]
  
    message1 = await ctx.send(embed = self.create_embed('Media', 'What kind of media do you want them to debut in?', ctx.author.display_name, ctx.author.avatar_url, fields))

    await message1.add_reaction('💻')
    await message1.add_reaction('🎞️')
    await message1.add_reaction('📺')

    emojis1 = ['💻', '🎞️', '📺']

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
    if reaction1[0].emoji == '💻':
      form = 'web_drama'
      dollars = 300

    #movie
    if reaction1[0].emoji == '🎞️':
      form = 'movie'
      dollars = 600

    #drama
    if reaction1[0].emoji == '📺':
      form = 'drama'
      dollars = 900
      
    await message1.delete()

    response = await self.confirmation(dollars, ctx.author.display_name, ctx.author.avatar_url, ctx.send, ctx.author.id)

    if response == True:
      self.make_trans('-', dollars, ctx.author.name)

      ceo = ctx.author.name
      
      query = {'ceo': ctx.author.name}
      update = {'$set': {'actors': actors}}
      self.companies.update_one(query, update)

      trainees.pop(name)

      update = {'$set': {'trainees': trainees}}
      self.companies.update_one(query, update)

      recognition += 1
      update = {'$set': {'recognition': recognition}}
      self.companies.update_one(query, update)

      await ctx.send(embed = self.create_embed('Road to Stardom', name + ' has debuted. Check back in 5 hours to claim your profits.',ctx.author.display_name, ctx.author.avatar_url).set_footer(text='Use "?collect"'))

      actorpromotion(form, name, ceo, self.companies, level, recognition)