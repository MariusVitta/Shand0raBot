from affichage import *
from config import *
import boutons

load_dotenv()

IDCHANNEL = int(os.getenv('IDCHANNEL'))
GUILD = str(os.getenv('DISCORD_GUILD'))


async def initVar():
    """ Méthode d'initialisation des variables globales."""
    global pointsTeam2, pointsTeam1, numeroJeu, valTeam1, valTeam2, tabPlayer, channel, questionActuelle, reponsesActuelles
    pointsTeam2, pointsTeam1, numeroJeu = 0, 0, 0
    valTeam1, valTeam2 = "", ""
    channel = client.get_channel(IDCHANNEL)
    questionActuelle = []
    reponsesActuelles = []


async def calculPoints(messageAuthor, tabJoueurDiscriminator: [str]):
    """ Méthode de mise à jour du score actuel.

        Parameters
        ----------
        messageAuthor : Message
            instance de Message
        tabJoueurDiscriminator : [str]
            tableau des joueurs avec leurs discriminants, nous sert essentiellement pour sauvegarder les points des joueurs en fin de partie
    """
    global pointsTeam2, pointsTeam1, valTeam1, valTeam2, tabPlayerDiscriminator
    tabPlayerDiscriminator = tabJoueurDiscriminator
    if tabRole[indiceEquipe1].lower() in [y.name.lower() for y in messageAuthor.roles]:
        pointsTeam1 += 1
        valTeam1 = " :```diff\n+ "
        valTeam2 = " :``` "
    else:
        pointsTeam2 += 1
        valTeam1 = " :``` "
        valTeam2 = " :```diff\n+ "
    joueurDiscriminator = messageAuthor.name + "#" + messageAuthor.discriminator
    for joueur in tabPlayerDiscriminator:
        # si le joueur avait déjà un score auparavant, on va mettre à jour son score simplement
        if joueur[0] == joueurDiscriminator:
            joueur[1] += 1
    return


def traitementImage(fichier: str, valeurResize: int, dossier: str):
    """ Methode de traitement de l'image.
        Cette méthode va resize l'image afin de lui donner un effet pixelisé
        on va créer une nouvelle image qui se trouvera dans le dossier `magesFloues`

        Parameters
        ----------
        fichier :str
            nom de l'image que l'on veut pixeliser
        valeurResize :int
            taille du resize de l'image
        dossier :str
            dossier ou se trouve l'image actuellement
    """
    img = Image.open(path + "/" + dossier + "/" + fichier)
    imgSmall = img.resize((valeurResize, valeurResize), resample=Image.BILINEAR)
    result = imgSmall.resize(img.size, Image.NEAREST)
    if not os.path.exists(pathFlou + "/" + dossier):
        os.makedirs(pathFlou + "/" + dossier, mode=0o777,
                    exist_ok=False)  # création du dossier s'il n'existe pas encore
    result.save(pathFlou + "/" + dossier + "/" + fichier)

    return


def selectManga():
    """ Methode de selectin d'un manga dans la liste des mangas disponibles"""
    mangas = listeMangas
    # Random number with system time
    random.seed(datetime.now())
    random.shuffle(mangas)
    return mangas[0]


