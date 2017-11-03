#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# RPiP0_OS - v1.6
# Por Nathan Drake (UrbanCompassPony)
# Faca o que quiser deste codigo!

#Bibliotecas Nativas Python
import os
import sys
import math
import time
import datetime
import subprocess
import RPi.GPIO as GPIO

#Bibliotecas que devem ser instalada!
try:
    import tweepy
except:
    print("Por favor, execute: $ sudo pip install tweepy")
    print("Modulo necessario para funcionar o acesso ao Twitter")

try:
    import requests
except:
    print("Por favor, execute: $ sudo pip install requests")
    print("Modulo necessario para funcionar o acesso a cotacao do Bitcoin")

try:
    import Adafruit_SSD1306
except:
    print("Instale o modulo SSD1306 de: https://github.com/adafruit/Adafruit_SSD1306")
    print("Modulo necessario para funcionar o display OLED 0.96 SSD1306")

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)

# Pinos GPIO - Altere se necessario
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 12 Avancar
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 19 Voltar
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 20 Retornar
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 24 it
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 25 Menu
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 26 Ok

#Global Var
RST = 24 # Variavel do Display

loop_main_screen = True
loop_while = True
loop1 = True
loop2 = True
loop3 = True
rows = "not"
ifttt1 = "A"
ifttt2 = "B"
ifttt3 = "C"
x = "0"
y = "0"
pt0 = 0
pt1 = 0
it = 0
doc = 0
menu = 0
wifi = 1
age = 0
document = 0

#Display Code
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

image = Image.new('1', (disp.width, disp.height))
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',14)
#font = ImageFont.load_default()
draw = ImageDraw.Draw(image)

# # # Blocos DEF # # #

def clear():
    time.sleep(0.1)
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)

def reset_var(): #Redefine todas as variaveis globais
    global loop_main_screen
    global loop_while
    global document
    global loop1
    global loop2
    global loop3
    global rows
    global wifi    
    global menu
    global pt0
    global pt1
    global doc
    global age
    global it
    loop_main_screen = True
    loop_while = True
    loop1 = True
    loop2 = True
    loop3 = True
    rows = "not"
    x = "0"
    y = "0"
    document = 0
    wifi = 0
    menu = 0
    pt0 = 0
    pt1 = 0
    doc = 0
    age = 0
    it = 0

