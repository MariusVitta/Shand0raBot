import asyncio
import random
import discord

from config import *

global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, partieEnCours
pointsTeam2 = 0
pointsTeam1 = 0
numeroJeu = 0
tabQuestions = questions


async def initVar():
    global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, valTeam1, valTeam2, tabPlayer
    pointsTeam2, pointsTeam1, numeroJeu = 0, 0, 0
    tabQuestions = questions["One Piece"]
    random.shuffle(tabQuestions)
    valTeam1, valTeam2 = "", ""
    # tabPlayer = [[],[]]
    # print(tabQuestions)
    # print(tabQuestions[0][1])
    # print(tabQuestions[1])


async def calculPoints(messageAuthor):
    global pointsTeam2, pointsTeam1, valTeam1, valTeam2
    if tabRole[0].lower() in [y.name.lower() for y in messageAuthor.roles]:
        pointsTeam1 += 1
        valTeam1 = " :```diff\n+ "
        valTeam2 = " :``` "
        # channel = client.get_channel(idChannel)
        # await channel.send("Youpi")
    else:
        pointsTeam2 += 1
        valTeam1 = " :``` "
        valTeam2 = " :```diff\n+ "

    return;


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
    choix = await channel.send(embed=embed)
    pass


async def printScore(numEpreuve):
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
    choix = await channel.send(embed=embed)
    pass


async def printPlayer():
    channel = client.get_channel(idChannel)
    team1,team2 = "",""
    print(tabPlayer)
    for player in tabPlayer[0]:
        team1 += "```" + player + "```\n"
    for player in tabPlayer[1]:
        team2 += "```" + player + "```\n"
    embed = discord.Embed(
        title=titreDBV,
        description=debutPartieDBV +\
                    tabEmoji[0] +\
                    "\n"+\
                    tabRoleBold[0] +\
                    team1 + \
                    "\n\n" + \
                    tabEmoji[1] + \
                    "\n" + \
                    tabRoleBold[1] + \
                    team2,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


# règles du jeu
async def jeu(numeroJeu):
    channel = client.get_channel(idChannel)
    indiceTab = 0

    def checkMessage(m):
        return m.content.lower() in [rep.lower() for rep in tabQuestions[numeroJeu][1]] and m.channel == channel

    for questionReponses in tabQuestions:

        if len(questionReponses[indiceReponses]) > 1:
            return;

        else:
            # print(questionReponses[indiceReponses])
            # print(questionReponses[indiceQuestion])
            embed = discord.Embed(
                title="Question " + str(indiceTab + 1) + " | " + tabEpreuves[numeroJeu],
                description=carreBlanc + questionReponses[indiceQuestion],
                color=colorEmbedWhiteDBV
            )
            await channel.send(embed=embed)

            try:
                message = await client.wait_for("message", timeout=20, check=checkMessage)
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
                var = f": ```diff\n"
                await channel.send(embed=embed)

                if indiceTab != len(tabQuestions) - 1:
                    await nextQuestion()
                elif numeroJeu != (len(tabEpreuves) - 1):
                    await nextEpreuve()
                indiceTab += 1

    return;


async def nextQuestion():
    await asyncio.sleep(5)
    await printEmbedNextQuestion()
    await asyncio.sleep(5)


async def nextEpreuve():
    await asyncio.sleep(5)
    await printEmbedNextEpreuve()
    await asyncio.sleep(5)


async def printEmbedNextEpreuve():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="Epreuve suivante",
        description="▫️ (Nom de l'épreuve)",
        color=discord.Color.blue()
    )
    await channel.send(embed=embed)


async def printEmbedNextQuestion():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="Prochaine question",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def printEmbedDebutPartie():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="La partie va démarrer",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def lancerJeux():
    await initVar()
    global numeroJeu, partieEnCours
    await printPlayer()
    await asyncio.sleep(3)
    await printEmbedDebutPartie()

    for numeroJeu in range(3):
        # JEU 1
        await jeu(numeroJeu)

        # gestion des points
        # await printScore(numeroJeu)

        # on patiente 3 secondes après l'affichage des scores
        await asyncio.sleep(3)

    pointsTeam2 = 0
    pointsTeam1 = 0
    await printWinners()
    partieEnCours = False
