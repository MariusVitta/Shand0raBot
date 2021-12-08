import asyncio

from config import *

global pointsTeamBleue
pointsTeamBleue = 0

global pointsTeamRouge
pointsTeamRouge = 0


async def initVar():
    global pointsTeamBleue
    pointsTeamBleue = 0

    global pointsTeamRouge
    pointsTeamRouge = 0

async def calculPoints(messageAuthor):
    global pointsTeamBleue
    global pointsTeamRouge
    if "bleu" in [y.name.lower() for y in messageAuthor.roles]:

        pointsTeamBleue += 1
        #channel = client.get_channel(idChannel)
        #await channel.send("Youpi")
    else:
        pointsTeamRouge += 1

    return;


async def printWinners():
    channel = client.get_channel(idChannel)
    descriptionWinners = "L'equipe gagnante est l'equipe bleue " if pointsTeamBleue > pointsTeamRouge else "L'equipe gagnante est l'equipe rouge "

    embed = discord.Embed(
        title=titreWinner,
        description=descriptionWinners,
        color=colorYellowEmbedJeu
    )
    choix = await channel.send(embed=embed)
    pass


async def printScore():
    channel = client.get_channel(idChannel)
    descriptionScore = "[🔴]: " + str(pointsTeamRouge) + "\n[🔵]: " + str(pointsTeamBleue)
    embed = discord.Embed(
        title=titreScoreActuel,
        description=descriptionScore,
        color=colorDarkRedEmbedJeu
    )
    choix = await channel.send(embed=embed)
    pass


# règles du jeu
async def jeu1():
    await initVar()
    channel = client.get_channel(idChannel)
    tailleTab = 0
    embed = discord.Embed(
        title=titreJeu1,
        description=descriptionJeu1,
        color=colorDarkBlueEmbedJeu
    )
    choix = await channel.send(embed=embed)

    def checkMessage(m):
        return m.content == answerGame1[tailleTab] and m.channel == channel

    for question in tabQuestionGame1:
        await channel.send(question)
        try:
            message = await client.wait_for("message", timeout=30, check=checkMessage)
        except asyncio.TimeoutError:
            await channel.send(f"La bonne réponse était {answerGame1[tailleTab]} !")
        else:
            await channel.send(f"C'est {message.author.mention} qui a trouvé la bonne, réponse !")
            tailleTab += 1
            await calculPoints(message.author)

    # gestion des points
    await printScore()

    await jeu2()
    return;


# règles du jeu
async def jeu2():
    channel = client.get_channel(idChannel)
    tailleTab = 0
    embed = discord.Embed(
        title=titreJeu2,
        description=descriptionJeu2,
        color=colorDarkBlueEmbedJeu
    )
    choix = await channel.send(embed=embed)

    def checkMessage(m):
        return m.content == answerGame2[tailleTab] and m.channel == channel

    for question in tabQuestionGame2:
        await channel.send(question)

        try:
            message = await client.wait_for("message", timeout=30, check=checkMessage)
        except asyncio.TimeoutError:
            await channel.send(f"La bonne réponse était {answerGame1[tailleTab]} !")
        else:
            await channel.send(f"C'est {message.author.mention} qui a trouvé la bonne, réponse !")
            tailleTab += 1
            await calculPoints(message.author)

    # gestion des points
    await printScore()
    await jeu3()

    return;


# règles du jeu
async def jeu3():
    channel = client.get_channel(idChannel)
    tailleTab = 0
    embed = discord.Embed(
        title=titreJeu2,
        description=descriptionJeu2,
        color=colorDarkBlueEmbedJeu
    )
    choix = await channel.send(embed=embed)

    def checkMessage(m):
        return m.content == answerGame3[tailleTab] and m.channel == channel

    for question in tabQuestionGame3:
        await channel.send(question)

        try:
            message = await client.wait_for("message", timeout=30, check=checkMessage)
        except asyncio.TimeoutError:
            await channel.send(f"La bonne réponse était {answerGame1[tailleTab]} !")
        else:
            await channel.send(f"C'est {message.author.mention} qui a trouvé la bonne, réponse !")
            tailleTab += 1
            await calculPoints(message.author)

    # gestion des points
    await printScore()

    pointsTeamBleu = 0
    pointsTeamRouge = 0
    await printWinners()

    return;