def boot(): #Logo de boot do Sistema
    image = Image.open('logo1.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    time.sleep(2) # Duração de Exibição da imagem de boot

def welcome(): #Tela de Bem-Vindo
    draw.text((16, 16), 'RPiP0 - v1.6', font=font, fill=255)
    draw.text((24, 32), 'Bem-Vindo!',  font=font, fill=255)
    draw.line((16,30,111,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(3) # Duração de Exibição da Tela de Boas vindas

def a_menu(): #Menu Primario
    global loop1

    font1 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',15)
    font3 = ImageFont.load_default()
    
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,16,126,16), fill=255)
    draw.text((5, 2), 'RPi Portable Zero', font=font1, fill=255)

    while loop1 == True:

        if GPIO.input(25) == False: # Com aperto
            draw.rectangle((9,30,disp.width-80,disp.height-19), outline=1, fill=255)
            draw.text((11, 30), 'Menu', font=font2, fill=0)
            disp.image(image)
            disp.display()
            clear()
            nav_menu()
            break
        
        else: # Sem aperto
            draw.rectangle((9,30,disp.width-80,disp.height-19), outline=1, fill=0)
            draw.text((11, 30), 'Menu', font=font2, fill=255)
            disp.image(image)
            disp.display()

        if GPIO.input(24) == False: # Com aperto
            draw.rectangle((61,30,disp.width-10,disp.height-19), outline=1, fill=255)
            draw.text((63,30), 'Config', font=font2, fill=0)
            disp.image(image)
            disp.display()
            clear()
            config_menu()
            break
        
        else: # Sem aperto
            draw.rectangle((61,30,disp.width-10,disp.height-19), outline=1, fill=0)
            draw.text((63,30), 'Config', font=font2, fill=255)
            disp.image(image)
            disp.display()

# MENU DE APLICATIVOS #

def nav_menu(): # Navegacao do Menu de App
    global menu
    global loop1

    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()

    #Introdução dos Apps
    draw.rectangle((5,5,disp.width-6,disp.height-6), outline=1, fill=255)
    draw.rectangle((7,7,disp.width-8,disp.height-8), outline=1, fill=0)
    draw.text((16, 16), 'Lista de', font=font, fill=255)
    draw.text((16, 32), 'Aplicativos!',  font=font, fill=255)
    draw.line((16,30,111,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    clear()
    menu = 0

    #Fake Menu dos Apps
    draw.line((0,15,126,15), fill=255)
    draw.line((50,0,50,15), fill=255)
    
    draw.text((55, 2), '0---------', font=font_menu, fill=255)
    draw.text((5, 20), 'Menu de Aplicativos',  font=font_menu2, fill=255)
    draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
    disp.image(image)
    disp.display()    
    
    while loop1 == True:                             
        if GPIO.input(12) == False: # Avanca
            menu = menu +1
            display()
                            
        if GPIO.input(19) == False: # Voltar
            menu = menu -1
            display()
            
        if GPIO.input(26) == False: # Ok
            var_menu()
            if menu == 0:
                pass
            else:
                break

        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            a_menu()
            break
            
        print("nav_menu")
        #time.sleep(0.01)

def display(): #Gera previa do menu em tempo real
    global menu
    
    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()
    clear()
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,15,126,15), fill=255)
    draw.line((50,0,50,15), fill=255)

    if menu < 0:
        menu = 9
        draw.text((55, 2), '---------9', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Energia',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Desliga ou Reinicia',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 0:
        draw.text((55, 2), '0---------', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Aplicativos',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 1:
        draw.text((55, 2), '-1--------', font=font_menu, fill=255)
        draw.text((5, 20), 'Bloco de Notas',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Anotacoes Rapidas',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 2:
        draw.text((55, 2), '--2-------', font=font_menu, fill=255)
        draw.text((5, 20), 'Consulta Bitcoin',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Atualize com It!',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 3:
        draw.text((55, 2), '---3------', font=font_menu, fill=255)
        draw.text((5, 20), 'Roll Text!',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Leitura Rapida',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 4:
        draw.text((55, 2), '----4-----', font=font_menu, fill=255)
        draw.text((5, 20), 'TweePy',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Ver Tweets',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 5:
        draw.text((55, 2), '-----5----', font=font_menu, fill=255)
        draw.text((5, 20), 'Relogio',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Analogico',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 6:
        draw.text((55, 2), '------6---', font=font_menu, fill=255)
        draw.text((5, 20), 'Game:',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Breakout',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Iniciar: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 7:
        draw.text((55, 2), '-------7--', font=font_menu, fill=255)
        draw.text((5, 20), 'Lanterna',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Usa a luz da tela.',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 8:
        draw.text((55, 2), '--------8-', font=font_menu, fill=255)
        draw.text((5, 20), 'Status do Sistema',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Exibe detalhes do OS',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)    
        disp.image(image)
        disp.display()

    elif menu == 9:
        draw.text((55, 2), '---------9', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Energia',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Desliga ou Reinicia',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu > 9:
        menu = 0
        draw.text((55, 2), '0---------', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Aplicativos',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
    
def var_menu(): # Analise da Variavel
    global menu    
    if menu == 1:
        document_a()
    elif menu == 2:
        bitcoin()
    elif menu == 3:
        roll_text()
    elif menu == 4:
        twitter()
    elif menu == 5:
        relogio()
    elif menu == 6:
        breakout()
    elif menu == 7:
        lantern()
    elif menu == 8:
        status_menu()
    elif menu == 9:
        shutdown()

# MENU DE CONFIGURACOES #

def config_menu(): # Navegacao do Menu de App
    global menu
    global loop1

    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()

    #Introdução dos Apps
    draw.rectangle((5,5,disp.width-6,disp.height-6), outline=1, fill=255)
    draw.rectangle((7,7,disp.width-8,disp.height-8), outline=1, fill=0)
    draw.text((16, 16), 'Ajustes do', font=font, fill=255)
    draw.text((16, 32), 'Sistema!',  font=font, fill=255)
    draw.line((16,30,95,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    clear()
    menu = 0

    #Fake Menu dos Apps
    draw.line((0,15,126,15), fill=255)
    draw.line((50,0,50,15), fill=255)
    
    draw.text((55, 2), '0---------', font=font_menu, fill=255)
    draw.text((5, 20), 'Menu de Ajustes',  font=font_menu2, fill=255)
    draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
    disp.image(image)
    disp.display()    
    
    while loop1 == True:                             
        if GPIO.input(12) == False: # Avanca
            menu = menu +1
            config_display()
                            
        if GPIO.input(19) == False: # Voltar
            menu = menu -1
            config_display()
            
        if GPIO.input(26) == False: # Ok
            var_config()
            if menu == 0:
                pass
            else:
                break

        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            a_menu()
            break
            
        print("nav_menu")
        #time.sleep(0.01)

def config_display(): #Gera previa do menu em tempo real
    global menu
    
    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()
    clear()
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,15,126,15), fill=255)
    draw.line((50,0,50,15), fill=255)

    if menu < 0:
        menu = 9
        draw.text((55, 2), '---------9', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 0:
        draw.text((55, 2), '0---------', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Ajustes',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 1:
        draw.text((55, 2), '-1--------', font=font_menu, fill=255)
        draw.text((5, 20), 'Status do Sistema',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Exibe detalhes do OS',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 2:
        draw.text((55, 2), '--2-------', font=font_menu, fill=255)
        draw.text((5, 20), 'Gestor de Redes',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Conecte a um AP',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 3:
        draw.text((55, 2), '---3------', font=font_menu, fill=255)
        draw.text((5, 20), 'Medidor de sinal',  font=font_menu2, fill=255)
        draw.text((5, 30), 'de redes Wifi',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 4:
        draw.text((55, 2), '----4-----', font=font_menu, fill=255)
        draw.text((5, 20), 'IFTTT',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Post Tweet',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 5:
        draw.text((55, 2), '-----5----', font=font_menu, fill=255)
        draw.text((5, 20), 'Comandos SSH',  font=font_menu2, fill=255)
        draw.text((5, 30), '',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 6:
        draw.text((55, 2), '------6---', font=font_menu, fill=255)
        draw.text((5, 20), '',  font=font_menu2, fill=255)
        draw.text((5, 30), '',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 7:
        draw.text((55, 2), '-------7--', font=font_menu, fill=255)
        draw.text((5, 20), '',  font=font_menu2, fill=255)
        draw.text((5, 30), '',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 8:
        draw.text((55, 2), '--------8-', font=font_menu, fill=255)
        draw.text((5, 20), '',  font=font_menu2, fill=255)
        draw.text((5, 30), '',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 9:
        draw.text((55, 2), '---------9', font=font_menu, fill=255)
        draw.text((5, 20), '',  font=font_menu2, fill=255)
        draw.text((5, 30), '',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu > 9:
        menu = 0
        draw.text((55, 2), '0---------', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Ajustes',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
    
def var_config(): # Analise da Variavel
    global menu    
    if menu == 1:
        status_menu()
    elif menu == 2:
        wifi_menu()
    elif menu == 3:
        pass
    elif menu == 4:
        ifttt()
    elif menu == 5:
        pass
    elif menu == 6:
        pass
    elif menu == 7:
        pass
    elif menu == 8:
        pass
    elif menu == 9:
        pass

# APLICATIVOS! #

def document_a():
    global doc
    global loop1

    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()

    #Introdução dos Documentos
    clear()
    draw.rectangle((5,5,disp.width-6,disp.height-6), outline=1, fill=255)
    draw.rectangle((7,7,disp.width-8,disp.height-8), outline=1, fill=0)
    draw.text((16, 16), 'Leitor de', font=font, fill=255)
    draw.text((16, 32), 'Documentos!',  font=font, fill=255)
    draw.line((16,30,100,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    clear()
    
    while loop1 == True:                             
        if GPIO.input(12) == False: # Avanca
            time.sleep(0.1)
            doc = doc +1
            doc_disp()
 
        if GPIO.input(19) == False: # Voltar
            time.sleep(0.1)
            doc = doc -1
            doc_disp()
            
        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            nav_menu()
            break
            
        print("document_a")

def doc_disp():
    global doc

    if doc < 0:
        doc = 3

    if doc > 3:
        doc = 0

    if doc == 1:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        
        with open('/home/pi/RPiP0_OS/doc/text1', 'r') as myfile:
            text1 = myfile.readlines()
            
        draw.text((1, 1), text1[0], font=font_text, fill=255)
        draw.text((1, 10), text1[1],  font=font_text, fill=255)
        draw.text((1, 20), text1[2],  font=font_text, fill=255)
        draw.text((1, 30), text1[3],  font=font_text, fill=255)
        draw.text((1, 40), text1[4],  font=font_text, fill=255)
        draw.text((1, 50), text1[5],  font=font_text, fill=255)
        
        disp.image(image)
        disp.display()
        myfile.close()
            
    elif doc == 2:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        
        with open('/home/pi/RPiP0_OS/doc/text1', 'r') as myfile:
            text1 = myfile.readlines()
            
        draw.text((1, 1), text1[6], font=font_text, fill=255)
        draw.text((1, 10), text1[7],  font=font_text, fill=255)
        draw.text((1, 20), text1[8],  font=font_text, fill=255)
        draw.text((1, 30), text1[9],  font=font_text, fill=255)
        draw.text((1, 40), text1[10],  font=font_text, fill=255)
        draw.text((1, 50), text1[11],  font=font_text, fill=255)
        
        disp.image(image)
        disp.display()
        myfile.close()
        
    elif doc == 3:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        
        with open('/home/pi/RPiP0_OS/doc/text1', 'r') as myfile:
            text1 = myfile.readlines()
            
        draw.text((1, 1), text1[12], font=font_text, fill=255)
        draw.text((1, 10), text1[13],  font=font_text, fill=255)
        draw.text((1, 20), text1[14],  font=font_text, fill=255)
        draw.text((1, 30), text1[15],  font=font_text, fill=255)
        draw.text((1, 40), text1[16],  font=font_text, fill=255)
        draw.text((1, 50), text1[17],  font=font_text, fill=255)
        
        disp.image(image)
        disp.display()
        myfile.close()    

def agenda_disp():
    global age

    if age < 0:
        age = 3
    if age > 3:
        age = 0

    if age == 1:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        font_text2 = ImageFont.load_default()

        with open('/home/pi/RPiP0_OS/doc/agenda', 'r') as myfile:
            text1 = myfile.readlines()

        draw.text((1, 1), text1[0], font=font_text, fill=255)
        draw.text((1, 10), text1[1],  font=font_text, fill=255)
        draw.text((1, 20), text1[2],  font=font_text, fill=255)
        draw.text((1, 30), text1[3],  font=font_text, fill=255)
        draw.text((1, 40), text1[4],  font=font_text, fill=255)
        draw.text((1, 50), text1[5],  font=font_text, fill=255)

        disp.image(image)
        disp.display()
        myfile.close()
            
    if age == 2:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        font_text2 = ImageFont.load_default()

        with open('/home/pi/RPiP0_OS/doc/agenda', 'r') as myfile:
            text1 = myfile.readlines()
            
        draw.text((1, 1), text1[6], font=font_text, fill=255)
        draw.text((1, 10), text1[7],  font=font_text, fill=255)
        draw.text((1, 20), text1[8],  font=font_text, fill=255)
        draw.text((1, 30), text1[9],  font=font_text, fill=255)
        draw.text((1, 40), text1[10],  font=font_text, fill=255)
        draw.text((1, 50), text1[11],  font=font_text, fill=255)
        
        disp.image(image)
        disp.display()
        myfile.close()
        
    if age == 3:
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
        font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
        font_text2 = ImageFont.load_default()

        with open('/home/pi/RPiP0_OS/doc/agenda', 'r') as myfile:
            text1 = myfile.readlines()
            
        draw.text((1, 1), text1[12], font=font_text, fill=255)
        draw.text((1, 10), text1[13],  font=font_text, fill=255)
        draw.text((1, 20), text1[14],  font=font_text, fill=255)
        draw.text((1, 30), text1[15],  font=font_text, fill=255)
        draw.text((1, 40), text1[16],  font=font_text, fill=255)
        draw.text((1, 50), text1[17],  font=font_text, fill=255)
        
        disp.image(image)
        disp.display()
        myfile.close()    

def status_menu():
    global loop1
    while loop1 == True:     
        clear()

        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        x = 2     
        #padding = -2
        #top = padding
        #bottom = height-padding
        
        font = ImageFont.load_default()
        
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)

        #try:
            #cmd = "hostname -I | cut -d\' \' -f1"
        #    cmd = "print ('Sem Conexao!')"

        #except:
         #   cmd = "print ('Sem Conexao!')"
        #IP = subprocess.check_output(cmd, shell = True)

        #try:
         #   cmd = "print ('Sem Conexao!')"

            #cmd = "iwconfig wlan0 |  awk '{print $4, $5, $6}' | grep ESSID"
        #except:
         #   cmd = "print ('Sem Conexao!')"
        #wifi = subprocess.check_output(cmd, shell = True)


        cmd = "top -bn1 | grep load | awk '{printf \"Carga da CPU: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disco: %d / %d Gb %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True)

        #draw.text((x, 0), "IP: " + str(IP), font=font, fill=255)
        #draw.text((x, 8), str(wifi), font=font, fill=255)
        draw.text((x, 16), str(CPU), font=font, fill=255)
        draw.text((x, 25), str(MemUsage), font=font, fill=255)
        draw.text((x, 34), str(Disk), font=font, fill=255)

        disp.image(image)
        disp.display()
                     
        if GPIO.input(20) == False: # Retornar
            clear()
            reset_var()
            nav_menu()
            break

def lantern():
    global loop1

    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=255)
    disp.image(image)
    disp.display()
    
    while loop1 == True:
        GPIO.wait_for_edge(20, GPIO.FALLING)
        clear()
        reset_var()
        nav_menu()
        break

def shutdown():
    global menu
    global loop1

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)

    clear()
    draw.text((1, 1), 'Energia:', font=font, fill=255)
    draw.text((1, 16), 'Press < Desliga', font=font, fill=255)
    draw.text((1, 32), 'Press > Reinicia', font=font, fill=255)
    draw.text((1, 48), 'Retornar cancela', font=font, fill=255)

    disp.image(image)
    disp.display()

    while loop1 == True:                             
        if GPIO.input(19) == False: # Avanca
            time.sleep(0.1)
            os.system('sudo shutdown -h now')
   
        if GPIO.input(12) == False: # Voltar
            time.sleep(0.1)
            os.system("sudo reboot")

        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            nav_menu()
            break
        
def wifi_menu():
    global wifi
    global loop1

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)

    clear()
    draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
    draw.text((1, 10), '  ClassicRock', font=font, fill=255)
    draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
    draw.text((1, 30), '  pfSense', font=font, fill=255)
    draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
    draw.text((1, 50), '  Outro...', font=font, fill=255)
    disp.image(image)
    disp.display()

    while loop1 == True:                             
        if GPIO.input(12) == False: # Avanca
            wifi = wifi +1
            wifi_disp()
        if GPIO.input(19) == False: # Voltar
            wifi = wifi -1
            wifi_disp()
        if GPIO.input(26) == False: # Ok
            wifi_set()
            if wifi == 0:
                pass
            else:
                break

        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            nav_menu()
            break

def wifi_disp():
    global wifi

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font2 = ImageFont.load_default()

    if wifi > 5:
        wifi = 1
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '> ClassicRock', font=font, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '  Outro...', font=font2, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)
        
    elif wifi < 0:
        wifi = 5
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '  ClassicRock', font=font, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '> Outro...', font=font2, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)


    elif wifi == 1:
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '> ClassicRock', font=font2, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '  Outro...', font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)

    elif wifi == 2:
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '  ClassicRock', font=font, fill=255)
        draw.text((1, 20), '> FlorDeMinas', font=font2, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '  Outro...', font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)

    elif wifi == 3:
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '  ClassicRock', font=font, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '> pfSense', font=font2, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '  Outro...', font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)

    elif wifi == 4:
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '  ClassicRock', font=font, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '> ParqueNautico', font=font2, fill=255)
        draw.text((1, 50), '  Outro...', font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)

    elif wifi == 5:
        clear()
        draw.text((1, 1), 'Selecione o Wifi:', font=font, fill=255)
        draw.text((1, 10), '  ClassicRock', font=font, fill=255)
        draw.text((1, 20), '  FlorDeMinas', font=font, fill=255)
        draw.text((1, 30), '  pfSense', font=font, fill=255)
        draw.text((1, 40), '  ParqueNautico', font=font, fill=255)
        draw.text((1, 50), '> Outro...', font=font2, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.1)

def wifi_set(): #Escolher entre os WIFI'S
    global wifi
    global loop3

    if wifi == 1:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Classic")
        clear()
        draw.text((1, 10), 'Definindo Wifi...', font=font, fill=255)
        draw.text((1, 30), 'ClassicRock', font=font, fill=255)
        disp.image(image)
        disp.display()
        os.system('sudo wpa_cli reconfigure')
        os.system('sudo service networking restart')
        time.sleep(2)
        config_menu()
        
    elif wifi == 2:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Hotel")
        clear()
        draw.text((1, 10), 'Definindo Wifi...', font=font, fill=255)
        draw.text((1, 30), 'Flor de Minas', font=font, fill=255)
        disp.image(image)
        disp.display()
        os.system('sudo wpa_cli reconfigure')
        os.system('sudo service networking restart')
        time.sleep(2)
        config_menu()

    elif wifi == 3:
        os.system("sudo /home/pi/RPiP0_OS/wifi/pfSense")
        clear()
        draw.text((1, 10), 'Definindo Wifi...', font=font, fill=255)
        draw.text((1, 30), 'pfSense', font=font, fill=255)
        disp.image(image)
        disp.display()
        os.system('sudo wpa_cli reconfigure')
        os.system('sudo service networking restart')
        time.sleep(2)
        config_menu()

    elif wifi == 4:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Parque")
        clear()
        draw.text((1, 10), 'Definindo Wifi...', font=font, fill=255)
        draw.text((1, 30), 'ParqueNautico!', font=font, fill=255)
        disp.image(image)
        disp.display()
        os.system('sudo wpa_cli reconfigure')
        os.system('sudo service networking restart')
        time.sleep(2)
        config_menu()

    elif wifi == 5:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Outro")
        clear()
        draw.text((1, 10), 'Definindo Wifi...', font=font, fill=255)
        draw.text((1, 30), 'Outro', font=font, fill=255)
        disp.image(image)
        disp.display()
        os.system('sudo wpa_cli reconfigure')
        os.system('sudo service networking restart')
        time.sleep(2)
        config_menu()

def fetch_price(crypto_currency, fiat_currency):
    bitstamp_api = "https://www.bitstamp.net/api/v2/ticker/" + crypto_currency.lower() + fiat_currency.lower()
    try:
        r = requests.get(bitstamp_api)
        return r.json()
    except:
        print("Error fetching from Bitstamp API!")

def get_price_text(crypto_currency, fiat_currency):
    
    data = fetch_price(crypto_currency, fiat_currency)
    return ['{}/{} {}'.format(crypto_currency, fiat_currency, data['last']), '24h Hi {} Lo {}'.format(data['high'], data['low'])]

def show_price():
    font_path = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)

    rows = get_price_text("BTC", "USD")
    draw.text((1, 2), rows[0], font=font2, fill=255)
    draw.text((1, 9), rows[1], font=font2, fill=255)
    disp.image(image)
    disp.display()
    rows = get_price_text("LTC", "USD")
    draw.text((1, 17), rows[0], font=font2, fill=255)
    draw.text((1, 25), rows[1], font=font2, fill=255)
    disp.image(image)
    disp.display()
            
def bitcoin():
    global loop1

    while loop1 == True:
        if GPIO.input(24) == False: # It
            clear()
            show_price()

        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            nav_menu()
            break    

def twitter():
    font_path = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    global rows
    
    ckey = "SUA CHAVE"
    csecret = "SUA CHAVE"
    atoken = "SEU TOKEN"
    asecret = "SEU SEGREDO"

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    stuff = api.user_timeline(screen_name = 'SEU USUARIO DO TWITTER', count = 100, include_rts = True)

    for status in stuff:
        print(status.text)
        rows = status.text
        
    clear()
    draw.text((1, 1), rows, font=font2, fill=255)
    draw.text((1, 15), rows, font=font2, fill=255)
    disp.image(image)
    disp.display()

def roll_text():
    clear()
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',36)
    text = '''SSD1306 ORGANIC LED
    DISPLAY. THIS IS AN
    OLD SCHOOL DEMO SCROLLER
    !! GREETZ TO: LADYADA &
    THE ADAFRUIT CREW,
    TRIXTER, FUTURE CREW,
    AND FARBRAUSCH
    '''
    maxwidth, unused = draw.textsize(text, font=font)
    amplitude = disp.height#/4
    offset = disp.height#/2 - 4
    velocity = -10
    startpos = disp.width

    print('Press Ctrl-C to quit.')
    pos = startpos
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
        # Enumerate characters and draw them offset vertically based on a sine wave.
        x = pos
        for i, c in enumerate(text):
            # Stop drawing if off the right side of screen.
            #if x > disp.width:
                #break
            # Calculate width but skip drawing if off the left side of screen.
            #if x < -10:
            #    char_width, char_height = draw.textsize(c, font=font)
            #    x += char_width
            #    continue
            y = offset
            
            #draw.text((0, 40 + (i * 12)), text, fill=255)
            draw.text((x, y), c, font=font, fill=255)

            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        disp.image(image)
        disp.display()
        pos += velocity
        # Start over if text has scrolled completely off left side of screen.
        #if pos < -maxwidth:
        #    pos = startpos
        time.sleep(0.1)

    #for _ in range(2):
    #    for i, line in enumerate(blurb.split("\n")):
    #        draw.text((0, 40 + (i * 12)), text=line, fill=255)
    #        disp.image(image)
    #        disp.display()
    #        time.sleep(1)

    #for y in range(450):
    #    blurb.set_position((0, y))
    #    disp.image(image)
    #    disp.display()
    #    time.sleep(0.01)

def command():
    pass

def ifttt():
    pass
    #global ifttt1
    #global ifttt2
    #global ifttt3
    
    #ifttt1 = "HA"
    #ifttt2 = "BA"
    #ifttt3 = "FA"

    #os.system("curl -X POST -H "Content-Type: application/json" -d '{'value1':ifttt1,'value2':ifttt2,'value3':ifttt3}' https://maker.ifttt.com/trigger/button_pressed/with/key/iY0FoW1yNGTxP62M2WspRdRbpjLEVm-ChOcNm_ucHDV")

def breakout():
    pass

def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)

def relogio():
    global loop1            
    while loop1 == True:
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")
        margin = 4
        cx = 30
        cy = min(disp.height, 64) / 2
        left = cx - cy
        right = cx + cy

        hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
        hrs = posn(hrs_angle, cy - margin - 7)
        min_angle = 270 + (6 * now.minute)
        mins = posn(min_angle, cy - margin - 2)
        sec_angle = 270 + (6 * now.second)
        secs = posn(sec_angle, cy - margin - 2)

        draw.ellipse((left + margin, margin, right - margin, min(disp.height, 64) - margin), outline=255)
        draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill=255)
        draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill=255)
        draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill=255)

        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=255, outline=255)
        draw.text((2 * (cx + margin), cy - 8), today_date, fill=255)
        draw.text((2 * (cx + margin), cy), today_time, fill=255)
        disp.image(image)
        disp.display()
        clear()
        time.sleep(0.1)

        if GPIO.input(20) == False: # Retornar
            loop1 = False
            reset_var()
            clear()
            nav_menu()
            break          

#FIM DOS DEFs

#Inicio do Sistema

boot()
clear()
welcome()
clear()
a_menu()
