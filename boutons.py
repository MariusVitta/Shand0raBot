import typing

import discord
from discord import Interaction

# from discord_components import Interaction

questions1 = [["Quel est le plus beau fruit du démon ?",
               ["Suna Suna no Mi", "Gomu Gomu no Mi", "Il lui retient son bras", "Ope Ope no Mi"],
               "Il lui retient son bras"],
              ["Laquelle de ces personnes n'a pas été grand corsaire ?", ["Luffy", "Law", "Jinbe", "Boa"], "Luffy"],
              ["Qui est Amiral parmi ces personnes ?", ["Kizaru, Akainu, Imu"], "Kizaru"]]


class QuizButton(discord.ui.Button):
    def __init__(self, reponse, numero, row):
        self.reponse = reponse
        self.numero = numero
        self.row = row
        super().__init__(style=discord.ButtonStyle.blurple, label=reponse, row=row)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: Quiz = self.view

        if questions1[self.numero][2] == self.reponse:  # Ici c'est la condition où c la bonne réponse
            await interaction.response.send_message("Bonne réponse ! :D")
            view.stop()
        else:
            await interaction.response.send_message("Mauvaise réponse ! :/")

        # view.stop()  # ça ça arrête la view donc c pas ce que yung voulait faire, je te laisse chercher


class Quiz(discord.ui.View):
    children: typing.List[QuizButton]

    def __init__(self, numero):
        self.numero = numero
        super().__init__()

        for i in range(len(questions1[numero][1])):
            self.add_item(QuizButton(questions1[numero][1][i], numero, i))