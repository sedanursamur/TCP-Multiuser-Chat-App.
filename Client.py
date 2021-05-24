from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


HOST = "127.0.0.1"    
PORT =  55555        
BUFSIZ = 1024          
ADDR = (HOST, PORT)    

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive():
    while True:                                                    
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")    

            separated_msg = msg.split(maxsplit=2)
            if separated_msg[0] == '@':
                joinened_clients_list.insert(tkinter.END, separated_msg[1])
                msg = separated_msg[1] + separated_msg[2]


            msg_list.insert(tkinter.END, msg)                        
        except OSError:                                             
            break


def send(event=None):                                                
    msg = my_msg.get()
    my_msg.set("")                                                   
    client_socket.send(bytes(msg, "utf8"))                           
    if msg == "$cıkıs":                                               
        client_socket.close()
        top.quit()                                               


def on_closing(event=None):
    my_msg.set("$cıkıs")
    send()                                                          


top = tkinter.Tk()                                                     
top.title("ANLIK MESAJLAŞMA UYGULAMASI")
top.config(bg="lightpink")


scrollbar = tkinter.Scrollbar(top)                                    


msg_list = tkinter.Listbox(top, height=18, width=100, yscrollcommand=scrollbar.set, bg="lightblue")


joinened_clients_list = tkinter.Listbox(top, height=15, width=22, bg="lightpink")
joinened_clients_list.insert(tkinter.END, "GRUPTA BULUNANLAR:")


my_msg = tkinter.StringVar()                                          
entry_field = tkinter.Entry(top,textvariable=my_msg)
entry_field.bind("<Return>", send)  
                 


Label_1 = tkinter.Label(top, text="Mesajınızı buraya yazınız...")


send_button = tkinter.Button(top, text="Gönder", command=send, bg="lightblue",height=1, width=10)

scrollbar.grid(row=0, column=1, sticky='ns')
msg_list.grid(row=0, column=2)
Label_1.grid(row=1, column=2)
entry_field.grid(row=2, column=2)
send_button.grid(row=3, column=2)
joinened_clients_list.grid(row=0, column=0, sticky='n')


top.protocol("WM_DELETE_WINDOW", on_closing)                         



receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()  