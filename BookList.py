import Member as me


conn = me.db()
cursorB = me.dc(conn)

# cursorB.execute("DROP TABLE books")


cursorB.execute('CREATE TABLE IF NOT EXISTS books(NAME VARCHAR(255) , AUTHOR VARCHAR(255) , CATEGORY VARCHAR(255) , INTERNATIONAL BOOLEAN , BOOKID TEXT, STATUS BOOLEAN , COUNT INTEGER , RENT VARCHAR(255))')
conn.commit()

class Book():
    def __init__(self , name , author , category , international ,  bookId , count):
        self.name = name
        self.author = author
        self.category = category
        self.bookId = bookId
        self.count = count
        self.status = True
        self.rent = None
        self.international = international
        self.motarjem = None 


    def setMotarjem(self , motarjem):
        if self.international:
            self.motarjem = motarjem

    def addBook(self):
        cursorB.execute('INSERT INTO books(NAME , AUTHOR , CATEGORY , INTERNATIONAL , BOOKID , COUNT) VALUES(? , ? , ? , ? , ? , ?)'
        , (self.name , self.author , self.category , self.international , self.bookId , self.count))
        
        conn.commit()

    def removeBook(self):
        cursorB.execute("SELECT * FROM books WHERE BOOKID = ?" , (self.bookId ,))
        s = cursorB.fetchall()

        if not len(s):
            print("There is not any book with this id")
            return

        cursorB.execute("DELETE FROM books WHERE BOOKID = ?" , (self.bookId ,)) 
        conn.commit()

        try:
            cursorB.execute("SELECT COUNT FROM books WHERE NAME = ?" , (self.name ,))
            t = cursorB.fetchall()
            a = t[0][0] - 1

            cursorB.execute("UPDATE books SET COUNT = ? WHERE NAME = ?" , (a , self.name))

        except:
            pass    

        conn.commit()


    # def rentBook(self , member):
    #     #type(memeber) = object
    #     if not self.status:
    #         print("This Book was rented before")

    #     if self.status and not member.expireCheck():
    #         self.status = False   
    #         cursorB.execute("UPDATE books SET STATUS = ? , RENT = ? WHERE BOOKID = ?" , (False, str(member.iD) , self.bookId))       
            
    #         member.rentedBook.append(self.bookId)
    #         cursorB.execute("UPDATE members SET BORROWEDBOOK = ? WHERE ID = ?"  , (str(member.rentedBook) , str(member.iD)))
            
    #     try:
    #         cursorB.execute("SELECT COUNT FROM books WHERE NAME = ?" , (self.name ,))
    #         t = cursorB.fetchall()
    #         a = t[0][0] - 1

    #         cursorB.execute("UPDATE books SET COUNT = ? WHERE NAME = ?" , (a , self.name))

    #     except:
    #         pass    

    #     conn.commit() 
    
    


if __name__ == "__main__":
    b = Book('OnSherly' , 'L.M.Muntegmary' , 'A' , True , '12' , 1)
    b2 = Book('Harry Potter' , 'J.K.Ruling' , 'B' , True , '13' , 2)
    b3 = Book('Harry Potter' , 'J.K.Ruling' , 'c' , True , '14' , 2)

    b.addBook()
    b2.addBook()
    b3.addBook()

    cursorB.execute("SELECT * FROM books")
    s = cursorB.fetchall()

    print(s)


    print("-------------------")


    b2.removeBook()

    # cursorB.execute("SELECT * FROM books")
    # s = cursorB.fetchall()

    # for i in s:
    #     print(i)


    print("-------------------")    

    m = me.Members('Navid' , 22)
    m.addMember()
    b.rentBook(m)
    b2.rentBook(m)

    # cursorB.execute("SELECT * FROM members")
    # s = cursorB.fetchall()

    # print(s)

    print('------------------')    

    cursorB.execute("SELECT STATUS FROM books")
    s = cursorB.fetchall()

    print(s, " #### ")

    print("-------------------")

    b.whoHaveBook()
    b2.whoHaveBook()
    b3.whoHaveBook()

    print("------------------")

    # b2.getInformetionAboutBook()
    # b3.getInformetionAboutBook()

    cursorB.execute("SELECT * FROM members")
    w = cursorB.fetchall()

    print("!!!!!" , w)