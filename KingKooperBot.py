# DiscordBotTesting.py
import os
import random
import json
import math

import discord
from dotenv import load_dotenv
from discord.ext import commands
from typing import List, Dict, Tuple
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
Magic_Words = [
    'wahoo',
    'oohaw',
    'yahoo',
    'oohay',
    'yipee',
    'Kooper Revolution',
    'oh boy do i love kooper',
]
random.seed()
number_choices = [ #must be less than 400 because discord only lets you type 2,000 characters in a single message
    16,
    50, 
    64, 
    65, 
    70, 
    100, 
    120, 
    121, 
    150, 
    240,
]

mercy_choices = [
    '-# No',
    '-# You gotta be kidding me',
    '-# Why should I?',
    '-# No way',
    '-# Ain\'t gonna happen',
    '-# Go bug someone else',
]

kooper_revolution_traitors = [
    'maxwell',
    'boots',
]

deposeBoots = False
bootNumber = 16
magic_number = random.choice(number_choices)

revolution_key = 'Invokers'
invoker = ''
revolution_complete = False
scorekeeping_key = 'Scorekeeping'
user_key = 'username'
coin_key = 'coins'
bet_key = 'bet'
magic_word_key = 'Magic_word_counter'

games = {}

def calculate_hand(hand) -> int:

        aces = hand.count(11)
        total = sum(hand)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total    

def valsort(val):
    return val[1]

