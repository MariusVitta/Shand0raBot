import discord

from config import *

load_dotenv()

IDCHANNEL = int(os.getenv('IDCHANNEL'))


# * AFFICHAGE JEU ------------------------------------------------------------------- #
async def affichage(numJeu: int, numQuestion: int, nomEpreuve: str):
    """ Méthode d'affichage du texte "Question suivante" ou "Epreuve suivante"

        Parameters
        ----------
        :param numJeu : int
            numéro du jeu actuel
        :param numQuestion : int
            numéro de la question acutelle
        :param nomEpreuve : str
            nom de l'epreuve

        Returns
        -------
        :return int nouvelle indice du tableau de question
    """
    if numQuestion != (nbQuestions *2) - 1:
        await nextQuestion()
    elif numJeu != (len(tabEpreuves) - 1):
        await nextEpreuve(nomEpreuve)
    numQuestion += 1
    return numQuestion


def traitementTabReponse(tabReponses: [str]):
    """ Méthode formattage du tableau de réponse pour les faire afficher une à une par ligne

        Paramaters
        ----------
        :param tabReponses: [str]
            tableau de réponses

        Returns
        -------
        :return string chaine des réponses
    """
    reponsesFormat = ""
    print(tabReponses)
    reps = tabReponses.split("/")
    print(reps)
    reponsesFormat = ','.join([rep for rep in reps])
    return reponsesFormat
    for rep in reps:
        reponsesFormat += rep + (", " if rep != tabReponses[-1] else "")
    return reponsesFormat


