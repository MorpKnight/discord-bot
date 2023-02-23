from asyncio import sleep
from os import getenv

import discord
import matplotlib.pyplot as plt
import numpy as np
import openai
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from dotenv import load_dotenv
from scipy.stats import linregress

load_dotenv()
openai.api_key = getenv("OPENAI")

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
        def check_len(x, y):
            if len(x) != len(y):
                return False
            else:
                return True
        check = check_len(x_table, y_table)

        x = np.array([])
        y = np.array([])

        x_table.split(" ")
        y_table.split(" ")

        x = [float(i) for i in x_table.split(" ")]
        y = [float(i) for i in y_table.split(" ")]

        slope, intercept, r_value, p_value, std_err = linregress(x, y)

        def regression_line(x):
            return slope * x + intercept
        
        x_values = x

        y_values = [regression_line(x) for x in x_values]

        plt.grid(which='both', color='k', linestyle='--', linewidth=0.5)
        plt.scatter(x, y)
        plt.plot(x_values, y_values)
        plt.savefig("plot.jpg", format="jpg")

        if intercept < 0:
            intercept_message = f"Linear formula (y): **{slope:.4f}x - {-intercept:.4f}**"
        else:
            intercept_message = f"Linear formula (y): **{slope:.4f}x + {intercept:.4f}**"

        await interaction.response.send_message(f"""Slope (b): **{slope:.4f}**
Intercept (a): **{intercept:.4f}**
Standard error of the estimate (STEYX): **{std_err:.4f}**
{intercept_message}""", file=discord.File("plot.jpg"))

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
