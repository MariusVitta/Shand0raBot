import asyncio
import random
from boutons import *

from config import *


async def initVar():
    """
    global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, partieEnCours
    pointsTeam2 = 0
    pointsTeam1 = 0
    numeroJeu = 0
    tabQuestions = questions"""

    """ Méthode d'initialisation des variables globales.

    """
    global pointsTeam2, pointsTeam1, numeroJeu, tabQuestions, valTeam1, valTeam2, tabPlayer, channel
    pointsTeam2, pointsTeam1, numeroJeu = 0, 0, 0
    tabQuestions = questions["One Piece"]
    random.shuffle(tabQuestions)
    valTeam1, valTeam2 = "", ""
    channel = client.get_channel(idChannel)


async def calculPoints(messageAuthor):
    """ Méthode de mise à jour du score actuel.

        Parameters
        ----------
        messageAuthor : Any
            une tuple de plusieurs arguments sur l'auteur du message

    """
    global pointsTeam2, pointsTeam1, valTeam1, valTeam2, indiceTab
    if tabRole[indiceEquipe1].lower() in [y.name.lower() for y in messageAuthor.roles]:
        pointsTeam1 += 1
        valTeam1 = " :```diff\n+ "
        valTeam2 = " :``` "
    else:
        pointsTeam2 += 1
        valTeam1 = " :``` "
        valTeam2 = " :```diff\n+ "

    return


async def printWinners():
    """ Méthode d'affichage du score final.
        affiche le resultat dans un embed

    """
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


async def printScore(numEpreuve: int):
    """ Méthode d'affichage du score actuel pour les equipes.

        Parameters
        ----------
        numEpreuve : int
            numéro de l'épreuve en cours

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


async def printPlayer():
    """ Méthode d'affichage de l'ensemble des joueurs


    """

    global tabPlayer
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


async def affichage(numeroJeu):
    global indiceTab
    if indiceTab != len(tabQuestions) - 1:
        await nextQuestion()
    elif numeroJeu != (len(tabEpreuves) - 1):
        await nextEpreuve()
    indiceTab += 1
    return


async def printEmbedImage(fichier: str):
    """ Methode d'affichage des messages du jeu.

    """
    global numeroJeu
    embed = discord.Embed(
        title="Question " + str(indiceTab + 1) + " | " + tabEpreuves[numeroJeu],
        description=carreBlanc + "Qui est ce personnage ?",
        color=colorEmbedWhiteDBV
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(pathFlou + "/" + fichier), embed=embed)


async def printEmbedTimeoutImage(fichier: str, reponse: str):
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title=timeout,
        description=reponseText + "`" + str(reponse) + "`",
        color=colorEmbedTimeout
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(path + "/" + fichier), embed=embed)


async def printEmbedBonneReponseImage(fichier: str, reponse: str, messageSender: any):
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title=pointVert + str(messageSender.author.name) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + str(reponse) + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    embed.set_image(url="attachment://" + fichier)
    await channel.send(file=discord.File(path + "/" + fichier), embed=embed)


async def printEmbedBonneReponse(answer: str, messageSender: any):
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title=pointVert + str(messageSender.author.name) + textGoodAnswer + "\n\n",
        description=reponseText + "`" + str(answer) + "`\n\n" +
                    carreBlanc + " " + tabEmoji[0] + " " + tabRoleBold[0] + valTeam1 + str(
            pointsTeam1) + " points``` \n\n" + \
                    carreBlanc + " " + tabEmoji[1] + " " + tabRoleBold[1] + valTeam2 + str(
            pointsTeam2) + " points``` \n\n",
        color=colorEmbedGoodAnswer,
    )
    await channel.send(embed=embed)


async def printEmbedTimeout(answer: str):
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title=timeout,
        description=reponseText + "`" + str(answer) + "`",
        color=colorEmbedTimeout
    )
    await channel.send(embed=embed)


async def printEmbedQuestions(questionReponses):
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title="Question " + str(indiceTab + 1) + " | " + tabEpreuves[numeroJeu],
        description=carreBlanc + questionReponses[indiceQuestion],
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


def traitementImage(fichier: str, valeurResize: int):
    """ Methode de traitement de l'image.

    """
    img = Image.open(path + "/" + fichier)
    imgSmall = img.resize((valeurResize, valeurResize), resample=Image.BILINEAR)
    result = imgSmall.resize(img.size, Image.NEAREST)
    result.save(pathFlou + "/" + fichier)

    return


async def jeuImage(numJeu):
    global indiceTab, numeroJeu
    numeroJeu = numJeu
    indiceTab = 0
    bonneReponse = ""

    def traitementNom(nomFichier):
        tempName = os.path.splitext(nomFichier)
        bonneReponse = tempName[0].replace("_", " ")
        return bonneReponse

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.

            Parameters
            ----------
            :param m tuple de plusieurs arguments sur le message

            Returns
            -------
            :return bool True si la réponse donnée est bonne et si le message a été envoye dans le bon salon
        """
        return m.content.lower() == bonneReponse.lower() and m.channel == channel

    files = os.listdir(path)
    random.shuffle(files)
    for f in files:
        traitementImage(f, tabTailleResize[0])
        await printEmbedImage(f)

        # récuperation du bon nom de l'image
        bonneReponse = traitementNom(f)

        for valeurResize in tabTailleResize[1:]:  # on exclut le premier item car on l'a deja traité
            # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
            try:
                message = await client.wait_for("message", timeout=delaiQuestions / len(tabTailleResize),
                                                check=checkMessage)
                # time.sleep(5)
                # await printClue(bonneReponse)
            # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
            except asyncio.TimeoutError:
                if valeurResize != tabTailleResize[-1]:
                    traitementImage(f, valeurResize)
                    await printEmbedImage(f)
                else:  # on est arrivé au bout du tableau et on affiche la bonne réponse
                    reponse = bonneReponse
                    await printEmbedTimeoutImage(f, reponse)

                    if indiceTab != len(files) - 1:
                        await nextQuestion()
                    indiceTab += 1

            # sinon on met à jour les points de l'equipe qui a marqué un point,
            # on affiche l'auteur du bon message dans un
            # embed et les points des equipes
            else:
                await calculPoints(message.author)
                reponse = bonneReponse
                await printEmbedBonneReponseImage(f, reponse, message)
                if indiceTab != len(files) - 1:
                    await nextQuestion()
                indiceTab += 1

    await nextEpreuve()
    return


