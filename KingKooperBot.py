# DiscordBotTesting.py
import os
import random
import json
import math
import asyncio
import datetime

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

item_dict = {}
item_list = [

    ['See Message History', 1000],
    ['Fishing Minigame', 2000],
    ['More Luigi Dialogue', 500],
    ['Unlock !Waluigi', 500],
    ['Unlock !Wario', 500],
    ['Unlock !Yoshi', 500],
    ['Unlock !Peach', 500],
    ['Unlock !Toad', 500],
    ['Free Boots', 5000],
    ['Big Spender Badge', 10000]
]

for i in range(len(item_list)):
    item_dict[item_list[i][0]] = item_list[i][1]


deposeBoots = False
bootNumber = 16
magic_number = random.choice(number_choices)

revolution_key = 'Invokers'
revolution_complete = False
scorekeeping_key = 'Scorekeeping'
user_key = 'username'
coin_key = 'coins'
bet_key = 'bet'
magic_word_key = 'Magic_word_counter'
inv_key = 'Inventory'
store_key = 'Shop'
loan_owing_key = 'Loan Owing'
loan_owed_key = 'Loan Owed'

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

def searchInListofDicts(value, list_of_dicts) -> bool:
    varCheck = False
    index = 0
    index_snapshot = 0
    for d in list_of_dicts:
        for key in d:
            if d[key] == value:
                varCheck = True
                index_snapshot = index
        index += 1
    return varCheck, index_snapshot

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

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

    def initialize_values(self, user:discord.Member) -> None:
        counter_json = self.load_data()
        user_value = user.global_name
        id_key = str(user.guild.id) + '_' + str(user.id)

        if scorekeeping_key not in counter_json: #initializing
            counter_json[scorekeeping_key] = {} #the value of the scorekeeping_key is a list
        
        if id_key not in counter_json[scorekeeping_key]:
            counter_json[scorekeeping_key][id_key] = {}

        if user_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][user_key] = user_value
        
        if coin_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][coin_key] = 20
        
        if bet_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][bet_key] = 0
        
        if magic_word_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][magic_word_key] = 0
        
        if inv_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][inv_key] = []

        if loan_owing_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][loan_owing_key] = []

        if loan_owed_key not in counter_json[scorekeeping_key][id_key]:
            counter_json[scorekeeping_key][id_key][loan_owed_key] = []

        if revolution_key not in counter_json: 
            counter_json[revolution_key] = []
        
        if store_key not in counter_json:
            counter_json[store_key] = item_dict
            
        self.save_data(counter_json)

    def update_coins(self, user: discord.Member) -> int:
        #for all money needs
        id_key = str(user.guild.id) + '_' + str(user.id)
        wahooboard.initialize_values(user)
        counter_json = self.load_data()
        user_coins = counter_json[scorekeeping_key][id_key][coin_key]
        list_owing = counter_json[scorekeeping_key][id_key][loan_owing_key]
        list_owed = counter_json[scorekeeping_key][id_key][loan_owed_key]
        self.save_data(counter_json)
        return user_coins, list_owing, list_owed
        
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

    def high_score(self) -> list:
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
    
    def loan_coins(self, giver: discord.Member, receiver: discord.Member, amount:int, interest_rate, time) -> None:
        wahooboard.initialize_values(giver) 
        wahooboard.initialize_values(receiver) #initialize values for the giver and receiver if they haven't done so already
        giver_id_key = str(giver.guild.id) + '_' + str(giver.id)
        giver_username = giver.global_name
        receiver_id_key = str(receiver.guild.id) + '_' + str(receiver.id)
        receiver_username = receiver.global_name
        payback = math.ceil(amount * interest_rate)
        dict_owing = { #you owe to the giver
            'id': giver_id_key,
            'username': giver_username,
            'total': amount + payback #the amount you owe to the original giver
        }
        dict_owed = { #what is owed to you
            'id': receiver_id_key,
            'username': receiver_username,
            'total': amount + payback, #the amount you are owed from the original receiver
            'Loan Issued': str(time)
        }
        counter_json = self.load_data()
        counter_json[scorekeeping_key][giver_id_key][coin_key] -= amount
        counter_json[scorekeeping_key][receiver_id_key][coin_key] += amount
        
        (user_found_owed, index_owed) = searchInListofDicts(dict_owed['id'], counter_json[scorekeeping_key][giver_id_key][loan_owed_key])
        (user_found_owing, index_owing) = searchInListofDicts(dict_owing['id'], counter_json[scorekeeping_key][receiver_id_key][loan_owing_key])


        if user_found_owed:
            counter_json[scorekeeping_key][giver_id_key][loan_owed_key][index_owed]["total"] += dict_owed['total']
            counter_json[scorekeeping_key][giver_id_key][loan_owed_key][index_owed]["Loan Issued"] = dict_owed['Loan Issued']
        else:
            counter_json[scorekeeping_key][giver_id_key][loan_owed_key].append(dict_owed)

        if user_found_owing:
            counter_json[scorekeeping_key][receiver_id_key][loan_owing_key][index_owing]["total"] += dict_owing['total']
        else:
            counter_json[scorekeeping_key][receiver_id_key][loan_owing_key].append(dict_owing)

        self.save_data(counter_json)

    def check_time(self, user: discord.Member, other_user, time) -> bool:
        id_key = str(user.guild.id) + '_' + str(user.id)
        wahooboard.initialize_values(user)
        counter_json = self.load_data()
        (user_found_owed, index_owed) = searchInListofDicts(other_user, counter_json[scorekeeping_key][id_key][loan_owed_key])
        timestamp = counter_json[scorekeeping_key][id_key][loan_owed_key][index_owed]['Loan Issued']
        time_remaining = 0
        if timestamp != None:
            #convert string into actual timestamp objects
            olddt = datetime.datetime.fromisoformat(timestamp)
            if time > olddt + datetime.timedelta(days=1):
               enoughTimePassed = True
            else:
              time_remaining = olddt + datetime.timedelta(days=1) - time
              enoughTimePassed = False
        else:
            enoughTimePassed = True
            counter_json[scorekeeping_key][id_key][loan_owed_key][index_owed]['Loan Issued'] = str(time)

        self.save_data(counter_json)
        return enoughTimePassed, time_remaining

    def payoff_loan(self, owed_user: discord.Member, ower_user: discord.Member, amount) -> None:
        owed_id_key = str(owed_user.guild.id) + '_' + str(owed_user.id)
        ower_id_key = str(ower_user.guild.id) + '_' + str(ower_user.id)
        counter_json = self.load_data()

        (user_found_ower, index_ower) = searchInListofDicts(ower_id_key, counter_json[scorekeeping_key][owed_id_key][loan_owed_key])
        (user_found_owed, index_owed) = searchInListofDicts(owed_id_key, counter_json[scorekeeping_key][ower_id_key][loan_owed_key])

        counter_json[scorekeeping_key][owed_id_key][coin_key] += amount
        counter_json[scorekeeping_key][ower_id_key][coin_key] -= amount
        #delete both records
        del counter_json[scorekeeping_key][owed_id_key][loan_owed_key][index_ower]
        del counter_json[scorekeeping_key][ower_id_key][loan_owing_key][index_owed]

        self.save_data(counter_json)

    def luigi_freedom(self, user: discord.Member) -> None:
        id_key = str(user.guild.id) + '_' + str(user.id)
        counter_json = self.load_data()
        counter_json[scorekeeping_key][id_key][coin_key] -= 1000
        self.save_data(counter_json)

    def update_counter(self, member: discord.Member) -> None:
        key2 = str(member.global_name)
        wahooboard.initialize_values(member)
        id_key = str(member.guild.id) + '_' + str(member.id)
        counter_json = self.load_data()
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
                (current_coins, list_owing, list_owed) = wahooboard.update_coins(message.author)
                if current_coins <= 0:
                    if random.randint(1, 100) < 39:
                        coin_num = random.randint(5, 15)
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
        await ctx.send("-# Bahaha, I don't know that command. Try another!")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("-# Hey, I need more info for this command!")

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

