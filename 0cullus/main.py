################################################################################

# Inicio

# NAO USAR O PINO 12!

# Import List
import ubluetooth, machine, gc, sys, uos, dht, math, BME280, ssd1306, esp, time, esp32
from time import sleep; from time import sleep_ms; from machine import TouchPad, Timer, Pin, PWM, SoftI2C; from MMA8452 import MMA8452
esp.osdebug(None)

# LED Azul - Fica ligado durante toda a Inicialização
p0 = Pin(2, Pin.OUT)
p0.on()

# Variáveis
hum = "0"; pres = "wait"; presA = "wait"; tempc = "wait"; tempf = 77
string = 1; string2 = 1; altloc = "wait"; altitude = "wait"; variacao = "wait"
second = -1; altd2 = "wait"; altd3 = "wait"; altd4 = "wait"; altd5 = "wait"
altd6 = "wait"; altd7 = "wait"; altd8 = "wait"; altd11 = "wait"; altd12 = "wait"; altd13 = "wait"
tempd1 = "1"; tempd2 = "15"; tempd3 = "30"; tempd4 = "45"; tempd5 = "1h"; tempd6 = ""
weather = "wait"; frequency = 5000; tempd7 = "115"; tempd8 = "130"; tempd9 = "145"; tempd10 = "2h"; tempd11 = "215"
ble = 0; mins = 0; horas = 0; menupoints = 0; oldpos = 0; newpos = 0

# DHT11
sensor = dht.DHT11(machine.Pin(13))

# Touch Sensor
touch_read = TouchPad(Pin(32)) # Touch can be: 4, 12, 13 14, 15, 27, 32, 33

# Chamadas Protocolo i2c
i2c = SoftI2C(scl=Pin(14), sda=Pin(27), freq=10000) # Sensor 
bme = BME280.BME280(i2c=i2c) # Sensor
i2cc = SoftI2C(scl=Pin(19), sda=Pin(18)) # Display 
disp = ssd1306.SSD1306_I2C(128, 64, i2cc) # Display
i2ccc = SoftI2C(scl=Pin(21), sda=Pin(22)) # Acelerometro
sensor = MMA8452(i2ccc) # Acelerometro

# Clear Display
disp.fill(0) #DISPz4
disp.show() #DISPz5

################################################################################

# Menu!

def menu_points():
  global menupoints
  global touch_read
  
  if touch_read.read() < 480: # Em bateria afetou a leitura
    menupoints = menupoints +1
    sleep(0.1)

    gc.collect()

  gc.collect()  

def menu_select():
  global menupoints

  if menupoints == 0:
    read_sensor1()
    read_sensor2()
    prevtemp()
    display0()
    sleep(0.1)

  if menupoints == 1:
    display1()
    sleep(0.1)

  if menupoints == 2:
    display2()
    sleep(0.1)

  if menupoints == 3:
    display3()
    sleep(0.1)

  if menupoints == 4:
    display4()
    sleep(0.1)

  if menupoints > 4:
    menupoints = 0
    sleep(0.1)

################################################################################

