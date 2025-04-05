import discord
from discord.ext import commands
from discord.ui import View, Select
import os
from logs import get_logger

logger = get_logger()

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)  # O View não expira

        # Criar o seletor de opções
        select = Select(
                placeholder="Escolhe uma opção",
            custom_id="painel_gerais",
            options=[
                discord.SelectOption(label="Dumps ❓", value="opc",description="Entrega ou aquisição de dumps"),
                discord.SelectOption(label="Triggers 🔎", value="opc2", description="Compra de triggers"),
                discord.SelectOption(label="Banimentos 🚫", value="opc3", description="Avisa sobre banimentos"),
                discord.SelectOption(label="Bugs 🩹", value="opc4", description="Relata um bug encontrado"),
            ]
        )
        select.callback = self.select_callback  # Associa o callback ao seletor
        self.add_item(select)  # Adiciona o seletor à View

    async def select_callback(self, interaction: discord.Interaction):
        selected_value = interaction.data["values"][0]  # Obtém a opção selecionada

        response_messages = {
            "opc1": "Selecionaste a opção **Dúvidas ❓**.",
            "opc2": "Selecionaste a opção **Reports 🔎**.",
            "opc3": "Selecionaste a opção **Banimentos 🚫**.",
            "opc4": "Selecionaste a opção **Bugs 🩹**."
        }

        await interaction.response.send_message(response_messages.get(selected_value, "Opção inválida!"), ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()  # Aguarda até o bot estar pronto
        channel_id = 1353407889531736065
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.purge()

            # Criar o embed com as opções
            embed = discord.Embed(
                title="Ticket system",
                description="Caso queiras abrir um ticket, escolhe a opção abaixo a que mais se adequa à tua situação",
                color=discord.Color.light_embed(),
            )
            embed.add_field(name="Aviso", value=f"Antes de abrir um ticket, certifica-te de que é realmente necessário. Tickets abertos desnecessariamente poderão ter consequências!",inline=True)
            embed.set_footer(text="Ticket system | Powered by NoLife Dev Team", icon_url="https://cdn.discordapp.com/attachments/1352771477845315685/1352791135730536548/e5b4a8673da2b6cf452368c17dad4fc5.jpg?ex=67df4c6c&is=67ddfaec&hm=14e28ef11de619bd26ba489bd5167606828c897374455e92e573c353ac00c7fa&")
            await channel.send(embed=embed, view=TicketView())  # Envia o embed + menu suspenso

async def setup(bot):
    await bot.add_cog(Ticket(bot))

