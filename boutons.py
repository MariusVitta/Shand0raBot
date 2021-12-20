import discord.ui
from config import *

global tentative, dataV
tentative = []
dataV = []

load_dotenv()

GUILD = str(os.getenv('DISCORD_GUILD'))




class QuizButton(discord.ui.Button):

    def __init__(self, tabReponses, rep, bonneReponse, row):
        self.tabReponses = tabReponses
        self.bonneReponse = bonneReponse
        self.rep = rep
        self.row = row

        super().__init__(style=discord.ButtonStyle.blurple, label=rep, row=row)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: Quiz = self.view

        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        roleTeam1 = discord.utils.get(guild.roles, name=tabRole[0])
        roleTeam2 = discord.utils.get(guild.roles, name=tabRole[1])

        # verification que c'est bien un joueur
        if roleTeam1 not in interaction.user.roles and roleTeam2 not in interaction.user.roles:
            return
        if interaction.user.display_name in tentative:  # Cas où le joueur a déjà répondu
            await interaction.response.send_message("Vous avez déjà répondu ! Une seule tentative par personne.",
                                                    ephemeral=True)

        elif self.rep == self.bonneReponse or (len(tentative) + 1) == view.nbJoueurs:
            if self.rep == self.bonneReponse:  # Cas où un joueur a trouvé la bonne réponse
                for i in view.children:
                    i.disabled = True
                    if i.rep == self.bonneReponse:
                        i.style = discord.ButtonStyle.green
                    else:
                        i.style = discord.ButtonStyle.red
                await interaction.response.edit_message(view=self.view)
                dataV.extend([True, interaction.user])
                view.stop()

            else:  # Cas où tout le monde a répondu mais il n'y a pas de bonne réponse
                for i in view.children:
                    i.disabled = True
                    if i.rep == self.bonneReponse:
                        i.style = discord.ButtonStyle.green
                    else:
                        i.style = discord.ButtonStyle.red
                await interaction.response.edit_message(view=self.view)
                dataV.extend([False, None])
                view.stop()

        else:  # Cas où le joueur répond faux
            await interaction.response.send_message("Mauvaise reponse ! Vous n'avez plus de tentative.", ephemeral=True)
            tentative.append(interaction.user.display_name)


class Quiz(discord.ui.View):
    children: typing.List[QuizButton]

    def __init__(self, tabReponses, bonneReponse, nbJoueurs):
        self.tabReponses = tabReponses
        self.bonneReponse = bonneReponse
        self.nbJoueurs = nbJoueurs

        super().__init__(timeout=20.0)
        for i in range(len(tabReponses)):
            self.add_item(QuizButton(tabReponses, tabReponses[i], bonneReponse, i))

    async def on_error(self, error: Exception, item: Item, interaction: Interaction):
        await interaction.response.send_message(str(error))
