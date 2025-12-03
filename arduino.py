import serial
PUERTO_ARDUINO = "COM3"
conectado = False
try:
    arduino = serial.Serial(PUERTO_ARDUINO, 9600)
    print("Conectado con arduino en el puerto "+PUERTO_ARDUINO)
    conectado = True
except Exception as e:
    print("Error al conectar con arduino")
    print(e)
    

def escribirMensaje(msg:str):
    msg += "\n"
    try:
        arduino.write(msg.encode())
    except Exception as e:
        print(e)