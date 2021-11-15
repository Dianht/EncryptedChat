import socket 
import threading
from rsa import *


print('Génération des clé en cours...')
clePb,clePv = genRsaKeyPair(512)
cle = []
# Choosing Nickname
nickname = input("Choisissiez votre pseudo : ")
'''
    On se connecte au server
    Le client a besoin de deux thread, un qui va recevoir constamment
    les données du serveur et le deuxieme qui va envoyer nos messages 

'''
#Connection To Server
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',5555))

'''
    Fonction qui va constamment recevoir les messages et les afficher sur l'écran
    Si on recoit le message 'NICK' on envoie notre pseudo
    sinon il y a une erreur alors on arrete la connexion avec le serveur
    et notre boucle
'''
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            first_word = message.split(' ', 1)[0]

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                client.send(str(clePb[0]).encode('ascii'))
                client.send(str(clePb[1]).encode('ascii'))
            elif first_word == 'INFO':
                info = client.recv(1024).decode('ascii')
                print(info)
            elif first_word == 'KEY':
                e =  int(message.split(' ', 3)[1])
                n = int(message.split(' ', 3)[2])
                cle.append(e)
                cle.append(n)
            else:
                print(message)
                
        except:
            # Close Connection When Erro
            print("An error occured!")
            client.close()
            break

'''
    La fonction v attendre que l'on envoie un message
'''
# Sending Messages to Server
def write():
    while True:
        message = input("")
        enc_m = rsa_enc(message,cle)
        message = '{}: {}'.format(nickname,enc_m)
        client.send(message.encode('ascii'))

'''
    Deux threads qui vont lancer les deux fonctions
'''
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()