def timer():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global tempd7; global tempd8
  global tempd9; global tempd10; global weather; global altd13
  
  try:

    second = second + 1

    if second > 60: # Modifique o tempo conforme o timer sleep demorar completar 1 minuto!
      second = -1
      mins = mins + 1 # minutos

    if mins == 1:
      altd2 = altitude; tempd1 = tempc
      
    if mins == 15:
      altd3 = altd2; altd2 = altitude; tempd2 = tempd1; tempd1 = tempc
      
    if mins == 30:
      altd4 = altd3; altd3 = altd2; altd2 = altitude; tempd3 = tempd2
      tempd2 = tempd1; tempd1 = tempc

    if mins == 45:
      altd5 = altd4; altd4 = altd3; altd3 = altd2; altd2 = altitude
      tempd4 = tempd3; tempd3 = tempd2; tempd2 = tempd1; tempd1 = tempc
      
    if mins == 60: # 1h
      horas = horas + 1 # horas
      
      altd6 = altd5; altd5 = altd4; altd4 = altd3; altd3 = altd2; altd2 = altitude
      tempd5 = tempd4; tempd4 = tempd3; tempd3 = tempd2; tempd2 = tempd1
      tempd1 = tempc

    if mins == 75: # 1h15
      altd7 = altd6; altd6 = altd5; altd5 = altd4; altd4 = altd3; altd3 = altd2
      altd2 = altitude; tempd6 = tempd5; tempd5 = tempd4; tempd4 = tempd3; tempd3 = tempd2
      tempd2 = tempd1; tempd1 = tempc

    if mins == 90: # 1h30
      altd8 = altd7; altd7 = altd6; altd6 = altd5; altd5 = altd4; altd4 = altd3; altd3 = altd2
      altd2 = altitude; tempd7 = tempd6; tempd6 = tempd5; tempd5 = tempd4; tempd4 = tempd3
      tempd3 = tempd2; tempd2 = tempd1; tempd1 = tempc
      
    if mins == 105: # 1h45
      altd11 = altd8; altd8 = altd7; altd7 = altd6; altd6 = altd5; altd5 = altd4; altd4 = altd3
      altd3 = altd2; altd2 = altitude; tempd8 = tempd7; tempd7 = tempd6; tempd6 = tempd5; tempd5 = tempd4
      tempd4 = tempd3; tempd3 = tempd2; tempd2 = tempd1; tempd1 = tempc
      
    if mins == 120: # 2h
      horas = horas + 1 # horas
      
      altd12 = altd11; altd11 = altd8; altd8 = altd7; altd7 = altd6; altd6 = altd5
      altd5 = altd4; altd4 = altd3; altd3 = altd2; altd2 = altitude; tempd9 = tempd8
      tempd8 = tempd7; tempd7 = tempd6; tempd6 = tempd5; tempd5 = tempd4; tempd4 = tempd3
      tempd3 = tempd2; tempd2 = tempd1; tempd1 = tempc
      
    if mins == 135: # 2h15
      altd13 = altd12; altd12 = altd11; altd11 = altd8; altd8 = altd7; altd7 = altd6
      altd6 = altd5; altd5 = altd4; altd4 = altd3; altd3 = altd2; altd2 = altitude
      tempd10 = tempd9; tempd9 = tempd8; tempd8 = tempd7; tempd7 = tempd6; tempd6 = tempd5
      tempd5 = tempd4; tempd4 = tempd3; tempd3 = tempd2; tempd2 = tempd1; tempd1 = tempc
      
    if mins > 135:
       mins = 0
    gc.collect()
    #break
  except:
    gc.collect()
    #break
  else:
    gc.collect()
    #break


################################################################################

# Previsão do Tempo

def read_sensor1():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global tempd7; global tempd8
  global tempd9; global tempd10; global weather; global altd13

  try:
    tempc = bme.temperature; tempc = tempc.replace("C","")
    tempc = math.trunc(float(tempc))
    
    pres = bme.pressure; pres = pres.replace("hPa","")
    presA = bme.pressure; presA = pres.replace("hPa","")
    presA = math.trunc(float(presA))

    # Calculo da Altitude
    pres2 = float(pres)*float(100)
    altitude = float(pres2)/float(101325)
    altitude = math.log(float(altitude))
    altitude = float(altitude)*float(287.053)
    altf = float(tempf)+float(459.67)
    altf = float(altf)*float(5/9)
    altitude = float(altf)*float(altitude)
    altitude = float(altitude)/float(-9.8)
    altitude = math.trunc(float(altitude))

    if string == 1:
      string = 0
      altloc = str(altitude)
    
    variacao = float(altloc)-float(altitude)
    variacao = -float(variacao) # Se variou acima, positivo. Se desceu, negativo.
    variacao = math.trunc(float(variacao))

    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()

def read_sensor2():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global tempd7; global tempd8
  global tempd9; global tempd10; global weather; global altd13

  try:
    sensor.measure(); hum = sensor.humidity()
  except:
    gc.collect()
  else:
    gc.collect()
    
def prevtemp():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global weather; global tempd7
  global tempd8; global tempd9; global tempd10; global altd13
  
  try:
    if int(altitude) > 600: # Detectando região: Uberaba (altitude média 795m)
      if int(altitude) > 795 and int(tempc) > 27: # Ceu Limpo e Calor
        weather = str("Condicao Alpha")
      elif int(altitude) > 800 and int(tempc) < 24: # Ceu Limpo e Frio
        weather = str("Condicao Beta")
      elif int(altitude) < 750 and int(tempc) > 27: # Nublado e Calor
        weather = str("Condicao Gamma")
      elif int(altitude) < 750 and int(tempc) < 27 and int(tempc) > 24: # Tempestade
        weather = str("Condicao Delta")
      else:
        weather = str("Tempo Estavel")
       
    else: # Detectando região: Rifaina (altitude média 565m)
      if int(altitude) > 400:
        weather = str("Prob.Chuva:400")
  except:
    gc.collect()