class WahooBoard:
    num_of_words_found = 0
    met_requirement = False
    def __init__(self, file_path='./KingKooper/counter.json'):
            self.file_path = file_path

    def load_data(self) -> Dict[str, int]:
        with open(self.file_path, 'r') as counter_file:
            return json.load(counter_file)
    
    def save_data(self, data: Dict[str, int]) -> None:
        with open(self.file_path, 'w') as counter_file_write:
            json.dump(data, counter_file_write, indent=4)

    def update_coins(self, user: discord.Member) -> int:
        #for blackjack
        counter_json = self.load_data()
        user_value = user.global_name
        id_key = str(user.guild.id) + '_' + str(user.id)
        
        if scorekeeping_key not in counter_json: #initializing
            counter_json[scorekeeping_key] = {} #the value of the scorekeeping_key is a list
        
        if id_key not in counter_json[scorekeeping_key]: #initializing
            counter_json[scorekeeping_key][id_key] = {}
            counter_json[scorekeeping_key][id_key][user_key] = user_value
            counter_json[scorekeeping_key][id_key][coin_key] = 20
            counter_json[scorekeeping_key][id_key][bet_key] = 0
            counter_json[scorekeeping_key][id_key][magic_word_key] = 0

        user_coins = counter_json[scorekeeping_key][id_key][coin_key]
        self.save_data(counter_json)
        return user_coins
        
    def place_bet(self, user: discord.Member, bet) -> None:
        id_key = str(user.guild.id) + '_' + str(user.id)
        counter_json = self.load_data()
        counter_json[scorekeeping_key][id_key][bet_key] = bet
        counter_json[scorekeeping_key][id_key][coin_key] = int(counter_json[scorekeeping_key][id_key][coin_key]) - bet
        self.save_data(counter_json)

    def update_score(self, user: discord.Member, result) -> None:
        id_key = str(user.guild.id) + '_' + str(user.id)
        counter_json = self.load_data()
        if result:
            counter_json[scorekeeping_key][id_key][coin_key] += math.ceil(counter_json[scorekeeping_key][id_key][bet_key] * 2.5)
        counter_json[scorekeeping_key][id_key][bet_key] = 0
        self.save_data(counter_json)

    def coin_mercy(self, user: discord.Member, coins) -> None:
        id_key = str(user.guild.id) + '_' + str(user.id)
        counter_json = self.load_data()
        counter_json[scorekeeping_key][id_key][coin_key] = int(coins)
        self.save_data(counter_json)

    def high_score(self, user: discord.Member) -> list:
        list_pairs = []
        list_of_list_pairs = []
        counter_json = self.load_data()
        for key, value in counter_json.items():
            if key == scorekeeping_key:
                for key2, value2 in value.items():
                    name = value2.get(user_key)
                    coins = value2.get(coin_key)
                    list_pairs = [name, coins]
                    list_of_list_pairs.append(list_pairs)

        #sort the list according to the value
        list_of_list_pairs.sort(key=valsort, reverse=True)
        return list_of_list_pairs


    def luigi_freedom(self, user: discord.Member) -> None:
        id_key = str(user.guild.id) + '_' + str(user.id)
        counter_json = self.load_data()
        counter_json[scorekeeping_key][id_key][coin_key] -= 1000
        self.save_data(counter_json)


    def update_counter(self, member: discord.Member) -> None:
        key2 = str(member.global_name)
        user_value = member.global_name
        id_key = str(member.guild.id) + '_' + str(member.id)
        counter_json = self.load_data()
        if revolution_key not in counter_json: 
            counter_json[revolution_key] = []

        if scorekeeping_key not in counter_json: #initializing
            counter_json[scorekeeping_key] = {} #the value of the scorekeeping_key is a list
        
        if id_key not in counter_json[scorekeeping_key]: #initializing
            counter_json[scorekeeping_key][id_key] = {}
            counter_json[scorekeeping_key][id_key][user_key] = user_value
            counter_json[scorekeeping_key][id_key][coin_key] = 20
            counter_json[scorekeeping_key][id_key][bet_key] = 0
            counter_json[scorekeeping_key][id_key][magic_word_key] = 0

        global current_user_count 
        global first_invoke
        match channelstring:
            case 'marios-jail-non-canon':
                current_user_count = counter_json[scorekeeping_key][id_key].get(magic_word_key, 0) + WahooBoard.num_of_words_found
                counter_json[scorekeeping_key][id_key][magic_word_key] = current_user_count 

            case 'mario-purgatory':
                current_user_count = counter_json[scorekeeping_key][id_key].get(magic_word_key, 0) + WahooBoard.num_of_words_found
                counter_json[scorekeeping_key][id_key][magic_word_key] = current_user_count 

            case 'mario-hell':
                if key2 not in counter_json[revolution_key]:
                    counter_json[revolution_key].append(key2)
                    current_user_count = len(counter_json[revolution_key])
                    first_invoke = True
                else:
                    current_user_count = len(counter_json[revolution_key])
                    first_invoke = False
                    
        WahooBoard.num_of_words_found = 0
        self.save_data(counter_json)

    def reset_counter(self, member: discord.Member) -> None:
        id_key = str(member.guild.id) + '_' + str(member.id)
        counter_json = self.load_data()
        counter_json[scorekeeping_key][id_key][magic_word_key] = 0
        self.save_data(counter_json)

    async def handle_message(self, message: discord.Message) -> bool:
        if self.contains_the_word(message.content):
            self.update_counter(message.author)
            if current_user_count < 100 and current_user_count > -99:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + '/100 Wahoo\'s logged'
            elif current_user_count >= 100:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + "/100 Wahoo\'s logged \n" + "## MARIO FORGIVENESS"
                await message.author.remove_roles(role1)
                self.reset_counter(message.author)
            elif current_user_count <= -100:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + "/100 Wahoo\'s logged \n" + "### BYE BYE"
                await message.author.add_roles(role2)
                await message.author.remove_roles(role1)
                await message.author.remove_roles(role3)
                self.reset_counter(message.author)
            await message.channel.send(response) 
        await bot.process_commands(message)

    async def handle_message_ext(self, message: discord.Message) -> bool:
        if self.contains_the_word(message.content):
            self.update_counter(message.author)
            if current_user_count < 999 and current_user_count > -998:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + '/999 Yahoo\'s logged'
            elif current_user_count >= 999:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + "/999 Yahoo\'s logged \n" + "## MARIO CLEMENCY"
                await message.author.add_roles(role1)
                await message.author.remove_roles(role2)
                await message.author.add_roles(role3)
                self.reset_counter(message.author)
            elif current_user_count <= -999:
                response = '-# ' + f'{message.author}: ' + str(current_user_count) + "/999 Yahoo\'s logged \n" + "# MAMMA MIA"
                await message.author.remove_roles(role2)
                await message.author.add_roles(role4)
                self.reset_counter(message.author)
            await message.channel.send(response)
        await bot.process_commands(message)        

    async def handle_message_ext_ext(self, message: discord.Message) -> bool:
        if self.contains_the_word(message.content) and deposeBoots == False:
            if gimmeCoins:
                #only do something if you have no coins
                current_coins = wahooboard.update_coins(message.author)
                if current_coins <= 0:
                    if random.randint(1, 100) < 39:
                        coin_num = random.randint(5, 150)
                        response = '-# The King is feeling generous today... ' + str(message.author.global_name) + ', have ' + str(coin_num) + ' Mario Coins as a loan.'
                        wahooboard.coin_mercy(message.author, coin_num)
                    else:
                        response = random.choice(mercy_choices)
                else:
                    response = '-# Do not beg for what you already have!'
                await message.channel.send(response)
            else:
                #does meet the requirement
                if WahooBoard.met_requirement:
                    
                    global magic_number 
                    global number_choices
                    magic_number = random.choice(number_choices)
                    print(
                        f'{magic_number}: New Number'
                    )
                    if message.author.global_name.lower() != 'boots':
                        response = '-# ' + f'{message.author.global_name}: Exact Yipee\'s logged \n' + '## MARIO ABSOLVEMENT'
                        await message.author.add_roles(role3)
                        await message.author.add_roles(role5)
                        await message.author.remove_roles(role4)
                        await message.channel.send(response)
                    else:
                        response = '-# ' + f'{message.author.global_name}: Exact Yipee\'s logged \n' + '## NO FREEDOM FOR BOOTS'
                        await message.channel.send(response)
                else:
                    if WahooBoard.num_of_words_found < magic_number:
                        response = '-# ' + f'{message.author}: ERROR: INCORRECT # OF YIPEES logged \n' + '# ERRCODE: YAHAH'
                    elif WahooBoard.num_of_words_found >= magic_number + 1:
                        response = '-# ' + f'{message.author}: ERROR: INCORRECT # OF YIPEES logged \n' + '# ERRCODE: WOHOO'
                    await message.channel.send(response)
            
        elif self.contains_the_word(message.content) and deposeBoots == True: #if bowser revolution was stated
            global revolution_complete
            self.update_counter(message.author)
            if message.author.global_name.lower() in kooper_revolution_traitors:
                response = '-# ' + f'{message.author.global_name}' + ' has betrayed the revolution for personal gain. Invocation not registered.'
                await message.channel.send(response)  
            else:
                if current_user_count < bootNumber:
                    if first_invoke:
                        response = '-# ' + f'{message.author.global_name}' + ' has invoked the revolution \n' + '# ' + str(bootNumber - current_user_count) + ' INVOCATIONS REMAIN'
                    else:
                        response = '-# ' + f'{message.author.global_name}' + ' has already invoked the revolution \n' + '# ' + str(bootNumber - current_user_count) + ' INVOCATIONS REMAIN'
                    await message.channel.send(response)    
                else:
                    boots = await guild.fetch_member(161000873680437248)
                    if revolution_complete == False:
                        revolution_complete = True
                        response = '-# INVOCATION: ADMINISTERED \n' + '# MARIO JUSTICE - BOOTS DEPOSED'
                        await boots.add_roles(role1)
                        await boots.add_roles(role3)
                        await boots.remove_roles(role6)
                        if message.author != boots:
                            #free everyone from jail
                            await message.author.add_roles(role3)
                            await message.author.add_roles(role5)
                            #await message.author.remove_roles(role4)
                        for x in range (0, 12):  
                            await message.channel.send(response)
                            sleep(0.2)
                    else:
                        response = '# BE FREE \n' + 'https://ssl-forum-files.fobby.net/forum_attachments/0050/0973/Bowser_Revolution.png'
                        if message.author != boots:
                            await message.author.add_roles(role3)
                            await message.author.add_roles(role5)
                            #await message.author.remove_roles(role4)    
                        await message.channel.send(response)
        await bot.process_commands(message) 

    
    @staticmethod
    def contains_the_word(
            text: str
    ) -> bool:
        wordfound = False
        global gimmeCoins
        gimmeCoins = False
        global deposeBoots
        deposeBoots = False
        WahooBoard.num_of_words_found = 0
        for index, word in enumerate(Magic_Words):
            match channelstring:
                case 'marios-jail-non-canon':
                    match index:
                        case 0: #wahoo
                            if word.lower() in text.lower():
                                WahooBoard.num_of_words_found = WahooBoard.num_of_words_found + text.lower().count(word)
                                wordfound = True
                            else:
                                continue

                        case 1: #oohaw
                            if word.lower() in text.lower():
                                WahooBoard.num_of_words_found = WahooBoard.num_of_words_found - text.lower().count(word)
                                wordfound = True
                            else:
                                continue
                case 'mario-purgatory':
                    match index:
                        case 2: #yahoo
                            if word.lower() in text.lower():
                                WahooBoard.num_of_words_found = WahooBoard.num_of_words_found + text.lower().count(word)
                                wordfound = True
                            else:
                                continue

                        case 3: #oohay
                            if word.lower() in text.lower():
                                WahooBoard.num_of_words_found = WahooBoard.num_of_words_found - text.lower().count(word)
                                wordfound = True
                            else:
                                continue
                case 'mario-hell':
                    match index:
                        case 4: #yipee
                            if word.lower() in text.lower():
                                WahooBoard.num_of_words_found = text.lower().count(word)
                                print(
                                    f'# of words: {WahooBoard.num_of_words_found} '
                                    f'Magic Number: {magic_number}'
                                )
                                if text.lower().count(word) == magic_number:
                                    WahooBoard.met_requirement = True
                                    wordfound = True
                                else:
                                    WahooBoard.met_requirement = False
                                    wordfound = True
                            else:
                                continue

                        case 5: #Bowser Revolution
                            if 'kooper revolution' in text.lower():
                                wordfound = True
                                deposeBoots = True
                            else:
                                continue
                        
                        case 6: #oh boy do i love kooper
                            if word.lower() in text.lower():
                                wordfound = True
                                gimmeCoins = True
                            else:
                                continue
        return wordfound
    
