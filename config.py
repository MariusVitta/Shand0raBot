# Bot
import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button


# Gestion des commandes du bot
descriptionBot = "Bot pour le Davy Back Fight"
prefixBot = '!'
usageBot = "Usage: " + prefixBot + "start dvb or " + prefixBot + "s dvb "

client = commands.Bot(command_prefix=prefixBot, description=descriptionBot)
buttons = DiscordComponents(client)

# Gestion des Equipes
# https://emojipedia.org/ pour les différents Emojis
tabEmoji = ["☠", "🦊"]  # emoji bleu, rouge
medaillePremier = "🥇"
medailleSecond = "🥈"
mugiBoutonBlanc = "▫️ ☠️ Mugiwara :"
foxyBoutonBlanc = "▫️ 🦊 Foxy :"
tabRole = ["Mugiwara", "Foxy"]
tabRoleBold = ["**Mugiwara**", "**Foxy**"]

# messages DavyBackFight
messageStart = 'dvb'
titreDBV = "🎮 Davy Back Fight"
descriptionDBV = "🔹 La partie va débuter dans 30 secondes... \n\n " \
                 "🔸 Pour rejoindre une équipe réagit à l'un des émojis \n\n " \
                 "▫️ ☠️ Mugiwara \n\n" \
                 "▫️ 🦊 Foxy"
colorEmbedWhiteDBV = discord.Color.from_rgb(255, 255, 255)
debutPartieDBV = "🔹 La première épreuve va commencer\n\n"

phraseQuestion = "▫️ **Question**"

# QUESTIONS
questionGame1 = "Question 1 - 1"
answerGame1 = ["1"]
# --- config jeu 1:
descriptionJeu1 = "🔹 **Epreuve 1 / 3** \n\n" + phraseQuestion

# -------------------------------------------------------------
questionGame2 = "Question 2 - 1"

# --- config jeu 2:
descriptionJeu2 = "🔹 **Epreuve 2 / 3** \n\n" + phraseQuestion

# -------------------------------------------------------------
questionGame3 = "Question 3 - 1"

# --- config jeu 3:
descriptionJeu3 = "🔹 **Epreuve 3 / 3** \n\n" + phraseQuestion

tabTextEpreuve = ["🔹 **Epreuve 1 / 3**", "🔹 **Epreuve 2 / 3**", "🔹 **Epreuve 3 / 3** "]

# tableaux
questions = {"One Piece": [[questionGame1, answerGame1], [questionGame2, answerGame1], [questionGame3, answerGame1]]}
indiceQuestion = 0
indiceReponses = 1


# tabQuestions = [tabQuestionGame1, tabQuestionGame2, tabQuestionGame3]
# tabAnswers = [answerGame1, answerGame1, answerGame1]
tabDescriptions = [descriptionJeu1, descriptionJeu2, descriptionJeu3]
tabEpreuves = ["Epreuve 1", "Epreuve 2", "Epreuve 3"]

# Gestions réponses
## mauvaises réponses
timeout = "⏰  **Temps écoulé**"
reponseText = "▫️ Réponse : "
colorEmbedTimeout = discord.Color.from_rgb(204, 61, 61)
## bonnes réponse
pointVert = "🟢 "
textGoodAnswer = " a donné la bonne réponse"
colorEmbedGoodAnswer = discord.Color.from_rgb(120, 177, 89)

carreBlanc = "▫️"

# Messages score et equipe gagnante
titreScoreActuel = "Scores actuels"

colorDarkRedEmbedJeu = discord.Color.dark_red()
# ---

titreWinner = "VAINQUEURS"
colorYellowEmbedJeu = discord.Color.dark_red()




# idSalon DBV
idChannel = 917858064932163629