def display0():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global weather; global tempd7
  global tempd8; global tempd9; global tempd10; global altd13

  try:     
    disp.fill(0)
    
    disp.hline(1, 53, 126, 1) # de 20 pra 50 preenche até o fim
    disp.vline(33, 1, 52, 1) # Principal Divisao

    disp.text("  Temp Celsius", 18, 1)
    disp.text("  % Humidade", 18, 12)
    disp.text("Pressao hPA", 34, 23)
    disp.text("Am TempoReal", 34, 34)
    disp.text("Delta A.m", 42, 45)
    
    disp.text(str(tempc), 0, 1)
    disp.text(str(hum), 0, 12)
    disp.text(str(presA), 0, 23) 
    disp.text(str(altitude), 0, 34)
    disp.text(str(variacao), 0, 45)
    
    disp.text(str(weather), 0, 56)
    
    disp.show()
    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()

def display1():
  global tempc; global tempf; global hum; global pres; global presA; global altitude
  global variacao; global altloc; global string; global string2; global second; global altd2
  global altd3; global altd4; global altd5; global altd6; global altd7; global altd8
  global mins; global horas; global altd11; global altd12; global tempd1; global tempd2
  global tempd3; global tempd4; global tempd5; global tempd6; global weather; global tempd7
  global tempd8; global tempd9; global tempd10; global altd13

  try:     
    disp.fill(0)

    disp.hline(1, 53, 126, 1) # de 20 pra 50 preenche até o fim
    disp.vline(58, 1, 52, 1) # Principal Divisao

    disp.text(str(altd2), 1, 1)
    disp.text(str(altd3), 1, 12) 
    disp.text(str(altd4), 1, 23)
    disp.text(str(altd5), 1, 34)
    disp.text(str(altd6), 1, 45)
    
    disp.text(":", 32, 1)
    disp.text(":", 32, 12)
    disp.text(":", 32, 23)
    disp.text(":", 32, 34)
    disp.text(":", 32, 45)
    
    disp.text(str(tempd1), 39, 1)
    disp.text(str(tempd2), 39, 12)
    disp.text(str(tempd3), 39, 23)
    disp.text(str(tempd4), 39, 34)
    disp.text(str(tempd5), 39, 45)
    
    disp.text(str(altd7), 62, 1)
    disp.text(str(altd8), 62, 12) 
    disp.text(str(altd11), 62, 23)
    disp.text(str(altd12), 62, 34)
    disp.text(str(altd13), 62, 45)

    disp.text(":", 93, 1)
    disp.text(":", 93, 12)
    disp.text(":", 93, 23)
    disp.text(":", 93, 34)
    disp.text(":", 93, 45)

    disp.text(str(tempd7), 100, 1)
    disp.text(str(tempd8), 100, 12)
    disp.text(str(tempd9), 100, 23)
    disp.text(str(tempd10), 100, 34)
    disp.text(str(tempd11), 100, 45)
    
    disp.text(str(weather), 0, 56)
    
    disp.show()
    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()
      
################################################################################

# Acelerometro

def acelerometro():
  try:
    global oldpos

    if not sensor.begin():
        print ("Sensor não detectado")

    sensor.active()
    sensor.setupPL()
    oldpos = -1
    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()
    
def conv(acel):
  try:
    coord = int ((acel+1)*31)
    if coord > 63:
        coord = 63
    elif coord < 0:
        coord = 0
    return coord
    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()

  # Rotina para converter leitura em coordenada
  # Assume que leitura estará entre -1g e +1g

def display2():
  global newpos; global oldpos
  
  disp.fill(0)
  disp.text("Giroscopio:", 2, 2)

  # Testa se mudou de posição
  acel = sensor.getCalclulatedAcel()
  newpos = sensor.readPL()

  # Mostra a aceleração (assume-se que está entre -1g e +1g)
  x = conv(acel[0])
  y = conv(acel[1])
  z = conv(acel[2])
  
  # rect (retangulo): x, y, comprimento, largura, cor