@bot.command(name='help')
async def _help(ctx):
    msg_value1 = '!help \n\n !Kooper \n\n !Mario \n\n !Luigi \n\n !jail \n\n !escape \n\n !K█Pr██oco█ \n\n !leaderboard \n\n !loaninfo'
    msg_value2 = 'Cries out for help \n\n Talk to King Kooper \n\n Talk to Mario \n\n See Luigi \n\n News about jail! \n\n How to leave peacfully! \n\n ṅ̶̩t̶̨̓r̷͙̎y̸̡͐e̴̠̒ ̴̥̈́ẽ̵̩r̷͕̍t̴̜͝ḏ̴̏c̸͕͝r̶͎͑u̵̞̿o̵̻͆p̶͙̆ \n\n Rise to the top! \n\n Get Money Quick!'

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
        (user_coins, list_owing, list_owed) = wahooboard.update_coins(ctx.author)
        await ctx.send('https://ssl-forum-files.fobby.net/forum_attachments/0050/0979/KooperJack.jpg')
        await ctx.send('-# Welcome to Koopers Table. You have ' + str(user_coins) + ' Mario Coins!')
        await ctx.send('-# Check your coins with *!coins* and place a bet with *!bet (number)*')

@bot.command(name='bet')
async def _bet(ctx, bet):
    if ctx.channel.name == 'mario-hell':
        try:
            int_bet = int(bet)
        except ValueError:
            await ctx.send('-# Hey, we only work with numbers here!')
            return
        
        member = ctx.author.global_name
        (user_coins, list_owing, list_owed) = wahooboard.update_coins(ctx.author)

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
    