wahooboard = WahooBoard()#
    
@bot.event
async def on_ready():
    global role1
    global role2
    global role3
    global role4
    global role5
    global role6
    global guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    role1 = discord.utils.get(guild.roles, name='Mario Jail')
    role2 = discord.utils.get(guild.roles, name='Mario Purgatory')
    role3 = discord.utils.get(guild.roles, name='Starman Jr.')
    role4 = discord.utils.get(guild.roles, name='Mario Pain')
    role5 = discord.utils.get(guild.roles, name='Mario Heaven')
    role6 = discord.utils.get(guild.roles, name='Starman Super')
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        f'Magic Number is: {magic_number}'
    )


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Haha, I don't know that one!")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Hey, you have to specify a number when you\'re betting!")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    
    global channelstring
    channelstring = message.channel.name
    if message.channel.name == 'marios-jail-non-canon':
        await wahooboard.handle_message(message)
    elif message.channel.name == 'mario-purgatory':
        await wahooboard.handle_message_ext(message)
    elif message.channel.name == 'mario-hell':
        if bot.user.mentioned_in(message):
            await message.channel.send('-# Hello ' + str(message.author.global_name) + '. Are you ready for what is to come?')
        else:
            await wahooboard.handle_message_ext_ext(message)
    elif message.channel.name == 'mario-centric-support-channel':
        if bot.user.mentioned_in(message):
            #Send yourself to jail
            await message.author.add_roles(role1)
            await message.author.remove_roles(role5)
            jail_messages = [
                'I\'m sending you to jail. I hope this helps!',
                'I\'m sending you to jail. Wahoo!',
                'I\'m sending you to jail. Yipee!',
                'It\'s curtains for you!',
                'I\'ve decided you belong in jail',
                'Mario Crime means Mario Time',
                'You should not have done that',
                'You should really not have done that',
            ]
            await message.channel.send('-# Hello ' + str(message.author.global_name) + '. ' + random.choice(jail_messages))


