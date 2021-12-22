from config import *

load_dotenv()

global channel
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
        :return int nouvel indice du tableau de question
    """
    if numQuestion != (nbQuestions * 2) - 1:
        await nextQuestion()
    elif numJeu != (len(tabEpreuves) - 1):
        await nextEpreuve(nomEpreuve)
    numQuestion += 1
    return numQuestion


def traitementTabReponse(tabReponses: list):
    """ Méthode formattage du tableau de réponse pour les faire afficher une à une par ligne

        Paramaters
        ----------
        :param tabReponses : list
            tableau de réponses

        Returns
        -------
        :return string chaine des réponses
    """
    reps = tabReponses.split("/")
    reponsesFormat = reps[0]
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
        title=carreBlanc + "Qui est ce personnage ?",
        color=colorEmbedWhiteDBV
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(pathFlou + "/" + dossier + "/" + fichier), embed=embed)


async def printEmbedTimeoutImage(fichier: str, reponse: list, dossier: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param fichier : str
            nom du fichier à faire afficher dans l'embed
        :param reponse : list
            ensemble des réponses pour l'image
        :param dossier : str
            nom du dossier contenant `fichier`
    """
    if "_" in reponse[0]:
        reponses = reponse[0].replace("_", " ")
    else:
        reponses = reponse[0]
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
        :param nomEpreuve : str
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