async def jeuImage(numJeu: int, tabJDiscriminator: [str]):
    """ Méthode principale du jeu version image.

        Parameters
        ----------
        numJeu : int
            Numéro du jeu actuel
        tabJDiscriminator : [str]
            tableaux des joueurs avec leurs discriminants
    """
    global numeroJeu, pointsTeam1, pointsTeam2, valTeam1, valTeam2, channel, tabPlayerDiscriminator
    tabPlayerDiscriminator = tabJDiscriminator
    numeroJeu = numJeu
    tabBonnesReponse = []
    imagesVues = []

    def traitementNom(nomFichier: str):
        tempName = os.path.splitext(nomFichier)
        tabRep = tempName[0].split("-")
        return tabRep

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.
            1) on va verifier que le nom que l'on cherche n'est pas dans la chaine → :
                - Sabo ✅
                - aSabo ❌ Pas validé, car le mot forme aSabo
                - a Sabo → ✅ Car le bot prend en compte seulement le "Sabo" et pas les caractères qui sont devant et derrière lorsqu'il y a un espace

            2) on va verifier qu'il y a qu'un seul caractère de faux dans la réponse
                - Lufyf au lieu de Luffy ❌ Pas validé, car ne dépasse pas 7 caractères
                - Sentomaur au lieu de Sentomaru ✅ Validé, car dépasse 7 caractères

            3) dans tous les autres cas on retourne False

            Parameters
            ----------
            m : Message
                instance de Message

            Returns
            -------
            bool
                True si la réponse donnée est bonne et si le message a été envoyé dans le bon salon
        """
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        roleTeam1 = discord.utils.get(guild.roles, name=tabRole[0])
        roleTeam2 = discord.utils.get(guild.roles, name=tabRole[1])

        if m.channel != channel:
            return False
        # on empêche aux non-joueurs de jouer simplement
        if roleTeam1 not in m.author.roles and roleTeam2 not in m.author.roles:
            return False

        trace.saveTraceAnswer(m.author.name, m.content)

        # 1)
        def contains_word(userAnswer, toGuess):
            return (' ' + userAnswer + ' ') in (' ' + toGuess + ' ')

        for rep in tabBonnesReponse:
            if "_" in rep: # on va différencier les réponses ou un ensemble de mot ne peuvent pas être séparé des autres
                rep = rep.replace("_", " ").lower()
                if contains_word(rep.lower(), m.content.lower()):
                    return True
            else:
                for word in m.content.split(" "):
                    if word.lower() in rep.lower():
                        return True
        return False

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
        trace.traceQuestionsImage(numQuestion, file)

        # pixelisation de l'image
        traitementImage(file, tabTailleResize[0], dossier)
        await printEmbedImage(file, dossier)

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
                    await printEmbedImage(file, dossier)
                else:  # on est arrivé au bout du tableau et on affiche la bonne réponse
                    reponse = tabBonnesReponse
                    await printEmbedTimeoutImage(file, reponse, dossier)

                    if numQuestion != nbQuestions - 1:
                        await nextQuestion()
                    break

            # sinon on met à jour les points de l'equipe qui a marqué un point,
            # on affiche l'auteur du bon message dans un
            # embed et les points des equipes
            else:
                await calculPoints(message.author, tabPlayerDiscriminator)
                reponse = tabBonnesReponse
                await printEmbedBonneReponseImage(file, reponse, message, dossier, pointsTeam1, pointsTeam2, valTeam1,
                                                  valTeam2)
                if numQuestion != nbQuestions - 1:
                    await nextQuestion()
                break

    await nextEpreuve(nomEpreuve3)
    return


def selectQuestion():
    """ Methode de selection d'un manga dans la liste des mangas disponibles """
    with open('One Piece.txt', 'r', encoding="utf-8") as source:
        data = [line for line in source]
    random.seed(datetime.now())
    random.shuffle(data)
    s = data[0].split(":")
    return s[1].split(";")


def getQuestion():
    global questionActuelle
    return questionActuelle


def getReponses():
    global reponsesActuelles
    return reponsesActuelles


