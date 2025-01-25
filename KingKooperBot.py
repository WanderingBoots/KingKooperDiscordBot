# KingKooperBot.py
import os
import random
import json

import discord
from dotenv import load_dotenv
from discord.ext import commands
from typing import List, Dict, Tuple

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
Magic_Words = [
    'wahoo',
    'oohaw',
    'yahoo',
    'demerit',
]


class WahooBoard:
    num_of_words_found = 0
    def __init__(self, file_path='./KingKooper/counter.json'):
            self.file_path = file_path

    def load_data(self) -> Dict[str, int]:
        with open(self.file_path, 'r') as counter_file:
            return json.load(counter_file)
    
    def save_data(self, data: Dict[str, int]) -> None:
        with open(self.file_path, 'w') as counter_file_write:
            json.dump(data, counter_file_write)

    def update_counter(self, member: discord.Member) -> None:
        key = str(member.guild.id) + "_" + str(member.id)
        counter_json = self.load_data()
        global current_user_count 
        match channelstring:
            case 'marios-jail-non-canon':
                current_user_count = counter_json.get(key, 0) + WahooBoard.num_of_words_found

            case 'mario-purgatory':
                current_user_count = counter_json.get(key, 0) + WahooBoard.num_of_words_found    
        counter_json[key] = current_user_count 
        WahooBoard.num_of_words_found = 0
        self.save_data(counter_json)

    def reset_counter(self, member: discord.Member) -> None:
        key = str(member.guild.id) + "_" + str(member.id)
        counter_json = self.load_data()
        counter_json[key] = 0
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
                self.reset_counter(message.author)
            await message.channel.send(response)
        await bot.process_commands(message)


    async def handle_message_ext(self, message: discord.Message) -> bool:
        if self.contains_the_word(message.content):
            self.update_counter(message.author)
            if current_user_count < 999:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + '/999 Yahoo\'s logged'
            elif current_user_count >= 999:
                response = '-# ' + f'{message.author.global_name}: ' + str(current_user_count) + "/999 Yahoo\'s logged \n" + "## MARIO CLEMENCY"
                await message.author.add_roles(role1)
                await message.author.remove_roles(role2)
                self.reset_counter(message.author)
            #elif current_user_count <= -999:
            #    response = '-# ' + f'{message.author}: ' + str(current_user_count) + "/999 Wahoo\'s logged \n" + "# MAMMA MIA"
            #    await message.author.add_roles(role3)
            #    self.reset_counter(message.author)
            await message.channel.send(response)
        await bot.process_commands(message)        

    
    @staticmethod
    def contains_the_word(
            text: str
    ) -> bool:
        wordfound = False
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

                        #case 3: #demerit
                        #    if word.lower() in text.lower():
                        #        WahooBoard.num_of_words_found = WahooBoard.num_of_words_found - text.lower().count(word)
                        #        wordfound = True
                        #    else:
                        #        continue
        return wordfound
    
    
wahooboard = WahooBoard()
    
@bot.event
async def on_ready():
    global role1
    global role2
    #global role3
    guild = discord.utils.get(bot.guilds, name=GUILD)
    role1 = discord.utils.get(guild.roles, name='Mario Jail')
    role2 = discord.utils.get(guild.roles, name='Mario Purgatory')
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
 
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
bot.run(TOKEN)