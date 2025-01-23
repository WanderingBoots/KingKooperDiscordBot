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
]

class WahooBoard:
    def __init__(self, file_path='./counter.json'):
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
        current_user_count = counter_json.get(key, 0)
        counter_json[key] = current_user_count + 1
        self.save_data(counter_json)

    async def handle_message(self, message: discord.Message) -> bool:
        if self.contains_the_word(message.content):
            if current_user_count < 100:
                self.update_counter(message.author)
                response = f'{message.author} - ' + str(current_user_count) + '/100 Wahoo\'s logged'
            else:
               response = f'{message.author} - ' + str(current_user_count) + '/100 Wahoo\'s logged \n'
               'MARIO FORGIVENESS'
            await message.channel.send(response)
            #- TODO: Remove the role and reset counter
        await bot.process_commands(message)
    
    async def get_info(self, member: discord.Member) -> int:
        key = str(member.guild.id) + "_" + str(member.id)
        counter_json = self.load_data()
        return counter_json.get(key, 0)


    @staticmethod
    def contains_the_word(
            text: str
    ) -> bool:
        for word in Magic_Words:
            if word.lower() in text.lower():
                return True
            else:
                continue

        return False
    
leaderboard = WahooBoard()
    
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
 
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await leaderboard.handle_message(message)
    

bot.run(TOKEN)