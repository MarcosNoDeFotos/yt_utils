import serial
PUERTO_ARDUINO = "COM4"
conectado = False
try:
    arduino = serial.Serial(PUERTO_ARDUINO, 9600)
    conectado = True
except Exception as e:
    print("Error al conectar con arduino")
    print(e)
    

def escribirMensaje(msg:str):
    try:
        arduino.write(msg.encode())
    except Exception as e:
        print(e)