# @bot.command(name='test')
# async def _test(ctx):
#     await ctx.send("-# This is only a test")

@bot.command(name='help')
async def _help(ctx):
    msg_value1 = '!help \n\n !Kooper \n\n !Mario \n\n !Luigi \n\n !jail \n\n !escape \n\n !K█Pr██oco█ \n\n !leaderboard'
    msg_value2 = 'Cries out for help \n\n Talk to King Kooper \n\n Talk to Mario \n\n See Luigi \n\n News about jail! \n\n How to leave peacfully! \n\n ṅ̶̩t̶̨̓r̷͙̎y̸̡͐e̴̠̒ ̴̥̈́ẽ̵̩r̷͕̍t̴̜͝ḏ̴̏c̸͕͝r̶͎͑u̵̞̿o̵̻͆p̶͙̆ \n\n Rise to the top! '

    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        fullmessage = 'Welcome ' + str(caller_name) + ', \n \n' + 'Please see the list of available commands below: \n \n'
        msg = discord.Embed(
            title = 'King Kooper Hears You',
            description = ''.join(fullmessage),
            colour = discord.Colour.dark_green()
        )
        msg.add_field(name='Command', value=msg_value1, inline=True)
        msg.add_field(name='Description', value=msg_value2, inline=True)
        msg.set_author(name='King Kooper', icon_url='https://ssl-forum-files.fobby.net/forum_attachments/0050/0976/kingkoops.png')
        await ctx.send(embed = msg)


