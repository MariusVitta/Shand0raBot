from boutons import *
from affichage import *
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
            un tuple de plusieurs arguments sur l'auteur du message

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


def traitementImage(fichier: str, valeurResize: int, dossier: str):
    """ Methode de traitement de l'image.
        Cette méthode va resize l'image afin de lui donner un effet pixelisé
        on va créer une nouvelle image qui se trouvera dans le dossier `magesFloues`

        Parameters
        ----------
        :param fichier :str
            nom de l'image que l'on veut pixelisée
        :param valeurResize :int
            taille du resize de l'image
        :param dossier :str
            dossier ou se trouve l'image actuellement
    """
    # define the access rights
    img = Image.open(path + "/" + dossier + "/" + fichier)
    imgSmall = img.resize((valeurResize, valeurResize), resample=Image.BILINEAR)
    result = imgSmall.resize(img.size, Image.NEAREST)
    if not os.path.exists(pathFlou + "/" + dossier):
        os.makedirs(pathFlou + "/" + dossier, mode=0o777, exist_ok=False)  # création du dossier s'il n'existe pas encore
    result.save(pathFlou + "/" + dossier + "/" + fichier)

    return


def selectManga():
    """ Methode de selectin d'un manga dans la liste des mangas disponibles

    """
    mangas = listeMangas
    random.shuffle(mangas)
    return mangas[0]


async def jeuImage(numJeu):
    """ Méthode principale du jeu version image.

        Parameters
        ----------
        :param numJeu : int
            Numéro du jeu actuel
    """
    global indiceTab, numeroJeu, pointsTeam1, pointsTeam2, valTeam1, valTeam2,channel
    numeroJeu = numJeu
    indiceTab = 0
    tabBonnesReponse = []

    def traitementNom(nomFichier: str):
        tempName = os.path.splitext(nomFichier)
        tabRep = tempName[0].split("-")
        tabRep = [rep.replace("_", " ") for rep in tabRep]
        return tabRep

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.

            Parameters
            ----------
            :param m tuple de plusieurs arguments sur le message

            Returns
            -------
            :return bool True si la réponse donnée est bonne et si le message a été envoyé dans le bon salon
        """
        val = True if (m.content.lower() in [rep.lower() for rep in tabBonnesReponse]) else False
        return val and m.channel == channel

    dossier = selectManga()
    files = os.listdir(path + "/" + dossier)
    random.shuffle(files)
    for file in files:
        traitementImage(file, tabTailleResize[0], dossier)
        await printEmbedImage(file, numJeu, indiceTab, dossier)

        # récuperation du bon nom de l'image
        tabBonnesReponse = traitementNom(file)

        for valeurResize in tabTailleResize[1:]:  # on exclut le premier item, car on l'a deja traité
            # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
            try:
                message = await client.wait_for("message", timeout=delaiQuestionsImages / len(tabTailleResize),
                                                check=checkMessage)
            # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
            except asyncio.TimeoutError:
                if valeurResize != tabTailleResize[-1]:
                    traitementImage(file, valeurResize, dossier)
                    await printEmbedImage(file, numJeu, indiceTab, dossier)
                else:  # on est arrivé au bout du tableau et on affiche la bonne réponse
                    reponse = tabBonnesReponse
                    await printEmbedTimeoutImage(file, reponse, dossier)

                    if indiceTab != len(files) - 1:
                        await nextQuestion()
                    indiceTab += 1
                    break

            # sinon on met à jour les points de l'equipe qui a marqué un point,
            # on affiche l'auteur du bon message dans un
            # embed et les points des equipes
            else:
                await calculPoints(message.author)
                reponse = tabBonnesReponse
                await printEmbedBonneReponseImage(file, reponse, message, dossier, pointsTeam1, pointsTeam2, valTeam1,
                                                  valTeam2)
                if indiceTab != len(files) - 1:
                    await nextQuestion()
                indiceTab += 1
                break

    await nextEpreuve()
    return


async def jeu(numJeu):
    """ Méthode principale du jeu version quiz.

        Parameters
        ----------
            :param numJeu :
                Numéro du jeu actuel
    """
    global contexteExecution, indiceTab, numeroJeu, channel
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
        print(tabQuestions[numeroJeu][1])
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
            await affichage(numeroJeu, indiceTab, tabQuestions)
            pass

        else:
            await printEmbedQuestions(questionReponses, indiceTab, numJeu)
            await asyncio.sleep(delaiDebutPartie)
            for nbAffichage in range(nombreTentatives):
                # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
                try:
                    message = await client.wait_for("message", timeout=delaiQuestions / nombreTentatives,
                                                    check=checkMessage)

                # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
                except asyncio.TimeoutError:
                    if nbAffichage == nombreTentatives / 2:  # affichage de la bonne réponse
                        reponse = questionReponses[indiceReponses][0]
                        await printEmbedTimeout(reponse)
                        indiceTab = await affichage(numeroJeu, indiceTab, tabQuestions)

                        break
                    else:  # affichage de l'indice
                        await printClue(questionReponses[indiceReponses][0])

                # sinon on met à jour les points de l'equipe qui a marqué un point,
                # on affiche l'auteur du bon message dans un
                # embed et les points des equipes
                else:
                    await calculPoints(message.author)
                    reponse = questionReponses[indiceReponses][0]
                    await printEmbedBonneReponse(reponse, message, pointsTeam1, pointsTeam2, valTeam1,
                                                 valTeam2)
                    await affichage(numeroJeu, indiceTab, tabQuestions)
                    break

    return


async def lancerJeux(tabJoueur, ctx):
    """ Methode de lancement du jeu.
        Initialise les variables et lance l'ensemble des jeux

        Parameters
        ----------
        :param tabJoueur : Array
            tableau de string contenant le nom de l'ensemble des joueurs
        :param ctx : Context
            contexte d'execution, nous sert principalement afin d'afficher les messages avec des boutons

        Returns
        ------
        :return bool fin de partie
    """
    global numeroJeu, partieEnCours, pointsTeam1, pointsTeam2, tabPlayer, contexteExecution, channel
    await initVar()
    tabPlayer = tabJoueur
    contexteExecution = ctx
    await printPlayer(tabPlayer)
    await asyncio.sleep(delaiDebutPartie)
    await printEmbedDebutPartie()
    await asyncio.sleep(delaiDebutPartie)

    #await jeu(numeroJeu)

    await jeuImage(1)

    pass

    """for numeroJeu in range(3):
        # JEU 1
        await jeu(numeroJeu)

        # on patiente 3 secondes après l'affichage des scores
        await asyncio.sleep(3)"""
    await printWinners(pointsTeam1, pointsTeam2)
    pointsTeam2 = 0
    pointsTeam1 = 0

    partieEnCours = False
    return partieEnCours
