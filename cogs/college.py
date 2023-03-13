import discord
import matplotlib.pyplot as plt
import numpy as np
from discord import app_commands
from discord.ext import commands
from scipy.stats import linregress
import os

class college(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client

    @app_commands.command(name='least_square', description="Separate array using space")
    async def leastsquare(self, interaction:discord.Interaction, x_table:str, y_table:str):
        await interaction.response.defer()
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

        await interaction.followup.send(f"""Slope (b): **{slope:.4f}**
Intercept (a): **{intercept:.4f}**
Standard error of the estimate (STEYX): **{std_err:.4f}**
{intercept_message}""", file=discord.File("plot.jpg"))
        os.remove("plot.jpg")
        x = np.array([])
        y = np.array([])
        x_table = ""
        y_table = ""
        

async def setup(client):
    await client.add_cog(college(client))
