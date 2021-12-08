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
tabEmoji = ["🔵", "🔴"]  # emoji bleu, rouge
tabRole = ["bleu", "rouge"]

# messages DavyBackFight
messageStart = 'dvb'
titreDBV = "Début du Davy BackFight, réagissez au message suivant pour participer"
descriptionDBV = "Equipe bleue / Equipe Rouge"
couleurEmbedDBV = discord.Color.blue()

# Points dvb
indiTab = 0



# QUESTIONS
tabQuestionGame1 = ["Question 1 - 1", "Question 2 - 1", "Question 3 - 1"]
answerGame1 = ["1", "2", "3"]
# --- config jeu 1:
titreJeu1 = "Début du jeu 1"
descriptionJeu1 = "[Règles du jeu numéro 1]"
colorDarkBlueEmbedJeu = discord.Color.dark_blue()

# -------------------------------------------------------------
tabQuestionGame2 = ["Question 2 - 1", "Question 2 - 2", "Question 2 - 3"]
answerGame2 = ["1", "2", "3"]
# --- config jeu 2:
titreJeu2 = "Début du jeu 2"
descriptionJeu2 = "[Règles du jeu numéro 2]"
colorDarkBlueEmbedJeu = discord.Color.dark_blue()

# -------------------------------------------------------------
tabQuestionGame3 = ["Question 3 - 1", "Question 3 - 2", "Question 3 - 3"]
answerGame3 = ["1", "2", "3"]
# --- config jeu 3:
titreJeu3 = "Début du jeu 2"
descriptionJeu3 = "[Règles du jeu numéro 2]"
colorDarkBlueEmbedJeu = discord.Color.dark_blue()


# Messages score et equipe gagnante
titreScoreActuel = "Scores actuels"

colorDarkRedEmbedJeu = discord.Color.dark_red()
# ---

titreWinner = "VAINQUEURS"
colorYellowEmbedJeu = discord.Color.dark_red()


# idSalon DBV
idChannel = 917858064932163629

# Token
token = 'OTE3ODU3ODQ5NTM3ODU5NjI1.Ya-zvA.bNUjZEygSPib0CLujI_7NhOnwHg'
