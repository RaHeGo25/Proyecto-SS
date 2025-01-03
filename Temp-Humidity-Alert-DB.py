import Adafruit_DHT as dht
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import mariadb
import datetime


DHT = 4 #Pin digital 4

# Correo de acceso al servidor
MY_ADDRESS = '*********@hotmail.com'

# Password de acceso a la cuenta de email
PASSWORD = '********.'


# Configurar el servidor de correo
s = smtplib.SMTP(host='smtp.live.com', port=25) # servidor y puerto
s.starttls() # Conexion tls
s.login(MY_ADDRESS, PASSWORD) # Iniciar sesion con los datos de acceso al servidor SMTP


while True:
#Lectura de temperatura y humedad
    h,t = dht.read_retry(dht.DHT11, DHT)

#imprime la temperatura y la humedad
    print('Temperatura={0:0.1f}*C Humedad={1:0.1f}%'.format(t,h))
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    with mariadb.connect(host="XXXXXXX", user="XXXXXX",password="XXXXX", db="XXxXXX") as conn: #conecta a la base de datos
        c=conn.cursor()
    c.execute("INSERT INTO tempdata (Date, Temperature, Humidity) VALUES (%s, %s, %s)",(date, t, h))
    conn.commit()
    sleep(10) #espera 10 segundos y vuleve a hacer otra lectura de datos
    if t > 29:
    # Crear el Mensaje
        msg = MIMEMultipart()
        message = f'¡Verifcar!, La temperatura es muy alta: {t}°'
        # Imprimir el mensaje
        print(message)
    # Configurar los parametros del mensaje
    msg['From']="XXXXXXXX@hotmail.com" #Correo de origen
    msg['To']= "XXXXXXXXXXX@gmail.com" #Correo de destino
    msg['Subject']="XXXXXXXxxXXXXX" #Asunto del mensaje


    # Agregar el texto del mensaje al mensaje
    msg.attach(MIMEText(message, 'plain',"utf-8"))
    # Enviar el mensaje
    s.send_message(msg)
    del msg
    # Finaliar sesion SMTP
    #s.quit()
    print("¡El correo ha sido enviado con exito!")