# Soma o valor de X rect ao valor fixado da condicional if sempre que movimentar as barras no disp! 
# O valor fixado do codigo original é 34, moveu, some o novo valor a 34.

# Eixo X
  disp.rect (16, 14, 64, 10, 1)
  disp.fill_rect (17, 15, 62, 8, 0)
  disp.text("X:", 2, 15)
  
  if x < 32:
      disp.fill_rect (x+17, 15, 33-x, 8, 1)
  else:
      disp.fill_rect (49, 15, x-31, 8, 1)
  gc.collect()
  
# Eixo Y
  disp.rect (16, 34, 64, 10, 1)
  disp.fill_rect (17, 35, 62, 8, 0)
  disp.text("Y:", 2, 35)
  if y < 32:
      disp.fill_rect (y+17, 35, 33-y, 8, 1)
  else:
      disp.fill_rect (49, 35, y-31, 8, 1)
  gc.collect()
  
# Eixo Z
  disp.rect (16, 54, 64, 10, 1)
  disp.fill_rect (17, 55, 62, 8, 0)
  disp.text("Z:", 2, 55)
  if z < 32:
      disp.fill_rect (z+17, 55, 33-z, 8, 1)
  else:
      disp.fill_rect (49, 55, z-31, 8, 1)
  gc.collect()
  
# Show
  disp.show()
  gc.collect()

################################################################################

# Bluetooth

class BLE():
  def __init__(self, name):   
    self.name = name
    self.ble = ubluetooth.BLE()
    self.ble.active(True)

    self.led = Pin(2, Pin.OUT)
    self.timer1 = Timer(0)
    self.timer2 = Timer(1)
        
    self.disconnected()
    self.ble.irq(self.ble_irq)
    self.register()
    self.advertiser()

  def connected(self):        
    self.timer1.deinit()
    self.timer2.deinit()

  def disconnected(self):        
    self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
    sleep_ms(200)
    self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

  def ble_irq(self, event, data):
    if event == 1:
      '''Central disconnected'''
      self.connected()
      self.led(1)
             
    elif event == 2:
      '''Central disconnected'''
      self.advertiser()
      self.disconnected()
              
    elif event == 3:
      '''New message received'''            
      buffer = self.ble.gatts_read(self.rx)
      message = buffer.decode('UTF-8').strip()
      print(message)

# Messages!

      if message == 'redled':
        Pin(2, Pin.OUT).value(not Pin(2, Pin.OUT).value())
        ble.send('red_led' + str(Pin(2, Pin.OUT).value()))
        color = int(Pin(2, Pin.OUT).value())
      
        if color == 0:
          try:
            gc.collect()
            #disp.fill(0)
            #disp_1("Desligado", 0, 0, 0, 0, 0)
            #disp.show()
          except:
            gc.collect()
          else:
            gc.collect()
          
        if color == 1:
          try:
            gc.collect()
            #disp.fill(0)
            #disp_1("Ligado", 0, 0, 0, 0, 0)
            #disp.show()
          except:
            gc.collect()
          else:
            gc.collect()
                    
  def register(self):        
    # Nordic UART Service (NUS)
    NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
    RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
    TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
    BLE_NUS = ubluetooth.UUID(NUS_UUID)
    BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
    BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
           
    BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
    SERVICES = (BLE_UART, )
    ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

  def send(self, data):
    self.ble.gatts_notify(0, self.tx, data + '\n')
  def advertiser(self):
    name = bytes(self.name, 'UTF-8')
    self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)

# Display OLED

def disp_1(a, b, c, d, e, f):
  try:
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    #disp.text("Conectado!", 2, 2)
    #disp.hline(1, 12, 126, 1)
    disp.text(a, 2, 3)
    disp.text(b, 2, 13)
    disp.text(c, 2, 23)
    disp.text(d, 2, 33)
    disp.text(e, 2, 43)
    disp.text(f, 2, 53)
  
    disp.show()
    gc.collect()
  except:
    gc.collect()
  else:
    gc.collect()

################################################################################

# Informações do Hardware

