import sys

from games import *
from logs import *
from traces import *

#load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = str(os.getenv('DISCORD_GUILD'))
IDCHANNEL = int(os.getenv('IDCHANNEL'))

# Partie en cours ?
global partieEnCours, nombreJoueurs, contexteExecution, trace
partieEnCours = False


def diff(li1, li2):
    """ Effectue la différence entre deux listes.

        Parameters
        ----------
        li1 : list
            Une liste de string
        li2 : list
            Une liste de string

        Returns
        -------
        list
            Une liste contenant tous les éléments de `li2` non contenus dans `li1`
    """
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


@client.event
async def on_ready():
    print('Connecte en tant que {0}!'.format(client.user))


async def choixNombreJoueurs():
    """ Methode qui prend en compte le nombre de joueurs dans la partie"""
    global nombreJoueurs
    embed = discord.Embed(
        title="Nombres de joueurs dans la partie ?",
        description=carreBlanc + " 2\n️️" + carreBlanc + " 3\n" + carreBlanc + " 4\n" + carreBlanc + " 5️️\n" + carreBlanc + " 6\n️️" + carreBlanc + " 7\n",
        color=colorEmbedWhiteDBV
    )
    # message = await client.wait_for("reaction_add")
    await client.get_channel(IDCHANNEL).send(embed=embed)


