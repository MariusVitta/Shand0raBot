import asyncio

from config import *

global pointsTeam2
pointsTeam2 = 0

global pointsTeam1
pointsTeam1 = 0

global numeroJeu
numeroJeu = 0


async def initVar():
    global pointsTeam2
    pointsTeam2 = 0

    global pointsTeam1
    pointsTeam1 = 0

    global numeroJeu
    numeroJeu = 0


async def calculPoints(messageAuthor):
    global pointsTeam2
    global pointsTeam1
    if tabRole[0].lower() in [y.name.lower() for y in messageAuthor.roles]:
        pointsTeam1 += 1
        # channel = client.get_channel(idChannel)
        # await channel.send("Youpi")
    else:
        pointsTeam2 += 1

    return;


async def printWinners():
    channel = client.get_channel(idChannel)
    descriptionWinners = "L'equipe gagnante est l'equipe bleue " if pointsTeam2 > pointsTeam1 else "L'equipe gagnante est l'equipe rouge "

    embed = discord.Embed(
        title=titreWinner,
        description=descriptionWinners,
        color=colorYellowEmbedJeu
    )
    choix = await channel.send(embed=embed)
    pass


async def printScore(numEpreuve):
    channel = client.get_channel(idChannel)
    descriptionScore = tabTextEpreuve[numEpreuve] + "\n\n" + \
                       tabEmoji[0] + \
                       "\n" + \
                       tabRoleBold[0] + "\n" \
                                        "`Score :" + str(pointsTeam1) +"` \n\n" + \
                       tabEmoji[1] + \
                       "\n" + \
                       tabRoleBold[1] + "\n" \
                                        "`Score :" + str(pointsTeam2) +"` \n"
    embed = discord.Embed(
        title=titreDBV,
        description=descriptionScore,
        color=colorEmbedWhiteDBV
    )
    choix = await channel.send(embed=embed)
    pass


# règles du jeu
async def jeu(numeroJeu):
    channel = client.get_channel(idChannel)
    tailleTab = 0

    def checkMessage(m):
        return m.content == tabAnswers[numeroJeu][tailleTab] and m.channel == channel

    for question in tabQuestions[numeroJeu]:
        embed = discord.Embed(
            title="Question " + str(tailleTab + 1) + " | " + tabEpreuves[numeroJeu],
            description=carreBlanc + question,
            color=colorEmbedWhiteDBV
        )
        await channel.send(embed=embed)


        try:
            message = await client.wait_for("message", timeout=15, check=checkMessage)
        except asyncio.TimeoutError:
            reponse = tabAnswers[numeroJeu][tailleTab]
            embed = discord.Embed(
                title=timeout,
                description=reponseText + "`"+ str(reponse) + "`",
                color=colorEmbedTimeout
            )
            await channel.send(embed=embed)

            if tailleTab != len(answerGame1) - 1:
                await nextQuestion()
            elif numeroJeu != (len(tabEpreuves) - 1):
                await nextEpreuve()
            tailleTab += 1
        else:
            await calculPoints(message.author)
            reponse = tabAnswers[numeroJeu][tailleTab]
            embed = discord.Embed(
                title=pointVert + str(message.author.name) + textGoodAnswer ,
                description= reponseText + "`"+ str(reponse) + "`\n\n" +
                             tabEmoji[0] + tabRoleBold[0] + ": `" + str(pointsTeam1) + " points` \n\n" + \
                            tabEmoji[1] + tabRoleBold[1] +  ": `" + str(pointsTeam2) + " points` \n\n",
                color=colorEmbedGoodAnswer
            )
            await channel.send(embed=embed)

            if tailleTab != len(answerGame1) - 1:
                await nextQuestion()
            elif numeroJeu != (len(tabEpreuves) - 1):
                await nextEpreuve()
            tailleTab += 1

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
        title="Prochaine épreuve",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)

async def printEmbedNextQuestion():
    channel = client.get_channel(idChannel)
    embed = discord.Embed(
        title="Prochaine question",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def lancerJeux():
    await initVar()
    global numeroJeu
    for numeroJeu in range(3):
        # JEU 1
        await jeu(numeroJeu)

        # gestion des points
        #await printScore(numeroJeu)

        # on patiente 3 secondes après l'affichage des scores
        await asyncio.sleep(3)

    pointsTeam2 = 0
    pointsTeam1 = 0
    await printWinners()
