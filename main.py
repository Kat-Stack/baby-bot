from discord.ext import commands
import os
import textManager as tm
flag = True


my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='$')




@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot) + "\nPlease use $init with any applicable corpi separated with a space or leave blank for defaults\nRegardless, $init or I won't work")
    
@bot.command()
async def init(ctx, *corpi):
  if len(corpi) == 0:
    tm.corpusInit()
  else:
    tm.corpusInit(corpi)
  await ctx.send("I have initialized the corpus with {} arguments".format(corpi))
  global flag 
  flag = False

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith("$init") and not flag:
      pass
    else:
     if message.author == bot.user:
          return
     else:
        response = message.content
        await message.reply(tm.getResponse(response))





bot.run(my_secret)
