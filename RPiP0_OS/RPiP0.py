#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Projeto RPiP0 - v1.4
# Por Nathan Drake (UrbanCompassPony)
# Faca o que quiser deste codigo!

#Bibliotecas Python
import os
import time
import subprocess
import RPi.GPIO as GPIO
import Adafruit_SSD1306

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
RST = 24 # Variavel do Display - NAO altere

loop_main_screen = True
loop_while = True
loop1 = True
loop2 = True
loop3 = True
pt0 = 0
pt1 = 0
it = 0
doc = 0
menu = 0
wifi = 0
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
    document = 0
    wifi = 0
    menu = 0
    pt0 = 0
    pt1 = 0
    doc = 0
    age = 0
    it = 0

def boot(): #Logo de boot do Sistema
    image = Image.open('RPiP0_OS/logo1.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    time.sleep(2) # Duração de Exibição da imagem de boot

def welcome(): #Tela de Bem-Vindo
    draw.text((16, 16), 'RPiP0 - v1.4', font=font, fill=255)
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
        draw.text((5, 20), 'Agenda Telefonica',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Nomes e Telefones',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 3:
        draw.text((55, 2), '---3------', font=font_menu, fill=255)
        draw.text((5, 20), 'Calendario',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Ano: 2017/2018',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 4:
        draw.text((55, 2), '----4-----', font=font_menu, fill=255)
        draw.text((5, 20), 'Comandos SSH',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Conexao Remota',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 5:
        draw.text((55, 2), '-----5----', font=font_menu, fill=255)
        draw.text((5, 20), 'IFTTT',  font=font_menu2, fill=255)
        draw.text((5, 30), 'RPi + IoT',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 6:
        draw.text((55, 2), '------6---', font=font_menu, fill=255)
        draw.text((5, 20), 'Jogo da Cobrinha',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Manual: it',  font=font_menu2, fill=255)
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
        agenda()
    elif menu == 3:
        calendar()
    elif menu == 4:
        command()
    elif menu == 5:
        ifttt()
    elif menu == 6:
        snake()
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
        draw.text((5, 20), 'Conectividade',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Ajuste do Wifi',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        
        disp.image(image)
        disp.display()
        
    elif menu == 3:
        draw.text((55, 2), '---3------', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 4:
        draw.text((55, 2), '----4-----', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 5:
        draw.text((55, 2), '-----5----', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 6:
        draw.text((55, 2), '------6---', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 7:
        draw.text((55, 2), '-------7--', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 8:
        draw.text((55, 2), '--------8-', font=font_menu, fill=255)
        
        disp.image(image)
        disp.display()

    elif menu == 9:
        draw.text((55, 2), '---------9', font=font_menu, fill=255)
        
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
        wifi()
    elif menu == 3:
        pass
    elif menu == 4:
        pass
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

def agenda():
    global age
    global loop1

    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()

    #Introdução da Agenda
    clear()
    draw.rectangle((5,5,disp.width-6,disp.height-6), outline=1, fill=255)
    draw.rectangle((7,7,disp.width-8,disp.height-8), outline=1, fill=0)
    draw.text((16, 16), 'Agenda', font=font, fill=255)
    draw.text((16, 32), 'Telefonica!',  font=font, fill=255)
    draw.line((16,30,100,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    clear()
    
    while loop1 == True:                             
        if GPIO.input(12) == False: # Avanca
            time.sleep(0.1)
            age = age +1
            agenda_disp()
 
        if GPIO.input(19) == False: # Voltar
            time.sleep(0.1)
            age = age -1
            agenda_disp()
            
        if GPIO.input(20) == False: # Retornar
            reset_var()
            clear()
            nav_menu()
            break
            
        print("agenda")

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

def calendar():
    pass

def command():
    pass

def ifttt():
    pass

def snake():
    pass

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

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        #cmd = ""
        #wifi = subprocess.check_output(cmd, shell = True)
        cmd = "top -bn1 | grep load | awk '{printf \"Carga da CPU: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disco: %d / %d Gb %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True)
        
        #cmd = "sudo iwlist wlp3s0 ap"
        #wifi = subprocess.check_output(cmd, shell = True)

        draw.text((x, 0), "IP: " + str(IP), font=font, fill=255)
        draw.text((x, 8), "Wifi: ", font=font, fill=255)
        draw.text((x, 16), str(CPU), font=font, fill=255)
        draw.text((x, 25), str(MemUsage), font=font, fill=255)
        draw.text((x, 34), str(Disk), font=font, fill=255)
        #draw.text((x, 43), str(wifi), font=font, fill=255)        

        disp.image(image)
        disp.display()
        #time.sleep(0.1)
                     
        if GPIO.input(20) == False: # Retornar
            #time.sleep(0.1)
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
            
        print("shutdown")

def imagem():
    pass

def wifi():
    global wifi
    global loop1

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)

    clear()
    draw.text((1, 1), 'Menu Wifi:', font=font, fill=255)
    draw.text((1, 10), 'ClassicRock', font=font, fill=255)
    draw.text((1, 20), 'FlorDeMinas', font=font, fill=255)
    draw.text((1, 30), 'pfSense', font=font, fill=255)
    draw.text((1, 40), 'ParqueNautico', font=font, fill=255)
    draw.text((1, 50), 'Outro...', font=font, fill=255)

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
            
        print("shutdown")

def wifi_disp():
    pass

def wifi_set(): #Escolher entre os WIFI'S
    global menu
    global loop3
    #loop3 = False

    if menu == 1:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Hotel")
        print("Hotel")
    
    if menu == 3:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Classic")
        print("Classic")

    if menu == 3:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Classic")
        print("Classic")

    if menu == 3:
        os.system("sudo /home/pi/RPiP0_OS/wifi/Classic")
        print("Classic")

#FIM DOS DEFs

#Inicio do Programa

boot()
clear()
welcome()
clear()
a_menu()
