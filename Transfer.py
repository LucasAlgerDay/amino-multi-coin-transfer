from pymino import *
from pymino.ext import *
import aminofix
from pyfiglet import figlet_format
from colored import fore, style
from tqdm import tqdm
from time import sleep



print(
    f"""{fore.CADET_BLUE_1 + style.BOLD}
    Multi Transfer
Script by Lucas Day
Github : https://github.com/LucasAlgerDay"""
)
print(figlet_format("Multi Transfer", font="fourtops"))


bot = Bot(
    command_prefix="!",
    community_id = "24821733"
)  


email = input("email: ")
password = input("password: ")

client = aminofix.Client()
client.login(email, password)


@bot.on_ready()
def ready():
     print(f"{bot.profile.username} acaba de iniciar sesion!")


def invite(chatId, user):
    bot.community.invite_chat(chatId = chatId, userIds= user)

@bot.on_error()
def error(error: Exception):
     print(f"An error has occurred: {error}")
bot.run(email, password)



def vip():
    vips = input("Link Vip: ")
    disponibles = client.get_wallet_info().totalCoins
    print(f"Coins disponibles: {disponibles}")
    total =int(input("Cantidad a donar: "))
    print("\nSugerencia: Para evitar error a la hora de donar no se sugiere bajar de 2 segundos")
    tiempos = int(input("Tiempo por cada donacion: "))
    count = 0
    fok=client.get_from_code(vips)
    communityid=fok.path[1:fok.path.index("/")]
    objectId =  bot.community.fetch_object_id(vips)
    try:
        bot.community.join_community(comId = communityid)
    except:
        print("Asegurate de que la comunidad sea publica, si la cuenta ya se encuentra dentro de la comunidad ignora este mensaje xd")
    for i in tqdm(range(total // 500)):
        try:
            bot.community.subscribe(userId=objectId, comId= communityid)
            count += 500
            sleep(tiempos)
        except Exception as e:
            print(e)
    print(f"Coins enviadas {count}")


def blogs():
    blog = input("Link blog: ")
    disponibles = client.get_wallet_info().totalCoins
    print(f"Coins disponibles: {disponibles}")
    total =int(input("Cantidad a donar: "))
    print("\nSugerencia: Para evitar error a la hora de donar no se sugiere bajar de 2 segundos")
    tiempos = int(input("Tiempo por cada donacion: "))
    count = 0
    fok=client.get_from_code(blog)
    communityid=fok.path[1:fok.path.index("/")]
    objectId =  bot.community.fetch_object_id(blog)
    try:
        bot.community.join_community(comId = communityid)
    except:
        print("Asegurate de que la comunidad sea publica, si la cuenta ya se encuentra dentro de la comunidad ignora este mensaje xd")
    for i in tqdm(range(total // 500)):
        bot.community.send_coins(coins= 500, blogId=objectId, comId= communityid)
        count += 500
        sleep(tiempos)
    print(f"Coins enviadas {count}")


def wikis():
    wiki = input("Link wiki: ")
    disponibles = client.get_wallet_info().totalCoins
    print(f"Coins disponibles: {disponibles}")
    total =int(input("Cantidad a donar: "))
    print("\nSugerencia: Para evitar error a la hora de donar no se sugiere bajar de 2 segundos")
    tiempos = int(input("Tiempo por cada donacion: "))
    count = 0
    fok=client.get_from_code(wiki)
    communityid=fok.path[1:fok.path.index("/")]
    objectId =  bot.community.fetch_object_id(wiki)
    try:
        bot.community.join_community(comId = communityid)
    except:
        print("Asegurate de que la comunidad sea publica, si la cuenta ya se encuentra dentro de la comunidad ignora este mensaje xd")
    for i in tqdm(range(total // 500)):
        bot.community.send_coins(coins= 500, wikiId=objectId, comId= communityid)
        count += 500
        sleep(tiempos)
    print(f"Coins enviadas {count}")

def chats():
    chat = input("Link chat: ")
    disponibles = client.get_wallet_info().totalCoins
    print(f"Coins disponibles: {disponibles}")
    total =int(input("Cantidad a donar: "))
    print("\nSugerencia: Para evitar error a la hora de donar no se sugiere bajar de 2 segundos")
    tiempos = int(input("Tiempo por cada donacion: "))
    count = 0
    fok=client.get_from_code(chat)
    communityid=fok.path[1:fok.path.index("/")]
    objectId =  bot.community.fetch_object_id(chat)
    try:
        bot.community.join_community(comId = communityid)
    except:
        print("Asegurate de que la comunidad sea publica, si la cuenta ya se encuentra dentro de la comunidad ignora este mensaje xd")
    for i in tqdm(range(total // 500)):
        bot.community.send_coins(coins= 500, chatId=objectId, comId= communityid)
        count += 500
        sleep(tiempos)
    print(f"Coins enviadas {count}")


print("1.Transfer Vip")
print("2.Transfer blog")
print("3.Transfer Wiki")
print("4.Transfer Chat")
select = input("Type Number: ")
if select == "1":
	vip()

elif select == "2":
    print("SOLO CON VALORES MULTIPLOS DE 500")
    blogs()

elif select == "3":
    print("SOLO CON VALORES MULTIPLOS DE 500")
    wikis()

elif select == "4":
    print("SOLO CON VALORES MULTIPLOS DE 500")
    chats()