async def printEmbedImage(fichier: str, numJeu: int, numQuestion: int, dossier: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param fichier : str
            nom du fichier à faire afficher dans l'embed
        :param numQuestion : int
            numéro de la question acutelle
        :param dossier : str
            nom du dossier contenant `fichier`
        :param numJeu : int
            numéro du jeu actuel
    """
    embed = discord.Embed(
        title="Question " + str(numQuestion + 1) + " | " + tabEpreuves[numJeu],
        description=carreBlanc + "Qui est ce personnage ?",
        color=colorEmbedWhiteDBV
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(pathFlou + "/" + dossier + "/" + fichier), embed=embed)


async def printEmbedTimeoutImage(fichier: str, reponse: [str], dossier: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param fichier : str
            nom du fichier à faire afficher dans l'embed
        :param reponse : [str]
            ensemble des réponses pour l'image
        :param dossier : str
            nom du dossier contenant `fichier`
    """
    reponses = ','.join([rep for rep in reponse])
    embed = discord.Embed(
        title=timeout,
        description=reponseText + "`" + reponses + "`",
        color=colorEmbedTimeout
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(path + "/" + dossier + "/" + fichier), embed=embed)


async def printEmbedNextEpreuve(nomEpreuve: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param nomEpreuve: str
            nom de l'epreuve actuelle
    """
    embed = discord.Embed(
        title="Epreuve suivante",
        description="▫️ " + nomEpreuve,
        color=discord.Color.blue()
    )
    await channel.send(embed=embed)


async def printEmbedNextQuestion():
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title="Prochaine question",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def printEmbedDebutPartie():
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title="Première épreuve",
        description=carreBlanc + nomEpreuve1,
        color=discord.Color.blue()
    )
    await channel.send(embed=embed)


async def printEmbedBonneReponseImage(fichier: str, reponse: [str], messageSender: any, dossier: str, pointsTeam1: int,
                                      pointsTeam2: int, valTeam1: str, valTeam2: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param fichier : str
            nom du fichier à faire afficher dans l'embed
        :param reponse : [str]
            tableau des réponses pour l'image
        :param messageSender :
            tuple sur l'expéditeur du message de la bonne réponse
        :param dossier : str
            nom du dossier contenant `fichier`
        :param pointsTeam1 : int
            points de l'equipe 1
        :param pointsTeam2 : int
            points de l'equipe 2
        :param valTeam1 : str
            string pour gerer l'affichage
        :param valTeam2 : str
            string pour gerer l'affichage
    """
    reponses = ','.join([rep for rep in reponse])
    embed = discord.Embed(
        title=pointVert + str(messageSender.author.name) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + reponses + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(path + "/" + dossier + "/" + fichier), embed=embed)


async def printEmbedBonneReponse(answer: [str], messageSender: any, pointsTeam1: int, pointsTeam2: int, valTeam1: str,
                                 valTeam2: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param answer : [str]
            tableau des réponses
        :param messageSender :
            tuple sur l'expéditeur du message de la bonne réponse
        :param pointsTeam1 : int
            points de l'equipe 1
        :param pointsTeam2 : int
            points de l'equipe 2
        :param valTeam1 : str
            string pour gerer l'affichage
        :param valTeam2 : str
            string pour gerer l'affichage
    """

    reponses = traitementTabReponse(answer)
    embed = discord.Embed(
        title=pointVert + str(messageSender.author.name) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + reponses + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    await channel.send(embed=embed)


async def printEmbedTimeout(answer: [str]):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param answer : [str]
            tableau des réponses
    """
    reponses = traitementTabReponse(answer)
    embed = discord.Embed(
        title=timeout,
        description=reponseText + "`" + reponses + "`",
        color=colorEmbedTimeout
    )
    await channel.send(embed=embed)


async def printEmbedQuestions(question: [str], numQuestion: int, numJeu: int):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param question : [str]
            tableau des questions
        :param numQuestion : int
            numéro de la question actuelle
        :param numJeu :int
            numéro du jeu actuel
    """
    """"Question " + str(numQuestion + 1) + " | " + tabEpreuves[numJeu] + "\n\n" + carreBlanc + question"""
    embed = discord.Embed(

        title="Question " + str(numQuestion + 1) + " | " + tabEpreuves[numJeu],
        description=carreBlanc + "**" + question + "**",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def nextQuestion():
    """ Methode d'attente entre 2 questions.

    """
    await asyncio.sleep(delaiEntreQuestions)
    await printEmbedNextQuestion()
    await asyncio.sleep(delaiDebutPartie)


async def nextEpreuve(nomEpreuve: str):
    """ Methode d'attente entre 2 épreuves.

    """
    await asyncio.sleep(delaiEntreEpreuves)
    await printEmbedNextEpreuve(nomEpreuve)
    await asyncio.sleep(delaiDebutPartie)


async def printClue(mot):
    """ Methode d'affichage des indices du jeu.

        Parameters
        ---------
        :param mot : string
            mot dont on va faire afficher 2 lettres en tant qu'indice
    """
    mots = mot.split("/")
    indice = mots[0]
    car1, car2 = 1, 1
    listMot = list(indice)
    while car1 == car2:  # on evite de choisir 2 fois la meme lettres à faire afficher en indice
        car1 = random.randrange(0, len(listMot))
        car2 = random.randrange(0, len(listMot))
    for i in range(len(listMot)):  # on tranforme tout sauf les 2 lettres selectionnés en underscore
        if listMot[i].isspace():
            listMot[i] = "\t"
        elif i != car1 and i != car2:
            listMot[i] = "\_"
    indice = "".join(listMot)

    embed = discord.Embed(
        title="⭐ Indice: " + indice,
        color=discord.Color.from_rgb(255, 255, 0)
    )
    await channel.send(embed=embed)


async def printPlayer(tabPlayer: [str]):
    """ Méthode d'affichage de l'ensemble des joueurs

        Parameters
        ----------
        :param tabPlayer : [str]
            tabeau contenant le non de tout les joueurs

    """
    global channel
    channel = client.get_channel(IDCHANNEL)

    team1, team2 = "", ""
    for player in tabPlayer[0]:
        team1 += "- `" + player + "`\n"
    for player in tabPlayer[1]:
        team2 += "- `" + player + "`\n"
    embed = discord.Embed(
        title=titreDBV,
        description=debutPartieDBV + carreBlanc + tabEmoji[indiceEquipe1] + " **" + tabRoleBold[
            indiceEquipe1] + "**\n" + team1 + "\n" + carreBlanc + tabEmoji[indiceEquipe2] + " **" + tabRoleBold[
                        indiceEquipe2] + "**\n" + team2,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def printWinners(pointsTeam1: int, pointsTeam2: int):
    """ Méthode d'affichage du score final.
        Affiche le resultat dans un embed

        Parameters
        ---------
        :param pointsTeam1 : int
            représente les points de l'équipe 1
        :param pointsTeam2 : int
            représente les points de l'équipe 2

    """
    descriptionWinners = "🏆  Vainqueur\n\n"
    if pointsTeam2 > pointsTeam1:
        vainqueurs = foxyBoutonBlanc + "`" + str(pointsTeam2) + " points`" + medaillePremier
        perdants = mugiBoutonBlanc + "`" + str(pointsTeam1) + " points`" + medailleSecond
    else:
        vainqueurs = mugiBoutonBlanc + "`" + str(pointsTeam1) + " points`" + medaillePremier
        perdants = foxyBoutonBlanc + "`" + str(pointsTeam2) + " points`" + medailleSecond

    embed = discord.Embed(
        title=titreDBV,
        description=descriptionWinners + vainqueurs + "\n\n" + perdants,
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)
    pass


async def printScore(numEpreuve: int, pointsTeam1: int, pointsTeam2: int):
    """ Méthode d'affichage du score actuel pour les equipes.

        Parameters
        ----------
        :param numEpreuve : int
            numéro de l'épreuve en cours
        :param pointsTeam1 : int
            représente les points de l'équipe 1
        :param pointsTeam2 : int
            représente les points de l'équipe 2

    """
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
# * AFFICHAGE JEU ------------------------------------------------------------------- #
