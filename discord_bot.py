import googletrans
from googletrans import Translator 
import discord
import json
import os
from discord.ext import commands
import random

uchiha = ['Sakura Haruno', 'Baru Uchiha', 'Fugaku Uchiha', 'Hazuki Uchiha', 'Hikaku Uchiha', 'Inabi Uchiha', 'Itachi Uchiha', 'Izumi Uchiha', 'Izuna Uchiha', 'Kagami Uchiha', 'Kagen Uchiha', 'Madara Uchiha', 'Mikoto Uchiha', 'Naka Uchiha', 'Naori Uchiha', 'Obito Uchiha', 'Rai Uchiha', 'Sarada Uchiha', 'Sasuke Uchiha', 'Setsuna Uchiha', 'Shisui Uchiha', 'Taiko Uchiha', 'Tajima Uchiha', 'Tekka Uchiha', 'Teyaki Uchiha', 'Uruchi Uchiha', 'Yakumi Uchiha', 'Yashiro Uchiha']

#server prefixes
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

#bot joins server
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#bot removed from server
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#changing prefix
@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')
    
#command errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Not a valid command.')

#clear messages
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1) 

#clear error message
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specifiy the amount of messages you want deleted.')

#embed setup
@client.command(name='version')
async def version(context):
    
    my_embed = discord.Embed(title="Current Version", description="Bot in version 1.0", color=0x5dbcd2)
    my_embed.add_field(name="Version Code:", value="v1.0.0", inline=False)
    my_embed.add_field(name="Date Released:", value="September 4th, 2020", inline=False)
    my_embed.set_footer(text='This is a sample footer')
    my_embed.set_author(name='Justin Tran')

    await context.message.channel.send(embed=my_embed)

#bot ready
@client.event
async def on_ready():
    general_channel = client.get_channel(751612229505384562)
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Coup d'état"))
    await general_channel.send("I'm awake!")
    

#disconnect
@client.event
async def on_disconnect():
    general_channel = client.get_channel(751612229505384562)
    await general_channel.send("Powering down :(")

#joining member   
@client.event
async def on_member_join(member):
    general_channel = client.get_channel(751612229505384562)
    await general_channel.send("{} is now part of the clan.".format(member))
    
    with open('level.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    with open('level.json', 'w') as f:
        json.dump(users, f)

#kicked member
@client.event
async def on_member_remove(member):
    general_channel = client.get_channel(751612229505384562)
    await general_channel.send("{} is facing Itachi.".format(member))

#ban member
@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been put in tsukuyomi.')

#unban member
@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban in banned_users:
        user = ban.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

@client.event
async def on_message(message):
    #level updating
    if message.author.bot == False:
        with open('level.json', 'r') as f:
            users = json.load(f)
        
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('level.json', 'w') as f:
            json.dump(users, f)

    #embed details
    if message.content == 'what is the version':
        general_channel = client.get_channel(751612229505384562)

        my_embed = discord.Embed(title="Current Version", description="Bot in version 1.0", color=0x5dbcd2)
        my_embed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        my_embed.add_field(name="Date Released:", value="September 4th, 2020", inline=False)
        my_embed.set_footer(text='This is a sample footer')
        my_embed.set_author(name='Justin Tran')

        await general_channel.send(embed=my_embed)
    
    #strongest memeber
    if message.content == 'who is the strongest uchiha?':
        general_channel = client.get_channel(751612229505384562)
        
        strongest = 'Our Shadow Hokage Sasuke Uchiha.'

        await general_channel.send('https://imgur.com/d6eaoa5')
        await general_channel.send(strongest)
    
    #what member are you?
    if message.content == 'which uchiha am I?':
        general_channel = client.get_channel(751612229505384562)
        
        rand_member = random.choice(uchiha)

        await general_channel.send(rand_member)
    
    if message.content == 'what are the translation codes?':
        general_channel = client.get_channel(751612229505384562)

        translation_codes = 'Use this to communicate with your international friends in the server!'

        await general_channel.send('https://imgur.com/G0KuyXK')
        await general_channel.send(translation_codes)
    await client.process_commands(message)

#leveling system
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

#Translator
@client.command()
async def translate(ctx, lang, *, args):
    t = Translator()
    a = t.translate(args, dest=lang)
    await ctx.channel.send(a.text)

client.run('NzUxNjA4NzU0OTE4Nzg1MDY3.X1LkMw.Q2xX76D3q1ysgGSHAfajp961Kvk')
