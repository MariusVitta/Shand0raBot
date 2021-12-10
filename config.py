# Bot
import discord
from discord.ext import commands

# Gestion des commandes du bot
descriptionBot = "Bot pour le Davy Back Fight"
prefixBot = '!'
usageBot = "Usage: " + prefixBot + "start dvb or " + prefixBot + "s dvb "

client = commands.Bot(command_prefix=prefixBot, description=descriptionBot)

# Gestion des Equipes
# https://emojipedia.org/ pour les différents Emojis
tabEmoji = ["☠", "🦊"]  # emoji bleu, rouge
tabRole = ["Equipe 1", "Equipe 2"]
tabRoleBold = ["**Equipe 1**", "**Equipe 2**"]
# messages DavyBackFight
messageStart = 'dvb'
titreDBV = "🎮 Davy Back Fight"
descriptionDBV = "🔹 La partie va débuter dans 30 secondes... \n\n " \
                 "🔸 Pour rejoindre une équipe réagit à l'un des émojis \n\n " \
                 "▫️ ☠️ Equipe 1 \n\n" \
                 "▫️ 🦊 Equipe 2"
colorEmbedWhiteDBV = discord.Color.from_rgb(255, 255, 255)
debutPartieDBV = "🔹 La première épreuve va commencer\n\n"


phraseQuestion = "▫️ **Question**"

# QUESTIONS
tabQuestionGame1 = ["Question 1 - 1"]
answerGame1 = ["1"]
# --- config jeu 1:
descriptionJeu1 = "🔹 **Epreuve 1 / 3** \n\n" + phraseQuestion

# -------------------------------------------------------------
tabQuestionGame2 = ["Question 2 - 1"]

# --- config jeu 2:
descriptionJeu2 = "🔹 **Epreuve 2 / 3** \n\n" + phraseQuestion

# -------------------------------------------------------------
tabQuestionGame3 = ["Question 3 - 1"]

# --- config jeu 3:
descriptionJeu3 = "🔹 **Epreuve 3 / 3** \n\n" + phraseQuestion

tabTextEpreuve = ["🔹 **Epreuve 1 / 3**", "🔹 **Epreuve 2 / 3**", "🔹 **Epreuve 3 / 3** "]

#tableaux
tabQuestions = [tabQuestionGame1, tabQuestionGame2, tabQuestionGame3]
tabAnswers = [answerGame1, answerGame1, answerGame1]
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

# Token
token = 'OTE3ODU3ODQ5NTM3ODU5NjI1.Ya-zvA.5VFzEepFAXlQpQs1TMnahlH_Wv8'