async def printEmbedBonneReponseImage(fichier: str, reponse: list, messageSender: any, dossier: str, pointsTeam1: int,
                                      pointsTeam2: int, valTeam1: str, valTeam2: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param fichier : str
            nom du fichier à faire afficher dans l'embed
        :param reponse : list
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
    if "_" in reponse[0]:
        reponses = reponse[0].replace("_", " ")
    else:
        reponses = reponse[0]
    embed = discord.Embed(
        title=pointVert + str(messageSender.author.display_name) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + reponses + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(path + "/" + dossier + "/" + fichier), embed=embed)


async def printEmbedBonneReponse(answer: list, messageSender: str, pointsTeam1: int, pointsTeam2: int, valTeam1: str,
                                 valTeam2: str):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param answer : list
            tableau des réponses
        :param messageSender : str
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
        title=pointVert + str(messageSender) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + reponses + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    await channel.send(embed=embed)


async def printEmbedTimeout(answer: list):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param answer : list
            tableau des réponses
    """
    reponses = traitementTabReponse(answer)
    embed = discord.Embed(
        title=timeout,
        description=reponseText + "`" + reponses + "`",
        color=colorEmbedTimeout
    )
    await channel.send(embed=embed)


async def printEmbedNoAnswer(answer: list):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param answer : [str]
            tableau des réponses
    """
    reponses = traitementTabReponse(answer)
    embed = discord.Embed(
        title=noAns,
        description=reponseText + "`" + reponses + "`",
        color=colorEmbedTimeout
    )
    await channel.send(embed=embed)


async def printEmbedQuestions(question: list, numQuestion: int, numJeu: int):
    """ Methode d'affichage des messages du jeu.

        Parameters
        ----------
        :param question : list
            tableau des questions
        :param numQuestion : int
            numéro de la question actuelle
        :param numJeu :int
            numéro du jeu actuel
    """
    """"Question " + str(numQuestion + 1) + " | " + tabEpreuves[numJeu] + "\n\n" + carreBlanc + question"""
    embed = discord.Embed(

        title="🔹 **" + question + "**",
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
        Si le mot fait 1 caractère, on n'affiche rien
        si le mot fait entre 2 et 3 caractères on affiche un seul caractère
        Si le mot fait entre 4 et 6 caractères, on affiche un deux caractere pr l'indice
        si le mot fait entre et entre 7 et 9 caractères, on affiche trois caractères
        sinon si plus de 9 caractères, on affiche quatre caractères

        Parameters
        ---------
        :param mot : string
            mot dont on va faire afficher X lettres en tant qu'indice

        Returns
        -------
        :return str l'indice
    """
    if len(mot) < 2:
        return
    mots = mot.split("/")
    random.seed(datetime.now())
    random.shuffle(mots)
    indice = mots[0]
    listMot = list(indice)
    espace = " "
    underscore = "_"
    charArray = [",", "\"", "'", ":", "(", ")"]

    if 2 <= len(mot) <= 3:
        car1 = random.randrange(0, len(listMot))
        for i in range(len(listMot)):  # on transforme tout sauf la lettre selectionné en underscore
            if listMot[i].isspace():
                listMot[i] = espace
            elif i != car1 and listMot[i] not in charArray:
                listMot[i] = underscore
        indice = "".join(listMot)

    elif 4 <= len(mot) <= 7:
        car1, car2 = 1, 1
        while car1 == car2:  # on évite de choisir 2 fois la meme lettres à faire afficher en indice
            car1 = random.randrange(0, len(listMot))
            car2 = random.randrange(0, len(listMot))
        for i in range(len(listMot)):  # on transforme tout sauf les 2 lettres selectionnés en underscore
            if listMot[i].isspace():
                listMot[i] = espace
            elif i != car1 and i != car2 and listMot[i] not in charArray:
                listMot[i] = underscore
        indice = "".join(listMot)
    elif 7 <= len(mot) <= 9:
        car1, car2, car3 = 1, 1, 1
        while car1 == car2 and car2 == car3:  # on évite de choisir 3 fois la meme lettre à faire afficher en indice
            car1 = random.randrange(0, len(listMot))
            car2 = random.randrange(0, len(listMot))
            car3 = random.randrange(0, len(listMot))
        for i in range(len(listMot)):  # on transforme tout sauf les 2 lettres selectionnés en underscore
            if listMot[i].isspace():
                listMot[i] = espace
            elif i != car1 and i != car2 and i != car3 and listMot[i] not in charArray:
                listMot[i] = underscore
        indice = "".join(listMot)
    else:
        car1, car2, car3, car4 = 1, 1, 1, 1
        while car1 == car2 and car2 == car3 and car3 == car4:  # on évite de choisir 3 fois la meme lettre à faire afficher en indice
            car1 = random.randrange(0, len(listMot))
            car2 = random.randrange(0, len(listMot))
            car3 = random.randrange(0, len(listMot))
            car4 = random.randrange(0, len(listMot))
        for i in range(len(listMot)):  # on transforme tout sauf les 2 lettres selectionnés en underscore
            if listMot[i].isspace():
                listMot[i] = espace
            elif i != car1 and i != car2 and i != car3 and i != car4 and listMot[i] not in charArray:
                listMot[i] = underscore
        indice = "".join(listMot)
    embed = discord.Embed(
        title="💡 Indice : `" + indice + "`",
        color=discord.Color.from_rgb(255, 216, 63)
    )
    await channel.send(embed=embed)

    return indice


async def printPlayer(tabJ: list):
    """ Méthode d'affichage de l'ensemble des joueurs

        Parameters
        ----------
        :param tabJ : list
            tabeau contenant le non de tous les joueurs

    """
    global channel
    channel = client.get_channel(IDCHANNEL)

    team1, team2 = "", ""
    for player in tabJ[0]:
        team1 += "- `" + player + "`\n"
    for player in tabJ[1]:
        team2 += "- `" + player + "`\n"
    embed = discord.Embed(
        title=titreDBV,
        description=debutPartieDBV + carreBlanc + tabEmoji[indiceEquipe1] + " **" + tabRoleBold[
            indiceEquipe1] + "**\n" + team1 + "\n" + carreBlanc + tabEmoji[indiceEquipe2] + " **" + tabRoleBold[
                        indiceEquipe2] + "**\n" + team2 + "\n🔸 Question à choix multiple\n\n🔹 Question simple",
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