@bot.command(name='Kooper')
async def _Kooper(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'I\'m da best',
            'How is it going ' + str(caller_name) + ' ?',
            'Don\'t get any fancy ideas!',
            'We love our goombas',
            'Mario Jail is very good!',
            'Nothing else to find here!',
            'You got any coins?',
            'How about a visit to ██████████?',
            'I\'d LOVE to have all your coins',
            'I gotta get me a power star!',
            'I love equality!',
            'Make sure you follow my *protocol*!',
            'Why don\'t you go talk to Luigi or something',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg + ' - King Kooper')

@bot.command(name='Mario')
async def _Mario(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'It\'s-a-me! Mario',
            'Okey dokey!',
            'Oof!',
            'Wahaa!',
            'Mamma mia!',
            'D\'oh!',
            'Honk shoo honk shoo!',
            'Thank-a you so much for to playing my game!',
            'WoAH!',
            'WoAoOAOHAOOAHOAooOHAOHOHDH!',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg + ' - Mario Mario')

@bot.command(name='jail')
async def _jail(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'Nobody likes Mario Jail!',
            'There are no secrets in here!',
            'Did you know there is no escape from King Kooper?',
            'Please pay your pennance to King Kooper!',
            'Rumours persist of an illegal gambling ring in Hell',
            'Only King Kooper can save you!',
            'It\'s like a Mario Party in here!',
            'Nobody likes a spoilsport ' + str(caller_name) + '!',
            'Freedom is a 5 letter word!',
            'M̵̡̧̠͇͍̖̼̳̘̦̻̙͚͉͍̃̽́̇̑̈́̂͂̑̓͌̔̾̄̀ͅą̵̨͚̰͖͎͕̥̟̩̹͍̭̟̀̌͊̌͋͛͠͝ͅr̸̬͉̂͗̈̈́i̵̧͙̘̺̟̫̯̮͋͊̐̏̀̈́̈͛̆̎̔̃̐̇o̸̦̺͚͉̲̮̦̖͉̱̬̲̟̙̩̓͠ͅ ̵̡̮̖̮͙̽̉̈́̄́͒̊̒͒͒̌̀̀̚̚Ṕ̴̜̪͇͠a̸̰̞̼͙̤̞͇̗̅͝r̷̢̨̫̩̤̳̱͓̮̳̩̖͔͉͐ṯ̶͖̞̖̦̗̼̟͔̥̋̑̓̊̑͆̎̋͑͐̒̓̈́̄͌̚͝y̷͚̆̾̀̃̈̐͐͠',
            'Ẹ̸̗̤̹̣͕̮͍͉̪̫̮͎̞̈́̏̓̒̎̄̃̈́ͅṞ̷̛̊̈̾̎͋́́̔̊̿R̷̢̨͚̣͎̠̺͇̯̼̪̫͖̝̞͖̀̓̎̏̓̋͐̈́͆̔̐̽̏́̓͂ͅŌ̶̢̳̪̩͍͍̟͈̼̟̏͂̓̀̇̿̈́̎͒̔̕R̵̡̨̞͍̱̭͓̰̄̅̄͂̿̾̍̌́̔͑̂̀̈̄̐̚:̶̡̛̦͕͚͂͑͐̋̾̈́̓͘̕͝͠ ̸̛͓͇̖̰̼̥̪3̸̹̭͉̞̼̲̦͙̍̏́̌̆͌̇̈̑͗̆́͊̚͜͝͝Ņ̸͔̤̙̳̯̣͛̈́͊̽̍̓͗́͌̌͘7̸̨͈͉̯̙̻͉̝̮͊̈́͑̀̎̒͆͌̄͘͘͘R̶̺̪̳̜͂̑̂̈́̓͊́̈́́̆̏͝Y̶̧̨̬͕̫͖͓̫̥̩͕̬͕̪̯̳̑̀̑̏̽̉́͆̽͛̽͝͝ ̵̧̧̦͙̆̿D̸̝̙̘̳̾̈̈́͒́͐͋̓̍̆̾̔̕͝͝3̸̖̑̑͌͒̐͜L̸͉̱̖͙̣͍̠̔̿͂̈́̿͒͆͂̈́͘3̷̛̛̼̗̞͎͕͓̝̼̼̮̬͎͗̉̊̑̄̍̈́͑͂͋̄̚͘͝7̷͚̰́̈̇̊̀͒̿̆̔̇̆̂̏̔̚̕͝3̵͎̝͈͎̩̟̥̖̦̦͑̀̏̄̔͘͠Ḑ̸̢̛͕͚̘͎̘̳͖̺̖̉̍̎̀̈́͊͗̋̏͋͑̀͑͘̕͜͝',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg + ' - Jail Facts')
    elif ctx.channel.name == 'mario-centric-support-channel':
        #Send yourself to jail
        member = ctx.author
        await member.add_roles(role1)

