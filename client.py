import socket 
import threading
from rsa import *


print('Génération des clé en cours...')
clePb,clePv = genRsaKeyPair(512)
print('Votre clé publique : ',clePb)
# Choosing Nickname
nickname = input("Choisissiez votre pseudo : ")
e = input('Entrez la clé publique de votre interlocuteur :\n e :')
n = input('n : ')
cle = [int(e),int(n)]
'''
    On se connecte au server
    Le client a besoin de deux thread, un qui va recevoir constamment
    les données du serveur et le deuxieme qui va envoyer nos messages 

'''
#Connection To Server
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',5556))

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
            elif first_word == '-':
                split_m = message.split(" ", 2)
                if split_m[1] != nickname + ":":
                    split_m = message.split(" ", 2)
                    dec_m = rsa_dec(int(split_m[2]),clePv)
                    print(split_m[0],split_m[1],dec_m)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("Une erreur !\n, Avez vous bien renseigné une bonne clé ?")
            client.close()
            break

'''
    La fonction v attendre que l'on envoie un message
'''
# Sending Messages to Server
def write():
    while True:
        enc_m = input(nickname + ': ')
        enc_m = rsa_enc(enc_m,cle)
        message = '- {}: {}'.format(nickname, enc_m)
        client.send(message.encode('ascii'))

'''
    Deux threads qui vont lancer les deux fonctions
'''
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()