@bot.command(name ='stay')
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
        (user_coins, list_owing, list_owed) = wahooboard.update_coins(ctx.author)
        if user_coins > 0:
            await ctx.send('-# ' + str(member) + ': Welcome to KooperBank! You have ' + str(user_coins) + ' Mario Coins!')
            if list_owing: #check if the list is empty
                total_amount_owing = 0
                owing_string = ''
                for i in list_owing:
                    for key in i:
                        if key == 'total':
                            total_amount_owing += i[key]
                    owing_string += f"- You owe {i["username"]} {i["total"]} Mario Coins\n"
                await ctx.send(f'-# {member}: **Owing:**\n{owing_string}')
            if list_owed:
                #loop through all entries and get total amount owed
                total_amount_owed = 0
                owed_string = ''
                for i in list_owed:
                    for key in i:
                        if key == 'total':
                            total_amount_owed += i[key]
                    owed_string += f"- {i["username"]} owes you {i["total"]} Mario Coins\n"
                await ctx.send(f'-# {member}: **Owed:**\n{owed_string}')
            await ctx.send(f'-# {member}: In total you owe {total_amount_owing} Mario Coins, and are owed {total_amount_owed} Mario Coins!')
        else:
            await ctx.send('-# ' + str(member) + ': Uh oh! You have ' + str(user_coins) + ' Mario Coins!')
            await ctx.send('-# ' + str(member) + ': Please appeal to Kooper for mercy by typing \"Oh boy do I love Kooper\", and he may take pity on you!')

@bot.command(name='bail')
async def _bail(ctx): 
    if ctx.channel.name == 'mario-hell':
        if ctx.author.global_name != 'Boots':
            await ctx.send('-# ' + 'Would you like to bail yourself out with 1,000 Mario Coins? Use !LuigiFreedom to pay the King his due')
        else:
            await ctx.send('-# ' + 'Would you like to bail yourself out with 10,000 Mario Coins? Use !LuigiFreedom to pay the King his due')

