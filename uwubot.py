from twitchio.ext import commands
import api
import os
import asyncio
import pyautogui
import time
import random


def click(choice):
    pyautogui.moveTo(916, 978)
    if choice == "lewo":
        pyautogui.move(-300, 0)
        pyautogui.click()
        pyautogui.move(0, -200)
        pyautogui.click()
    elif choice == "prawo":
        pyautogui.move(300, 0)
        pyautogui.click()
        pyautogui.move(0, -200)
        pyautogui.click()


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=api.oauth, prefix='$',
                         initial_channels=['lewus'])
        self.counter_left = 0
        self.counter_right = 0
        self.user_voted = []
        self.voting_enabled = False

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick} to {self.connected_channels}')

    @commands.command()
    async def start(self, ctx: commands.Context):
        if ctx.author.name == ctx.channel.name:
            self.voting_enabled = True

    async def koniec(self, ctx):
        os.system('cls')
        print('WYBIERA')
        time.sleep(5)
        if self.counter_right > self.counter_left:
            click("prawo")
            ctx.send(f'Wygrało prawo {self.counter_right} do {self.counter_left}')
        elif self.counter_right < self.counter_left:
            click("lewo")
            ctx.send(f'Wygrało lewo {self.counter_left} do {self.counter_right}')
        else:
            click(random.choice(['prawo', 'lewo']))
            ctx.send('REMIS XD. Wybiera losowo.')
        self.voting_enabled = False
        await asyncio.sleep(5)
        self.user_voted.clear()
        self.counter_left = 0
        self.counter_right = 0
        self.voting_enabled = True
        await ctx.send('Można znowu głosować.')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if ctx.author.name == ctx.channel.name:
            self.voting_enabled = False

    @commands.command()
    async def lewo(self, ctx: commands.Context):
        if self.voting_enabled and ctx.author.name not in self.user_voted:
            self.user_voted.append(ctx.author.name)
            self.counter_left += 1
            os.system('cls')
            print(f'{ctx.author.name} zagłosował na lewo. \n'
                  f'Aktualna liczba głosów na lewo {self.counter_left}.\n'
                  f'Aktualna liczba głosów na prawo {self.counter_right}.\n')
            if abs(self.counter_right - self.counter_left) > 15:
                await self.koniec(ctx)
            elif self.counter_left > 25 or self.counter_right > 25:
                await self.koniec(ctx)

    @commands.command()
    async def prawo(self, ctx: commands.Context):
        if self.voting_enabled and ctx.author.name not in self.user_voted:
            self.user_voted.append(ctx.author.name)
            self.counter_right += 1
            os.system('cls')
            print(f'{ctx.author.name} zagłosował na prawo. \n'
                  f'Aktualna liczba głosów na lewo {self.counter_left}.\n'
                  f'Aktualna liczba głosów na prawo {self.counter_right}.\n')
            if abs(self.counter_right - self.counter_left) > 15:
                await self.koniec(ctx)
            elif self.counter_left > 25 or self.counter_right > 25:
                await self.koniec(ctx)



if __name__ == "__main__":
    bot = Bot()
    bot.run()
