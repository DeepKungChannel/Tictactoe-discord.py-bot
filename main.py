import discord
from discord.ext import commands, tasks
from replit import db  #Use replit database
import json
from get_prefix import update_prefix
import random

TOKEN = "----TOKEN----"
def get_prefix(client,message):
  try:
    jsons = db['prefixes']
    json = jsons.value
    result = json[str(message.guild.id)]
    # print("getprefix1")
    update_prefix()
    return result
  except:
    jsons = db['prefixes']
    json = jsons.value
    json[str(message.guild.id)] = "d/"
    db['prefixes'] = json
    result = json[str(message.guild.id)]
    # print("getprefix2")
    update_prefix()
    return result

def addprefix(guild):
  json = db['prefixes'].value
  json[str(guild.id)] = "d/"
  db['prefixes'] = json
def changeprefix(guild,prefix:str):
  json = db['prefixes'].value
  json[str(guild.id)] = prefix
  db['prefixes'] = json
def deleteprefix(guild):
  json = db['prefixes'].value
  json.pop(str(guild.id))
  db['prefixes'] = json

def get_game(client,guild):
  try:
    json = db['games'].value
    result = json[str(guild.id)]
    return result
  except:
    json[str(guild.id)] = {
      "gameOver":True,
      "turn":"",
      "numturn":0,
      "board":[[0,0,0],[0,0,0],[0,0,0]],
      "player1":"",
      "player2":"",
      "msgid":0
    }
    db['games'] = json
    result = json[str(guild.id)]
    return result
def addgame(guild):
  json = db['games']
  json[str(guild.id)] = {
      "gameOver":True,
      "turn":"",
      "numturn":0,
      "board":[[0,0,0],[0,0,0],[0,0,0]],
      "player1":"",
      "player2":"",
      "msgid":0
    }
  db['games'] = json
def set_game(message,game):
  json = db['games'].value
  json[str(message.guild.id)] = game
  db['games']= json
def deletegame(guild):
  json = db['games'].value
  json.pop(str(guild.id))
  db['games'] = json

# db['games'] = {}
# key = db['games']
# print(key)
def windetect(board,num):
  for i in range(3):
    if board[0].value[i] == num and board[1].value[i] == num and board[2].value[i] == num:
      return True
  for i in range(3):
    if board[i].value[0] == num and board[i].value[1] == num and board[i].value[2] == num:
      return True
  
  if board[0].value[0] == num and board[1].value[1] == num and board[2].value[2] == num:
    return True
  
  if board[0].value[2] == num and board[1].value[1] == num and board[2].value[0] == num:
    return True
  
  return False
def render(board,turn,numturn):
  embed=discord.Embed(title="Tictactoe Game",color=discord.Color.green())
  display=''
  for i in range(3):
    if i != 0 :
      display+='━━━━━━━\n'
    for j in range(3):
      if board[i].value[j] == 0:
        d = ":white_large_square:  "
      elif board[i].value[j] == 1:
        d = ":x:  "
      elif board[i].value[j] == 2:
        d = ":o:  "
      if j != 0:
        display+=str("|  "+d)
      else:
        display+=str(d)
    display+="\n"
  if numturn == 1:
    disturn = ':x:'
  elif numturn == 2:
    disturn = ":o:"
  embed.add_field(name='`{} Turn!` {}'.format(turn,disturn),value=display)
  return embed
def rendertie(board,turn):
  embed=discord.Embed(title="Tictactoe Game",color=discord.Color.green())
  display=''
  for i in range(3):
    if i != 0 :
      display+='━━━━━━━\n'
    for j in range(3):
      if board[i].value[j] == 0:
        d = ":white_large_square:  "
      elif board[i].value[j] == 1:
        d = ":x:  "
      elif board[i].value[j] == 2:
        d = ":o:  "
      if j != 0:
        display+=str("|  "+d)
      else:
        display+=str(d)
    display+="\n"
  embed.add_field(name='`Tie!`',value=display)
  return embed