@bot.command(name='LuigiFreedom')
async def _LuigiFreedom(ctx):
    if ctx.channel.name == 'mario-hell':
        (user_coins, list_owing, list_owed) = wahooboard.update_coins(ctx.author)
        if ctx.author.global_name != 'Boots':
            if user_coins >= 1000:
                member = ctx.author
                wahooboard.luigi_freedom(ctx.author)
                await ctx.send('# LUIGI FREEDOM IS HERE!')
                await member.add_roles(role3) #starman jr.
                await member.add_roles(role5) #mario heaven
                await member.remove_roles(role4) #mario pain
            else:
                await ctx.send('-# ' + 'You do not have the Mario Coins to buy Luigi Freedom')
        else:
            if user_coins >= 10000:
                member = ctx.author
                wahooboard.luigi_freedom(ctx.author)
                await ctx.send('# LUIGI FREEDOM IS HERE!')
                await member.add_roles(role3) #starman jr.
                await member.add_roles(role5) #mario heaven
                await member.remove_roles(role4) #mario pain
            else:
                await ctx.send('-# ' + 'You do not have the Mario Coins to buy Luigi Freedom, and you never will.')

@bot.command(name='leaderboard')
async def _leaderboard(ctx):
    if ctx.channel.name == 'mario-hell':
        #search the thing for the top 10
        high_score_list = wahooboard.high_score(ctx.author)
        counter = 1
        msg_value1 = ''
        for k, v in high_score_list:
            msg_value1 += '#' + str(counter) + '. ' + str(k) + ': ' + str(v) + ' Mario Coins \n'
            counter += 1
            if counter >= 11:
                break

        msg = discord.Embed(
            title = 'Casino Leaderboard',
            colour = discord.Colour.dark_green()
        )
        msg.add_field(name='High Scores: \n', value=msg_value1, inline=True)
        msg.set_author(name='King Kooper', icon_url='https://ssl-forum-files.fobby.net/forum_attachments/0050/0976/kingkoops.png')
        await ctx.send(embed = msg)
    
@bot.command(name='loan')
async def _loan(ctx, user:discord.Member, amount, interest_rate = random.randrange(10, 49)):
    #update your coins
    if ctx.channel.name == 'mario-hell':
        (user_coins, list_owed, list_owing) = wahooboard.update_coins(ctx.author)
        try:
            interest_int = int(interest_rate)
        except ValueError:
            await ctx.send('-# Hey, we only work with numbers here!')
            return
        interest_rate = int(interest_rate) / 100
        try:
            amount_int = int(amount)
        except ValueError:
            await ctx.send('-# Hey, we only work with numbers here!')
            return
        
        if user == ctx.author:
            msg = '-# Good job, you trired to give coins to yourself. I hope you feel productive.'
            await ctx.send(msg)
            return
        elif user == None:
            msg = '-# Tell me who to give your coins to!'
            await ctx.send(msg)
            return

        if amount_int > user_coins:
            msg = f'-# {ctx.author.global_id}: You do not have enough Mario Coins to issue this loan!'
        elif amount_int <= 0:
            msg = f'-# {ctx.author.global_id}: Don\'t try getting smart with me buddy! Pick a better number'
        else:
            await ctx.send(f"-# {user.mention}: Do you accept this loan? Respond \"Yes\" or \"No\" in 10 seconds or forfeit this opportunity.")

            def check(m):
                return m.author.id == user.id and m.channel == ctx.channel
            
            try: #waiting 10 seconds
                response = await bot.wait_for('message', check=check, timeout=10.0) #timeout in seconds
            except asyncio.TimeoutError: #returning after timeout
                await ctx.send("-# Error: No response received within timeframe! Kooper says deal's off!")
                return
            
            if response.content.lower() not in ("yes", "yeah"): 
                return

            wahooboard.loan_coins(ctx.author, user, amount_int, interest_rate, ctx.message.created_at)
            msg = f'-# You have loaned {user.mention}: {amount_int} Mario Coins at {interest_rate}% interest! Be sure to pay it back!' 

        await ctx.send(msg)

