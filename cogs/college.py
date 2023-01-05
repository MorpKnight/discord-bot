import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import numpy as np
from scipy.stats import linregress
import openai
from asyncio import sleep

openai.api_key = ""

class college(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client

    def chat(self, machine_type, creativity, prompt):
        completions = openai.Completion.create(
            engine = machine_type,
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            temperature = creativity
        )

        message = completions.choices[0].text
        return message.strip()

    @app_commands.command(name='least_square', description="Separate array using space")
    async def leastsquare(self, interaction:discord.Interaction, x_table:str, y_table:str):
        x = np.array([])
        y = np.array([])

        x_table.split(" ")
        y_table.split(" ")

        for i in x_table:
            x = np.append(x, float(i))
        for i in y_table:
            y = np.append(y, float(i))

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        if intercept < 0:
            intercept_message = f"Linear formula (y)              : {slope:.4f}x - {-intercept:.4f}"
        else:
            intercept_message = f"Linear formula (y)              : {slope:.4f}x + {intercept:.4f}"
        await interaction.response.send_message(f"""Slope (b)                       : {slope:.4f}
Intercept (a)                   : {intercept:.4f}
Standard error of the estimate  : {std_err:.4f}
{intercept_message}""")

    @app_commands.command(name="chatgpt", description="Pre-trained Chat GPT")
    @app_commands.choices(machine_type = [
        Choice(name="Davinci_002", value="text-davinci-002"),
        Choice(name="Davinci_003", value="text-davinci-003")
    ])
    async def chat_gpt(self, interaction:discord.Interaction, machine_type:Choice[str], creativity:float, msg:str):
        if machine_type.value == "text-davinci-002":
            message = self.chat(machine_type.value, creativity, msg)
        else:
            message = self.chat(machine_type.value, creativity, msg)

        await sleep(10)
        await interaction.response.send_message(message)
    

async def setup(client):
    await client.add_cog(college(client))
