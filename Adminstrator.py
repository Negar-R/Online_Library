import BookList as bo

conn = bo.me.db()
cursorA = bo.me.dc(conn)

class Admin():
    def __init__(self):
        pass

    def getInformetionAboutBook(self , bookId):

        cursorA.execute("SELECT * FROM books WHERE BOOKID = ?" , (bookId ,))
        s = cursorA.fetchall()

        return(str(s))

    def getListOfBorrowedBook(self , iD):  

        cursorA.execute("SELECT BORROWEDBOOK FROM members WHERE ID = ?" , (iD ,))
        s = cursorA.fetchall()
        
        return(str(s))

    def whoHaveBook(self , iD):
        cursorA.execute("SELECT RENT FROM books WHERE BOOKID = ?" , (iD ,))
        s = cursorA.fetchall()
        return(str(s))

    def rentBook(self , bookId , memberId):
        cursorA.execute("SELECT STATUS FROM books WHERE BOOKID = ?" , (bookId,))
        s = cursorA.fetchall()
        if s[0][0] == False:
            return False
        else:
            cursorA.execute("UPDATE books SET STATUS = '{}' , RENT = '{}' WHERE BOOKID = '{}'".format(False , memberId , bookId))
            cursorA.execute("SELECT BORROWEDBOOK FROM members WHERE ID = ?" , (memberId,))
            s = cursorA.fetchall()
            # print(s)
            # print(s[0][0] , type(s[0][0]))
            if not s[0][0]:
                upd = bookId
            else:
                upd = str(s[0][0])
                upd += " , {}".format(bookId)
            cursorA.execute("UPDATE members SET BORROWEDBOOK = ? WHERE ID = ?" , (upd, memberId))
            conn.commit()
            return True


    
# b = bo.Book('OnSherly' , 'L.M.Muntegmary' , 'A' , True , '12' , 1)
# b2 = bo.Book('Harry Potter' , 'J.K.Ruling' , 'B' , True , '13' , 2)
# b3 = bo.Book('Harry Potter' , 'J.K.Ruling' , 'c' , True , '14' , 2)

# b.addBook()
# b2.addBook()
# b3.addBook()

# b2.getInformetionAboutBook()
# b3.getInformetionAboutBook()
if __name__ =="__main__":
    m = Admin()
    m.getListOfBorrowedBook('0ea60458-1fbc-11ea-a4a6-6045cb27803b')
    m.getInformetionAboutBook('14')
    m.rentBook('15' , '72486a4a-1fc7-11ea-9af9-6045cb27803b')
# m.getInformetionAboutBook('12')
# bo.me.conn.close()