async def jeu(numJeu: int, tabJoueurDiscriminator: list):
    """ Méthode principale du jeu version quiz.

        Parameters
        ----------
        numJeu : int
            Numéro du jeu actuel
        tabJoueurDiscriminator : list
            tableau des joueurs avec leurs discriminants
    """
    global contexteExecution, numeroJeu, channel, questionActuelle, reponsesActuelles, tabPlayerDiscriminator
    numeroJeu = numJeu
    questionsVues = []
    tabPlayerDiscriminator = tabJoueurDiscriminator

    def checkMessage(m):
        """Méthode de verification de la validité d'une réponse.
            1) on va verifier que le nom que l'on cherche n'est pas dans la chaine → :
                - Sabo ✅
                - aSabo ❌ Pas validé, car le mot forme aSabo
                - a Sabo → ✅ Car le bot prend en compte seulement le "Sabo" et pas les caractères qui sont devant et derrière lorsqu'il y a un espace

            2) on va verifier qu'il y a qu'un seul caractère de faux dans la réponse
                - Lufyf au lieu de Luffy ❌ Pas validé, car ne dépasse pas 7 caractères
                - Sentomaur au lieu de Sentomaru ✅ Validé, car dépasse 7 caractères

            3) dans tous les autres cas on retourne False

            Parameters
            ----------
            m : Message
                instance de Message

            Returns
            -------
            bool
                True si la réponse donnée est bonne et si le message a été envoye dans le bon salon
                True si la réponse donnée est bonne et si le message a été envoye dans le bon salon
        """
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        roleTeam1 = discord.utils.get(guild.roles, name=tabRole[0])
        roleTeam2 = discord.utils.get(guild.roles, name=tabRole[1])
        if m.channel != channel:
            return False

        if roleTeam1 not in m.author.roles and roleTeam2 not in m.author.roles:
            return False
        trace.saveTraceAnswer(m.author.name, m.content)

        # 1)
        def contains_word(userAnswer, toGuess):
            return (' ' + userAnswer + ' ') in (' ' + toGuess + ' ')

        reponses = getReponses()
        tableauReps = reponses.split("/")
        for bonneReponse in tableauReps:
            if contains_word(bonneReponse.lower(), m.content.lower()):
                return True

        # 2)
        if len(m.content) > 7:
            for reps in tableauReps:
                if jellyfish.damerau_levenshtein_distance(m.content.lower(),
                                                          reps.lower()) <= 1:  # on regarde les changements de position des lettres
                    return True
                elif jellyfish.levenshtein_distance(m.content.lower(),
                                                    reps.lower()) <= 1:  # puis on regarde le changement de lettre
                    return True
            return False

    for numQuestion in range(nbQuestions * 2):

        # récuperation d'un manga différent à chaque tour de jeu
        data = selectQuestion()
        question = data[indiceQuestion]
        tabRep = data[indiceReponses]
        typeQuestion = data[indiceTypeQuestion]
        if question in questionsVues:
            while question in questionsVues:
                data = selectQuestion()
                question = data[indiceQuestion]
                tabRep = data[indiceReponses]
                typeQuestion = data[indiceTypeQuestion]
        trace.saveTraceQuestions(numQuestion, question, tabRep, typeQuestion)
        questionsVues.append(question)
        questionActuelle = question
        reponsesActuelles = tabRep

        # Si la question comporte plusieurs réponses possibles, on lance la question à choix multiple
        #
        # Si la question comporte plusieurs réponses possibles, on lance la question à choix multiple
        if int(typeQuestion) == choixMultiple:
            embed = discord.Embed(
                title="🔸 " + questionActuelle,
                color=colorEmbedWhiteDBV
            )
            rep = data[indiceBonneReponse].rstrip("\n")
            msgv = await contexteExecution.send(embed=embed)
            await asyncio.sleep(delaiDebutPartie)
            # dataV = []
            view = boutons.Quiz(tabRep.replace("\n", "").split("/"), rep, (len(tabPlayer[0]) + len(tabPlayer[1])))
            await msgv.edit(view=view)
            finView = await view.wait()
            if finView:
                await printEmbedTimeout(rep)
            else:
                if boutons.dataV[0]:
                    await calculPoints(boutons.dataV[1], tabPlayerDiscriminator)
                    await printEmbedBonneReponse(rep, boutons.dataV[1].display_name, pointsTeam1, pointsTeam2, valTeam1,
                                                 valTeam2)
                    trace.saveTraceBoutons(boutons.dataV[1].display_name, rep)
                elif not boutons.dataV[0]:
                    await printEmbedNoAnswer(rep)
                    trace.traceTimeoutBoutons(rep)
            numeroJeu = await affichage(numeroJeu, numQuestion, nomEpreuve2)
            boutons.dataV = []
            boutons.tentative = []
            pass

        else:
            await printEmbedQuestions(questionActuelle)
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
                        trace.traceTimeout()
                        break
                    else:  # affichage de l'indice
                        indice = await printClue(tabRep)
                        trace.saveTraceIndice(indice)

                # sinon on met à jour les points de l'equipe qui a marqué un point,
                # on affiche l'auteur du bon message dans un
                # embed et les points des equipes
                else:
                    await calculPoints(message.author, tabPlayerDiscriminator)
                    reponse = tabRep
                    await printEmbedBonneReponse(reponse, message.author.display_name, pointsTeam1, pointsTeam2,
                                                 valTeam1,
                                                 valTeam2)
                    numeroJeu = await affichage(numeroJeu, numQuestion, nomEpreuve2)
                    break

    return