@bot.command(name='collect')
async def _collect(ctx, user:discord.Member):
    if ctx.channel.name == 'mario-hell':
        id_key = str(user.guild.id) + '_' + str(user.id)
        (user_coins, list_owed, list_owing) = wahooboard.update_coins(ctx.author)
        (user_coins2, list_owed2, list_owing2) = wahooboard.update_coins(user)
        (debtfound, index) = searchInListofDicts(id_key, list_owing)

        if debtfound: 
            #check to see if it has been a day since last collect command was sent
            (timecheck, time_remaining) = wahooboard.check_time(ctx.author, id_key, ctx.message.created_at)
            if timecheck:
                if user_coins2 < list_owing[index]['total']:
                    #TODO: offer user to pay what they can, at an increased intrest rate on the balance left of 10%
                    msg = f"-# {user.global_name} **lacks the proper funds** to pay {list_owing[index]['total']} Mario Coins to {ctx.author.global_name}!"
                else:
                    wahooboard.payoff_loan(ctx.author, user, list_owing[index]['total'])
                    msg = f"-# {user.global_name}'s account has been debited {list_owing[index]['total']} Mario Coins to {ctx.author.global_name}!"
            else:
                #strftime doesn't work because time_remaining is a datetime.timedelta, not datetime.datetime, have to make some kind of custom function
                msg = f'-# {ctx.author.global_name}: Not so fast! You must wait at least {strfdelta(time_remaining, "{hours} hours, {minutes} minutes, and {seconds} more seconds")} before collecting!'
        else:
            msg = f'-# {ctx.author.global_name}: This user does not owe you any debts!'
        
        await ctx.send(msg)

@bot.command(name='payoff')
async def _payoff(ctx, user:discord.Member):
    if ctx.channel.name == 'mario-hell':
        id_key = str(user.guild.id) + '_' + str(user.id)
        (user_coins, list_owing, list_owed) = wahooboard.update_coins(ctx.author)
        (debtfound, index) = searchInListofDicts(id_key, list_owing)
        if debtfound: #check if ctx.author has any debts with the user
            if user_coins >= list_owing[index]['total']: #check if ctx.author has enough money to pay it off
                wahooboard.payoff_loan(user, ctx.author, list_owing[index]['total'])
                msg = f"-# {ctx.author.global_name}: Your account has been debited {list_owing[index]['total']} Mario Coins to {user.global_name}.\n Thank you for using KooperBank!"
            else:
                msg = f"-# {ctx.author.global_name}: You **lack the proper funds** to pay off your debt to {user.global_name}! Oh no!"
        else:
            msg = f"-# {ctx.author.global_name}: You do not have any debts outstanding with {user.global_name}! Good for you!"
        await ctx.send(msg)

@bot.command(name='loaninfo')
async def _loaninfo(ctx):
    msg = "-# Want to loan out a few Mario Coins to a friend? Look no further! \n- Use `!loan \"@user\" \"# of coins\"` to offer a loan! \n- When you want to collect simply use `!collect \"@user\"` \n- When you want to payoff your loan, use `!payoff \"@user\"`"
    await ctx.send(msg)

async def _shop(ctx):
    if ctx.channel.name == 'mario-hell':
        msg_value1 = ''
        msg_value2 = ''
        for k, v in item_list:
            msg_value1 += f'{k}\n'
            msg_value2 += f'{v}\n'

        msg = discord.Embed(
            title = "Kail's Ye Olde Hell Shoppe",
            colour = discord.Colour.dark_red()
        )
        msg.add_field(name='Shoppe Selection:', value=msg_value1, inline=True)
        msg.add_field(name='Price', value=msg_value2, inline=True)
        msg.set_author(name='Kail', icon_url='https://cdn.discordapp.com/avatars/132899865062670336/b7fbaac1c733480b5fd94084b6e028e8.webp')
        await ctx.send(embed = msg)


bot.run(TOKEN)