import discord
from discord.ext import commands
import os, sqlite3, youtube_dl
import ffmpeg
import asyncio
import functools
import itertools
import math
import random

Alice = commands.Bot(command_prefix='.', Intents=discord.Intents.all())
Alice.remove_command('help')
bad_words = ['шлюха','хуй','пенис','hui','бля','блядский','впиздячил','выблядок','наблядовал','ебать','выебывается','выебываеться','доебался','доебаться','ебало','ебло','ебанул','ебанулся','поебался','ебашит','заебал','заебись','наебашился','наебнулся','козлоеб','поебень','уебался','уебище','хитровыебанный','пизда','пиздабол','пиздатый','пиздец','подпиздывает','спиздил','хуево','хуйня','негр','гандон','долбоеб','трахнул','отимел']

youtube_dl.utils.bug_reports_message = lambda: ''


"Ивент который заработает в момент готовности бота"
@Alice.event
async def on_ready():
    print('Alice was start!')
    
    global base, cur
    base = sqlite3.connect('Alice.db')
    cur = base.cursor()
    if base:
        print('Alice database was connected to Alice!')

"Комманда на проверку в онлайн ли бот"
@Alice.command()
async def online(ctx):
    await ctx.send('Alice a online!')

"комманда инфо о боте"
@Alice.command()
async def info (ctx , st = None):
    stlist = ['develop', 'author', 'bot', 'rules', None, 'Git']
    if st == None:
        embed=discord.Embed(title="Info", description="для использования подробностей пропишите .info <раздел>", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.add_field(name="Информация о разработке", value=".info develop", inline=False)
        embed.add_field(name="Информация о авторе", value=".info author", inline=False)
        embed.add_field(name="Информация о боте", value=".info bot", inline=False)
        embed.add_field(name="Информация о правилах использования", value=".info rules", inline=False)
        embed.add_field(name="Информация о Исходном коде бота", value=".info Git", inline=False)
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    if st == 'develop':
        develop=discord.Embed(title="Разработка", color=0x7f7f7f)
        develop.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        develop.add_field(name="Автор", value="Wolfrik", inline=False)
        develop.add_field(name="Библиотеки", value="**youtube_dl,discord.py,PyNaCL,ffmpeg,os**", inline=False)
        develop.add_field(name="Язык программирования", value="Python", inline=False)
        develop.set_footer(text="Alice 2022")
        await ctx.send(embed=develop)
    if st == 'author':
        embed=discord.Embed(title="Автор", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.add_field(name="Никнейм", value="Wolfrik", inline=False)
        embed.add_field(name="Имя", value="Эгор", inline=False)
        embed.add_field(name="Сколько лет", value="14", inline=False)
        embed.add_field(name="Чем увлекаеться", value=" Программирование,игры,Моделлирование", inline=False)
        embed.add_field(name="Языки программирования которые знает", value="C# junior(скоро Senior),Python junior,lua junior", inline=False)
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    if st == 'bot':
        embed=discord.Embed(title="Инфо о боте", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.add_field(name="Имя бота", value="Alice", inline=False)
        embed.add_field(name="Язык программирования", value="python", inline=False)
        embed.add_field(name="База данных", value="SqlLite", inline=False)
        embed.add_field(name="Преднозначение", value="Моделированние,Розвлечение,Музыка", inline=False)
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    if st == 'rules':
        embed=discord.Embed(title="Правила", description="Запрещено спамить флудить,некультурно выражаться", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    if st == 'Git':
        embed=discord.Embed(title="Исходный код бота", description="GitHub - https://github.com/wolfrik11/Alice", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    if st not in stlist:
        embed=discord.Embed(title="Ошибка", description="Ты неправельно ввел название раздела", color=0x7f7f7f)
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.send(embed=embed)
    
"Комманда для очистки чата"
@Alice.command()
@commands.has_permissions( administrator = True )
async def clear ( ctx, amount = 100 ):
    await ctx.channel.purge( limit= 1 )
    await ctx.channel.purge( limit= amount )
    embed=discord.Embed(title="Очистка", description="я очистила указзаное кол-во сообщений, помните я не могу удалять сообщения которым есть 3 недели", color=0x7f7f7f)
    embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
    embed.set_footer(text="Alice 2022")
    await ctx.send(embed=embed)
    
"Комманда для кика пользователя"
@Alice.command()
@commands.has_permissions( administrator = True )
async def kick ( ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge( limit=1)
    await member.kick(reason= reason)
    await ctx.send( f'Я кикнула пользователя { member.mention } по причине { reason }')

"комманда для бана пользователя"
@Alice.command()
@commands.has_permissions( administrator = True )
async def ban ( ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge( limit=1 )
    await member.ban( reason= reason )
    await ctx.send( f'Я забанила пользователя { member.mention }, по причине { reason }')

"комманда для мута пользователя"
@Alice.command()
@commands.has_permissions( administrator = True )
async def mute( ctx,member:discord.Member, reason = None ):
    await ctx.channel.purge( limit = 1 )
    mute_role = discord.utils.get( ctx.message.guild.roles, name = '[MUTED]')
    await member.add_roles( mute_role )
    await ctx.send(f'У { member.mention }, ограничение чата,за {reason} !')
    
"комманда для временного мута пользователя"
@Alice.command()
@commands.has_permissions( administrator = True )
async def tempmute( ctx,member:discord.Member, time = 60, reason = None ):
    await ctx.channel.purge( limit = 1 )
    mute_role = discord.utils.get( ctx.message.guild.roles, name = '[MUTED]')
    await member.add_roles( mute_role )
    await ctx.send(f'У {member.mention}, ограничение чата на {time} секунд, за {reason} !')
    if time < 60:
        await member.remove_roles( mute_role )
        
"Ивент для защиты серверов"
@Alice.event
async def on_message(message):
    await Alice.process_commands(message)
    msg = message.content.lower()
    if msg in bad_words:
        await message.delete()
    if message.content.startswith("!Suggest"):
        await message.add_reaction("✅")
        await message.add_reaction("❌")
    

domains: ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
async def check_domains(link):
    for x in domains:
        if link.startswith(x):
            return Turn
    return False

#Комманда для проигрывания музыки
@Alice.command()
async def play(ctx, *, command = None):
    await ctx.channel.purge( limit = 1 )
    global server, server_id, name_channel
    author = ctx.author
    server = ctx.guild
    if command == None:
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
    params = command.split(' ')
    if len(params) == 1:
        server = ctx.guild
        sourse = params[0]
        name_channel = ctx.author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
        print('param 1')
    elif len(params) == 3:
        server = ctx.guild
        server_id = params[0]
        voice_id = params[1]
        sourse = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.channel.send(f'{author.mention}, id сервера или голосового каннала должно быть численным  ')
            return
        print('param 3')
        server = Alice.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention}, я тебя не понимаю!')
        return
    voice = discord.utils.get(Alice.voice_clients, guild = server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(Alice.voice_clients, guild=server)
        
    if sourse == None:
        pass
    elif sourse.startswith('http'):
        if not check_domains(sourse):
            await ctx.channel.send(f'{author.mention}, Твоя ссылка не разрешена для использования напиши Wolfrik#8341!')
            return
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
        except PermissionError:
            await ctx.channel.send('Недостаточно прав для удаления файла!')
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': "mp3",
                    'preferredquality': '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sourse])
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio('song.mp3'))
    else:
        voice.play(discord.FFmpegPCMAudio(f'music/{sourse}'))

#комманда для разработки бота
@Alice.command()
@commands.has_permissions( administrator = True )
async def ctx( ctx ):
    print(ctx)
    
#комманда для помощи по коммандам
@Alice.command()
async def help(ctx, listcommand = None):
    embed=discord.Embed(title="Мои комманды", description="для использования подробности о комманде или странице используйте .help <Комманда или страница>", color=0x7f7f7f)
    embed.add_field(name=".help", value="Комманда для списка всех комманд", inline=False)
    embed.add_field(name=".ban", value="Комманда для бана пользователя", inline=False)
    embed.add_field(name=".kick", value="Комманда для кика пользователя", inline=False)
    embed.add_field(name=".clear", value="Комманда для очистки чата", inline=False)
    embed.add_field(name=".mute", value="Комманда для мута пользователя", inline=False)
    embed.add_field(name=".play", value="Комманда для проигрывания музыки", inline=False)
    embed.add_field(name=".tempmute", value="Комманда для временного мута пользователя", inline=False)
    embed.add_field(name=".embed", value="embed <""Название""> <""Описание""> <Ссылка на картинку>")
    embed.set_footer(text="Alice 2022")
    await ctx.send(embed=embed)
    
@Alice.command()
@commands.has_permissions( administrator = True )
async def embed( ctx, code):
    await ctx.channel.purge( limit=1)
    await ctx.send(embed=code)
    #else
    
@Alice.command()
async def leave(ctx):
    await ctx.channel.purge( limit=1)
    global server, name_channel
    voice = discord.utils.get(Alice.voice_clients, guild=server)
    if voice.is_connected():
        await voice.disconnect()
    else:
        embed=discord.Embed(title="Я не подключена!", description="Ошибка,я не подключена к голосовому каналу будь внемателен!")
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.channel.send(embed=embed)
        
@Alice.command()
async def pause(ctx):
    await ctx.channel.purge( limit=1)
    voice = discord.utils.get(Alice.voice_clients, guild=server)
    if voice.is_playing():
        voice.pause()
    else:
        embed=discord.Embed(title="Я и так не проигриваю музыку!", description="Ошибка,я не проигрываю музыку!")
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.channel.send(embed=embed)
    
@Alice.command()
async def resume(ctx):
    await ctx.channel.purge( limit=1)
    voice = discord.utils.get(Alice.voice_clients, guild=server)
    if voice.is_paused():
        voice.resume()
    else:
        embed=discord.Embed(title="Я не могу продолжить прослушивание!", description="Ошибка,я не могу продолжить по причине того что я и так проигрываю или не играю музыку!")
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.channel.send(embed=embed)
        
@Alice.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=server)
    voice.stop()
    
@Alice.command()
async def skip(ctx):
    await ctx.channel.purge( limit=1)
    voice = discord.utils.get(bot.voice_clients, guild=server)
    if voice.is_playing():
        voice.skip()
    else:
        embed=discord.Embed(title="Я не могу пропустить проигрывание!", description="Ошибка,я не могу пропустить проигрывание по причине того что я не играю музыку!")
        embed.set_author(name="Alice", icon_url="https://i.ytimg.com/vi/pl8Fh9dK_54/sddefault.jpg")
        embed.set_footer(text="Alice 2022")
        await ctx.channel.send(embed=embed)
        
@Alice.command()
async def volume(ctx, volume_arg):
    await ctx.channel.purge( limit=1)
    if voice.is_playing():
        voice.sourse.volume(volume_arg)
    else:
        return

    
Alice.run('')