@bot.command(name='escape')
async def _escape(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'The best way to escape is to pay the price!',
            'Find the right number of freedom words to escape!',
            'I believe in you, ' + str(caller_name) + '!',
            'Don\'t keep the King waiting!',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg + ' - A Message from your Warden')

@bot.command(name='Luigi')
async def _Luigi(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'Hello ' + str(caller_name) + '!',
            'Would you like to know my secret?',
            'It\'s-a me! Luigi!',
            'How about a game of !Ko███rJ██k?',
            'Wa-hey!',
            'Wa-ha!',
            'Owie!',
            'Let\'s-a go!',
            'Luigi Time!',
            'I work at the Casino!',
            'We\'re-a gonna be best friends!',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg + ' - Luigi Mario')

@bot.command(name='secret')
async def _secret(ctx):
    if ctx.channel.name == 'mario-hell':
        caller_name = ctx.author.global_name
        message_choices = [
            'It\'s never that easy, ' + str(caller_name),
            'Go talk to Luigi',
            'Investigate thoroughly',
        ]
        msg = random.choice(message_choices)
        await ctx.send('-# ' + msg)

@bot.command(name='KRProtocol')
async def _KRProtocol(ctx):
    if ctx.channel.name == 'mario-hell':
        await ctx.send('-# WARNING: INVOKING KRProtocol CAN **NOT** BE UNDONE!')
        await ctx.send('-# WARNING: CONTINUE AT OWN RISK')
        await ctx.send('-# WARNING: WOULD YOU FORSAKE HEAVEN? FOR THE **██████ RE█O██T██N**?')