def sauvegardeScore(tabJDiscriminator: list):
    """ Methode de sauvegarde du score des joueurs.

           Parameters
           ----------
           tabJDiscriminator : list
               tableau de string contenant le nom de l'ensemble des joueurs avec leurs discriminants

    """
    data = []
    # récuperation de l'ensemble des scores actuels
    with open('scores.txt', 'r', encoding="utf-8") as source:
        for line in source:
            if line != "\n":
                line = line.rstrip("\n")
                line = line.split("/")
                data.append([line[0], int(line[1])])

    # joueurDiscriminator = messageAuthor.name + "#" + messageAuthor.discriminator
    # on parcourt le tableau des resultats pour modifier le score des joueurs déjà existant
    for joueur in tabJDiscriminator:
        # si le joueur avait déjà un score auparavant, on va mettre à jour son score simplement
        if joueur[0] in [j[0] for j in data]:
            for i in range(len(data)):
                if data[i][0] == joueur[0]:
                    data[i][1] += joueur[1]
        else:
            data.append([joueur[0], joueur[1]])
    # sauvegarde de tous les scores après les avoir mis à jour
    with open('scores.txt', 'w') as target:
        for i in range(len(data)):
            target.write(data[i][0] + "/" + str(data[i][1]) + "\n")

    pass


async def lancerJeux(tabJoueur: list, ctx, tabJoueurDiscriminator: list, traceGame):
    """ Methode de lancement du jeu.
        Initialise les variables et lance l'ensemble des jeux

        Parameters
        ----------
        tabJoueur : list
            tableau de string contenant le nom de l'ensemble des joueurs
        ctx : Context
            contexte d'execution, nous sert principalement afin d'afficher les messages avec des boutons
        tabJoueurDiscriminator : list
            tableau de string contenant le nom de l'ensemble des joueurs avec leurs discriminants
        traceGame : Traces
            instance de la classe Traces qui nous permettra de sauvegarder l'ensemble des parties dans un fichier de trace

        Returns
        ------
        bool
            booleen représentant la fin de partie
    """
    global numeroJeu, partieEnCours, pointsTeam1, pointsTeam2, tabPlayer, contexteExecution, channel, tabPlayerDiscriminator, trace
    await initVar()
    tabPlayer = tabJoueur
    contexteExecution = ctx
    tabPlayerDiscriminator = tabJoueurDiscriminator
    trace = traceGame

    await printPlayer(tabPlayer)
    await asyncio.sleep(delaiDebutPartie)
    await printEmbedDebutPartie()
    await asyncio.sleep(delaiDebutPartie)

    # quiz
    trace.traceQuestionQuiz()
    await jeu(0, tabPlayerDiscriminator)
    trace.traceFinQuestionQuiz()

    # "qui est-ce"
    trace.traceQuestionImage()
    await jeuImage(1, tabPlayerDiscriminator)
    trace.traceFinQuestionImage()

    # affichage des vainqueurs
    await printWinners(pointsTeam1, pointsTeam2)

    # Sauvegarde des points
    trace.saveTracePoints()
    sauvegardeScore(tabPlayerDiscriminator)

    # reset
    pointsTeam1 = 0
    pointsTeam2 = 0
    partieEnCours = False

    return partieEnCours
