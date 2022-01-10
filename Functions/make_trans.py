from main import companies

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