@bot.command(name='KooperJack')
async def _KooperJack(ctx):
    if ctx.channel.name == 'mario-hell':
        user_coins = wahooboard.update_coins(ctx.author)
        await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0979/KooperJack.jpg')
        await ctx.send('-# Welcome to Koopers Table. You have ' + str(user_coins) + ' Mario Coins!')
        await ctx.send('-# Check your coins with *!coins* and place a bet with *!bet (number)*')

@bot.command(name='bet')
async def _bet(ctx, bet):
    if ctx.channel.name == 'mario-hell':
        try:
            int_bet = int(bet)
        except ValueError:
            await ctx.send('-# Hey we only work with numbers here!')
            return
        
        member = ctx.author.global_name
        user_coins = wahooboard.update_coins(ctx.author)

        if user_coins > 0:
            if int_bet > user_coins:
                await ctx.send('-# Bahaha! You cannot bet that many coins! Try again.')
                return
            elif int_bet <= 0:
                await ctx.send('-# A wise guy eh? That won\'t fly here in Mario Hell. Try again.')
                return
            else:
                #call a function to update the coin counter and store a bet variable
                wahooboard.place_bet(ctx.author, int_bet)
                await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0982/KooperJack2.gif')
        
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
            random.shuffle(deck)
            #function to initialize coins/get coins below
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            if calculate_hand(player_hand) == 21:
                result = True
                wahooboard.update_score(ctx.author, result)
                await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0985/KooperJack3.gif')
                await ctx.send(f'-# ' + str(member) + ': KooperJack! You win with ' + str(player_hand))
                return

            games[ctx.author.id] = (deck, player_hand, dealer_hand)
            
            await ctx.send(f'-# ' + str(member) + ': Nobody beats da boss!' + '\nYour hand: ' + str(player_hand) + '\nLuigi\'s hand: ' + str(dealer_hand[0]) + '\n\n' + '# !hit  or  !stay?')
        else:
            #call a generosity function
            await ctx.send('-# '  + str(member) + ': You\'re all out of coins! Go bother King Kooper and maybe he can help you.')

        
@bot.command(name='hit',)
async def _hit(ctx):
    if ctx.channel.name == 'mario-hell':
        deck, player_hand, dealer_hand = games[ctx.author.id]
        member = ctx.author.global_name
        player_hand.append(deck.pop())

        player_total = calculate_hand(player_hand)
        if player_total > 21:
            del games[ctx.author.id]
            result = False
            wahooboard.update_score(ctx.author, result)
            await ctx.send('-# ' + str(member) + f': You busted with {player_hand}! Too bad!')
        elif player_total == 21:
            del games[ctx.author.id]
            result = True
            wahooboard.update_score(ctx.author, result)
            await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0985/KooperJack3.gif')
            await ctx.send('-# ' + str(member) + f': You hit KooperJack with {player_hand}! You Win!')
        else:
            games[ctx.author.id] = (deck, player_hand, dealer_hand)
            await ctx.send('-# ' + str(member) + f": Your hand is now {player_hand}")
    