async def jeu(numJeu):
    """ Méthode principale du jeu version quiz.

        Parameters
        ----------
            :param numJeu :
                Numéro du jeu actuel
    """
    global contexteExecution, indiceTab, numeroJeu
    numeroJeu = numJeu
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
            embed = discord.Embed(
                title=questions1[0][0],
                color=colorEmbedWhiteDBV
            )
            await contexteExecution.send(embed=embed)
            await asyncio.sleep(delaiDebutPartie)
            await contexteExecution.send(" ‏‏‎ ", view=Quiz(0))
            await affichage(numeroJeu)
            pass

        else:
            await printEmbedQuestions(questionReponses)
            await asyncio.sleep(delaiDebutPartie)
            for nbAffichage in range(nombreTentatives):
                # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
                try:
                    message = await client.wait_for("message", timeout=delaiQuestions / nombreTentatives,
                                                    check=checkMessage)

                # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
                except asyncio.TimeoutError:
                    if nbAffichage == nombreTentatives / 2: # affichage de la bonne réponse
                        reponse = questionReponses[indiceReponses][0]
                        await printEmbedTimeout(reponse)
                        await affichage(numeroJeu)
                    else:  # affichage de l'indice
                        await printClue(questionReponses[indiceReponses][0])

                # sinon on met à jour les points de l'equipe qui a marqué un point,
                # on affiche l'auteur du bon message dans un
                # embed et les points des equipes
                else:
                    await calculPoints(message.author)
                    reponse = questionReponses[indiceReponses][0]
                    await printEmbedBonneReponse(reponse,message)
                    await affichage(numeroJeu)

    return


async def nextQuestion():
    """ Methode d'attente entre 2 questions.

    """
    await asyncio.sleep(delaiEntreQuestions)
    await printEmbedNextQuestion()
    await asyncio.sleep(delaiDebutPartie)


async def nextEpreuve():
    """ Methode d'attente entre 2 épreuves.

    """
    await asyncio.sleep(delaiEntreEpreuves)
    await printEmbedNextEpreuve()
    await asyncio.sleep(delaiDebutPartie)


async def printEmbedNextEpreuve():
    """ Methode d'affichage des messages du jeu.

    """
    embed = discord.Embed(
        title="Epreuve suivante",
        description="▫️ (Nom de l'épreuve)",
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
        title="La partie va démarrer",
        color=colorEmbedWhiteDBV
    )
    await channel.send(embed=embed)


async def printClue(mot):
    """ Methode d'affichage des indices du jeu.

        Parameters
        ---------
        :param mot : string
            mot dont on va faire afficher 2 lettres en tant qu'indice
    """
    car1, car2 = 1, 1
    listMot = list(mot)
    while car1 == car2: #on evite de choisir 2 fois la meme lettres à faire afficher en indice
        car1 = random.randrange(0, len(listMot))
        car2 = random.randrange(0, len(listMot))
    for i in range(len(listMot)): # on tranforme tout sauf les 2 lettres selectionnés en underscore
        if i != car1 and i != car2:
            listMot[i] = "_"
    indice = "".join(listMot)

    embed = discord.Embed(
        title="⭐ Indice: " + indice,
        color=discord.Color.from_rgb(255, 255, 0)
    )
    await channel.send(embed=embed)


async def lancerJeux(tabJoueur, ctx):
    """ Methode de lancement du jeu.
        Initialise les variables et lance l'ensemble des jeux

        Parameters
        ----------
        :param tabJoueur : Array
            tableau de string contenant le nom de l'ensemble des joueurs
        :param ctx : Context
            contexte d'execution, nous sert principalement afin d'afficher les messages avec des boutons
    """

    global numeroJeu, partieEnCours, pointsTeam1, pointsTeam2, tabPlayer, contexteExecution
    await initVar()
    tabPlayer = tabJoueur
    contexteExecution = ctx
    await printPlayer()
    await asyncio.sleep(delaiDebutPartie)
    await printEmbedDebutPartie()
    await asyncio.sleep(delaiDebutPartie)

    await jeu(numeroJeu)

    await jeuImage(1)

    pass

    """for numeroJeu in range(3):
        # JEU 1
        await jeu(numeroJeu)

        # on patiente 3 secondes après l'affichage des scores
        await asyncio.sleep(3)"""

    pointsTeam2 = 0
    pointsTeam1 = 0
    await printWinners()
    partieEnCours = False
