from imports import *

questions1 = [["Quel est le plus beau fruit du démon ?",
               ["Suna Suna no Mi", "Gomu Gomu no Mi", "Il lui retient son bras", "Ope Ope no Mi"],
               "Il lui retient son bras"],
              ["Laquelle de ces personnes n'a pas été grand corsaire ?", ["Luffy", "Law", "Jinbe", "Boa"], "Luffy"],
              ["Qui est Amiral parmi ces personnes ?", ["Kizaru, Akainu, Imu"], "Kizaru"]]


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

        if self.rep == self.bonneReponse:
            await interaction.response.send_message("Bonne reponse")
            self.disabled = True
            for i in view.children:
                view.remove_item(i)
                # view.clear_items()
        else:
            await view.stop1()
            await interaction.response.send_message("Mauvaise reponse\nLa bonne réponse était: " + self.bonneReponse)




class Quiz(discord.ui.View):
    children: typing.List[QuizButton]

    def __init__(self, tabReponses, bonneReponse):
        self.tabReponses = tabReponses
        self.bonneReponse = bonneReponse
        super().__init__(timeout=20)
        for i in range(len(tabReponses)):
            self.add_item(QuizButton(tabReponses, tabReponses[i], bonneReponse, i))

    async def on_timeout(self):
        self.stop()

        print("timeout")
        return
        # await self.send("Timeout masta")

    async def stop1(self):
        for i in self.children:
            print(i)
            i.disabled = True
            self.remove_item(i)

    async def on_error(self, error: Exception, item: Item, interaction: Interaction):
        await interaction.response.send_message(str(error))
