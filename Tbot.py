print("Hola buenas tardes")
import os
import telebot 
from telebot import types
import json
import time
import requests
from flask import Flask
TOKEN = "1707383819:AAH6vydQNj78mRV0BfWwQnDrOSE_O7fUS-Y" # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
server = Flask(__name__)

partidaActual = {} #diccionario de diccionarios (clave= id del usuario, valor= datos de la partida actual)
#almacenar solo jugadores y sus cartas formateadas de la siguiente manera [1H,9S,5H,KD]

@bot.message_handler(commands=['start'])
def comienzo(message):
    bot.reply_to(message, "¡Hola! Este bot te ayudará a resolver partidas de póker. Añade a los jugadores y sus manos y descubre quién gana la partida. Comienza usando el comando /help para ver el uso de los comandos")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Para añadir una nueva mano usa el siguiente comando como se indica \n -> /nuevaMano : [lamano] : [nombreJugador] \n Por ejemplo: /nuevaMano : 2H,3D,5S,9C,KD : Messi \n Cada palo corresponde a la siguiente letra: Tréboles-> C | Rombos -> D | Corazones -> H | Picas -> S \n Para consultas las manos que hay usa /manos \n Una vez tengas los jugadores que deseas, usa /resolver para obtener la resolución de la partida. \n Si deseas borrar un jugador usa /borrarManos [jugador], y si lo quieres borrar todo usa /borrarManos todo ")
 
@bot.message_handler(func=lambda msg: msg.text is not None and '/nuevaMano' in msg.text) #Crea una nuevo jugado con su mano
def at_answer(message):
    try:
        texts = message.text.split(':') #separa por punto y coma
        mano = texts[1].strip() #strip para quitarle los espacios iniciales y finales
        jugador = texts[2].strip()

        uid = message.from_user.id #user id
        if(uid not in partidaActual):
            partidaActual[uid] = {}
        partidaActual[uid][jugador] = mano
        bot.reply_to(message, 'Mano nueva: '+mano + " de " + jugador)
    except Exception:
        bot.reply_to(message, 'Por favor, use correctamente el comando /nuevaMano (ver /help)')
        print("Error provocado por el usuario " + message.from_user.username + "\n Provocado en /nuevaMano")

@bot.message_handler(commands=['manos']) #Solicita los datos de la partida actual
def info(message):
    try:
        uid = message.from_user.id #user id
        bot.reply_to(message, 'Manos en la partida: '+ str(partidaActual[uid]))
    except Exception:
        bot.reply_to(message, 'No has creado manos')
        print("Error provocado por el usuario " + message.from_user.username + "\n Provocado en /manos")

@bot.message_handler(commands=['admin']) #Solicita los datos 
def info(message):
    bot.reply_to(message, 'Todo: '+ str(partidaActual))

@bot.message_handler(func=lambda msg: msg.text is not None and '/borrarManos' in msg.text) #'todo' borra todo, '[jugador]' borra el jugador en concreto
def borrar(message):
    try:
        texts = message.text.split() #separa por espacio
        uid = message.from_user.id #user id
        if(texts[1] == "todo"):
            partidaActual[uid].clear()
            bot.reply_to(message, 'Borrado todo')
        else: #en otro caso se borrará el jugador y su mano con el nombre especificado
            try:
                jugador = texts[1] 
                del partidaActual[uid][jugador]
                bot.reply_to(message, jugador +' ha sido borrado')
            except Exception:
                bot.reply_to(message, 'No existe un jugador con ese nombre')

        bot.reply_to(message, 'Manos en la partida: '+ str(partidaActual[uid]))
    except Exception:
        bot.reply_to(message, 'Por favor, use correctamente el comando /borrarManos (ver /help)')
        print("Error provocado por el usuario " + message.from_user.username + "\n Provocado en /borrarManos")

@bot.message_handler(commands=["resolver"])
def resolver(message):
    try:
        uid = message.from_user.id
        url= 'https://pokersolver.herokuapp.com/api/v1/handTelegram'
        response = requests.post(url, json = partidaActual[uid])
        print(response.json())
        bot.reply_to(message, response.json())
    except Exception:
        bot.reply_to(message, 'Error llamando a la API')

