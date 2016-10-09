#!/usr/bin/python

# Install Telebot: git clone https://github.com/eternnoir/pyTelegramBotAPI.git

import telebot
import logging
import os
import sys
from telebot import types
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

TOKEN = "254655344:AAFV_iiWL3MprmuBAfSWzZ5Jd56wFc_G8rc"

BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

bot = telebot.TeleBot(TOKEN)

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

def send_message(cid, text):
    bot.send_message(cid, text)

def send_document(cid, document):
    bot.send_document(cid, document)

def reply_to(message, text):
    bot.reply_to(message, text)

@bot.inline_handler(lambda query: query.query == '')
def query_text(inline_query):
    try:
       days = []
       result_final = types.InlineQueryResultArticle('6', 'Obtener programa completo', types.InputTextMessageContent('/programa_completo'))
       days.append(result_final)
       for i in range(7, 17):
          result = types.InlineQueryResultArticle(str(i), 'Obtener dia ' + str(i), types.InputTextMessageContent('/dia ' + str(i)))
          days.append(result)
       bot.answer_inline_query(inline_query.id, days)
    except Exception as e:
        print("Exception : " + e)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    reply_to(message, "Este es el bot de Telgram que te informa de los actos de cada dia en las fiestas del Pilar 2016 (del 7 al 16 de Octubre)\n\nModo de uso:\n\n/dia NUMERO_DE_DIA\n\nEjemplo: /dia 7\n\nPara obtener el programa completo:\n\n/programa_completo")

@bot.message_handler(commands=['dia'])
def command_dia(message):
    cid = message.chat.id
    original_message = str(message.text).lower()
    if ('/dia' in original_message):
    	check_string = message.text.replace("/", "")
        check_string = check_string.replace(" ", "_")
        text_file = BASE_PATH + "/pilar2016_" + check_string + ".txt"
        if os.path.isfile(text_file) == False:
           send_message(cid, "Por favor escribe el comando /dia NUMERO_DE_DIA para obtener los actos del dia.")
        else:
           send_message(cid, "Enviando archivo....")
           doc = open(text_file, 'rb')
           send_document(cid, doc)
           send_message(cid, "Archivo enviado. Gracias.")
    else:
        send_message(cid, "Por favor escribe el comando /dia NUMERO_DE_DIA para obtener los actos del dia.")

@bot.message_handler(commands=['programa_completo'])
def command_programa_completo(message):
    cid = message.chat.id
    send_message(cid, "Enviando programa completo....")
    for i in range(7,17):    
        text_file = BASE_PATH + "/pilar2016_dia_" + str(i) + ".txt"
        doc = open(text_file, 'rb')
        bot.send_document(cid, doc)
    send_message(cid, "Programa de Fiestas del Pilar 2016 enviado. Gracias.")

bot.polling(none_stop=True, interval=0)
