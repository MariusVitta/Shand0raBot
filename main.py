from games import *
from config import *
from logs import *
from token import *
import os

from discord.utils import get

TOKEN = os.getenv('DISCORD_TOKEN')

# discord.ext.commands.errors.CommandNotFound: Command "re" is not found
# await channel.send(f"C'est {message.author.mention} qui a trouvé la bonne, réponse !")
# await channel.send(f"La bonne réponse était {answerGame1[tailleTab]} !")

@client.event
async def on_ready():
    print('Connecte en tant que {0}!'.format(client.user))


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Le bot se deconnecte")
    await ctx.close()


@client.command(aliases=['s'])
async def start(self, message):
    message.lower()
    channel = self.channel
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
        # suppression du message cmd
        await client.delete_message(self.message)


@start.error
async def start_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(usageBot)
        return


@client.command()
async def restart(self):
    await start(self, 'dvb')
    return


@client.command(name='list')
async def _list(ctx, arg):
    pass


@client.event
async def on_raw_reaction_add(payload):
    # print("Ajout de reaction")
    member = payload.member

    if member.bot:
        # print("Ajout de reaction du bot")
        return

    if payload.channel_id == idChannel:
        guild = member.guild
        emoji = payload.emoji.name
        if emoji == tabEmoji[0]:
            role = discord.utils.get(guild.roles, name=tabRole[0])
        elif emoji == tabEmoji[1]:
            role = discord.utils.get(guild.roles, name=tabRole[1])
        await member.add_roles(role)

        await attente_joueur(payload)


@client.event
async def on_raw_reaction_remove(payload):
    # print("Suppression de reaction")
    if payload.channel_id == idChannel:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        if emoji == tabEmoji[0]:
            role = discord.utils.get(guild.roles, name=tabRole[0])
        elif emoji == tabEmoji[1]:
            role = discord.utils.get(guild.roles, name=tabRole[1])
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role, reason=None, atomic=True)
        else:
            print("Member not found")


# en attente de l'ensemble des joueurs
async def attente_joueur(payload):
    channel = client.get_channel(idChannel)
    message = await channel.fetch_message(payload.message_id)
    reaction0 = get(message.reactions, emoji=tabEmoji[0])
    reaction1 = get(message.reactions, emoji=tabEmoji[1])

    if reaction0 and reaction1 and (reaction0.count == 2 and reaction1.count == 1):
        await lancerJeux()
        channel = client.get_channel(idChannel)
        message = await channel.send("Fin du Davy Back Fight")


@client.command()
async def clear(ctx):
    await ctx.channel.purge()


@client.event
async def delete_message(msg):
    await msg.delete()

print("--------------------------------------------------------------------------" + os.getenv('TOKEN'))
client.run(TOKEN)