def renderwin(board,turn):
  embed=discord.Embed(title="Tictactoe Game",color=discord.Color.green())
  display=''
  for i in range(3):
    if i != 0 :
      display+='━━━━━━━\n'
    for j in range(3):
      if board[i].value[j] == 0:
        d = ":white_large_square:  "
      elif board[i].value[j] == 1:
        d = ":x:  "
      elif board[i].value[j] == 2:
        d = ":o:  "
      if j != 0:
        display+=str("|  "+d)
      else:
        display+=str(d)
    display+="\n"
  embed.add_field(name='`{} Win!`'.format(turn),value=display)
  return embed
def checkempty(board,num1,num2):
  if board[num1].value[num2] == 0:
    return True
  return False
def tiedetect(board):
  if board[0].value[0] != 0 and board[0].value[1] != 0 and board[0].value[2] != 0 and board[1].value[0] != 0 and board[1].value[1] != 0 and board[1].value[2] != 0 and board[2].value[0] != 0 and board[2].value[1] != 0 and board[2].value[2] != 0:
    return True
  return False
class Mybot(commands.Bot):
  def __init__(self, prefix, self_bot):
    commands.Bot.__init__(self,command_prefix = prefix,self_bot=self_bot)
    self.onmsg = "Bot is ready"
    self.add_commands()
  
  async def on_ready(self):
    self.task.start()
    print(self.onmsg)

  async def on_message(self,msg):
    if msg.content == "addprefix":
      addprefix(msg.guild)
      await msg.channel.send("Added!")
      # print("addprefix")
    try:
      if msg.mentions[0] == self.user:
        pre = get_prefix(self,msg)
        await msg.channel.send("The prefix is {}".format(pre))
      else:
        await self.process_commands(msg)
    except:
      await self.process_commands(msg)
  
  async def on_guild_join(self,guild):
    addprefix(guild)
    addgame(guild)

  async def on_guild_remove(self,guild):
    deleteprefix(guild)
    deletegame(guild)
   
  @tasks.loop(minutes=10)
  async def task(self):
    await self.change_presence(activity=discord.Game(name='Joined {} Server!'.format(len(self.guilds))))
  
  def add_commands(self):
    self.remove_command('help')

    @self.command()
    async def ping(ctx):
      await ctx.send("{} ms".format(round(self.latency*100)))
    
    @self.command()
    async def cprefix(ctx,prefix:str):
      changeprefix(ctx.guild,prefix)
      await ctx.send("Change prefix to {}!".format(prefix))

    #--------------------game command----------------------
    @self.command(aliases=['ttt'])
    async def tictactoe(ctx,p1:discord.Member,p2:discord.Member):
      games = get_game(self,ctx.guild)
      game = games.value
      if game['gameOver']:
        p1 = p1.name
        p2 = p2.name
        game['player1'] = p1
        game['player2'] = p2
        tnum = random.randint(1,2)
        if tnum == 1:
          game['turn'] = game['player1']
          game['numturn'] = 1
        if tnum == 2:
          game['turn'] = game['player2']
          game['numturn'] = 2
        board = render(game['board'],game['turn'],game['numturn'])
        message = await ctx.send(embed=board)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        await message.add_reaction("5️⃣")
        await message.add_reaction("6️⃣")
        await message.add_reaction("7️⃣")
        await message.add_reaction("8️⃣")
        await message.add_reaction("9️⃣")
        await message.add_reaction("😫")
        game['gameOver'] = False
        game['msgid'] = message.id
        set_game(ctx.message,games)
        while not game['gameOver']:
          reaction, user = await self.wait_for('reaction_add',check=lambda reaction,user: user.name != self.user.name)
          if user.name == game['turn'] and reaction.message.id == message.id:
            win = False
            reset = False
            if reaction.emoji == "1️⃣":
              num = 1
            elif reaction.emoji == "2️⃣":
              num = 2
            elif reaction.emoji == "3️⃣":
              num = 3
            elif reaction.emoji == "4️⃣":
              num = 4
            elif reaction.emoji == "5️⃣":
              num = 5
            elif reaction.emoji == "6️⃣":
              num = 6
            elif reaction.emoji == "7️⃣":
              num = 7
            elif reaction.emoji == "8️⃣":
              num = 8
            elif reaction.emoji == "9️⃣":
              num = 9
            elif reaction.emoji == "😫":
              win = True
            if win:
              if game['numturn'] == 2:
                game['turn'] = game['player1']
                game['numturn'] = 1
              elif game['numturn'] == 1:
                game['turn'] = game['player2']
                game['numturn'] = 2
              if win:
                display = renderwin(game['board'],game['turn'])
              else:
                display = rendertie(game['board'],game['turn'])
              await message.edit(embed=display)
              if not game['gameOver']:
                game['gameOver'] = True
                game["turn"]=""
                game["numturn"]=0
                for i in range(3):
                  game["board"][i].value = [0,0,0]
                game["player1"]=""
                game["player2"]=""
                game["msgid"]=0
                set_game(ctx.message,games)
              return
            if not reset:
              if num >= 1 and num <= 3:
                empty = checkempty(game['board'],0,num-1)
              elif num >= 4 and num <= 6:
                empty = checkempty(game['board'],1,num-4)
              elif num >= 7 and num <= 9:
                empty = checkempty(game['board'],2,num-7)
              if empty:
                await message.remove_reaction(reaction,user)
                if num >= 1 and num <= 3:
                  game['board'][0].value[num-1] = game['numturn']
                elif num >= 4 and num <= 6:
                  game['board'][1].value[num-4] = game['numturn']
                elif num >= 7 and num <= 9:
                  game['board'][2].value[num-7] = game['numturn']
                win = windetect(game['board'],game['numturn'])
                tie = tiedetect(game['board'])
                if win or tie:
                  if win:
                    display = renderwin(game['board'],game['turn'])
                  else:
                    display = rendertie(game['board'],game['turn'])
                  await message.edit(embed=display)
                  if not game['gameOver']:
                    game['gameOver'] = True
                    game["turn"]=""
                    game["numturn"]=0
                    for i in range(3):
                      game["board"][i].value = [0,0,0]
                    game["player1"]=""
                    game["player2"]=""
                    game["msgid"]=0
                    set_game(ctx.message,games)
                  return
                else:
                  if str(game['turn']) == str(game['player2']):
                    game['turn'] = game['player1']
                    game['numturn'] = 1
                  elif str(game['turn']) == str(game['player1']):
                    game['turn'] = game['player2']
                    game['numturn'] = 2
                  set_game(ctx.message,games)
                  display = render(game['board'],game['turn'],game['numturn'])
                  await message.edit(embed=display)
              else:
                set_game(ctx.message,games)
                await message.remove_reaction(reaction,user)
          else:
            await message.remove_reaction(reaction,user)

    @self.command()
    async def stop(ctx):
      games = get_game(self,ctx.guild)
      game = games.value
      if not game['gameOver']:
        game['gameOver'] = True
        game["turn"]=""
        game["numturn"]=0
        for i in range(3):
          game["board"][i].value = [0,0,0]
        game["player1"]=""
        game["player2"]=""
        game["msgid"]=0
        set_game(ctx.message,game)
        message = await ctx.send("Game has stopped.")
        await message.add_reaction("🙂")
    #---------help--------------
    @self.command()
    async def help(ctx):
      prefixes = db['prefixes'].value
      prefix = prefixes[str(ctx.guild.id)]
      embed = discord.Embed(title = 'Help',color=discord.Color.from_rgb(248,255,0))
      embed.add_field(name = "Start",value = "Start the game `{}tictactoe`".format(prefix),inline=False)
      embed.add_field(name="Stop",value='Stop the game `{}stop`'.format(prefix))
      embed.add_field(name = "Ping",value = "Get the latency info of the bot. `{}ping`".format(prefix),inline=False)
      embed.add_field(name='Cprefix',value='Change prefix`{}cprefix`'.format(prefix),inline=False)
      embed.set_thumbnail(url=self.user.avatar_url)
      embed.set_footer(text="Request by {}".format(ctx.author),icon_url=ctx.author.avatar_url)
      await ctx.send(embed = embed)

bot = Mybot(get_prefix,False)
bot.run(TOKEN)


