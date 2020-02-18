import socket
import time
import select
import threading
import Adminstrator

IP = ''
PORT = 5734

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen(10)
print("server up!")

socket_list = [server_socket]

clients = {}

def check(tableName, username, passw, cnt):
    conn = Adminstrator.bo.me.db()
    cursorT = Adminstrator.bo.me.dc(conn)

    cursorT.execute("SELECT * FROM '{}' WHERE ID = '{}' AND NAME = '{}'".format(tableName, passw , username))
    s = cursorT.fetchall()

    if not len(s):
        return False

    return True  

def captcha(client_socket):
    pass


def adminLogin(client_socket):

    while True:
        client_socket.send(bytes("1:Add Member , 2:Add Book, 3:Add Admin, 4:GetInformation of book, 5:Tamdid Zaman 6:Remove Book , 7:Rent Book , 8:Who Have Book", 'utf-8'))
        msg = client_socket.recv(1024).decode("utf-8")

        if msg == '1':
            client_socket.send(bytes("Name, Age", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")
            info_l = msg.split(",")
            
            m = Adminstrator.bo.me.Members(info_l[0] , int(info_l[1]))
            m.addMember()
            client_socket.send(bytes("member added", 'utf-8'))
            Show_exist("members")

        elif msg == '2':   
            client_socket.send(bytes("Name, Author , Category , International ,  BookId , Count", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")
            info_l = msg.split(",") 

            b = Adminstrator.bo.Book(info_l[0] , info_l[1] , info_l[2] , info_l[3] , info_l[4] , int(info_l[5]))
            b.addBook()
            client_socket.send(bytes("book added", 'utf-8'))
            Show_exist("books")

        elif msg == '3':

            client_socket.send(bytes("Name, Age", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")
            info_l = msg.split(",")
            
            m = Adminstrator.bo.me.Members(info_l[0] , int(info_l[1]))
            m.addAdmin()
            client_socket.send(bytes("admin added", 'utf-8'))
            Show_exist("admins")

        elif msg == '4':

            client_socket.send(bytes("Enter Id of the book", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")

            a = Adminstrator.Admin()
            get_l = a.getInformetionAboutBook(msg)
            client_socket.send(bytes(get_l, 'utf-8'))

        elif msg == '5':
            client_socket.send(bytes("we do not have this service now :)", 'utf-8'))

        elif msg == '6':
            client_socket.send(bytes("Name, Author , Category , International ,  BookId , Count", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")
            info_l = msg.split(",") 

            b = Adminstrator.bo.Book(info_l[0] , info_l[1] , info_l[2] , info_l[3] , info_l[4] , int(info_l[5]))
            b.removeBook()
            client_socket.send(bytes("book removed", 'utf-8'))
            Show_exist("books")

        elif msg == '7':
            client_socket.send(bytes("Enter Id of the book , memberId", 'utf-8'))
            msgg = client_socket.recv(1024).decode('utf-8')
            get_msg = msgg.split(',')

            a = Adminstrator.Admin()
            state = a.rentBook(get_msg[0], get_msg[1])
            if not state:
                client_socket.send(bytes("this book does not exist", 'utf-8'))
            else:
                client_socket.send(bytes("action Done", 'utf-8'))

        else:
            client_socket.send(bytes("Enter Id of the book", 'utf-8'))
            bookId = client_socket.recv(1024).decode("utf-8")

            a = Adminstrator.Admin()
            get_l = a.whoHaveBook(bookId)
            client_socket.send(bytes(get_l, 'utf-8'))

def memberLogin(client_socket):

    while True:
        client_socket.send(bytes("1:List of  borrowed book 2:Get Information of book" , 'utf-8'))
        msg = client_socket.recv(1024).decode("utf-8")

        if msg == '1':
            client_socket.send(bytes("Enter your Id", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")

            a = Adminstrator.Admin()
            get_l = a.getListOfBorrowedBook(msg)
            client_socket.send(bytes(get_l, 'utf-8'))

        else:
            client_socket.send(bytes("Enter Id of the book", 'utf-8'))
            msg = client_socket.recv(1024).decode("utf-8")

            a = Adminstrator.Admin()
            get_l = a.getInformetionAboutBook(msg)
            client_socket.send(bytes(get_l, 'utf-8'))
            


def askCircumstance(client_socket):

    cnt = 0
    while cnt<3:
        client_socket.send(bytes("1 : Admin or 2 : Member", 'utf-8'))
        msg1 = client_socket.recv(1024).decode("utf-8")

        client_socket.send(bytes("username,pass", 'utf-8'))
        msg2 = client_socket.recv(1024).decode("utf-8")
        l_msg = msg2.split(",")

        if msg1 == '1':
            if check("admins", l_msg[0], l_msg[1], cnt):
                break
            else:
                cnt += 1
        
        else:
            if check("members", l_msg[0], l_msg[1], cnt):
                break
            else:
                cnt += 1

    if cnt == 3:
        captcha(client_socket)
    else:
        if msg1 == '1':
            adminLogin(client_socket)
        else:
            memberLogin(client_socket)
        return

def Show_exist(tableName):
    conn = Adminstrator.bo.me.db()
    cursorm = Adminstrator.bo.me.dc(conn)
    print("this is list of exist {} : ".format(tableName))
    cursorm.execute("SELECT * FROM '{}'".format(tableName))
    s1 = cursorm.fetchall()
    for i in s1:
        print(i)



while True:
    read_socket, write_socket, exception_socket = select.select(socket_list, [], socket_list)

    for s in read_socket:
        if s == server_socket:

            client_socket, address = server_socket.accept() 
            if client_socket:  

                client_socket.send(bytes("welcome!", 'utf-8'))
                
                print("Connection Established from {}".format(address))

                Show_exist("books")
                Show_exist("members")
                Show_exist("admins")

                t = threading.Thread(target = askCircumstance, args = (client_socket,))
                t.start()

                socket_list.append(client_socket)
            
    for s in exception_socket:
        try:
            socket_list.remove(s)
            del clients[s]
        except:
            pass
    time.sleep(2)

server_socket.close()
conn.close()
#ilink