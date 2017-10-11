#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Projeto RPiP0
# Por Nathan Drake (Urban Compass Pony)
# Faca o que quiser deste codigo!
# Boa parte do codigo foi escrito em ingles pelo costume.
# Mas os comentarios sao em portugues.

#Libraries
import os
import time
import RPi.GPIO as GPIO
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)

#GPIO Ports
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 12 Avancar
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 19 Voltar
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 20 Retornar
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 24 Neutro
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 25 Menu
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 26 Confirmar

#Global Var
RST = 24
loop_main_screen = True
loop1 = True
loop2 = True
loop3 = True
loop4 = True
loop5 = True
pt0 = 0
pt1 = 0
pt2 = 0
pt3 = 0
pt4 = 0

#Display Code
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

image = Image.new('1', (disp.width, disp.height))
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',14)
draw = ImageDraw.Draw(image)
#font = ImageFont.load_default()

#Blocos DEF

def reset_var(): #Redefine todas as variaveis globais caso necessario
    #Variaveis Globais
    global loop_main_screen
    global loop1
    global loop2
    global loop3
    global loop4
    global loop5
    global pt0
    global pt1
    global pt2
    global pt3
    global pt4
    
    loop_main_screen = True
    loop1 = True
    loop2 = True
    loop3 = True
    loop4 = True
    loop5 = True
    pt0 = 0
    pt1 = 0
    pt2 = 0
    pt3 = 0
    pt4 = 0

def boot(): #Logo do Sistema
    image = Image.open('logo1.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    time.sleep(2)

def welcome(): #Tela de BemVindo
    draw.text((16, 16), 'RPiP0 - v1.0', font=font, fill=255)
    draw.text((24, 32), 'Bem-Vindo!',  font=font, fill=255)
    draw.line((16,30,111,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(4)

def a_menu(): #Menu Primario
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,16,126,16), fill=255)
    
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    draw.text((5, 2), 'RPi Portable Zero', font=font2, fill=255)

    font3 = ImageFont.load_default()
    #font3 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',8)

    draw.text((10, 20), 'Menu',  font=font3, fill=255)
    draw.text((50, 30), 'aperte:',  font=font3, fill=255)
    draw.text((10, 40), 'Menu',  font=font3, fill=255)
    #draw.text((60, 50), 'Retornar',  font=font3, fill=255)

    disp.image(image)
    disp.display()

    while loop_main_screen == True:
        GPIO.wait_for_edge(25, GPIO.FALLING)
        b_menu()
        clear()
        print('a-menu')
        break

def b_menu():
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,16,126,16), fill=255)
    
    font4 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    draw.text((5, 2), 'RPi Portable Zero', font=font4, fill=255)
    draw.text((10, 20), 'Voltar!',  font=font4, fill=255)
    disp.image(image)
    disp.display()

    while loop_main_screen == True:
        GPIO.wait_for_edge(20, GPIO.FALLING)
        clear()
        a_menu()
        print('b-menu')
        break

def c_menu():
    pass

def d_menu():
    pass

def e_menu():
    pass

def f_menu():
    pass

def g_menu():
    pass

def h_menu():
    pass

def i_menu():
    pass

def j_menu():
    pass
    
def lantern():
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=255)

def clear():
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)

def shutdown():
    print("Shutdown Menu")
    clear()
    draw.text((32, 8), 'Desligar?',  size=150, font=font, fill=255)
    draw.text((32, 32), 'Press. 2',  size=150, font=font, fill=255)
    disp.image(image)
    disp.display()
    
    while loop3 == True:
        GPIO.wait_for_edge(24, GPIO.FALLING)
        os.system('sudo shutdown -h now')
    else:
        pass
    
def reboot():
    print("Reboot")
    os.system("sudo reboot")

def menu_wifi(): #ESCOLHER ENTRE 2 WIFI'S
    global pt1
    global loop3
    #loop3 = False
    print("menu wifi")
    print(pt1)

    if pt1 == 1:
        os.system("sudo /home/pi/GPIO/Hotel")
        print("Hotel")
        correct()
        ent()
        loop3 = False
        menu1()
    
    elif pt1 == 3:
        os.system("sudo /home/pi/GPIO/Classic")
        print("Classic")
        correct()
        ent()
        loop3 = False
        menu1()
    else:
        print("FIM DO WIFI")
        return
        
def menu7(): # MENU VERDE - WIFI
    global loop3
    global pt1
    #global loop2
    #loop2 = False
    try:
        while loop3 == True:
                                
            if GPIO.input(25) == False:
                time.sleep(0.1)
                pt1 = pt1 +1
                print(pt1)
                                                
            if GPIO.input(20) == False:
                time.sleep(0.1)
                pt1 = pt1 -1
                print(pt1)
                
            if GPIO.input(5) == False:
                menu4()
            #break
            
            print("MENU VERDE WIFI")

            menu1()
            time.sleep(0.1)
        #break

    except KeyboardInterrupt:
        quit()

def main_menu_a(): # ANALISE DO MENU PRINCIPAL DE 3 OPÇÕES
    global pt0
    global loop2
    global loop1
    loop1 = False
    #while loop2 == True: #ficar no menu2
    
    if pt0 == 1:
        menu3()
        
    elif pt0 == 2:
        menu5()
        
    elif pt0 == 3:
        menu6()
    #else:
     #   pt0 = 2
    

def menu9(): # MENU PRINCIPAL DE 3 OPÇÕES
    global loop0
    loop0 = False
    try:
        while loop1 == True:

            global pt0
                                
            if GPIO.input(25) == False:
                time.sleep(0.1)
                pt0 = pt0 +1
                print(pt0)
                LED0()
                                
            if GPIO.input(20) == False:
                time.sleep(0.1)
                pt0 = pt0 -1
                print(pt0)
                LED0()
                
            if GPIO.input(5) == False:
                menu2()
                break
                
            print("MENU PRINCIPAL")
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        quit()

def ent():
    while loopa == True:
        #loop4 = False
        GPIO.wait_for_edge(19, GPIO.FALLING)
        menu1() #Iniciar Menu 1
        break

#FIM DOS DEFs

#Inicio do Programa

boot()
clear()
welcome()
clear()
a_menu()
