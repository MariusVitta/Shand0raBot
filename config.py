# Bot
from imports import *

global tabPlayer, channel, contexteExecution


# ------------------------------------------------------------------------------------------------------------#
# Gestion des commandes du bot
descriptionBot = "Bot pour le Davy Back Fight"
prefixBot = '!'
usageBot = "Usage: " + prefixBot + "start dbf or " + prefixBot + "s dbf "
intents = discord.Intents().default()
intents.members = True
intents.presences = True

# CLIENT
client = commands.Bot(command_prefix=prefixBot, description=descriptionBot, intents=intents)
# buttons = DiscordComponents(client)

# ------------------------------------------------------------------------------------------------------------#
# Gestion des Equipes
# https://emojipedia.org/ pour les différents Emojis
tabEmoji = ["☠", "🦊"]  # emoji bleu, rouge
medaillePremier = "🥇"
medailleSecond = "🥈"
mugiBoutonBlanc = "▫️ ☠️ Mugiwara :"
foxyBoutonBlanc = "▫️ 🦊 Foxy :"
tabRole = ["Mugiwara", "Foxy"]
tabRoleBold = ["**Mugiwara**", "**Foxy**"]
tabPlayer = [[], []]  # tableau des joueurs
nombreJoueursEquipe1 = 1
nombreJoueursEquipe2 = 2
indiceEquipe1 = 0
indiceEquipe2 = 1

# ------------------------------------------------------------------------------------------------------------#
# MESSAGES DAVYBACKFIGHT
messageStart = 'dbf'
titreDBV = "🎮 Davy Back Fight"
descriptionDBV = "🔹 La partie va débuter dans 30 secondes... \n\n " \
                 "🔸 Pour rejoindre une équipe réagis à l'un des émojis \n\n " \
                 "▫️ ☠️ Mugiwara \n\n" \
                 "▫️ 🦊 Foxy"
colorEmbedWhiteDBV = discord.Color.from_rgb(255, 255, 255)
debutPartieDBV = "🔹 La première épreuve va commencer\n\n"
tabTextEpreuve = ["🔹 **Epreuve 1 / 3**", "🔹 **Epreuve 2 / 3**", "🔹 **Epreuve 3 / 3** "]
phraseQuestion = "▫️ **Question**"
carreBlanc = "▫️"

tabEpreuves = ["Epreuve 1", "Epreuve 2", "Epreuve 3"]
descriptionJeu1 = "🔹 **Epreuve 1 / 3** \n\n" + phraseQuestion
descriptionJeu2 = "🔹 **Epreuve 2 / 3** \n\n" + phraseQuestion
descriptionJeu3 = "🔹 **Epreuve 3 / 3** \n\n" + phraseQuestion
tabDescriptions = [descriptionJeu1, descriptionJeu2, descriptionJeu3]

# ------------------------------------------------------------------------------------------------------------#
# QUESTIONS
questionGame1 = "Question 1 - 1"
questionGame2 = "Question 2 - 1"
questionGame3 = "Question 3 - 1"

answerGame1 = ["Luffy"]
answerGame2 = ["Luffy"]

# tableaux
questions = {"One Piece": [["Quel pirate de l'équipage de Shanks s'est occupé des brigands à lui tout seul", "Ben Beckman"], ["La planque secrète de Ivankov à Impeldown se trouve à l'étage", "5.5"], ["En échange de sauver Luffy du poison de Magellan combien d'années de vie devait donner Luffy", "10 ans"],
                           ["Combien de temps s'était écoulé à la fin du traitement de Ivankov", "moins de 24h"],"Selon le narrateur environ combien d'hommes de la marine attendaient que la bataille commence","10 000"],
             "Death Note": [[questionGame1, answerGame2], [questionGame2, answerGame2], [questionGame3, answerGame2]]
             }
indiceQuestion = 0
indiceReponses = 1

listeMangas = ["One Piece", "Death Note"]

# ------------------------------------------------------------------------------------------------------------#
# GESTIONS DES REPONSES

# ----- MAUVAISES REPONSES -----
timeout = "⏰  **Temps écoulé**"
reponseText = "▫️ Réponses : "
colorEmbedTimeout = discord.Color.from_rgb(204, 61, 61)

# ----- BONNES REPONSES -----
pointVert = "🟢 "
textGoodAnswer = " a donné la bonne réponse"
colorEmbedGoodAnswer = discord.Color.from_rgb(120, 177, 89)

# ----- INDICES -----
nombreTentatives = 2  # nombre de fois que le bot va attendre avant d'envoyer la bonne réponse (envoie un incide à `nombreTentatives`\2`)

# ------------------------------------------------------------------------------------------------------------#
# GESTIONS DU DELAI
delaiEntreEpreuves = 5
delaiEntreQuestions = 5
delaiJoinMessage = 30
delaiQuestions = 20
delaiQuestionsImages = 28
delaiDebutPartie = 3
delaiReponse = 5

# ------------------------------------------------------------------------------------------------------------#
# GESTION DES IMAGES
path = 'images'
pathFlou = 'imagesFloues'
tabTailleResize = [8, 12, 16, 200]

# ------------------------------------------------------------------------------------------------------------#
# GESTION DE L'AFFICHAGE ETC
# idSalon DBV
idChannel = 917858064932163629
idTeam1 = 917917672820322305
idTeam2 = 917922031729799218

