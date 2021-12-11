# Bot
import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button

global tabPlayer

# ------------------------------------------------------------------------------------------------------------#
# Gestion des commandes du bot
descriptionBot = "Bot pour le Davy Back Fight"
prefixBot = '!'
usageBot = "Usage: " + prefixBot + "start dvb or " + prefixBot + "s dvb "

# CLIENT
client = commands.Bot(command_prefix=prefixBot, description=descriptionBot)
buttons = DiscordComponents(client)

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
tabPlayer = [[], []] # tableau des joueurs
nombreJoueursEquipe1 = 1
nombreJoueursEquipe2 = 2
indiceEquipe1 = 0
indiceEquipe2 = 1

# ------------------------------------------------------------------------------------------------------------#
# MESSAGES DAVYBACKFIGHT
messageStart = 'dvb'
titreDBV = "🎮 Davy Back Fight"
descriptionDBV = "🔹 La partie va débuter dans 30 secondes... \n\n " \
                 "🔸 Pour rejoindre une équipe réagit à l'un des émojis \n\n " \
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

answerGame1 = ["1"]

# tableaux
questions = {"One Piece": [[questionGame1, answerGame1], [questionGame2, answerGame1], [questionGame3, answerGame1]]}
indiceQuestion = 0
indiceReponses = 1

# ------------------------------------------------------------------------------------------------------------#
# GESTIONS DES REPONSES

# ----- MAUVAISES REPONSES -----
timeout = "⏰  **Temps écoulé**"
reponseText = "▫️ Réponse : "
colorEmbedTimeout = discord.Color.from_rgb(204, 61, 61)

# ----- BONNES REPONSES -----
pointVert = "🟢 "
textGoodAnswer = " a donné la bonne réponse"
colorEmbedGoodAnswer = discord.Color.from_rgb(120, 177, 89)

# ------------------------------------------------------------------------------------------------------------#
# GESTIONS DU DELAI
delaiEntreEpreuves = 5
delaiEntreQuestions = 5


# ------------------------------------------------------------------------------------------------------------#
# idSalon DBV
idChannel = 917858064932163629