@bot.command(name = 'stay')
async def _stay(ctx):
    if ctx.channel.name == 'mario-hell':
        deck, player_hand, dealer_hand = games[ctx.author.id]
        member = ctx.author.global_name
        player_total = calculate_hand(player_hand)
        dealer_total = calculate_hand(dealer_hand)

        while dealer_total < 17:
            dealer_hand.append(deck.pop())
            dealer_total = calculate_hand(dealer_hand)

        del games[ctx.author.id]

        if dealer_total > 21:
            result = True
            wahooboard.update_score(ctx.author, result)
            await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0985/KooperJack3.gif')
            await ctx.send('-# ' + str(member) + f": Luigi busted with {dealer_hand}! You Win!")
        elif dealer_total > player_total:
            result = False
            wahooboard.update_score(ctx.author, result)
            await ctx.send('-# ' + str(member) + f": Luigi wins with {dealer_hand}! Too Bad!")
        elif dealer_total < player_total:
            result = True
            wahooboard.update_score(ctx.author, result)
            await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0985/KooperJack3.gif')
            await ctx.send('-# ' + str(member) + f": You win with {player_hand}!")
        else:
            result = False
            wahooboard.update_score(ctx.author, result)
            await ctx.send('-# ' + str(member) + f": Luigi has {dealer_hand}. It's a tie! The house wins anyway! TOO BAD")

@bot.command(name='coins')
async def _coins(ctx): 
    if ctx.channel.name == 'mario-hell':
        member = ctx.author.global_name
        #display your current coin count, or give out mercy coins if you have none
        user_coins = wahooboard.update_coins(ctx.author)
        if user_coins > 0:
            await ctx.send('-# ' + str(member) + ': Welcome to KooperBank! You have ' + str(user_coins) + ' Mario Coins!')
        else:
            await ctx.send('-# ' + str(member) + ': Uh oh! You have ' + str(user_coins) + ' Mario Coins!')
            await ctx.send('-# ' + str(member) + ': Please appeal to Kooper for mercy by typing \"Oh boy do I love Kooper\", and he may take pity on you!')

@bot.command(name='bail')
async def _bail(ctx): 
    if ctx.channel.name == 'mario-hell':
        await ctx.send('-# ' + 'Would you like to bail yourself out with 1,000 Mario Coins? Use !LuigiFreedom to pay the King his due')

@bot.command(name='LuigiFreedom')
async def _LuigiFreedom(ctx):
    if ctx.channel.name == 'mario-hell':
        user_coins = wahooboard.update_coins(ctx.author)
        if user_coins >= 1000:
            member = ctx.author
            wahooboard.luigi_freedom(ctx.author)
            await ctx.send('# LUIGI FREEDOM IS HERE!')
            await member.add_roles(role3) #starman jr.
            await member.add_roles(role5) #mario heaven
            await member.remove_roles(role4) #mario pain
        else:
            await ctx.send('-# ' + 'You do not have the Mario Coins to buy Luigi Freedom')

@bot.command(name='leaderboard')
async def _leaderboard(ctx):

    #search the thing for the top 10
    high_score_list = wahooboard.high_score(ctx.author)
    counter = 1
    msg_value1 = ''
    for k, v in high_score_list:
        msg_value1 += '#' + str(counter) + '. ' + str(k) + ': ' + str(v) + ' Mario Coins \n'
        counter += 1
        if counter >= 10:
            break

    msg = discord.Embed(
        title = 'Casino Leaderboard',
        colour = discord.Colour.dark_green()
    )
    msg.add_field(name='High Scores: \n', value=msg_value1, inline=True)
    msg.set_author(name='King Kooper', icon_url='https://ssl-forum-files.fobby.net/forum_attachments/0050/0976/kingkoops.png')
    await ctx.send(embed = msg)

# @bot.command(name='loan')
# async def _loan(ctx, user, amount, interest_rate):
#     await ctx.send('You have loaned ' + str(user) + ': ' + amount + 'Mario Coins at ' + interest_rate + ' interest! Be sure to pay it back!' )
#     pass

bot.run(TOKEN)