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
import subprocess
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
RST = 24 # Variavel do Display - NAO altere
loop_main_screen = True
loop_while = True
loop1 = True
loop2 = True
loop3 = True

menu = 0

pt0 = 0
pt1 = 0
pt2 = 0
pt3 = 0
pt4 = 0
pt5 = 0
pt6 = 0
pt7 = 0
pt8 = 0
pt9 = 0
pt10 = 0
pt11 = 0
pt12 = 0
pt13 = 0
pt14 = 0
pt15 = 0

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
    
    global loop_main_screen
    loop_main_screen = True

    global loop_while
    loop_while = True

    global loop1
    global loop2
    global loop3
    loop1 = True
    loop2 = True
    loop3 = True

    global menu
    menu = 0

    global pt0
    global pt1
    global pt2
    global pt3
    global pt4
    global pt5
    global pt6
    global pt7
    global pt8
    global pt9
    global pt10
    global pt11
    global pt12
    global pt13
    global pt14
    global pt15
    pt0 = 0
    pt1 = 0
    pt2 = 0
    pt3 = 0
    pt4 = 0
    pt5 = 0
    pt6 = 0
    pt7 = 0
    pt8 = 0
    pt9 = 0
    pt10 = 0
    pt11 = 0
    pt12 = 0
    pt13 = 0
    pt14 = 0
    pt15 = 0

def boot(): #Logo do Sistema
    image = Image.open('logo1.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    time.sleep(2)

def welcome(): #Tela de BemVindo
    draw.text((16, 16), 'RPiP0 - v1.2', font=font, fill=255)
    draw.text((24, 32), 'Bem-Vindo!',  font=font, fill=255)
    draw.line((16,30,111,30), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(4)

def a_menu(): #Menu Primario    
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,16,126,16), fill=255)
    draw.ellipse((10,10,10,10), fill=255)
    
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    draw.text((5, 2), 'RPi Portable Zero', font=font2, fill=255)

    font3 = ImageFont.load_default()

    draw.text((10, 20), 'Para iniciar, ',  font=font3, fill=255)
    draw.text((70, 30), 'aperte:',  font=font3, fill=255)
    draw.text((10, 40), 'Menu',  font=font3, fill=255)

    disp.image(image)
    disp.display()

    while loop_main_screen == True:
            GPIO.wait_for_edge(25, GPIO.FALLING)
            clear()
            nav_menu()
            break

def nav_menu(): # Navegacao dos Menus - c_menu
    draw.text((16, 16), 'Lista de', font=font, fill=255)
    draw.text((16, 32), 'Aplicativos!',  font=font, fill=255)
    draw.line((16,30,111,30), fill=255)
    disp.image(image)
    disp.display()
    clear()
    #display()
    
    global menu
    global loop1
    
    try:
        while loop1 == True:                             
            if GPIO.input(12) == False: # Avanca
                time.sleep(0.1)
                menu = menu +1
                display()
                                
            if GPIO.input(19) == False: # Voltar
                time.sleep(0.1)
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
    
    except KeyboardInterrupt:
        quit()

