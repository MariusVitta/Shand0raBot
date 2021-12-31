from config import *

# Définition de deux variables globales qu'on utilisera dans games.py
global tentative, dataV

load_dotenv()


def initVar():
    global tentative, dataV
    tentative = []
    dataV = []


class QuizButton(discord.ui.Button):
    """
    Classe qui représente un bouton d'interface Discord
    On subclass les boutons pour pouvoir associer une fonction de callback à chacun d'eux sans problème

    ...

    Attributes
    -----
    tabReponses : list
        Tableau contenant les réponses possibles
    rep : str
        La réponse correspondant au bouton
    bonneReponse : str
        La bonne réponse à la question
    row : int
        La ligne sur laquelle s'affiche le bouton (commence à 0)

    Methods
    -----
    callback()
        Action associée au bouton créé (dépendamment de quelle réponse est sélectionnée)
    """

    def __init__(self, tabReponses, rep, bonneReponse, row):
        """
        Parameters
        -----
        tabReponses : list
            Tableau contenant les réponses possibles
        rep : str
            La réponse correspondant au bouton
        bonneReponse : str
            La bonne réponse à la question
        row : int
            La ligne sur laquelle s'affiche le bouton (commence à 0)
        """
        self.tabReponses = tabReponses
        self.bonneReponse = bonneReponse
        self.rep = rep
        self.row = row

        # Création du bouton en lui donnant sa couleur, son texte et la ligne sur laquelle il est
        super().__init__(style=discord.ButtonStyle.blurple, label=rep, row=row)

    async def callback(self, interaction: Interaction):
        """
        Fonction appelée quand on appuie sur le bouton
        Renvoie à l'utilisateur qu'il ne peut pas réponse s'il ne joue pas la session
        Renvoie à l'utilisateur qu'il a droit à une seule tentative s'il a déjà répondu
        Renvoie à l'utilisateur qu'il a faux s'il s'est trompé
        Si tout le monde a répondu ou que quelqu'un a donné une bonne réponse, on arrête la vue qui contient le bouton
        et tous les boutons sont désactivés en rouge, la bonne réponse en vert.

        Parameters
        -----
        interaction : Interaction
            L'interaction liée au message
        """
        assert self.view is not None
        view: Quiz = self.view

        # Vérification que c'est bien un joueur de la session en cours. Si ce n'en est pas un, on lui dit
        guild = interaction.guild
        roleTeam1 = discord.utils.get(guild.roles, name=tabRole[0])
        roleTeam2 = discord.utils.get(guild.roles, name=tabRole[1])
        member = guild.get_member(interaction.user.id)
        if roleTeam1 not in member.roles and roleTeam2 not in member.roles:
            await interaction.response.send_message("Vous ne pouvez pas répondre ! Vous ne jouez pas cette session.",
                                                    ephemeral=True)
            return

        # Cas où le joueur a déjà répondu
        if interaction.user.display_name in tentative:
            await interaction.response.send_message("Vous avez déjà répondu ! Une seule tentative par personne.",
                                                    ephemeral=True)

        # Cas final : soit tout le monde a répondu OU le temps est écoulé soit un joueur a trouvé la bonne réponse
        elif self.rep == self.bonneReponse or (len(tentative) + 1) == view.nbJoueurs:
            if self.rep == self.bonneReponse:  # Cas où un joueur a trouvé la bonne réponse
                for i in view.children:  # Ici on désactive tous les boutons et on le met en rouge, sauf la bonne réponse qui est mise en vert
                    i.disabled = True
                    if i.rep == self.bonneReponse:
                        i.style = discord.ButtonStyle.green
                    else:
                        i.style = discord.ButtonStyle.red
                await interaction.response.edit_message(
                    view=self.view)  # On édite le message qui contient la vue avec les boutons mis à jour
                dataV.extend([True,
                              interaction.user])  # On exporte dans dataV qu'une bonne réponse a été trouvée et le nom de celui qui a la bonne réponse
                view.stop()

            else:  # Cas où tout le monde a répondu, mais il n'y a pas de bonne réponse OU que le temps est écoulé
                for i in view.children:  # Ici on désactive tous les boutons et on le met en rouge, sauf la bonne réponse qui est mise en vert
                    i.disabled = True
                    if i.rep == self.bonneReponse:
                        i.style = discord.ButtonStyle.green
                    else:
                        i.style = discord.ButtonStyle.red
                await interaction.response.edit_message(view=self.view)
                dataV.extend([False, None])  # On exporte dans dataV que personne n'a trouvé la bonne réponse
                view.stop()

        # Cas où le joueur répond faux
        else:
            await interaction.response.send_message("Mauvaise reponse ! Vous n'avez plus de tentative.", ephemeral=True)
            tentative.append(
                interaction.user.display_name)  # On ajoute son pseudo à la liste de ceux qui ont déjà répondu, pour qu'il ne puisse pas répondre à nouveau


class Quiz(discord.ui.View):
    """
    Classe qui représente une interface Discord

    ...

    Attributes
    -----
    tabReponses : list
        Tableau contenant les réponses possibles
    bonneReponse : str
        La bonne réponse à la question
    nbJoueurs : int
        Le nombre de joueurs dans la partie

    Methods
    -----
    on_error()
        Renvoyé si une erreur se produit avec l'interface
    """
    children: typing.List[QuizButton]

    def __init__(self, tabReponses, bonneReponse, nbJoueurs):
        """
        Parameters
        -----
        tabReponses : list
            Tableau contenant les réponses possibles
        bonneReponse : str
            La bonne réponse à la question
        nbJoueurs : int
            Le nombre de joueurs dans la partie
        """
        initVar()
        self.tabReponses = tabReponses
        self.bonneReponse = bonneReponse
        self.nbJoueurs = nbJoueurs

        # On définit le timeout de l'interface, autrement dit le temps maximal pour répondre à la question
        super().__init__(timeout=20.0)

        # Pour chaque proposition de réponse, on crée le bouton correspondant à la réponse puis on les ajoute à l'interface
        for i in range(len(tabReponses)):
            self.add_item(QuizButton(tabReponses, tabReponses[i], bonneReponse, i))

    async def on_error(self, error: Exception, item: Item, interaction: Interaction):
        """
        Parameters
        -----
        error : Exception
            L'exception à l'origine de l'erreur
        item : Item
            L'item Discord lié à l'erreur s'il y en a un
        interaction : Interaction
            L'interaction liée au message d'origine
        """

        await interaction.response.send_message(str(error))
