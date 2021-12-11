import asyncio
import random

from config import *

"""
global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, partieEnCours
pointsTeam2 = 0
pointsTeam1 = 0
numeroJeu = 0
tabQuestions = questions"""

""" Méthode d'initialisation des variables globales.

"""


async def initVar():
    global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, valTeam1, valTeam2, tabPlayer
    pointsTeam2, pointsTeam1, numeroJeu = 0, 0, 0
    tabQuestions = questions["One Piece"]
    random.shuffle(tabQuestions)
    valTeam1, valTeam2 = "", ""


""" Méthode de mise à jour du score actuel.

    Parameters
    ----------
    messageAuthor : Any
        une tuple de plusieurs arguments sur l'auteur du message

"""


async def calculPoints(messageAuthor):
    global pointsTeam2, pointsTeam1, valTeam1, valTeam2
    if tabRole[indiceEquipe1].lower() in [y.name.lower() for y in messageAuthor.roles]:
        pointsTeam1 += 1
        valTeam1 = " :```diff\n+ "
        valTeam2 = " :``` "
    else:
        pointsTeam2 += 1
        valTeam1 = " :``` "
        valTeam2 = " :```diff\n+ "

    return


""" Méthode d'affichage du score final.
    affiche le resultat dans un embed
    
"""


async def printWinners():
    channel = client.get_channel(idChannel)

    descriptionWinners = "🏆  Vainqueur\n\n"
    if pointsTeam2 > pointsTeam1:
        vainqueurs = foxyBoutonBlanc + "` " + str(pointsTeam2) + " points`" + medaillePremier
        perdants = mugiBoutonBlanc + "` " + str(pointsTeam1) + " points`" + medailleSecond
    else:
        vainqueurs = mugiBoutonBlanc + "` " + str(pointsTeam1) + " points`" + medaillePremier
        perdants = foxyBoutonBlanc + "` " + str(pointsTeam2) + " points`" + medailleSecond

    embed = discord.Embed(
        title=titreDBV,
        description=descriptionWinners + vainqueurs + "\n\n" + perdants,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)
    pass


""" Méthode d'affichage du score actuel pour les equipes.

    Parameters
    ----------
    numEpreuve : int
        numéro de l'épreuve en cours
    
"""


async def printScore(numEpreuve: int):
    channel = client.get_channel(idChannel)
    descriptionScore = tabTextEpreuve[numEpreuve] + "\n\n" + \
                       tabEmoji[0] + \
                       "\n" + \
                       tabRoleBold[0] + "\n" \
                                        "`Score :" + str(pointsTeam1) + "` \n\n" + \
                       tabEmoji[1] + \
                       "\n" + \
                       tabRoleBold[1] + "\n" \
                                        "`Score :" + str(pointsTeam2) + "` \n"
    embed = discord.Embed(
        title=titreDBV,
        description=descriptionScore,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)
    pass


""" Méthode d'affichage de l'ensemble des joueurs

    
"""


async def printPlayer():
    channel = client.get_channel(idChannel)
    team1, team2 = "", ""
    print(tabPlayer)
    for player in tabPlayer[0]:
        team1 += "```" + player + "```\n"
    for player in tabPlayer[1]:
        team2 += "```" + player + "```\n"
    embed = discord.Embed(
        title=titreDBV,
        description=debutPartieDBV + \
                    tabEmoji[0] + \
                    "\n" + \
                    tabRoleBold[0] + \
                    team1 + \
                    "\n\n" + \
                    tabEmoji[1] + \
                    "\n" + \
                    tabRoleBold[1] + \
                    team2,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


""" Méthode principale du jeu.

    Parameters
    ----------
    numeroJeu : int
        Numéro du jeu actuel
"""


async def jeu(numeroJeu):
    channel = client.get_channel(idChannel)
    indiceTab = 0

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.

            Parameters
            ----------
            :param m tuple de plusieurs arguments sur le message

            Returns
            -------
            :return bool True si la réponse donnée est bonne et si le message a été envoye dans le bon salon
        """
        return m.content.lower() in [rep.lower() for rep in tabQuestions[numeroJeu][1]] and m.channel == channel

    for questionReponses in tabQuestions:

        # Si la question comporte plusieurs réponses possibles, on lance la question à choix multiple
        if len(questionReponses[indiceReponses]) > 1:
            return

        else:
            embed = discord.Embed(
                title="Question " + str(indiceTab + 1) + " | " + tabEpreuves[numeroJeu],
                description=carreBlanc + questionReponses[indiceQuestion],
                color=colorEmbedWhiteDBV
            )
            await channel.send(embed=embed)

            # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
            try:
                message = await client.wait_for("message", timeout=20, check=checkMessage)

            # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
            except asyncio.TimeoutError:
                reponse = questionReponses[indiceReponses][0]
                embed = discord.Embed(
                    title=timeout,
                    description=reponseText + "`" + str(reponse) + "`",
                    color=colorEmbedTimeout
                )
                await channel.send(embed=embed)

                if indiceTab != len(tabQuestions) - 1:
                    await nextQuestion()
                elif numeroJeu != (len(tabEpreuves) - 1):
                    await nextEpreuve()
                indiceTab += 1

            # sinon on met à jour les points de l'equipe qui a marqué un point,
            # on affiche l'auteur du bon message dans un
            # embed et les points des equipes
            else:
                await calculPoints(message.author)
                reponse = questionReponses[indiceReponses][0]
                embed = discord.Embed(
                    title=pointVert + str(message.author.name) + textGoodAnswer + "\n\n",
                    description=reponseText + "`" + str(reponse) + "`\n\n" +
                                carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
                        pointsTeam1) + " points``` \n\n" + \
                                carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
                        pointsTeam2) + " points``` \n\n",
                    color=colorEmbedGoodAnswer,
                )
                await channel.send(embed=embed)

                if indiceTab != len(tabQuestions) - 1:
                    await nextQuestion()
                elif numeroJeu != (len(tabEpreuves) - 1):
                    await nextEpreuve()
                indiceTab += 1

    return


""" Methode d'attente entre 2 questions.

"""
async def nextQuestion():
    await asyncio.sleep(delaiEntreQuestions)
    await printEmbedNextQuestion()
    await asyncio.sleep(delaiEntreQuestions)


""" Methode d'attente entre 2 épreuves.

"""


async def nextEpreuve():
    await asyncio.sleep(delaiEntreEpreuves)
    await printEmbedNextEpreuve()
    await asyncio.sleep(delaiEntreEpreuves)


""" Methode d'affichage des messages du jeu.

"""


async def printEmbedNextEpreuve():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="Epreuve suivante",
        description="▫️ (Nom de l'épreuve)",
        color=discord.Color.blue()
    )
    await channel.send(embed=embed)


""" Methode d'affichage des messages du jeu.

"""


async def printEmbedNextQuestion():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="Prochaine question",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


""" Methode d'affichage des messages du jeu.

"""


async def printEmbedDebutPartie():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="La partie va démarrer",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


""" Methode de lancement du jeu.
    initialise les variables et lance l'ensemble des jeux

"""


async def lancerJeux():
    await initVar()
    global numeroJeu, partieEnCours, pointsTeam1, pointsTeam2
    await printPlayer()
    await asyncio.sleep(3)
    await printEmbedDebutPartie()

    for numeroJeu in range(3):
        # JEU 1
        await jeu(numeroJeu)

        # on patiente 3 secondes après l'affichage des scores
        await asyncio.sleep(3)

    pointsTeam2 = 0
    pointsTeam1 = 0
    await printWinners()
    partieEnCours = False