def display(): #Gera previa do menu em tempo real
    global menu
    font_menu = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    font_menu2 = ImageFont.load_default()
    clear()
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)
    draw.line((0,16,126,16), fill=255)

    if menu < 0:
        menu = 0

    elif menu == 0:
        draw.text((5, 2), '0---------', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Aplicativos',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte > ou Retornar',  font=font_menu2, fill=255)
        #draw.text((10, 40), 'Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 1:
        draw.text((5, 2), '-1--------', font=font_menu, fill=255)
        draw.text((5, 20), 'Status do Sistema',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Exibe detalhes do OS',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 2:
        draw.text((5, 2), '--2-------', font=font_menu, fill=255)
        draw.text((5, 20), 'Lanterna',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Usa a luz da tela.',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar', font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
        
    elif menu == 3:
        draw.text((5, 2), '---3------', font=font_menu, fill=255)
        draw.text((5, 20), 'Documento de Texto',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Exibe Documentos',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 4:
        draw.text((5, 2), '----4-----', font=font_menu, fill=255)
        draw.text((5, 20), 'Menu de Energia',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Desliga ou Reinicia',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 5:
        draw.text((5, 2), '-----5----', font=font_menu, fill=255)
        draw.text((5, 20), 'Agenda Telefonica',  font=font_menu2, fill=255)
        draw.text((5, 30), 'Nomes e Telefones',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Aperte: Ok',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 6:
        draw.text((5, 20), 'menu 6',  font=font_menu2, fill=255)
        draw.text((5, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((5, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 7:
        draw.text((10, 20), 'menu 7',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 8:
        draw.text((10, 20), 'menu 8',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 9:
        draw.text((10, 20), 'menu 9',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 10:
        draw.text((10, 20), 'menu 10',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 11:
        draw.text((10, 20), 'menu 11',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 12:
        draw.text((10, 20), 'menu 12',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 13:
        draw.text((10, 20), 'menu 13',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 14:
        draw.text((10, 20), 'menu 14',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()

    elif menu == 15:
        draw.text((10, 20), 'menu 15',  font=font_menu2, fill=255)
        draw.text((10, 30), 'aperte:',  font=font_menu2, fill=255)
        draw.text((10, 40), 'Menu',  font=font_menu2, fill=255)
        #draw.text((60, 50), 'Retornar',  font=font_menu2, fill=255)
        disp.image(image)
        disp.display()
    
def var_menu(): # Analise da Variavel
    global menu    
    if menu == 1:
        status_menu()
    elif menu == 2:
        lantern()
    elif menu == 3:
        document()
    elif menu == 4:
        shutdown()
    elif menu == 5:
        agenda()
    elif menu == 6:
        pass
    elif menu == 7:
        pass
    elif menu == 8:
        pass
    elif menu == 9:
        pass
    elif menu == 10:
        pass
    
def document(): #Entrada App Menu 1
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
    font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    
    with open('/home/pi/text/text1', 'r') as myfile:
        text1 = myfile.readlines()
        
    draw.text((1, 1), text1[2], font=font_text, fill=255)
    draw.text((1, 9), text1[1],  font=font_text, fill=255)
    draw.text((1, 17), text1[3],  font=font_text, fill=255)
    draw.text((1, 25), text1[4],  font=font_text, fill=255)
    draw.text((1, 33), text1[6],  font=font_text, fill=255)
    draw.text((1, 41), text1[5],  font=font_text, fill=255)
    
    disp.image(image)
    disp.display()
    myfile.close()

    while loop_main_screen == True:
        GPIO.wait_for_edge(20, GPIO.FALLING)
        clear()
        reset_var()
        nav_menu()
        break

def status_menu():
    while True:     
        clear()

        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        padding = -2
        top = padding
        bottom = height-padding
        x = 0
        font = ImageFont.load_default()
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True)

        draw.text((x, top+2),       "IP: " + str(IP),  font=font, fill=255)
        draw.text((x, top+10),     str(CPU), font=font, fill=255)
        draw.text((x, top+18),    str(MemUsage),  font=font, fill=255)
        draw.text((x, top+27),    str(Disk),  font=font, fill=255)

        disp.image(image)
        disp.display()
        time.sleep(0.1)

        if loop_main_screen == True:
            GPIO.wait_for_edge(20, GPIO.FALLING)
            clear()
            reset_var()
            nav_menu()
            break
        else:
            print('none')

def agenda(): #Entrada App Menu 1
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)  
    font_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',12)
    
    with open('/home/pi/text/agenda', 'r') as myfile:
        text_agenda = myfile.readlines()
        
    draw.text((1, 1), text_agenda[2], font=font_text, fill=255)
    draw.text((1, 16), text_agenda[1], font=font_text, fill=255)
    draw.text((1, 24), text_agenda[3], font=font_text, fill=255)
    draw.text((1, 32), text_agenda[4], font=font_text, fill=255)
    draw.text((1, 40), text_agenda[6], font=font_text, fill=255)
    draw.text((1, 48), text_agenda[5], font=font_text, fill=255)
    
    disp.image(image)
    disp.display()
    myfile.close()

    while loop_main_screen == True:
        GPIO.wait_for_edge(20, GPIO.FALLING)
        clear()
        reset_var()
        nav_menu()
        break

def g_menu():
    pass

def h_menu():
    pass

def i_menu():
    pass

def j_menu():
    pass
    
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
    else:
        pass

def clear():
    time.sleep(0.1)
    draw.rectangle((0,0,disp.width-1,disp.height-1), outline=1, fill=0)

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
            
        print("nav_menu")

def menu_wifi(): #ESCOLHER ENTRE 2 WIFI'S
    global menu
    global loop3
    #loop3 = False

    if menu == 1:
        os.system("sudo /home/pi/GPIO/Hotel")
        print("Hotel")
        correct()
        ent()
        loop3 = False
        menu1()
    
    elif menu == 3:
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

#FIM DOS DEFs

#Inicio do Programa

boot()
clear()
welcome()
clear()
a_menu()
