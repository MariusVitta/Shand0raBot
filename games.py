from boutons import *
from affichage import *
from config import *

load_dotenv()

IDCHANNEL = int(os.getenv('IDCHANNEL'))


async def initVar():
    """ Méthode d'initialisation des variables globales.

    """
    global pointsTeam2, pointsTeam1, numeroJeu, valTeam1, valTeam2, tabPlayer, channel, questionActuelle,reponsesActuelles
    pointsTeam2, pointsTeam1, numeroJeu = 0, 0, 0
    valTeam1, valTeam2 = "", ""
    channel = client.get_channel(IDCHANNEL)
    questionActuelle = []
    reponsesActuelles = []


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
        os.makedirs(pathFlou + "/" + dossier, mode=0o777,
                    exist_ok=False)  # création du dossier s'il n'existe pas encore
    result.save(pathFlou + "/" + dossier + "/" + fichier)

    return


def selectManga():
    """ Methode de selectin d'un manga dans la liste des mangas disponibles

    """
    mangas = listeMangas
    # Random number with system time
    random.seed(datetime.now())
    random.shuffle(mangas)
    return mangas[0]


async def jeuImage(numJeu):
    """ Méthode principale du jeu version image.

        Parameters
        ----------
        :param numJeu : int
            Numéro du jeu actuel
    """
    global indiceTab, numeroJeu, pointsTeam1, pointsTeam2, valTeam1, valTeam2, channel
    numeroJeu = numJeu
    indiceTab = 0
    tabBonnesReponse = []
    imagesVues = []

    def traitementNom(nomFichier: str):
        tempName = os.path.splitext(nomFichier)
        tabRep = tempName[0].split("-")
        tabRep = [rep.replace("_", " ") for rep in tabRep]
        return tabRep

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.
            1) on va verifier que le nom que l'on cherche est pas dans la chaine => :
                - Sabo ✅
                - aSabo ❌ Pas validé car le mot forme aSabo
                - a Sabo => ✅ Car le bot prend en compte seulement le "Sabo" et pas les caractères qui sont devant et derrière lorsqu'il y a un espace

            2) on va verifier qu'il y a qu'un seul caractère de faux dans la réponse
                - Lufyf au lieu de Luffy ❌ Pas validé car ne dépasse pas 7 caractères
                - Sentomaur au lieu de Sentomaru ✅  Validé car dépasse 7 caractères

            3) dans tous les autres cas on retourne False
            Parameters
            ----------
            :param m tuple de plusieurs arguments sur le message

            Returns
            -------
            :return bool True si la réponse donnée est bonne et si le message a été envoyé dans le bon salon
        """
        if m.channel != channel:
            return False

        # 1)
        def contains_word(toGuest, userAnswer):
            return (' ' + userAnswer + ' ') in (' ' + toGuest + ' ')

        for rep in tabBonnesReponse:
            if contains_word(rep.lower(), m.content.lower()):
                return True
        # 2)
        if len(m.content) > 7:
            wrongLettersUser = []
            goodLettersAnswer = []
            for rep in tabBonnesReponse:

                tailleUserAnswer = len(rep)
                tailleAnswer = len(m.content)
                # on ne s'occupe pas du cas ou les 2 chaines ont une taille différente
                if tailleUserAnswer == tailleAnswer:
                    tabCarAnswer = list(rep.lower())
                    tabCarUser = list(m.content.lower())

                    for i in range(tailleUserAnswer):
                        if tabCarAnswer[i].lower() != tabCarUser[i].lower():
                            wrongLettersUser.append(tabCarUser[i].lower())
                            goodLettersAnswer.append(tabCarAnswer[i].lower())

                    if len(wrongLettersUser) == 1 and len(goodLettersAnswer) == 1:
                        return True

                    elif len(wrongLettersUser) <= 2 and len(goodLettersAnswer) <= 2:
                        return False

        else:  # 3
            return False
        return

    for numQuestion in range(nbQuestions):

        # récuperation d'un manga différent à chaque tour de jeu
        dossier = selectManga()
        files = os.listdir(path + "/" + dossier)
        # Random number with system time
        random.seed(datetime.now())
        random.shuffle(files)
        file = files[0]
        if file in imagesVues:
            while file in imagesVues:
                dossier = selectManga()
                files = os.listdir(path + "/" + dossier)
                # Random number with system time
                random.seed(datetime.now())
                random.shuffle(files)
                file = files[0]
        imagesVues.append(file)

        # pixelisation de l'image
        traitementImage(file, tabTailleResize[0], dossier)
        await printEmbedImage(file, numJeu, numQuestion, dossier)

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
                    await printEmbedImage(file, numJeu, numQuestion, dossier)
                else:  # on est arrivé au bout du tableau et on affiche la bonne réponse
                    reponse = tabBonnesReponse
                    await printEmbedTimeoutImage(file, reponse, dossier)

                    if numQuestion != nbQuestions - 1:
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
                if numQuestion != nbQuestions - 1:
                    await nextQuestion()
                break

    await nextEpreuve(nomEpreuve3)
    return


def selectQuestion():
    """ Methode de selection d'un manga dans la liste des mangas disponibles

    """
    """global tabQuestions
       mangas = listesQuestions
       random.seed(datetime.now())
       random.shuffle(mangas)
       tabQuestions = questions[mangas[0]]
       # Random number with system time
       random.seed(datetime.now())"
       random.shuffle(tabQuestions)

       return tabQuestions[0]"""

    with open('One Piece.txt', 'r') as source:
        data = [line for line in source]
    random.shuffle(data)
    return data[0].split(";")


def getQuestion():
    global questionActuelle
    return questionActuelle

def getReponses():
    global reponsesActuelles
    return reponsesActuelles


async def jeu(numJeu):
    """ Méthode principale du jeu version quiz.

        Parameters
        ----------
            :param numJeu :
                Numéro du jeu actuel
    """
    global contexteExecution, numeroJeu, channel, questionActuelle,reponsesActuelles
    numeroJeu = numJeu
    questionsVues = []

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.
            1) on va verifier que le nom que l'on cherche est pas dans la chaine => :
                - Sabo ✅
                - aSabo ❌ Pas validé car le mot forme aSabo
                - a Sabo => ✅ Car le bot prend en compte seulement le "Sabo" et pas les caractères qui sont devant et derrière lorsqu'il y a un espace

            2) on va verifier qu'il y a qu'un seul caractère de faux dans la réponse
                - Lufyf au lieu de Luffy ❌ Pas validé car ne dépasse pas 7 caractères
                - Sentomaur au lieu de Sentomaru ✅  Validé car dépasse 7 caractères

            3) dans tous les autres cas on retourne False

            Parameters
            ----------
            :param m tuple de plusieurs arguments sur le message

            Returns
            -------
            :return bool True si la réponse donnée est bonne et si le message a été envoye dans le bon salon
        """
        if m.channel != channel:
            return False

        # 0)

        # 1)
        def contains_word(toGuest, userAnswer):
            return (' ' + userAnswer + ' ') in (' ' + toGuest + ' ')

        reponses = getReponses()
        tableauReps = reponses.split("/")
        for rep in tableauReps:
            if contains_word(rep.lower(), m.content.lower()):
                return True

        # 2)
        if len(m.content) > 7:
            print("#2")
            wrongLettersUser = []
            goodLettersAnswer = []

            for rep in tableauReps:

                tailleUserAnswer = len(rep)
                tailleAnswer = len(m.content)

                # on ne s'occupe pas du cas ou les 2 chaines ont une taille différente
                if tailleUserAnswer == tailleAnswer:
                    tabCarAnswer = list(rep.lower())
                    tabCarUser = list(m.content.lower())

                    for i in range(tailleUserAnswer):
                        if tabCarAnswer[i].lower() != tabCarUser[i].lower():
                            wrongLettersUser.append(tabCarUser[i].lower())
                            goodLettersAnswer.append(tabCarAnswer[i].lower())
                    if len(wrongLettersUser) == 1 and len(goodLettersAnswer) == 1:
                        return True

                    elif len(wrongLettersUser) <= 2 and len(goodLettersAnswer) <= 2:
                        return False

        else:  # 3
            print("#3")
            return False
        print("#4")

        return m.content.lower() in [y.lower() for y in tableauReps]
        # m.content.lower() == rep.lower

    for numQuestion in range(nbQuestions):

        # récuperation d'un manga différent à chaque tour de jeu
        data = selectQuestion()
        question = data[indiceQuestion]
        tabRep = data[indiceReponses]
        typeQuestion = data[indiceTypeQuestion]
        if question in questionsVues:
            while question in questionsVues:
                data = selectQuestion()
                question = data[indiceQuestion]

        questionsVues.append(str(question))
        questionActuelle = str(question)
        reponsesActuelles = tabRep
        # Si la question comporte plusieurs réponses possibles, on lance la question à choix multiple
        #
        if int(typeQuestion) == choixMultiple:
            embed = discord.Embed(
                title=questions1[0][0],
                color=colorEmbedWhiteDBV
            )
            await contexteExecution.send(embed=embed)
            await asyncio.sleep(delaiDebutPartie)
            await contexteExecution.send(" ‏‏‎ ", view=Quiz(["Luffy", "Law", "Jinbe", "Boa"], "Luffy" ))
            await client.wait_for("button_click")
            numeroJeu = await affichage(numeroJeu, numQuestion, nomEpreuve2)
            pass

        else:
            await printEmbedQuestions(questionActuelle, numQuestion, numJeu)
            await asyncio.sleep(delaiDebutPartie)
            for nbAffichage in range(nombreTentatives):
                # attente d'un message des joueurs puis verification de la réponse à l'aide la méthode de verification
                try:
                    message = await client.wait_for("message", timeout=delaiQuestions / nombreTentatives,
                                                    check=checkMessage)

                # si le timeout est dépassé, on envoie un message embed contenant la bonne réponse
                except asyncio.TimeoutError:
                    if nbAffichage == nombreTentatives / 2:  # affichage de la bonne réponse
                        reponse = tabRep
                        await printEmbedTimeout(reponse)
                        numeroJeu = await affichage(numeroJeu, numQuestion, nomEpreuve2)

                        break
                    else:  # affichage de l'indice
                        await printClue(tabRep)

                # sinon on met à jour les points de l'equipe qui a marqué un point,
                # on affiche l'auteur du bon message dans un
                # embed et les points des equipes
                else:
                    await calculPoints(message.author)
                    reponse = tabRep
                    await printEmbedBonneReponse(reponse, message, pointsTeam1, pointsTeam2, valTeam1,
                                                 valTeam2)
                    numeroJeu = await affichage(numeroJeu, numQuestion, nomEpreuve2)
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

    await jeu(0)
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