@client.command(aliases=['s'])
async def start(self, message):
    """ Commande de lancement du bot.
        On vérifie si le salon de lancement du jeu est correct, si non on envoie un message
        On vérifie si une partie n'est pas déjà en cours, si oui on envoie un message d'erreur

        Parameters
        ----------
        self :
            contexte d'execution
        message : string
            message pour lancer le jeu voulu
    """
    global contexteExecution, trace
    contexteExecution = self
    message.lower()
    channel = self.channel

    # gestion du mauvais salon
    if IDCHANNEL != channel.id:
        await channel.send(
            f"Je ne peux pas me lancer dans ce salon là :( \n ➡️ {client.get_channel(IDCHANNEL).mention}")
        return

    # gestion de la partie en cours
    if partieEnCours:
        embed = discord.Embed(
            title="Une partie est déjà en cours.",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await self.channel.send(embed=embed)
        return

    # verification que le message est bien "dbf"
    if message.lower() != messageStart.lower():
        await self.channel.send(usageBot)
        return

    # création de la trace pour cette partie
    trace = Traces()
    await removeRoles(self, [])
    # await choixNombreJoueurs()
    embed = discord.Embed(
        title=titreDBV,
        description=descriptionDBV,
        color=colorEmbedWhiteDBV
    )
    embed.set_footer(text="Session lancée par {}".format(self.message.author.display_name),
                     icon_url=self.message.author.avatar)
    choix = await channel.send(embed=embed, delete_after=30.0)
    # ---- trace ------
    trace.createFile(self.message.author.name)

    # ajout des réactions au message du bot
    for emoji in tabEmoji:
        await choix.add_reaction(emoji)

    # suppression du message envoyé par l'utilisateur
    await client.delete_message(self.message)


@start.error
async def start_error(ctx, error):
    """ Gestion d'erreur sur la commande start
        on vérifie que l'erreur `error` est bien une instance de `MissingRequiredArgument`
        on retourne dans le salon d'utilisation un exemple d'usage de la commande

        Parameters
        ----------
        ctx :
            contexte d'execution
        error : erreur
            instance de Error
    """
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(usageBot)
    if isinstance(error, discord.ext.commands.errors.ArgumentParsingError):
        await ctx.send(usageBot)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def restart(self):
    """ Commande de lancement du bot simplifiée.
        Appel la méthode `start`

        Parameters
        ----------
            :param self :
                contexte d'execution
    """
    await start(self, messageStart)
    return


@client.event
async def on_raw_reaction_add(payload):
    """ Méthode d'evenement pour le bot. À l'ajout d'une reaction on va verifie si l'utilisateur qui a effectué
    l'action, - Si c'est le bot lui-même ou un bot, on quitte la fonction pour ne pas le prendre en compte dans le
    traitement - Si c'est un utilisateur, on va chercher la réaction sur laquelle il a cliqué et on va lui ajouter
    le rôle associé, si l'utilisateur clique sur autre réaction de jeu cela lui fait changer de rôle de jeu A la fin
    de la méthode, on lance la méthode d'attente

        Parameters
        ----------
        payload : RawReactionActionEvent
            ensemble des données lorsque l'évenement est réalisé
    """
    global partieEnCours
    member = payload.member

    if member.bot:
        return

    # Verification sur le salon afin d'eviter de prendre en compte des réactions dans des salons non voulus
    if payload.channel_id == IDCHANNEL:
        guild = member.guild
        emoji = payload.emoji.name
        # récuperation du role à assigner à l'utilisateur
        if emoji == tabEmoji[indiceEquipe1]:
            role = discord.utils.get(guild.roles, name=tabRole[indiceEquipe1])
        elif emoji == tabEmoji[indiceEquipe2]:
            role = discord.utils.get(guild.roles, name=tabRole[indiceEquipe2])

        # On va recuperer l'ancien role du joueur (s'il existe)
        ancienRole = diff([role.name], tabRole)
        ancienEmoji = diff([payload.emoji.name], tabEmoji)

        # verification que l'emoji que l'utilisateur a ajouté est dans la liste des emojis autorisé
        # et qu'il a bien un role de jeu différent de celui sur lequel il a cliqué
        if role.name.lower() not in [y.name.lower() for y in member.roles] and ancienRole[0].lower() in [y.name.lower()
                                                                                                         for y in
                                                                                                         member.roles]:
            guild = await(client.fetch_guild(payload.guild_id))
            ancienRole = discord.utils.get(guild.roles, name=ancienRole[0])
            member = await(guild.fetch_member(payload.user_id))
            if member is not None:
                await member.remove_roles(ancienRole, reason=None, atomic=True)

            # on supprime son ancienne réaction
            channel = client.get_channel(IDCHANNEL)
            message = await channel.fetch_message(payload.message_id)
            reaction0 = get(message.reactions, emoji=ancienEmoji[0])
            async for user in reaction0.users():
                if user == member:
                    await reaction0.remove(user)
        # sinon on lui ajoute le role simplement
        await member.add_roles(role)

        await attente_joueur(payload)


@client.event
async def on_raw_reaction_remove(payload):
    """ Méthode d'evenement pour le bot.
        À la suppression d'une reaction, on retire l'utilisateur du rôle associé (s'il existe)

        Parameters
        ----------
        payload : RawReactionActionEvent
            ensemble des données lorsque l'évenement est réalisé
    """
    global partieEnCours
    if not partieEnCours:
        return
    # Verification sur le salon afin d'eviter les traitements sur des salons non voulus
    if payload.channel_id == IDCHANNEL:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        # récuperation du rôle
        if emoji == tabEmoji[0]:
            role = discord.utils.get(guild.roles, name=tabRole[indiceEquipe1])
        elif emoji == tabEmoji[1]:
            role = discord.utils.get(guild.roles, name=tabRole[indiceEquipe2])
        member = await(guild.fetch_member(payload.user_id))

        if member is not None:
            await member.remove_roles(role, reason=None, atomic=True)
        else:
            print("Member not found")


async def attente_joueur(payload):
    """ Méthode d'attente des joueurs.
        À la suppression d'une reaction, on retire l'utilisateur du rôle associé (s'il existe)
        Si le nombre de joueurs requiert est bon, on lance la partie

        Parameters
        ----------
        payload : RawReactionActionEvent
            ensemble des données lorsque l'évenement est réalisé
    """
    global partieEnCours, stopCount
    tabPlayer = [[], []]
    tabPlayerDiscriminator = []
    channel = client.get_channel(IDCHANNEL)
    message = await channel.fetch_message(payload.message_id)
    reactionEquipe1 = get(message.reactions, emoji=tabEmoji[indiceEquipe1])
    reactionEquipe2 = get(message.reactions, emoji=tabEmoji[indiceEquipe2])
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    # le jeu démarrage si on a bien 3 joueurs dans chaque equipe, bot exclu
    if reactionEquipe1 and reactionEquipe2 and (
            reactionEquipe1.count >= nombreJoueursEquipe1 and reactionEquipe2.count >= nombreJoueursEquipe2):

        # récuperation de l'ensemble des joueurs
        async for user in reactionEquipe1.users(limit=nombreJoueursEquipe1):
            if not user.bot:
                tabPlayer[0].append(guild.get_member(user.id).display_name)
                tabPlayerDiscriminator.append(
                    [guild.get_member(user.id).name + "#" + guild.get_member(user.id).discriminator, 0])
        async for user in reactionEquipe2.users(limit=nombreJoueursEquipe2):
            if not user.bot:
                tabPlayer[1].append(guild.get_member(user.id).display_name)
                tabPlayerDiscriminator.append(
                    [guild.get_member(user.id).name + "#" + guild.get_member(user.id).discriminator, 0])
        await reactionEquipe1.clear()
        await reactionEquipe2.clear()
        if not partieEnCours:
            # ---- trace ------
            trace.numberPlayer(tabPlayer)
            partieEnCours = True
            partieEnCours = await lancerJeux(tabPlayer, contexteExecution, tabPlayerDiscriminator, trace)
        await removeRoles(payload, tabPlayer)


async def removeRoles(ctx, players: list):
    """ Methode de retrait des rôles de jeux des joueurs.

        Parameters
        ----------
        ctx : Context
            Context d'execution
        players : list
            tableau contenant des noms des joueurs
    """
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    roleTeam1 = discord.utils.get(guild.roles, name=tabRole[indiceEquipe1])
    roleTeam2 = discord.utils.get(guild.roles, name=tabRole[indiceEquipe2])

    for member in guild.members:
        if member.bot:
            pass
        elif roleTeam1 not in member.roles and roleTeam2 not in member.roles:
            pass
        elif member is not None and member.name not in players:
            await member.remove_roles(roleTeam1, roleTeam2, reason=None, atomic=True)


@client.event
async def delete_message(msg):
    """ Méthode d'evenement pour le bot.
        Supprime le message un message spécifique

    """
    await msg.delete()


@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    """ Méthode d'arret du bot.
        Eteint le bot

    """
    await ctx.channel.send("Le bot se deconnecte")
    await ctx.close()


@client.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    """ Commande d'arret du jeu.
        On vérifie si une partie est en cours ou non
        si oui on redémarre le bot
        si non on annonce qu'aucune partie n'est en cours

    """
    if partieEnCours:
        embed = discord.Embed(
            title="Fin de la partie",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await ctx.channel.send(embed=embed)

        quit()
        await client.login(TOKEN)

    else:
        embed = discord.Embed(
            title="Aucune partie est en cours !",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await ctx.channel.send(embed=embed)


client.run(TOKEN)
