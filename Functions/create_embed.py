import discord

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