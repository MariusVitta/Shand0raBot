from games import *
from logs import *
from token_2 import *
from discord.utils import get


TOKEN = os.getenv('DISCORD_TOKEN')

# Partie en cours ?
global partieEnCours
partieEnCours = False



""" Effectue la différence entre deux liste.

    Parameters
    ----------
    li1 : list
        Une liste de string
    li2 : list
        Une liste de string

    Returns
    -------
    list
        Une liste contenant tout les éléments de `li2` non contenus dans `li1`
"""
def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


@client.event
async def on_ready():
    print('Connecte en tant que {0}!'.format(client.user))


""" Commande de lancement du bot.
    On verifie si le salon de lancement du jeu est correct, si non on envoie un message
    On verfie si une partie est pas déjà en cours, si oui on envoie un message d'erreur
    
    Parameters
    ----------
    self : 
        contexte d'execution
    message : string
        message pour lancer le jeu voulu
"""
@client.command(aliases=['s'])
async def start(self, message):
    global contexteExecution
    contexteExecution= self
    message.lower()
    channel = self.channel

    # gestion du mauvais salon
    if idChannel != self.channel.id:
        await self.channel.send(f"Je ne peux pas me lancer dans ce salon là :( \n ➡️ {client.get_channel(idChannel).mention}")
        return;

    # gestion de la partie en cours
    if partieEnCours == True:
        embed = discord.Embed(
            title="Une partie est déjà en cours.",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await self.channel.send(embed=embed)
        return;

    # verification que le message est bien "dvb"
    if message == messageStart:
        embed = discord.Embed(
            title=titreDBV,
            description=descriptionDBV,
            color=colorEmbedWhiteDBV
        )
        choix = await channel.send(embed=embed)

        # ajout des réactions au message du bot
        for emoji in tabEmoji:
            await choix.add_reaction(emoji)

        # suppression du message envoyé par l'utilisateur
        await client.delete_message(self.message)


""" Gestion d'erreur sur la commande start
    on verifie que l'erreur `error` est bien une instance de `MissingRequiredArgument`
    on retourne dans le salon d'utilisation un exemple d'usage de la commande
    
    Parameters
    ----------
    ctx : 
        contexte d'execution
    error : erreur
        instance de Error
"""
@start.error
async def start_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(usageBot)
        return


""" Commande de lancement du bot simplifiée.
    Appel la méthode `start`

    Parameters
    ----------
    ctx : 
        contexte d'execution
"""
@client.command()
async def restart(self):
    await start(self, 'dvb')
    return;


""" Méthode d'evenement pour le bot.
    A l'ajout d'une reaction on va verifie si l'utilisateur qui a effectué l'action,
        - Si c'est le bot lui même ou un bot, on quitte la fonction pour ne pas le prendre en compte dans le traitement 
        - Si c'est un utilisateur, on va chercher la réaction sur laquelle il a  cliqué et on va lui ajouter le rôle
        associé, si l'utilisateur clique sur autre réaction de jeu cela lui fait changer de rôle de jeu
    A la fin de la méthode, on lance la méthode d'attente
    
    Parameters
    ----------
    payload : RawReactionActionEvent
        ensemble des données lorsque l'évenement est réalisé
"""
@client.event
async def on_raw_reaction_add(payload):

    member = payload.member

    if member.bot:
        return;

    # Verification sur le salon afin d'eviter de prendre en compte des réactions dans des salons non voulus
    if payload.channel_id == idChannel:
        guild = member.guild
        emoji = payload.emoji.name
        # récuperation du role à assigner à l'utilisateur
        if emoji == tabEmoji[0]:
            role = discord.utils.get(guild.roles, name=tabRole[0])
        elif emoji == tabEmoji[1]:
            role = discord.utils.get(guild.roles, name=tabRole[1])

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
            channel = client.get_channel(idChannel)
            message = await channel.fetch_message(payload.message_id)
            reaction0 = get(message.reactions, emoji=ancienEmoji[0])
            async for user in reaction0.users():
                if user == member:
                    await reaction0.remove(user)
        # sinon on lui ajoute le role simplement
        await member.add_roles(role)

        await attente_joueur(payload)


""" Méthode d'evenement pour le bot.
    A la suppression d'une reaction, on retire l'utilisateur du rôle associé (s'il existe)

    Parameters
    ----------
    payload : RawReactionActionEvent
        ensemble des données lorsque l'évenement est réalisé
"""
@client.event
async def on_raw_reaction_remove(payload):
    # Verification sur le salon afin d'eviter les traitements sur des salons non voulus
    if payload.channel_id == idChannel:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        # récuperation du rôle
        if emoji == tabEmoji[0]:
            role = discord.utils.get(guild.roles, name=tabRole[0])
        elif emoji == tabEmoji[1]:
            role = discord.utils.get(guild.roles, name=tabRole[1])
        member = await(guild.fetch_member(payload.user_id))

        if member is not None:
            await member.remove_roles(role, reason=None, atomic=True)
        else:
            print("Member not found")


""" Méthode d'attente des joueurs.
    A la suppression d'une reaction, on retire l'utilisateur du rôle associé (s'il existe)
    Si le nombre de joueurs requiert est bon, on lance la partie
    
    Parameters
    ----------
    payload : RawReactionActionEvent
        ensemble des données lorsque l'évenement est réalisé
"""
async def attente_joueur(payload):
    global partieEnCours, tabPlayer
    tabPlayer = [[], []]

    channel = client.get_channel(idChannel)
    message = await channel.fetch_message(payload.message_id)
    reactionEquipe1 = get(message.reactions, emoji=tabEmoji[indiceEquipe1])
    reactionEquipe2 = get(message.reactions, emoji=tabEmoji[indiceEquipe2])

    # le jeu démarrage si on a bien 3 joueurs dans chaque equipe, bot exclu
    if reactionEquipe1 and reactionEquipe2 and (reactionEquipe1.count >= nombreJoueursEquipe1 and reactionEquipe2.count == nombreJoueursEquipe2):

        # récuperation de l'ensemble des joueurs
        async for user in reactionEquipe1.users():
            if not user.bot:
                tabPlayer[0].append(user.name)
        async for user in reactionEquipe2.users():
            if not user.bot:
                tabPlayer[1].append(user.name)

        partieEnCours = True
        await lancerJeux(tabPlayer,contexteExecution)



@client.command()
async def button(ctx):
    components = [
        Button(label="Button 1", custom_id="button1"),
        Button(label="Button 2", custom_id="button2"),
        Button(label="Button 3", custom_id="button3"),
        Button(label="Button 4", custom_id="button4")
    ]
    random.shuffle(components)
    await ctx.send(
        "**Choix:**",
        components=components
    )
    while True:
        interaction = await client.wait_for("button_click", check=lambda i: i.custom_id == "button1", timeout=15)
        await interaction.channel.send(content="Button clicked!")


@client.command()
async def pixel(ctx):
    print(os.path.splitext("sample.txt")[0])
    img = Image.open('gars.png')
    imgSmall = img.resize((12, 12), resample=Image.BILINEAR)
    result = imgSmall.resize(img.size, Image.NEAREST)
    result.save('gars_32.png')

    await ctx.channel.send(file=discord.File('gars_32.png'))


""" Commande de bot.
    Supprime l'ensemble des messages du salon
    Requiert d'être admin sur le serveur

"""
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    await ctx.channel.purge()


""" Méthode d'evenement pour le bot.
    Supprime le message un message spécifique
    
"""
@client.event
async def delete_message(msg):
    await msg.delete()


""" Méthode d'arret du bot.
    Eteint le bot

"""
@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.channel.send("Le bot se deconnecte")
    await ctx.close()



@client.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    """ Commande d'arret du jeu.
        On verifie si une partie est en cours ou non
        si oui on redemarre le bot
        si non on annonce qu'aucune partie n'est en cours

    """
    if partieEnCours == True:
        embed = discord.Embed(
            title="Fin de la partie",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await ctx.channel.send(embed=embed)
        await client.connect(reconnect=True)
        """await asyncio.sleep(2)
        await client.connect()"""
    else:
        embed = discord.Embed(
            title="Aucune partie est en cours !",
            color=discord.Color.from_rgb(19, 19, 19)
        )
        await ctx.channel.send(embed=embed)

@client.command()
async def getMember(self):
    for guild in client.users:
        print( guild)
    async for guild in client.fetch_guilds(limit=150):
        print(guild.name)

        """guild = client.get_guild(idTeam2)
        memberList = guild.members
        print(memberList)"""

@client.command()
async def deuxLettres(self,mot):
    indice = list("saperlipopette")
    channel = client.get_channel(idChannel)
    car1 = ''
    car2 = ''
    while car1 == car2:
        car1 = random.randrange(0, len(indice))
        car2 = random.randrange(0, len(indice))
    for i in range(len(indice)):
        if i != car1 and i != car2:
            indice[i] = "_"

    mot = "".join(indice)
    print(mot)
    return

    await asyncio.sleep(2)

    await channel.send(car1 + " " + car2)

client.run(token)
