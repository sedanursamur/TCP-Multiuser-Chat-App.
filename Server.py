from socket import AF_INET, socket, SOCK_STREAM  
from threading import Thread

clients = {}          
addresses = {}   

HOST = '127.0.0.1'  
PORT = 55555        
BUFSIZ = 1024         
ADDR = (HOST, PORT)  

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)



def accept_incoming_connections():                           

    while True:                                              
        client, client_address = SERVER.accept()
        print("%s:%s bağlandı..." % client_address)
        client.send(bytes("__________________________ MESAJLAŞMAYA BAŞLAMAK İÇİN BİR KULLANICI İSMİ BELİRLEYİNİZ... _________________________________\n\n\n", "utf8"))
        addresses[client] = client_address                   
        Thread(target=handle_client, args=(client,)).start()  


def handle_client(client):                                   

    name = client.recv(BUFSIZ).decode("utf8")                


    giris = 'Hoşgeldin %s! Çıkmak istiyorsanız, çıkmak için $cıkıs yazın.\n' % name    
    client.send(bytes(giris, "utf8"))

    msg = "@ %s sohbete katıldı..." % name
    broadcast(bytes(msg, "utf8"))                          
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)                           
        if msg != bytes("$cıkıs", "utf8"):                  
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("$cıkıs", "utf8"))             
            client.close()                                  
            del clients[client]
            broadcast(bytes("%s sohbetten ayrıldı." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)



if __name__ == "__main__":
    SERVER.listen(5)    
    print("Bağlantı bekleniyor...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()