def display3():
  global tempf0; global hall0; global horas; global mins

  tempf0 = esp32.raw_temperature()
  tempf0 = (tempf0 - 32) // 1.8

  hall0 = esp32.hall_sensor()
  
  disp.fill(0)
  #disp.rect(0, 0, 126, 64, 1)
  disp.text("Informacoes:", 2, 2)
  disp.hline(1, 12, 126, 1)
  disp.text("Temp. CPU: " + str(tempf0), 2, 14)

  #print(hall0)
  
  disp.rect (50, 26, 40, 3, 1) # > ==
  disp.fill_rect (50, 26, 40, 3, 0) # > ==
  
  if hall0 < 100:
      disp.fill_rect (int(hall0)+26, 26, 126-int(hall0), 3, 1) # < ==
  else:
      disp.fill_rect (50, 26, int(hall0)-103, 3, 1) # == >
  
  disp.text("Hall.: ", 2, 24) #+ str(hall0)
  
  disp.text("Uptime: " + str(horas) + ":" + str(mins), 2, 34)
  disp.text(" ", 2, 44)
  disp.text("RAM Livre:" + str(gc.mem_free()), 2, 54)
  
  disp.show()
  gc.collect()

################################################################################

def display4():
  global ble
  global menupoints

  disp.fill(0)
  disp.rect(0, 0, 126, 64, 1)
  disp.text("Bluetooth", 2, 2)
  disp.hline(1, 12, 126, 1)
  disp.text("ERROR.", 2, 13)
  disp.text("Reiniciando...", 2, 23)
  disp.show()
  
  # Habilitando Bluetooth!
  try:
    ble = BLE("0cculus")
    menupoints = 0
  except:
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    disp.text("Bluetooth", 2, 2)
    disp.hline(1, 12, 126, 1)
    disp.text("ERROR!", 2, 13)
    disp.text("Tente novamente", 2, 23)
    disp.show()
    sleep(2)
    gc.collect()
  else:
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    disp.text("Bluetooth", 2, 2)
    disp.hline(1, 12, 126, 1)
    disp.text("Bem-Sucedido!", 2, 13)
    disp.text(" ", 2, 23)
    disp.show()
    sleep(2)
    gc.collect()
    
################################################################################

# Sensor Hall

def hall_sensor():
  global hall0
  
  hall0 = esp32.hall_sensor()
  
  if hall0 > 130 or hall0 < 50: 
  
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    disp.text("  ALERTA HALL!", 2, 2)
    disp.hline(1, 12, 126, 1)
    disp.text("   Campo", 2, 18)
    disp.text("   Magnetico", 2, 28)
    disp.text("   Intenso", 2, 38)
    disp.text("   Detectado!", 2, 48)
    #disp.text("32 GPIO", 2, 54)
  
    disp.show()
    sleep(3)
    gc.collect()
  
################################################################################

# Sensor Temperatura

def temp_sensor():
  global tempf0
  
  tempf0 = esp32.raw_temperature()
  tempf0 = (tempf0 - 32) // 1.8
  
  if tempf0 > 60: 
  
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    disp.text("  ALERTA TEMP!", 2, 2)
    disp.hline(1, 12, 126, 1)
    #disp.text("     Alta", 2, 18)
    disp.text("  Altissima", 2, 28)
    disp.text("  Temperatura", 2, 38)
    disp.text("  Detectada!", 2, 48)
    #disp.text("32 GPIO", 2, 54)
  
    disp.show()
    sleep(3)
    gc.collect()
    
  if tempf0 < 10: 
  
    disp.fill(0)
    disp.rect(0, 0, 126, 64, 1)
    disp.text("  ALERTA TEMP!", 2, 2)
    disp.hline(1, 12, 126, 1)
    #disp.text("    Intenso", 2, 18)
    disp.text("   Baixissima", 2, 28)
    disp.text("   Temperatura", 2, 38)
    disp.text("   Detectada!", 2, 48)
    #disp.text("32 GPIO", 2, 54)
  
    disp.show()
    sleep(3)
    gc.collect()
  
################################################################################

# Inicializar o Sistema Principal #

hall_sensor() # hall da esp32 ao ligar
temp_sensor() # temp da esp32 ao ligar
acelerometro() # calibrar acelerometro
p0.off() # desligar led azul ao concluir todo o boot!

while True: # O que executa aqui, executa independentemente do menu escolhido!

  timer() # Horas e Minutos em tempo real
  read_sensor1 # Sensor Temp e Pressao Real Time
  read_sensor2 # Sensor Umidade Real Time

  menu_points() # Select A Valores
  menu_select() # Select B Menus
  
  #weather = touch_read.read()
# Fim

################################################################################