@bot.message_handler(commands=["resolverSample"])
def resolver(message):
    try:
        url= 'https://pokersolver.herokuapp.com/api/v1/hand'
        loPaso = [
                    {
                        "jugadas":[
                            {
                                "jugador":"Cristiano",
                                "apuesta":1000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"H"
                                },
                                {
                                    "valor":"3",
                                    "palo":"D"
                                },
                                {
                                    "valor":"5",
                                    "palo":"S"
                                },
                                {
                                    "valor":"9",
                                    "palo":"C"
                                },
                                {
                                    "valor":"K",
                                    "palo":"D"
                                }
                                ]
                            },
                            {
                                "jugador":"Neymar",
                                "apuesta":20000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"C"
                                },
                                {
                                    "valor":"3",
                                    "palo":"H"
                                },
                                {
                                    "valor":"4",
                                    "palo":"S"
                                },
                                {
                                    "valor":"8",
                                    "palo":"C"
                                },
                                {
                                    "valor":"A",
                                    "palo":"H"
                                }
                                ]
                            }
                        ],
                        "bote":10000
                    },
                    {
                        "jugadas":[
                            {
                                "jugador":"Cristiano",
                                "apuesta":1000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"H"
                                },
                                {
                                    "valor":"3",
                                    "palo":"D"
                                },
                                {
                                    "valor":"5",
                                    "palo":"S"
                                },
                                {
                                    "valor":"9",
                                    "palo":"C"
                                },
                                {
                                    "valor":"K",
                                    "palo":"D"
                                }
                                ]
                            },
                            {
                                "jugador":"Neymar",
                                "apuesta":20000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"D"
                                },
                                {
                                    "valor":"3",
                                    "palo":"H"
                                },
                                {
                                    "valor":"5",
                                    "palo":"C"
                                },
                                {
                                    "valor":"9",
                                    "palo":"S"
                                },
                                {
                                    "valor":"K",
                                    "palo":"H"
                                }
                                ]
                            }
                        ],
                        "bote":0
                    },
                    {
                        "jugadas":[
                            {
                                "jugador":"Cristiano",
                                "apuesta":1000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"H"
                                },
                                {
                                    "valor":"4",
                                    "palo":"S"
                                },
                                {
                                    "valor":"4",
                                    "palo":"C"
                                },
                                {
                                    "valor":"2",
                                    "palo":"D"
                                },
                                {
                                    "valor":"4",
                                    "palo":"H"
                                }
                                ]
                            },
                            {
                                "jugador":"Neymar",
                                "apuesta":20000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"S"
                                },
                                {
                                    "valor":"8",
                                    "palo":"S"
                                },
                                {
                                    "valor":"A",
                                    "palo":"S"
                                },
                                {
                                    "valor":"Q",
                                    "palo":"S"
                                },
                                {
                                    "valor":"3",
                                    "palo":"S"
                                }
                                ]
                            }
                        ],
                        "bote":21000
                    },
                    {
                        "jugadas":[
                            {
                                "jugador":"Cristiano",
                                "apuesta":1000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"H"
                                },
                                {
                                    "valor":"3",
                                    "palo":"D"
                                },
                                {
                                    "valor":"5",
                                    "palo":"S"
                                },
                                {
                                    "valor":"9",
                                    "palo":"C"
                                },
                                {
                                    "valor":"K",
                                    "palo":"D"
                                }
                                ]
                            },
                            {
                                "jugador":"Neymar",
                                "apuesta":20000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"C"
                                },
                                {
                                    "valor":"3",
                                    "palo":"H"
                                },
                                {
                                    "valor":"4",
                                    "palo":"S"
                                },
                                {
                                    "valor":"8",
                                    "palo":"C"
                                },
                                {
                                    "valor":"K",
                                    "palo":"H"
                                }
                                ]
                            },
                            {
                                "jugador":"Maradona",
                                "apuesta":40000,
                                "cartas":[
                                {
                                    "valor":"2",
                                    "palo":"H"
                                },
                                {
                                    "valor":"4",
                                    "palo":"D"
                                },
                                {
                                    "valor":"3",
                                    "palo":"S"
                                },
                                {
                                    "valor":"7",
                                    "palo":"C"
                                },
                                {
                                    "valor":"A",
                                    "palo":"D"
                                }
                                ]
                            }
                        ],
                        "bote":0
                    }
                    ]
        response = requests.post(url, json = loPaso)
        print(response.json())
        n= 1
        for res in response.json():
            bot.reply_to(message, 'Partida '+ str(n) +': '+ res)
            n = n+1
    except Exception:
        bot.reply_to(message, 'Error llamando a la API')


# SERVER SIDE 
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://telebot-pokersolver.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


    


bot.polling()